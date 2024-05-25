import datetime
import logging

from fastapi import UploadFile, File, Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from src.dao.HumanDAO import human
from src.dao.IdentificateDAO import human_identifications
from src.database.connection.database import get_async_session
from src.service.Image.ImageService import bytes_to_image, compress_image
from src.service.client.ClientService import get_client_token2id_service
from src.service.detector.DetectorService import FaceDetector

detect = FaceDetector()


async def identification_service(client_token: str, file: Annotated[UploadFile, File()],
                                 session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = get_client_token2id_service(client_token, session)
    byte_image = file.file.read()
    person_image = bytes_to_image(byte_image)
    person_descriptor = detect.find_main_descriptor(person_image)
    statement = select(human.c.id, human.c.fullname, human.c.photo, human.c.descriptor)
    descriptor = await session.execute(statement)
    await session.commit()
    known_person = descriptor.fetchall()
    result = detect.comparison(known_person, person_descriptor)
    unknown_person_photo = compress_image(byte_image)
    if not result[2]:
        statement = insert(human_identifications).values(id_client=client_id,
                                                         name=known_person[result[1]][1],
                                                         date=datetime.datetime.today(),
                                                         worker_photo=known_person[result[1]][2],
                                                         person_to_detect=unknown_person_photo,
                                                         conclusion=result[0])
        logging.info(f'Human {known_person[result[1]][1]} identificated')
    else:
        statement = insert(human_identifications).values(id_client=client_id,
                                                         name='Uknown',
                                                         date=datetime.datetime.today(),
                                                         worker_photo=None,
                                                         person_to_detect=unknown_person_photo,
                                                         conclusion=result[0])
        logging.info(f'Person not identificated')
    await session.execute(statement)
    await session.commit()


async def get_identification_service(client_token: str, identification_id: int,
                                     session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = select(human_identifications).where(human_identifications.c.id == identification_id
                                                    and human_identifications.c.id_client == client_id)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    # decompress_photo = decompress_image(response[4])
    # worker_image = bytes_to_image(decompress_photo)
    # worker_image.show()
    # decompress_photo = decompress_image(response[5])
    # person_image = bytes_to_image(decompress_photo)
    # person_image.show()
    logging.info(f'Data of identification with id {identification_id} received')
    return response


async def identification_delete_service(client_token: str, identification_id: int,
                                        session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = delete(human_identifications).where(human_identifications.c.id == identification_id and
                                                    human_identifications.c.id_client == client_id)
    await session.execute(statement)
    await session.commit()
