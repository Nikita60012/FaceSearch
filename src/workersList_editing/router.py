from typing import Annotated

import numpy as np
from PIL import Image
from fastapi import APIRouter, Depends, UploadFile, File, Form
import io
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.workersList_editing.models import worker
from src.workersList_editing.shemas import AddWorker, UpdateWorker
from src.workersList_editing.utils import reduce_image, bytes_to_image, make_descriptor, image_to_bytes

router = APIRouter(
    prefix='/edit_workers',
    tags=['Редактирование данных работников']
)


@router.post('/add', name='Добавление работника')
async def add_worker(new_worker: Annotated[AddWorker, Form()],
                     file: Annotated[UploadFile, File],
                     landmarks_data: Annotated[UploadFile, File],
                     data_model: Annotated[UploadFile, File],
                     session: Annotated[AsyncSession, Depends(get_async_session)]):
    image = bytearray(file.file.read())
    img = reduce_image(image)
    result = make_descriptor(img, landmarks_data, data_model)
    img = image_to_bytes(img)
    descriptor = np.asarray(result[0])
    statement = insert(worker).values(photo=img, descriptor=descriptor, **new_worker.model_dump())
    await session.execute(statement)
    await session.commit()
    return {'status': str(result)}


# @router.post('/reduce_image', name='Сжатие изображения')
# async def reduce(path: str, file: UploadFile):
#     image = bytearray(file.file.read())
#     img = reduce_image(image)
#     img.save(path, quality=95)
#     return {'status': 'success'}


@router.get('/get/{worker_id}', name='Получение данных работника')
async def show_worker_photo(worker_id: int,
                            session: AsyncSession = Depends(get_async_session)):
    statement = select(worker).where(worker.c.id == worker_id)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    img = io.BytesIO(response[4])
    img.seek(0)
    image = Image.open(img)
    image.show()

    return {'fullname': response[1],
            'birthdate': response[2],
            'phone': response[3],
            # 'photo': str(response[4]),
            'descriptor': response[5]
            }


# @router.put('/photo', name='Установление фотографии работника')
# async def photo(worker_id: int,
#                 file: UploadFile,
#                 landmarks_data: UploadFile,
#                 data_model: UploadFile,
#                 session: AsyncSession = Depends(get_async_session)
#                 ):
#     image = bytearray(file.file.read())
#     img = reduce_image(image)
#     result = make_descriptor(image, landmarks_data, data_model)
#     statement = update(worker).where(worker.c.id == worker_id).values(photo=img, descriptor=str(result[0]))
#     await session.execute(statement)
#     await session.commit()
#     return {'status': 'success'}


@router.put('/upd/{worker_id}', name='Обновление данных работника')
async def update_worker(worker_id: int, upd_worker: UpdateWorker,
                        session: AsyncSession = Depends(get_async_session)):
    statement = update(worker).where(worker.c.id == worker_id) \
        .values(**upd_worker.model_dump())
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


# @router.put('/descriptor_making', name='Создание дескрипторов фотографии')
# async def descriptor_maker(worker_id: int,
#                            landmarks_data: UploadFile,
#                            data_model: UploadFile,
#                            session: AsyncSession = Depends(get_async_session)):
#     statement = select(worker.c.photo).where(worker.c.id == worker_id)
#     result = await session.execute(statement)
#     await session.commit()
#     image = bytes_to_image(result)
#     result = make_descriptor(image, landmarks_data, data_model)
#     statement = update(worker).where(worker.c.id == worker_id).values(descriptor=str(result[0]))
#     await session.execute(statement)
#     await session.commit()
#     return str(result[0])


@router.delete('/del/{del_id}', name='Удаление работника')
async def delete_worker(
        del_id: str, session: AsyncSession = Depends(get_async_session)):
    statement = delete(worker).where(worker.c.fullname == del_id)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}
