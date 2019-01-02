import server
import sys

sys.path.append('controllers')
import image_controller

def process_image(req, alexnet):
  img = None

  try:
    img = req.files['image']
  except:
    return server.bad_req()

  return image_controller.analyze_image(img, alexnet)

