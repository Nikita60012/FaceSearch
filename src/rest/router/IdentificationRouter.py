import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection.database import get_async_session
from src.dto.request.IdentificationDTO import Identification
from src.dto.response.GetIdentificationResultDTO import GetIdentificationResult
from src.service.detector.DetectorService import FaceDetector
from src.service.identification.IdentificationService import identification_service, get_identification_service, \
    identification_delete_service, get_identification_known_person_photo_service, \
    get_identification_unknown_person_photo_service, identification_check_people_availability_service

router = APIRouter(
    prefix='/identification_people',
    tags=['Идентификация']
)

detect = FaceDetector()


@router.post('/identification/{client_token}', name='Идентификация')
async def identify(client_token: str, photo: Identification,
                   session: Annotated[AsyncSession, Depends(get_async_session)]):
    try:
        await identification_service(client_token, photo.photo, session)
        return True
    except Exception:
        return False


@router.get('/identification_get/{client_token}/{identification_id}', name='получение записи идентификации')
async def get_identification(client_token: str, identification_id: int,
                             session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await get_identification_service(client_token, identification_id, session)
    return GetIdentificationResult(human_id=result[1], conclusion=result[0])


@router.get('/identification_get_known_person_photo/{client_token}/{identification_id}')
async def get_identification_known_person_photo(client_token: str, identification_id: int,
                                                session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await get_identification_known_person_photo_service(client_token, identification_id, session)
    return result


@router.get('/identification_get_unknown_person_photo/{client_token}/{identification_id}')
async def get_identification_unknown_person_photo(client_token: str, identification_id: int,
                                                  session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await get_identification_unknown_person_photo_service(client_token, identification_id, session)
    return result


@router.get('/identification_check_people_availability/{client_token}')
async def identification_check_people_availability(client_token: str,
                                                   session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await identification_check_people_availability_service(client_token, session)
    return result


@router.delete('/identification_delete/{identification_id}', name='удаление записи идентификации')
async def delete_identification(client_token: str, identification_id: int,
                                session: Annotated[AsyncSession, Depends(get_async_session)]):
    await identification_delete_service(client_token, identification_id, session)
    logging.info(f'Data of identification with id {identification_id} deleted')
    return {'status': 'success'}
