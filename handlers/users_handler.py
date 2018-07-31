import sys
sys.path.append('../')
import server
from controllers import users_controller

def get_users(req):
  page_size = int(req.args['page_size'])
  page_index = int(req.args['page_index'])

  if page_size < 0 or page_index < 0:
    return server.bad_req('invalid params')

  return users_controller.get_users(page_size, page_index)