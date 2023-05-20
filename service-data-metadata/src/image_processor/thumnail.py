import hashlib
import os

from PIL import Image

def generate_image_thumbnail(source, target_folder, size=(128, 128)):
  _, ext = os.path.splitext(source)
  target_name = hashlib.md5(source.encode()).hexdigest()

  with Image.open(source) as im:
    im.thumbnail(size=size)
    im.save(target_folder + target_name + ext, "PNG")

  print("Generated thumnail for " + source)
  print("Thumbnail path " + target_folder + target_name  + ext)
