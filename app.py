import os
import server
import subprocess
import sys

from database import Database as db
from datetime import datetime
from flask import Flask, abort, request
from flask_cors import CORS

sys.path.append('handlers')
import auth_handler, users_handler, image_handler
sys.path.append('grApevIne/convnets_keras')
from alexnet_base import get_alexnet

APP_NAME = 'Grapevine PD API'
app = Flask(APP_NAME)
alexnet = None
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

@app.route('/analyze', methods=['POST'])
def analyze_image():
  return image_handler.process_image(request, alexnet)


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
  # subprocess.run('conda activate grapevinepd-venv'.split())

  # uncomment to view model summary
  # print alexnet.summary()

  # - need to load in image or access users directory & images
  # - example only gives predicted probability of each instance belonging to one
  # class, need to research into how to give probs for all classes.
  # - probably need to create a "master" program to run at all times and create
  # threads to call instances of this function for each user. Maybe a queue system
  weights = 'grApevIne/convnets_keras/weights/alexnet_weights_grapevine.h5'
  input_size = (3, 227, 227)
  nb_classes = 6
  mean_flag = True # if False, then the mean subtraction layer is not prepended
  alexnet = get_alexnet(input_size, nb_classes, mean_flag)
  alexnet.load_weights(weights, by_name=True)
  
  
  app.run(host="136.168.201.106", port="5001")
