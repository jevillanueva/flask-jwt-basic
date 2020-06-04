import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, exceptions
import logging
import routes
LOG_FILENAME = 'aplication.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Flask(__name__)
errors = {
  'InternalError': {
      'message': "Internal Error. Wait few Minutes or Contact the Administrator",
      'status': 500,
  },
  'NotFound': {
      'message': "Resource Not Found",
      'status': 404
  },
}
api = Api(app,errors=errors)

app.config['JWT_SECRET_KEY'] = 'Secret_key_text123123'
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
	jti = decrypted_token['jti']
    #Para black List
	entry = routes.revoked_store.get(jti)
	print (jti)
	print (entry)
	if entry is None:
		return True
	return entry == 'true'

api.add_resource(routes.Index, '/',)
api.add_resource(routes.Login, '/login')
api.add_resource(routes.Secure, '/secure')
api.add_resource(routes.Logout, '/logout')



@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
	token_type = expired_token['type']
	return {
  'code': 0,
  'message': 'The {} token has expired'.format(token_type)
	}, 401

@jwt.revoked_token_loader
def my_revoked_token_callback():
	return {
    'code': 0,
    'message': 'The token has revoked'
	}, 401

@jwt.unauthorized_loader
def my_unauthorized_token_callback(unauth):
	return {
    'code': 0,
    'message': 'Token is required'
	}, 401

@jwt.invalid_token_loader
def my_invalid_token_callback(invalid):
	return {
		'code': 0,
		'message': 'Token is invalid'
	}, 422


if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
        DEBUG = os.environ.get('DEBUG','True') == "True"
    except ValueError:
        DEBUG = True
        PORT = 5000
    app.logger.info("Starting Service")
    print (HOST,PORT)
    app.run(host=HOST,port=PORT,debug=DEBUG)
