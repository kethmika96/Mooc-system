import os
from collections import Counter

from PIL import Image
from face_detection import RetinaFace
from .expressions_detection import Ratings

detector = RetinaFace()
ratings = Ratings()


def get_face(imgs):

    faces = []
    for img in imgs:
        box, landmarks, score = detector(img)[0]
        top_left = (int(box[0]), int(box[1]))
        bottom_right = (int(box[2]), int(box[3]))
        img = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        file_name = len(os.listdir("predictions/detected_faces/"))
        Image.fromarray(img).save(f"predictions/detected_faces/{file_name}.jpg")

        faces.append(img)

    return faces


def get_rating(detected_faces):
    rates, confs = ratings(detected_faces)
    rate_counts = Counter(rates)
    return rate_counts.most_common(1)[0][0]
