from src.detector import FaceDetector


def comparison(landmarks_data, data_model, worker_descriptors, person_descriptor):
    detect = FaceDetector(landmarks_data.file, data_model.file)
    result = detect.comparison(worker_descriptors, person_descriptor)

    return result
