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

  if not email or not password:
    return server.bad_req('missing email or password')

  return auth_controller.login(email, password)