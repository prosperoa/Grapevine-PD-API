import os
import server
import sys

from flask import Flask, abort, request
from database import Database as db
from handlers import auth_handler

APP_NAME = 'Grapevine PD API'
app = Flask(APP_NAME)

@app.before_request
def init_db():
  try:
    db.init(
      minconn=1,
      maxconn=20,
      dsn=os.environ.get('DATABASE_URL')
    )
  except Exception as e:
    print(e)
    abort(500)

@app.teardown_request
def close_db(error):
  db.close_all_connections()

@app.route('/login', methods=['POST'])
def login():
  return auth_handler.login(request)

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