import base64
import datetime
import logging
from io import BytesIO

import numpy as np
from click import File
from fastapi import UploadFile, Form, Depends
from starlette.responses import Response
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated
from src.dao.HumanDAO import human
from src.database.connection.database import get_async_session
from src.dto.request.AddHumanDTO import HumanAdd
from src.dto.request.UpdateHumanDTO import UpdateWorker
from src.dto.response.GetHumanDTO import GetHuman
from src.dto.response.GetPeoplesDTO import GetPeoples
from src.service.Image.ImageService import compress_image, bytes_to_image, decompress_image
from src.service.client.ClientService import get_client_token2id_service
from src.service.detector.DetectorService import FaceDetector

detect = FaceDetector()


async def human_add_service(client_token: str,
                            new_worker: HumanAdd,
                            session: Annotated[AsyncSession, Depends(get_async_session)]):
    image = base64.b64decode(new_worker.photo)
    client_id = await get_client_token2id_service(client_token, session)
    img = compress_image(image)
    photo = bytes_to_image(image)
    try:
        result = detect.find_main_descriptor(photo)
        descriptor = np.asarray(result)
        birthdate = datetime.datetime.strptime(new_worker.birthdate, "%d%m%Y").date()
        statement = insert(human).values(id_client=client_id, photo=img, descriptor=descriptor, birthdate=birthdate,
                                         phone=new_worker.phone, fullname=new_worker.fullname)
        await session.execute(statement)
        await session.commit()
        return True
    except TypeError:
        logging.error('Wrong photo')
        return False


async def human_get_service(client_token: str, human_id: int,
                            session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = select(human.c["fullname", "birthdate", "phone", "photo"]).where(
        (human.c.id == human_id) & (human.c.id_client == client_id))
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    # decompress = decompress_image(response[3])
    # photo = base64.b64decode(response[3])
    return GetHuman(fullname=response[0],
                    birthdate=str(response[1]),
                    phone=response[2])


async def people_get_service(client_token: str,
                             session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = select(human.c["id", "fullname"]).where(human.c.id_client == client_id)
    result = await session.execute(statement)
    await session.commit()
    response = result.all()
    people_list = []
    for people in response:
        people_list.append(GetPeoples(id=people[0], fullname=people[1]))
    logging.info(f'Client {client_id} people data received')
    return people_list


async def update_human_service(client_token: str,
                               human_id: int,
                               upd_worker: UpdateWorker,
                               session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    image = base64.b64decode(upd_worker.photo)
    img = compress_image(image)
    photo = bytes_to_image(image)
    try:
        raw_descriptor = detect.find_main_descriptor(photo)
        descriptor = np.asarray(raw_descriptor)
        statement = update(human).where((human.c.id_client == client_id) & (human.c.id == human_id)) \
            .values(photo=img, descriptor=descriptor, **upd_worker.model_dump())
        await session.execute(statement)
        await session.commit()
        return True
    except TypeError:
        return False


async def delete_human_service(client_token: str, human_id: int,
                               session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = delete(human).where((human.c.id_client == client_id) & (human.c.id == human_id))
    await session.execute(statement)
    await session.commit()


async def get_human_photo_service(client_token: str, human_id: int,
                                  session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = select(human.c.photo).where((human.c.id_client == client_id) & (human.c.id == human_id))
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    decompress = decompress_image(response[0])
    # image = bytes_to_image(decompress)
    # buf = BytesIO()
    # image.save(buf, format='JPEG', quality=100)
    # buf.seek(0)  # important here!
    # image.show()
    response = Response(content=decompress, media_type="image/jpeg")
    return response
