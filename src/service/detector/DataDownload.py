import os
import wget

dlib_data_path = 'src\\resource\\'
dlib_download_model = f'{dlib_data_path}dlib_model.dat'
dlib_download_landmark = f'{dlib_data_path}dlib_landmark.dat'

if not (os.path.isfile(dlib_download_model) and os.path.isfile(dlib_download_landmark)):
    model_url = 'https://drive.google.com/u/0/uc?id=1IgUL8X7jb0bDXow0JZZJwHNB-f-Jo00x&export=download'
    landmark_url = 'https://drive.google.com/u/0/uc?id=1fCHIUgpwmcK5iHMtD6r6a6D0NUSKNcvf&export=download'
    os.mkdir(dlib_data_path)
    wget.download(model_url, dlib_data_path)
    wget.download(landmark_url, dlib_data_path)
