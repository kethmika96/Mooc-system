from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# recommendations = db.Table("user_recommendations",
#                            db.Column('user_id', db.Integer, db.ForeignKey("users.id")),
#                            db.Column('video_id', db.Integer, db.ForeignKey("videos.id")), )
#
# ratings = db.Table("user_ratings",
#                    db.Column('user_id', db.Integer, db.ForeignKey("users.id")),
#                    db.Column('video_id', db.Integer, db.ForeignKey("videos.id")),
#                    db.Column('rating_id', db.Integer, db.ForeignKey("ratings.id")), )


class Users(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(32))
    password = db.Column(db.String(32), nullable=False)

    # recommendations = db.Column(db.Integer, db.ForeignKey("recommendations.id"))
    # user_ratings = db.Column(db.Integer, db.ForeignKey("ratings.id"))


class Videos(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    thumb = db.Column(db.String(255), nullable=True)
    category = db.Column(db.Integer, db.ForeignKey("video_categories.id"))
    tech = db.Column(db.Integer, db.ForeignKey("technologies.id"))

    # video_ratings = db.Column(db.Integer, db.ForeignKey("ratings.id"))


class Technologies(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    tech = db.Column(db.String(255), nullable=False)


class VideoCategories(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255), nullable=False)


class Recommendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    video_id = db.Column(db.Integer, db.ForeignKey("videos.id"))


class Ratings(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    video_id = db.Column(db.Integer, db.ForeignKey("videos.id"))


def init_db(app):
    db.init_app(app)

    with app.app_context():
        # db.drop_all()
        db.create_all()

    return db
