import io

import numpy
import wget
import os
import zlib

from PIL import Image
from src.detector import FaceDetector

dlib_download_model = 'dlib_model.dat'
dlib_download_landmark = 'dlib_landmark.dat'


def compress_image(file: bytes):
    compressed_image = zlib.compress(file, zlib.Z_BEST_COMPRESSION)
    return compressed_image


def decompress_image(file: bytes):
    decompressed_image = zlib.decompress(file)
    return decompressed_image


def bytes_to_image(byte_code: bytes):
    image = io.BytesIO(byte_code)
    image.seek(0)
    image = Image.open(image)
    return image


# Проверка наличия моделей
def check_data():
    if not (os.path.isfile(dlib_download_model) and os.path.isfile(dlib_download_landmark)):
        model_url = 'https://drive.google.com/u/0/uc?id=1IgUL8X7jb0bDXow0JZZJwHNB-f-Jo00x&export=download'
        landmark_url = 'https://drive.google.com/u/0/uc?id=1fCHIUgpwmcK5iHMtD6r6a6D0NUSKNcvf&export=download'
        wget.download(model_url)
        wget.download(landmark_url)


# Создание дескриптора к фотографии
def make_descriptor(image: Image):
    check_data()
    nparray = numpy.asarray(image)
    detect = FaceDetector()
    result = detect.find_main_descriptor(nparray)
    return result


# Поиск соответствия
def comparison(worker_descriptors, person_descriptor):
    check_data()
    detect = FaceDetector()
    result = detect.comparison(worker_descriptors, person_descriptor)
    return result
