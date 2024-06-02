import base64
import datetime
import logging

from fastapi import Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from typing_extensions import Annotated

from src.dao.HumanDAO import human
from src.dao.IdentificateDAO import human_identifications
from src.database.connection.database import get_async_session
from src.service.Image.ImageService import bytes_to_image, compress_image, decompress_image
from src.service.client.ClientService import get_client_token2id_service
from src.service.detector.DetectorService import FaceDetector

detect = FaceDetector()


async def identification_service(client_token: str, image: str,
                                 session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    photo = base64.b64decode(image)
    person_image = bytes_to_image(photo)
    person_descriptor = detect.find_main_descriptor(person_image)
    statement = select(human.c.id, human.c.fullname, human.c.photo, human.c.descriptor)
    descriptor = await session.execute(statement)
    await session.commit()
    known_person = descriptor.fetchall()
    result = detect.comparison(known_person, person_descriptor)
    unknown_person_photo = compress_image(photo)
    date = datetime.datetime.today()
    if not result[2]:
        statement = insert(human_identifications).values(id_client=client_id,
                                                         name=known_person[result[1]][1],
                                                         date=date,
                                                         known_person_photo=known_person[result[1]][2],
                                                         person_to_detect=unknown_person_photo,
                                                         conclusion=(result[0][:-1] + known_person[result[1]][1]))
        logging.info(f'Human {known_person[result[1]][1]} identificated')
        statement2 = select(human_identifications.c.id) \
            .where((human_identifications.c.id_client == client_id))\
            .where(human_identifications.c.name == known_person[result[1]][1])\
            .where(human_identifications.c.date == date) \
            .where(human_identifications.c.conclusion == (result[0][:-1] + known_person[result[1]][1]))
    else:
        statement = insert(human_identifications).values(id_client=client_id,
                                                         name=known_person[result[1]][1],
                                                         date=date,
                                                         known_person_photo=known_person[result[1]][2],
                                                         person_to_detect=unknown_person_photo,
                                                         conclusion=(result[0] + known_person[result[1]][1]))
        logging.info(f'Person not identificated')
        statement2 = select(human_identifications.c.id) \
            .where(human_identifications.c.id_client == client_id)\
            .where(human_identifications.c.name == known_person[result[1]][1])\
            .where(human_identifications.c.date == date)\
            .where(human_identifications.c.conclusion == (result[0] + known_person[result[1]][1]))
    await session.execute(statement)
    await session.commit()
    result = await session.execute(statement2)
    await session.commit()
    identification_id = result.first()
    return identification_id[0]


async def get_identification_service(client_token: str, identification_id: int,
                                     session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = select(human_identifications.c["name", "conclusion"]).where(
        (human_identifications.c.id_client == client_id) &
        (human_identifications.c.id == identification_id))
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    data = [response[1]]
    statement = select(human.c.id).where(human.c.fullname == response[0]).where(human.c.id_client == client_id)
    result = await session.execute(statement)
    await session.commit()
    data.append(result.first()[0])
    # decompress_photo = decompress_image(response[4])
    # worker_image = bytes_to_image(decompress_photo)
    # worker_image.show()
    # decompress_photo = decompress_image(response[5])
    # person_image = bytes_to_image(decompress_photo)
    # person_image.show()
    logging.info(f'Data of identification with id {identification_id} received')
    return data


async def identification_delete_service(client_token: str, identification_id: int,
                                        session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = delete(human_identifications).where((human_identifications.c.id == identification_id) &
                                                    (human_identifications.c.id_client == client_id))
    await session.execute(statement)
    await session.commit()


async def get_identification_known_person_photo_service(client_token: str, identification_id: int,
                                                        session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = select(human_identifications.c.known_person_photo). \
        where((human_identifications.c.id_client == client_id) & (human_identifications.c.id == identification_id))
    result = await session.execute(statement)
    await session.commit()
    photo = decompress_image(result.first()[0])
    response = Response(content=photo, media_type="image/jpeg")
    return response


async def get_identification_unknown_person_photo_service(client_token: str, identification_id: int,
                                                          session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = select(human_identifications.c.person_to_detect). \
        where((human_identifications.c.id_client == client_id) & (human_identifications.c.id == identification_id))
    result = await session.execute(statement)
    await session.commit()
    photo = decompress_image(result.first()[0])
    response = Response(content=photo, media_type="image/jpeg")
    return response


async def identification_check_people_availability_service(client_token: str,
                                                           session: Annotated[
                                                               AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = select(human).where(human.c.id_client == client_id)
    result = await session.execute(statement)
    await session.commit()
    response = result.all()
    if len(response) > 0:
        return True
    else:
        return False
