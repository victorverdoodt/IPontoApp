import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key_facerecognition'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///banco.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    ELASTIC_EMAIL = {
        "URL": "https://api.elasticemail.com/v2/email/send",
        "FROM_MAIL": "noreply@iponto.com",
        "FROM_NAME": "iPonto",
        "APIKEY": "979C66AAE704278F5C06B6231D07963C57FD8F48FD9E9AAED9D2BAFB62384D59ED5EEE8AA0A7BB46EF5889849A34245F"
    }
