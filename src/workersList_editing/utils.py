import io
import os

from PIL import Image

from src.detector import FaceDetector


def reduce_image(file: bytearray):
    img = io.BytesIO(file)
    img.seek(0)
    image = Image.open(img)
    image = image.resize((160, 300))
    return image


def bytes_to_image(byte_code):
    image = io.BytesIO(byte_code.first()[0])
    image.seek(0)
    image = Image.open(image)
    return image


def make_descriptor(image, landmarks_data, data_model):
    image.save('photo.jpg')
    detect = FaceDetector(landmarks_data.file, data_model.file)
    result = detect.find_main_descriptor(image)
    # plt.imshow(result[1])
    # plt.show()
    os.remove('photo.jpg')
    return result
