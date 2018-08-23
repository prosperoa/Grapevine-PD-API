import jwt
import os
import sys
sys.path.append('../')
import server
from controllers import auth_controller

def login(req):
  try:
    req = req.get_json()
  except:
    return server.bad_req()

  email = req['email']
  password = req['password']
  auth_type = req['auth_type'].lower()

  if auth_type not in server.auth_types:
    return server.bad_req('invalid auth type')

  if not email or not password or not auth_type:
    return server.bad_req('missing params')

  return auth_controller.login(email, password, auth_type)

def auth_user(req, user_id):
  encoded_auth_token = req.headers['Authorization'].split(' ')[1]

  if not encoded_auth_token:
    return server.bad_req('missing auth header')

  decoded_auth_token = jwt.decode(
    encoded_auth_token,
    os.environ.get('JWT_SIGNING_KEY'),
    algorithms=['HS256']
  )
  print(decoded_auth_token)

  if decoded_auth_token['user_id'] != user_id:
    return server.unauth()

  return auth_controller.auth_user(user_id)