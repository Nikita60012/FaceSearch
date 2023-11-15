import logging
from typing import Annotated

import numpy as np
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection.database import get_async_session
from src.dao.WorkersListModels import worker
from src.dto.request.AddWorkerDTO import AddWorker
from src.dto.request.UpdateWorkerDTO import UpdateWorker
from src.service.Image.ImageService import compress_image, bytes_to_image, decompress_image
from src.service.detector.DetectorService import FaceDetector

router = APIRouter(
    prefix='/edit_workers',
    tags=['Редактирование данных работников']
)

detect = FaceDetector()


@router.post('/add', name='Добавление работника')
async def add_worker(new_worker: Annotated[AddWorker, Form()],
                     file: Annotated[UploadFile, File],
                     session: Annotated[AsyncSession, Depends(get_async_session)]):
    image = file.file.read()
    img = compress_image(image)
    photo = bytes_to_image(image)
    result = detect.find_main_descriptor(photo)
    descriptor = np.asarray(result)
    statement = insert(worker).values(photo=img, descriptor=descriptor, **new_worker.model_dump())
    await session.execute(statement)
    await session.commit()
    logging.info(f'Worker {new_worker.fullname} successfully added')
    return {'status': 'success'}


@router.get('/get/{worker_id}', name='Получение данных работника')
async def get_worker(worker_id: int,
                     session: AsyncSession = Depends(get_async_session)):
    statement = select(worker).where(worker.c.id == worker_id)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    decomp_image = decompress_image(response[4])
    image = bytes_to_image(decomp_image)
    image.show()
    logging.info(f'Worker data {response[1]} received')
    return {'fullname': response[1],
            'birthdate': response[2],
            'phone': response[3],
            # 'photo': str(response[4]),
            'descriptor': response[5]
            }


@router.put('/upd/{worker_id}', name='Обновление данных работника')
async def update_worker(worker_id: int, upd_worker: UpdateWorker,
                        file: Annotated[UploadFile, File],
                        session: AsyncSession = Depends(get_async_session)):
    image = file.file.read()
    img = compress_image(image)
    photo = bytes_to_image(image)
    raw_descriptor = detect.find_main_descriptor(photo)
    descriptor = np.asarray(raw_descriptor)
    statement = update(worker).where(worker.c.id == worker_id) \
        .values(photo=img, descriptor=descriptor, **upd_worker.model_dump())
    await session.execute(statement)
    await session.commit()
    logging.info(f'Worker data with id {worker_id} updated')
    return {'status': 'success'}


@router.delete('/del/{del_id}', name='Удаление работника')
async def delete_worker(worker_id: int,
                        session: AsyncSession = Depends(get_async_session)):
    statement = delete(worker).where(worker.c.id == worker_id)
    await session.execute(statement)
    await session.commit()
    logging.info(f'Worker with id {worker_id} deleted')
    return {'status': 'success'}
