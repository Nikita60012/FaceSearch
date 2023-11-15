import datetime
import logging
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.identificate.models import worker_identifications
from src.utils import comparison, decompress_image
from src.workersList_editing.models import worker
from src.utils import make_descriptor, bytes_to_image, compress_image

router = APIRouter(
    prefix='/identify_workers',
    tags=['Идентификация']
)


@router.post('/identify', name='Идентифицирование')
async def identify(file: Annotated[UploadFile, File()],
                   session: Annotated[AsyncSession, Depends(get_async_session)]):
    byte_image = file.file.read()
    person_image = bytes_to_image(byte_image)
    person_descriptor = make_descriptor(person_image)
    statement = select(worker.c.id, worker.c.fullname, worker.c.photo, worker.c.descriptor)
    descriptor = await session.execute(statement)
    await session.commit()
    worker_person = descriptor.fetchall()
    result = comparison(worker_person, person_descriptor)
    person_photo = compress_image(byte_image)
    if not result[2]:
        statement = insert(worker_identifications).values(name=worker_person[result[1]][1],
                                                      date=datetime.datetime.today(),
                                                      worker_photo=worker_person[result[1]][2],
                                                      person_to_detect=person_photo,
                                                      conclusion=result[0])
        logging.info(f'Worker {worker_person[result[1]][1]} identificated')
    else:
        statement = insert(worker_identifications).values(name='Uknown',
                                                          date=datetime.datetime.today(),
                                                          worker_photo=None,
                                                          person_to_detect=person_photo,
                                                          conclusion=result[0])
        logging.info(f'Person not identificated')
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
    decomp_image = decompress_image(response[3])
    worker_image = bytes_to_image(decomp_image)
    worker_image.show()
    decomp_image = decompress_image(response[4])
    person_image = bytes_to_image(decomp_image)
    person_image.show()
    logging.info(f'Data of identification with id {identification_id} received')
    return {'name': response[1],
            'date': response[2],
            'conclusion': response[5]}


@router.delete('/delete_identification/{identification_id}', name='удаление записи идентификации')
async def delete_identification(identification_id: int,
                                session: Annotated[AsyncSession, Depends(get_async_session)]):
    statement = delete(worker_identifications).where(worker_identifications.c.id == identification_id)
    await session.execute(statement)
    await session.commit()
    logging.info(f'ЗData of identification with id {identification_id} deleted')
    return {'status': 'success'}
