import datetime
import io
import logging
import struct
from typing import Annotated

from PIL import Image
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.identificate.models import worker_identifications
from src.identificate.utils import comparison
from src.workersList_editing.models import worker
from src.workersList_editing.utils import make_descriptor, bytes_to_image, reduce_image, image_to_bytes

router = APIRouter(
    prefix='/identify_workers',
    tags=['Идентификация']
)


@router.post('/identify', name='Идентифицирование')
async def identify(file: Annotated[UploadFile, File()],
                   landmarks_data: Annotated[UploadFile, File],
                   data_model: Annotated[UploadFile, File],
                   session: Annotated[AsyncSession, Depends(get_async_session)]):
    byte_image = bytearray(file.file.read())
    person_image = bytes_to_image(byte_image)
    person_descriptor = make_descriptor(person_image, landmarks_data, data_model)
    statement = select(worker.c.fullname, worker.c.photo, worker.c.descriptor)
    descriptor = await session.execute(statement)
    await session.commit()
    worker_person = descriptor.fetchall()
    result = comparison(landmarks_data, data_model, worker_person, person_descriptor[0])
    person_photo = reduce_image(byte_image)
    person_photo = image_to_bytes(person_photo)
    if(not result[2]):
        statement = insert(worker_identifications).values(name=worker_person[result[1]][0],
                                                      date=datetime.datetime.today(),
                                                      worker_photo=worker_person[result[1]][1],
                                                      person_to_detect=person_photo,
                                                      conclusion=result[0])
    else:
        statement = insert(worker_identifications).values(name='Uknown',
                                                          date=datetime.datetime.today(),
                                                          worker_photo=None,
                                                          person_to_detect=person_photo,
                                                          conclusion=result[0])
    await session.execute(statement)
    await session.commit()
    return result[0]


@router.get('/get_identification/{identification_id}', name='получение записи идентификации')
async def get_identification(identification_id: int,
                             session: Annotated[AsyncSession, Depends(get_async_session)]):
    statement = select(worker_identifications).where(worker_identifications.c.id == identification_id)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    worker_image = bytes_to_image(response[3])
    worker_image.show()
    person_image = bytes_to_image(response[4])
    person_image.show()
    return {'name': response[1],
            'date': response[2],
            'conclusion': response[5]}


@router.delete('/delete_identification/{identification_id}', name='удаление записи идентификации')
async def delete_identification(identification_id: int,
                                session: Annotated[AsyncSession, Depends(get_async_session)]):
    statement = delete(worker_identifications).where(worker.c.id == identification_id)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}
