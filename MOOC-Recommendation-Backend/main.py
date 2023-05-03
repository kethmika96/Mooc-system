import base64
import io
import os
import re
import cv2

import numpy as np

from PIL import Image

from flask import Flask, request, current_app
from flask_cors import CORS
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError, NoResultFound

from config import Config
from db import init_db, Users, Videos, Ratings, Recommendations, Technologies

from models.recommendation import ExplicitMF, create_train_test
from models.rate import get_face, get_rating

app = Flask(__name__)
app.config.from_object('config.Config')

CORS(app, resources={r"*": {"origins": "*", "expose_headers": "Content-Range"}})
db = init_db(app)


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = base64.encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64
    return encoded_img


@app.route("/login/", methods=['POST'])
def login():
    data = request.get_json()

    # user = db.one_or_404((db.select(Users).filter_by(username=data["username"])).scalar_one(),
    #                      description=f"No user named '{data['username']}'.")
    try:
        user = db.session.execute(db.select(Users).filter_by(username=data["username"],
                                                             password=data["password"])).scalar_one()
        user = user.to_dict()
        user.pop("password")
        return user
    except NoResultFound as ex:
        return {"error": f"No user named '{data['username']}'."}, 404


@app.route("/register/", methods=['POST'])
def user_register():
    data = request.get_json()
    try:
        user = Users(**data)
        db.session.add(user)
        db.session.commit()

        return user.to_dict()

    except IntegrityError as ex:
        if "Duplicate entry" in str(ex):
            return {"error": f"Duplicate user {data['username']}"}, 400
        else:
            return {"error": "Internal server error"}, 500


@app.route("/videos/upload", methods=['POST'])
def upload_video():
    data = request.form

    if 'video' not in request.files:
        return {"error": "No video attached"}, 400
    file = request.files['video']

    if file.filename == '':
        return {"error": "No filename"}, 400
    else:
        filename, ext = secure_filename(file.filename).split(".")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}.{ext}'))
        thumb_file = os.path.join(app.config['UPLOAD_FOLDER'], "thumbs", f"{filename}thumb.jpg")
        # ff = FFmpeg()
        # ff.convert(os.path.join(app.config['UPLOAD_FOLDER'], filename), thumb_file)
        cap = cv2.VideoCapture(os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}.{ext}'))

        ret = False
        while not ret:
            ret, frame = cap.read()
            if frame is not None:
                Image.fromarray(frame).save(thumb_file)

        video = Videos(name=filename, location=os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}.{ext}'), thumb=thumb_file,
                       category=int(data["category_id"]), tech=int(data["tech_id"]))
        db.session.add(video)
        db.session.commit()
        return video.to_dict()


@app.route("/videos/download/<int:id>", methods=['GET'])
def download_video(id):
    try:
        video = db.session.execute(db.select(Videos).filter_by(id=id)).scalar_one()

        headers = request.headers
        if not "range" in headers:
            return current_app.response_class(status=400)

        video_path = os.path.abspath(video.location)
        size = os.stat(video_path)
        size = size.st_size

        chunk_size = (10 ** 6) * 3  # 1000kb makes 1mb * 3 = 3mb (this is based on your choice)
        start = int(re.sub("\\D", "", headers["range"]))
        end = min(start + chunk_size, size - 1)

        content_lenght = end - start + 1

        def get_chunk(video_path, start, chunk_size):
            with open(video_path, "rb") as f:
                f.seek(start)
                chunk = f.read(chunk_size)
            return chunk

        headers = {
            "Content-Range": f"bytes {start}-{end}/{size}",
            "Accept-Ranges": "bytes",
            "Content-Length": content_lenght,
            "Content-Type": "video/mp4",
        }

        return current_app.response_class(get_chunk(video_path, start, chunk_size), 206, headers)
    except NoResultFound as ex:
        return {"error": f"No video bearing id '{id}'."}, 404


@app.route("/videos/recommend/<int:user_id>", methods=['POST'])
def recommend_video(user_id):
    users = db.session.execute(db.select(Users)).scalars().fetchall()
    ratings = db.session.execute(db.select(Ratings)).scalars().fetchall()
    videos = db.session.execute(db.select(Videos)).scalars().fetchall()

    # if db.session.execute(db.select(Users).filter_by(id=user_id)).scalar_one_or_none():
    if not any([user.id == user_id for user in users]):
        return {"error": f"No users found for user id '{user_id}'."}, 404

    # elif not db.session.execute(db.select(Ratings).filter_by(user_id=user_id)).scalar_one_or_none():
    elif not any(rating.user_id == user_id for rating in ratings):
        return {"error": f"No ratings found for user id '{user_id}'."}, 404

    elif len(ratings):
        rates = np.zeros((len(users), len([rating.video_id for rating in ratings])))
        for rating in ratings:
            rates[rating.user_id - 1, rating.video_id - 1] = rating.rating

        train, test = create_train_test(rates)
        als = ExplicitMF(n_iters=100, n_factors=40, reg=0.01)
        als.fit(train, test)

        preds = als.predict().round()[user_id - 1]
        video_ids = (-preds).argsort()[:5] + 1

        recommendationed = []

        for video in videos:
            video = video.to_dict()
            video.pop("location")
            if video["id"] in video_ids:
                recommendationed.append(video)
                recommendation = Recommendations(user_id=user_id, video_id=video["id"])
                db.session.add(recommendation)

        db.session.commit()

        videos_dict = {}
        for video in recommendationed:
            tech = db.session.execute(db.select(Technologies).filter_by(id=video["tech"])).scalar_one()
            if tech.tech in videos_dict:
                thumb = get_response_image(video.get("thumb"))
                video["thumb"] = thumb
                video.pop("tech")
                video.pop("category")
                videos_dict[tech.tech].append(video)
            else:
                thumb = get_response_image(video.get("thumb"))
                video["thumb"] = thumb
                video.pop("tech")
                video.pop("category")
                videos_dict[tech.tech] = [video]

        return videos_dict, 200

    else:
        return {"error": f"Videos are not rated yet."}, 404


@app.route("/videos/rate", methods=['POST'])
def rate_video():

    if 'faces' not in request.files:
        return {"error": "No images attached"}, 400

    else:
        files = request.files.getlist("faces")

        faces = []
        for file in files:
            faces.append(np.asarray(Image.open(file).convert("RGB")))

        video_rating = get_rating(get_face(np.array(faces)))

        video_rating = Config.RATINGS[video_rating]

        data = request.form
        user = db.session.execute(db.select(Users).filter_by(id=data['user_id'])).scalar_one()
        video = db.session.execute(db.select(Videos).filter_by(id=data['video_id'])).scalar_one()

        rating = Ratings(rating=video_rating, user_id=user.id, video_id=video.id)
        db.session.add(rating)
        db.session.commit()

        return {"msg": "Successfully rated the video"}, 200


@app.route("/videos/list", methods=['GET'])
def list_videos():
    videos = db.session.execute(db.select(Videos)).scalars().fetchall()

    videos_dict = {}
    for video in videos:
        tech = db.session.execute(db.select(Technologies).filter_by(id=video.tech)).scalar_one()
        if tech.tech in videos_dict:
            video = video.to_dict()
            thumb = get_response_image(video.get("thumb"))
            video["thumb"] = thumb
            video.pop("location")
            video.pop("tech")
            video.pop("category")
            videos_dict[tech.tech].append(video)
        else:
            video = video.to_dict()
            thumb = get_response_image(video.get("thumb"))
            video["thumb"] = thumb
            video.pop("location")
            video.pop("tech")
            video.pop("category")
            videos_dict[tech.tech] = [video]

    return videos_dict


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
