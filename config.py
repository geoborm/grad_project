import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tofu-is-the-most-delicious'
    SQLALCHEMY_DATABASE_URI = os.environ.get('postgres://aftzbrid:XXpwMwkpEIEzUBa2YMgNub-CQfmwjJMO@lallah.db.elephantsql.com/aftzbrid') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False