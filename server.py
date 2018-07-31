from flask import jsonify

auth_types = ['regular', 'admin']

def respond(success, status, message=None, data=None):
  """Custom HTTP response"""
  return jsonify({'success': success, 'status': status, 'message': message,
    'data': data}), status

def ok(message='ok', data=None):
  """HTTP 200: ok"""
  return respond(True, 200, message=message, data=data)

def bad_req(message='bad request'):
  """HTTP 400: bad request"""
  return respond(False, 400, message)

def invalid():
  """HTTP 400: invalid request parameters"""
  return bad_req('invalid params')

def not_found(message='requested url not found'):
  """HTTP 404: route not found"""
  return respond(False, 404, message)

def unauth(message='unauthorized'):
  """HTTP 401: unauthorized request"""
  return respond(False, 401, message)

def not_allowed(message='method not allowed for requested url'):
  """HTTP 405: method not allowed"""
  return respond(False, 405, message)

def error(message='an error occurred'):
  """HTTP 500: internal server error"""
  return respond(False, 500, 'ERROR: ' + message)