import base64
import io
import logging
from typing import Annotated

import numpy as np
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.ClientDAO import client
from src.database.connection.database import get_async_session
from src.dao.WorkerDAO import worker
from src.dto.request.AddWorkerDTO import AddWorker
from src.dto.request.UpdateWorkerDTO import UpdateWorker
from src.dto.response.GetPeopleDTO import GetPeople
from src.dto.response.getPeoplesDTO import GetPeoples
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


@router.get('/get/{client_email}/{worker_id}', name='Получение данных работника')
async def get_worker(client_email: str, worker_id: int,
                     session: AsyncSession = Depends(get_async_session)):
    statement = select(client).where(client.c.email == client_email)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    client_id = response[0]
    statement = select(worker.c["fullname", "birthdate", "phone", "photo"]).where(
        worker.c.id == worker_id and worker.c.id_client == client_id)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    people_info = GetPeople(fullname=response[0],
                            birthdate=str(response[1]),
                            phone=response[2],
                            photo="photo")
    logging.info(f'Worker data {response[0]} received')
    decomp_image = decompress_image(response[3])
    people_info.photo = str(decomp_image)
    return {f"byteio={io.BytesIO(decomp_image)}",
            f"byteioseek2={io.BytesIO(decomp_image).seek(2)}",
            f"byteioread0={io.BytesIO(decomp_image).flush()}"}


@router.get('/get_all/{client_email}', name='Получение данных работников')
async def get_workers(client_email: str,
                      session: AsyncSession = Depends(get_async_session)):
    statement = select(client).where(client.c.email == client_email)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    client_id = response[0]
    statement = select(worker.c["id", "fullname"]).where(worker.c.id_client == client_id)
    result = await session.execute(statement)
    await session.commit()
    response = result.all()
    people_list = []
    for people in response:
        people_list.append(GetPeoples(id=people[0], fullname=people[1]))
    logging.info(f'Workers data {client_id} received')
    return people_list


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
async def delete_worker(client_id: int, worker_id: int,
                        session: AsyncSession = Depends(get_async_session)):
    statement = delete(worker).where(worker.c.id == worker_id and worker.c.id_client == client_id)
    await session.execute(statement)
    await session.commit()
    logging.info(f'Worker with id {worker_id} deleted')
    return {'status': 'success'}
