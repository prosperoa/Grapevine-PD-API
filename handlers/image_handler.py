import sys
sys.path.append("/controllers/image_controller")

def analyze_image(req, alexnet):
  img = req.files['image']
  return image_controller.analyze_image(img, alexnet)
