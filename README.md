# FaceSearch

Backend-сервис биометрической идентификации человека по изображению лица.

Возможности: регистрация пользователя, сохранение биометрических данных, поиск/идентификация по фотографии, REST API для мобильного клиента...

Для системы также разработан мобильный Android-клиент, взаимодействующий с backend через REST API. https://github.com/Nikita60012/QuickIdenti.git

### Стек: Python / FastAPI / PostgreSQL / SQLAlchemy / Alembic / Docker / Dlib / Docker Compose
### Архитектура: Mobile App → REST API → FaceSearch → Database
Для запуска требуется установка библиотеки Dlib

Инструкция по установке Dlib: https://www.geeksforgeeks.org/how-to-install-dlib-library-for-python-in-windows-10/

Запуск:
1. cd FaceSearch
2. pip install -r requirements.txt 
3. python main.py
