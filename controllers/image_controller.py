import numpy as np
import scipy.ndimage
import server
import sys

from datetime import datetime
sys.path[0] += '/grApevIne/convnets_keras'
from alexnet_base import *
from utils import *

from keras.preprocessing import image

def analyze_image(leaf, alexnet):
  try:
    # predicting images
    img = image.load_img(leaf, target_size=(227, 227))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    classes = alexnet.predict(images)

    return server.ok(data=classes[0].tolist())
  except:
    return server.error('unable to analyze image')
