import os

import dlib
import numpy
import wget
from PIL import Image
from scipy.spatial import distance
import logging

dlib_data_path = 'src\\resource\\'
dlib_download_model = f'{dlib_data_path}dlib_model.dat'
dlib_download_landmark = f'{dlib_data_path}dlib_landmark.dat'


class FaceDetector:

    # Подгрузка весов и инициализация детектора лица
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.check_data()
        self.sp = dlib.shape_predictor(dlib_download_landmark)
        self.facerec = dlib.face_recognition_model_v1(dlib_download_model)

    # Нахождение дескриптора каждой из фотографии, представленной в базе данных
    # def find_face_descriptors(self, path: str):
    #     try:
    #         descriptors = []
    #         self.faces = os.listdir(f'{path}\\')
    #         count = 0
    #         for i in self.faces:
    #             count += 1
    #             images = io.imread(f'{path}\\' + '/' + i)
    #             dets = self.detector(images, 1)
    #             for k, d in enumerate(dets): shape = self.sp(images, d)
    #             descriptors.append(self.facerec.compute_face_descriptor(images, shape))
    #             progress = str(round((100 / len(self.faces)) * count))
    #             logging.info("Загружено фото в базу: {}% из 100%".format(progress))
    #         logging.info("Все фото успешно загружены!")
    #         return descriptors, self.faces
    #
    #     except:
    #         logging.exception("Что-то пошло не так. Возможно вы не правильно указали путь к папке с фотографиями.")

    # Нахождение дескриптора фотографии
    def find_main_descriptor(self, image: Image):
        nparray = numpy.asarray(image)
        img = nparray.astype('uint8')
        dets_webcam = self.detector(img, 1)
        for k, d in enumerate(dets_webcam):
            shape = self.sp(img, d)
        descriptor = self.facerec.compute_face_descriptor(img, shape)
        return descriptor

    # Поиск минимальнейшего расстояния между дескрипторами
    def comparison(self, descriptors, descriptor):
        distances = []
        unknown: bool = True
        result: str
        workers_array = []
        for k in descriptors:
            workers_array.append(k[3])
        for i in workers_array:
            distances.append(distance.euclidean(descriptor, i))
        min_dist = min(distances)
        min_index: int
        for k in range(0, len(distances)):
            if distances[k] == min_dist:
                min_index = k
        if min_dist > 0.6 and len(descriptors) == 1:
            logging.info('На фотографиях разные люди!')
            result = 'На фотографиях разные люди!'
            unknown = False
        elif min_dist < 0.6 and len(descriptors) == 1:
            logging.info('На фотографях один и тот же человек')
            result = 'На фотографях один и тот же человек'
            unknown = False
        elif min_dist <= 0.6 and len(descriptors) > 1:
            logging.info(f'Полученное лицо совпадает с лицом на фото записи с индексом '
                         f'{descriptors[min_index][0]}')
            result = f'Полученное лицо совпадает с лицом на фото записи с индексом ' \
                     f'{descriptors[min_index][0]}'
            unknown = False
        elif min_dist > 0.6 and len(descriptors) > 1:
            logging.info('Это незнакомый человек')
            result = 'Это незнакомый человек'
        logging.info(f'min_dist: {len(descriptors)}')
        logging.info('Эвклидово расстояние между дескрипторами: ' + str(min_dist) + '\n')
        return result, min_index, unknown

    def check_data(self):
        if not (os.path.isfile(dlib_download_model) and os.path.isfile(dlib_download_landmark)):
            model_url = 'https://drive.google.com/u/0/uc?id=1IgUL8X7jb0bDXow0JZZJwHNB-f-Jo00x&export=download'
            landmark_url = 'https://drive.google.com/u/0/uc?id=1fCHIUgpwmcK5iHMtD6r6a6D0NUSKNcvf&export=download'
            os.mkdir(dlib_data_path)
            wget.download(model_url, dlib_data_path)
            wget.download(landmark_url, dlib_data_path)
