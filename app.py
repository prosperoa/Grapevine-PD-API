import server
from flask import Flask

APP_NAME = 'Grapevine PD API'
app = Flask(APP_NAME)

@app.route('/')
def index():
  return server.ok(APP_NAME)

@app.errorhandler(400)
def page_not_found(err):
  return server.bad_req()

@app.errorhandler(404)
def page_not_found(err):
  return server.not_found()

@app.errorhandler(405)
def method_not_allowed(err):
  return server.not_allowed()

@app.errorhandler(500)
def internal_server_error(err):
  return server.error()

if __name__ == '__main__':
  app.run()