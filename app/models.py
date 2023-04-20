from random import randint
from app import db, login  
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin

class Comic(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False) 
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    profiles = db.relationship('Com_Profile', backref='comic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password'))
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Comic {self.id}|{self.email}>'
    
    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)
    
@login.user_loader
def get_a_comic_by_id(comic_id):
    return db.session.get(Comic, comic_id)

def random_photo_url():
    return f"https://picsum.photos/500?random={randint(1,100)}"


class Com_Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(75), nullable=False, unique=True)
    location = db.Column(db.String(50), nullable=False)
    about_me = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String(200), nullable=False, default=random_photo_url)
    twitter_url = db.Column(db.String(200))
    instagram_url = db.Column(db.String(200))
    facebook_url = db.Column(db.String(200))
    tiktok_url = db.Column(db.String(200))
    youtube_url = db.Column(db.String(200))
    comic_id = db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Profile {self.username}>"
