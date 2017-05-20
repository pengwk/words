
import os

from PIL import Image

def crop_image(image):
    _image = Image.open(image)
    size = (0, 44, 480, 314)
    _image.crop(size).save(image)

def batch_crop():
    images = [image for image in os.listdir("./") if image.endswith(".jpg")]
    print images

    map(crop_image, images)
    return None

if __name__ == "__main__":
    batch_crop()