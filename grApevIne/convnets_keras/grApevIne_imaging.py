from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import scipy.ndimage
import json

import os
import sys
sys.path.append(os.path.dirname(__file__))
from alexnet_base import *
from utils import *
from datetime import datetime

#code ported from https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html


def load_alexnet(weights):
	input_size = (3, 227, 227)
	nb_classes = 6
	mean_flag = True  # if False, then the mean subtraction layer is not prepended
	alexnet = get_alexnet(input_size, nb_classes, mean_flag)
	alexnet.load_weights(weights, by_name=True)
	# weights are in grApevIne/convnets-keras/weights/alexnet_weights_grapevine.h5

# uncomment to view model summary
# print alexnet.summary()

# - need to load in image or access users directory & images
# - example only gives predicted probability of each instance belonging to one
# class, need to research into how to give probs for all classes.
# - probably need to create a "master" program to run at all times and create
# threads to call instances of this function for each user. Maybe a queue system


def image_pred(img):
	# _folder = "../Data/Users/Test/Untested/"

	# predicting images
	# height = width = 227
	# img = image.load_img(_folder+'test1.jpg', target_size=(width, height))
  img = image.load_img(img, target_size=(227, 227))

  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)

  images = np.vstack([x])
  classes = alexnet.predict(images)
  print(classes)

  # generate json file
  cust = {'cust': '001', 'name': 'Test Name',
          'time': datetime.now().time(), 'classes': [classes]}

  print(cust)
