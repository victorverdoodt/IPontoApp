import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key_facerecognition'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
