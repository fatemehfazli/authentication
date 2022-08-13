import re
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(128))

    def __init__(self, username, email, phone, name, password):
        self.username = username
        self.email = email
        self.phone = phone
        self.name = name
        self.password = password

    def json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'name': self.name
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod    
    def find_by_username(cls, username):
            return cls.query.filter_by(username=username).first()
    
    @classmethod    
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod    
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def check_username(cls, username):
        if not  username.strip():
            return True

    @classmethod
    def check_name(cls, name):
        if not  name.strip():
            return True
    
    @classmethod
    def check_email(cls,email): 
        match=re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)",email)
        if not match:
            return True
    @classmethod
    def check_phone(cls,phone): 
        match=re.search(r"(09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}$)",phone)
        if not match:
            return True
    @classmethod
    def check_password(cls, password): 
        if not  password.strip():
            return True

    @classmethod 
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()