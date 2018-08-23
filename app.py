import os
import server
import sys

from flask import Flask, abort, request
from flask_cors import CORS
from database import Database as db
from handlers import auth_handler, users_handler

APP_NAME = 'Grapevine PD API'
app = Flask(APP_NAME)
CORS(app)


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


@app.route('/')
def index() : return server.ok(APP_NAME)

@app.route('/login', methods=['POST'])
def login() : return auth_handler.login(request)


@app.route('/users', methods=['GET'])
def get_users() : return users_handler.get_users(request)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id) : return users_handler.delete_user(user_id)

@app.route('/users/<int:user_id>/auth', methods=['POST'])
def auth_user(user_id) : return auth_handler.auth_user(request, user_id)

@app.route('/users/create', methods=['POST'])
def create_user() : return users_handler.create_user(request)


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