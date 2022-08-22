
import json
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_bcrypt import  generate_password_hash, check_password_hash
from flask_jwt_extended import (
                create_access_token,
                jwt_required,
                get_jwt_identity
                )

class UserRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                            type = str,
                            required = True,
                            help="This username filed cannot be blank",
                        
                            )
        parser.add_argument('email',
                            type=str,
                            required= True,
                            help="This email filed cannot be blank"
                            )    
        parser.add_argument('phone',
                            type=str,
                            required= True,
                            help="This phone filed cannot be blank"
                            ) 
        parser.add_argument('name',
                            type=str,
                            required= True,
                            help="This name filed cannot be blank"
                            )   
        parser.add_argument('password',
                            type=str,
                            required= True,
                            help="This password filed cannot be blank"
                            )  
        data = parser.parse_args()
        if UserModel.check_username(data['username']):
            return {"message":" A username not found"}, 404

        if UserModel.check_email(data['email']):
            return {"message":" A email not found"}, 404
            
        if UserModel.check_phone(data['phone']):
            return {"message":" A phone not found"}, 404        
        
        if UserModel.check_name(data['name']):
            return {"message":" A name not found"}, 404

        if UserModel.check_password(data['password']):
            return {"message":" A password not found"}, 404
            
        if UserModel.find_by_username(data['username']):
            return {"message":" A user with that username already exists"}, 400

        if UserModel.find_by_email(data['email']):
            return {"message":" A user with that email already exists"}, 400

        if UserModel.find_by_phone(data['phone']):
            return {"message":" A user with that phone already exists"}, 400

        
        user = UserModel(data['username'], data['email'], data['phone'], data['name'], generate_password_hash(data["password"]))
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                            type = str,
                            required = True,
                            help="This username filed cannot be blank",
                        
                            )
        parser.add_argument('password',
                            type=str,
                            required= True,
                            help="This password filed cannot be blank"
                            )          
        data = parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and (check_password_hash(user.password, data["password"])):
            access_token = create_access_token(identity=user.id, fresh=True)
            return{
                'access_token':access_token
            }, 200
        return {'message': 'invalid credentials'}, 401


class UserAuth(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        for row in UserModel.find_all():
            if row[0] == user_id:
                return {'users':json.loads(json.dumps(dict(row)))}, 200

