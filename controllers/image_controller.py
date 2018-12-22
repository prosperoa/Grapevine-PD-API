import numpy as np
import scipy.ndimage
import server
import sys
from datetime import datetime
from keras.preprocessing import image
import scipy.ndimage

sys.path.append('grApevIne/convnets_keras')
from alexnet_base import *
from utils import *

def analyze_image(leaf, alexnet):
  try:
    # predicting images
    img = image.load_img(leaf, target_size=(227, 227))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    results = [round(r * 100, 2) for r in alexnet.predict(images)[0].tolist()]
    results = {
      'BlackRot': results[0],
      'Control': results[1],
      'Esca': results[2],
      'LeafSpot': results[3],
      'Other': results[4],
      'Pierce\'s Disease': results[5]
    }

    return server.ok(data=results)
  except:
    return server.error('unable to analyze image')
