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


  if not email or not password:
    return server.bad_req('missing email or password')

  return auth_controller.login(email, password)