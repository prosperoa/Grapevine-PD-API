import numpy as np
import scipy.ndimage
import sys

from datetime import datetime
sys.path[0] += '/grApevIne/convnets_keras'
from alexnet_base import *
from utils import *

from keras.preprocessing import image

def analyze_image(img):
  try:
    # predicting images
    img = image.load_img(img, target_size=(227, 227))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    classes = alexnet.predict(images)
    print(classes)

    cust = {'cust': '001', 'name': 'Test Name',
            'time': datetime.now().time(), 'classes': [classes]}

    print(cust)
  except:
    return 'exception'