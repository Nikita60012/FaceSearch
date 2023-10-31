import os
import cv2
import dlib
from skimage import io
import matplotlib.pyplot as plt
from scipy.spatial import distance

CONST_PATH_TO_LEARNING_PHOTOS = "C://faces"  # Путь к фотографиям, с которыми будет проводится сравнение
CONST_PATH_TO_SEARCHING_PHOTO = "C://search"  # Путь к фото, соответствие которого нужно найти
CONST_PATH_TO_DATA = os.path.dirname(os.path.realpath(__file__)) + '\\data'  # Путь к весам

# Подгрузка весов и инициализация детектора лица
sp = dlib.shape_predictor(f'{CONST_PATH_TO_DATA}\\shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1(f'{CONST_PATH_TO_DATA}\\dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()


class FaceDetector:
    def __init__(self, pathToFaces, pathToFace, pathToData):
        self.path_to_faces = pathToFaces
        self.path_to_face = pathToFace
        self.path_to_data = pathToData

    # Нахождение дескриптора каждой из фотографии, представленной в базе данных
    def find_face_descriptors(self, path: str):
        try:
            descriptors = []
            faces = os.listdir(f'{path}\\')
            count = 0
            for i in faces:
                count += 1
                images = io.imread(f'{path}\\' + '/' + i)
                dets = detector(images, 1)
                for k, d in enumerate(dets): shape = sp(images, d)
                descriptors.append(facerec.compute_face_descriptor(images, shape))
                progress = str(round((100 / len(faces)) * count))
                print("Загружено фото в базу: {}% из 100%".format(progress))
            print("Все фото успешно загружены!")
            return descriptors, faces

        except:
            print("Что-то пошло не так. Возможно вы не правильно указали путь к папке с фотографиями.")

    # Нахождение дескриптора фотографии для идентификации
    def find_main_descriptor(self, path: str):
        image = os.listdir(f'{path}\\')
        img1 = io.imread(f'{path}\\' + image[0])
        dets_webcam = detector(img1, 1)
        for k, d in enumerate(dets_webcam): shape = sp(img1, d)
        descriptor = facerec.compute_face_descriptor(img1, shape)
        return descriptor, image, img1, dets_webcam

    # Поиск минимальнейшего расстояния между дескрипторами
    def comparison(self, path: str, descriptors, descriptor):
        distances = []
        for i in descriptors: distances.append(distance.euclidean(descriptor, i))
        min_dist = min(distances)
        image2 = io.imread(f'{path}' + '/' + faces[distances.index(min_dist)])
        if min_dist > 0.6 and len(face_descriptors) == 1:
            print('На фотографиях разные люди!')
        elif min_dist <= 0.6 and len(face_descriptors) > 1:
            print('Полученное лицо совпадает с лицом на фото ' + faces[distances.index(min_dist)])
        elif min_dist > 0.6 and len(face_descriptors) > 1:
            print('Точно сказать не могу, но наверное это человек с фотографии ' + faces[distances.index(min_dist)])
        print('Эвклидово расстояние между дескрипторами: ' + str(min_dist) + '\n')
        return image2

    # Отрисовка результата
    def draw_result(self, detect, image, image2):
        ltrb = [detect[0].tl_corner(), detect[0].br_corner()]
        plt.figure(figsize=(10, 6))
        cv2.rectangle(image, (ltrb[0].x, ltrb[0].y, ltrb[1].x, ltrb[1].y), (255, 0, 0), 5)
        plt.subplot(1, 2, 1)
        plt.title(f"Полученное лицо:")
        plt.imshow(image)
        plt.subplot(1, 2, 2)
        plt.title("Предполагаемое лицо:")
        plt.imshow(image2)
        plt.show()


face_detect = FaceDetector(CONST_PATH_TO_LEARNING_PHOTOS, CONST_PATH_TO_SEARCHING_PHOTO, CONST_PATH_TO_DATA)
face_descriptors, faces = face_detect.find_face_descriptors(CONST_PATH_TO_LEARNING_PHOTOS)
main_descriptor, face, img, detection = face_detect.find_main_descriptor(CONST_PATH_TO_SEARCHING_PHOTO)
img2 = face_detect.comparison(CONST_PATH_TO_LEARNING_PHOTOS, face_descriptors, main_descriptor)
face_detect.draw_result(detection, img, img2)
