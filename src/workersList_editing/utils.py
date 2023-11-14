import io
import logging
import os

from PIL import Image
from matplotlib.pyplot import box

from src.detector import FaceDetector


def reduce_image(file: bytearray):
    img = io.BytesIO(file)
    img.seek(0)
    image = Image.open(img)
    image = image.resize((160, 300))
    return image


def bytes_to_image(byte_code):
    image = io.BytesIO(byte_code)
    logging.info(f'first {image}')
    image.seek(0)
    logging.info(f'second {image}')
    image = Image.open(image)
    return image


def image_to_bytes(image):
    roi_img = image.crop(box())
    img_byte_arr = io.BytesIO()
    roi_img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


def make_descriptor(image, landmarks_data, data_model):
    image.save('photo.jpg')
    detect = FaceDetector(landmarks_data.file, data_model.file)
    result = detect.find_main_descriptor()
    # plt.imshow(result[1])
    # plt.show()
    os.remove('photo.jpg')
    return result
