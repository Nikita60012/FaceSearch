import os
import cv2
import dlib
import argparse

from fastapi import UploadFile
from skimage import io
import matplotlib.pyplot as plt
from scipy.spatial import distance
import logging

logging.basicConfig(level=logging.INFO, filename='face_search_log.log', filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")


# parser = argparse.ArgumentParser(description='pathes to data and faces')
# parser.add_argument('data_dir', type=str, help='Path to data')
# parser.add_argument('learn_dir', type=str, help='Path to faces')
# parser.add_argument('search_dir', type=str, help='Path to recognizing face')
# args = parser.parse_args()

# Подгрузка весов и инициализация детектора лица
# sp = dlib.shape_predictor(f'{args.data_dir}\\shape_predictor_68_face_landmarks.dat')
# facerec = dlib.face_recognition_model_v1(f'{args.data_dir}\\dlib_face_recognition_resnet_model_v1.dat')


class FaceDetector:

    def __init__(self, landmarks_data, model_data):
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor('C:\\dats\\shape_predictor_68_face_landmarks.dat')
        self.facerec = dlib.face_recognition_model_v1('C:\\dats\\dlib_face_recognition_resnet_model_v1.dat')

    # Нахождение дескриптора каждой из фотографии, представленной в базе данных
    def find_face_descriptors(self, path: str):
        try:
            descriptors = []
            self.faces = os.listdir(f'{path}\\')
            count = 0
            for i in self.faces:
                count += 1
                images = io.imread(f'{path}\\' + '/' + i)
                dets = self.detector(images, 1)
                for k, d in enumerate(dets): shape = self.sp(images, d)
                descriptors.append(self.facerec.compute_face_descriptor(images, shape))
                progress = str(round((100 / len(self.faces)) * count))
                logging.info("Загружено фото в базу: {}% из 100%".format(progress))
            logging.info("Все фото успешно загружены!")
            return descriptors, self.faces

        except:
            logging.exception("Что-то пошло не так. Возможно вы не правильно указали путь к папке с фотографиями.")

    # Нахождение дескриптора фотографии для идентификации
    def find_main_descriptor(self, image):
        img1 = io.imread('photo.jpg')
        dets_webcam = self.detector(img1, 1)
        for k, d in enumerate(dets_webcam):
            shape = self.sp(img1, d)
        descriptor = self.facerec.compute_face_descriptor(img1, shape)
        return descriptor, img1

    # Поиск минимальнейшего расстояния между дескрипторами
    def comparison(self, path: str, descriptors, descriptor):
        distances = []
        result: str
        for i in descriptors: distances.append(distance.euclidean(descriptor, i))
        min_dist = min(distances)
        image2 = io.imread(f'{path}' + '/' + self.faces[distances.index(min_dist)])
        if min_dist > 0.6 and len(descriptors) == 1:
            logging.info('На фотографиях разные люди!')
            result = 'На фотографиях разные люди!'
        elif min_dist <= 0.6 and len(descriptors) > 1:
            logging.info('Полученное лицо совпадает с лицом на фото ' + self.faces[distances.index(min_dist)])
            result = 'Полученное лицо совпадает с лицом на фото'
        elif min_dist > 0.6 and len(descriptors) > 1:
            logging.info('Точно сказать не могу, но наверное это человек с фотографии '
                         + self.faces[distances.index(min_dist)])
            result = 'Точно сказать не могу, но наверное это человек с фотографии'
        logging.info('Эвклидово расстояние между дескрипторами: ' + str(min_dist) + '\n')
        return image2, result

    # Отрисовка результата
    def draw_result(self, detect, image, image2, result):
        ltrb = [detect[0].tl_corner(), detect[0].br_corner()]
        plt.figure(figsize=(10, 6))
        cv2.rectangle(image, (ltrb[0].x, ltrb[0].y, ltrb[1].x, ltrb[1].y), (255, 0, 0), 5)
        plt.subplot(1, 2, 1)
        plt.title('Полученное лицо:')
        plt.xlabel(result)
        plt.imshow(image)
        plt.subplot(1, 2, 2)
        plt.title('Предполагаемое лицо:')
        plt.imshow(image2)
        plt.show()

# face_detect = FaceDetector()
# face_descriptors, faces = face_detect.find_face_descriptors(args.learn_dir)
# main_descriptor, face, img, detection = face_detect.find_main_descriptor(args.search_dir)
# img2, result = face_detect.comparison(args.learn_dir, face_descriptors, main_descriptor)
# face_detect.draw_result(detection, img, img2, result)
