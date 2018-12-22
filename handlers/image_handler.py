import os
import sys
sys.path.append('controllers')
import image_controller

def process_image(req, alexnet):
  img = req.files['image']
  return image_controller.analyze_image(img, alexnet)
