from controllers import image_controller

def analyze_image(req):
  img = req.files['image']
  return image_controller.analyze_image(img)