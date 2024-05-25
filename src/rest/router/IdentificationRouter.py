import logging
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection.database import get_async_session
from src.service.detector.DetectorService import FaceDetector
from src.service.identification.IdentificationService import identification_service, get_identification_service, \
    identification_delete_service

router = APIRouter(
    prefix='/identification_people',
    tags=['Идентификация']
)

detect = FaceDetector()


@router.post('/identification/{client_token}', name='Идентификация')
async def identify(client_token: str, file: Annotated[UploadFile, File()],
                   session: Annotated[AsyncSession, Depends(get_async_session)]):
    await identification_service(client_token, file, session)
    return {"status": "success"}


@router.get('/identification_get/{identification_id}', name='получение записи идентификации')
async def get_identification(client_token: str, identification_id: int,
                             session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await get_identification_service(client_token, identification_id, session)
    return {'name': result[2],
            'date': result[3],
            'conclusion': result[6]}


@router.delete('/identification_delete/{identification_id}', name='удаление записи идентификации')
async def delete_identification(client_token: str, identification_id: int,
                                session: Annotated[AsyncSession, Depends(get_async_session)]):
    await identification_delete_service(client_token, identification_id, session)
    logging.info(f'Data of identification with id {identification_id} deleted')
    return {'status': 'success'}
