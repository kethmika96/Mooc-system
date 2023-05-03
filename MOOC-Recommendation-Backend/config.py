import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))


class ConfigMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ConfigMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=ConfigMeta):
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI="mysql://root:root@localhost:3306/video_recommendation"
    UPLOAD_FOLDER = 'videos'

    RATINGS = {
        "sad": 1,
        "neutral": 2,
        "happy": 3
    }

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(os.path.join(UPLOAD_FOLDER, "thumbs")):
        os.makedirs(os.path.join(UPLOAD_FOLDER, "thumbs"))
