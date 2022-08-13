
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta

from resources.user import UserRegister, UserLogin, UserAuth



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app) #/auth


api.add_resource(UserAuth, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')

from db import db
db.init_app(app)
if __name__ == '__main__':

    app.run(port=5000, debug=True)