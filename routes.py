import redis
from flask_restful import Resource, reqparse
from datetime import datetime, timedelta
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, get_jti)
from flask import session, jsonify

expires = timedelta(days=1)
revoked_store = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

class Index(Resource):
    def get(self):
        return {"code": 1 , "message": "Bienvenido"}


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help = 'This field cannot be blank', required = True)
parser.add_argument('password',type=str, help = 'This field cannot be blank', required = True)
class Login(Resource):
    def post(self):
        data = parser.parse_args()
        print (data["username"])
        print (data["password"])
        if data["password"] == "12345789":
            access_token = create_access_token(identity = data["username"], expires_delta=expires)
            revoked_store.set(get_jti(access_token), "false", expires*1.5)
            expiresTime = datetime.today() + expires
            return {"code":1, "message":"Token de acceso al sistema", "token": access_token, "expires": str(expiresTime) }
        else:
            return {"code": 0 , "message": "Password Incorrect"}

class Secure(Resource):
    @jwt_required
    def get(self):
        return {"code": 1, "message": "Secure"}


class Logout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoked_store.set(jti, 'true', expires*1.5)
        return {"code": 1, "message": "Token Revoked"}

