import base64
import logging
from io import BytesIO
from typing import Annotated

import numpy as np
from PIL.Image import Image
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse, Response, StreamingResponse

from src.dao.ClientDAO import client
from src.database.connection.database import get_async_session
from src.dao.WorkerDAO import worker
from src.dto.request.AddHumanDTO import AddWorker
from src.dto.request.UpdateHumanDTO import UpdateWorker
from src.dto.response.GetHumanDTO import GetHuman
from src.dto.response.getPeoplesDTO import GetPeoples
from src.service.Image.ImageService import compress_image, bytes_to_image, decompress_image
from src.service.detector.DetectorService import FaceDetector

router = APIRouter(
    prefix='/edit_workers',
    tags=['Редактирование данных работников']
)

detect = FaceDetector()


@router.post('/add/{client_email}', name='Добавление работника')
async def add_worker(client_email: str,
                     new_worker: Annotated[AddWorker, Form()],
                     file: Annotated[UploadFile, File],
                     session: Annotated[AsyncSession, Depends(get_async_session)]):
    image = file.file.read()
    statement = select(client).where(client.c.email == client_email)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    client_id = response[0]
    img = compress_image(image)
    photo = bytes_to_image(image)
    result = detect.find_main_descriptor(photo)
    descriptor = np.asarray(result)
    statement = insert(worker).values(id_client=client_id, photo=img, descriptor=descriptor, **new_worker.model_dump())
    await session.execute(statement)
    await session.commit()
    logging.info(f'Worker {new_worker.fullname} successfully added')
    return True


@router.post('/add_photo/photo')
async def photo(file: Annotated[UploadFile, File()],
                session: Annotated[AsyncSession, Depends(get_async_session)]):
    image = file.file.read()
    image = bytes_to_image(image)
    image.show()
    return True


@router.get('/get_human_photo/{worker_id}', name='Получение фото работника')
async def get_human_image(worker_id: int,
                          session: AsyncSession = Depends(get_async_session)):
    statement = select(worker.c.photo).where(
        worker.c.id == worker_id)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    decomp = decompress_image(response[0])
    image = bytes_to_image(decomp)
    buf = BytesIO()
    image.save(buf, format='JPEG', quality=100)
    buf.seek(0)  # important here!
    response = Response(content=decomp, media_type="image/jpeg")
    return response


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
    decomp = decompress_image(response[3])
    # photo = base64.b64decode(response[3])
    people_info = GetHuman(fullname=response[0],
                           birthdate=str(response[1]),
                           phone=response[2])
    logging.info(f'human data {response[0]} received')
    return people_info


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


@router.delete('/del/{client_email}/{human_id}', name='Удаление работника')
async def delete_worker(client_email: str, human_id: int,
                        session: AsyncSession = Depends(get_async_session)):
    statement = select(client).where(client.c.email == client_email)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    client_id = response[0]
    statement = delete(worker).where(worker.c.id == human_id and worker.c.id_client == client_id)
    await session.execute(statement)
    await session.commit()
    logging.info(f'Worker with id {human_id} deleted')
    return True
