import logging
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection.database import get_async_session
from src.dto.request.AddHumanDTO import AddWorker
from src.dto.request.UpdateHumanDTO import UpdateWorker
from src.service.Image.ImageService import bytes_to_image
from src.service.detector.DetectorService import FaceDetector
from src.service.human.HumanListService import human_add_service, human_get_service, people_get_service, \
    update_human_service, delete_human_service, get_human_photo

router = APIRouter(
    prefix='/edit_people',
    tags=['Редактирование данных работников']
)

detect = FaceDetector()


@router.post('/human_add/{client_token}', name='Добавление человека')
async def add_human(client_token: str,
                    new_worker: Annotated[AddWorker, Form()],
                    file: Annotated[UploadFile, File],
                    session: Annotated[AsyncSession, Depends(get_async_session)]):
    await human_add_service(client_token, new_worker, file, session)
    logging.info(f'Worker {new_worker.fullname} successfully added')
    return True


@router.post('/add_photo/photo')
async def photo(file: Annotated[UploadFile, File()]):
    image = file.file.read()
    image = bytes_to_image(image)
    image.show()
    return True


@router.get('/get_human_photo/{client_token}/{human_id}', name='Получение фото человека')
async def get_human_image(client_token: str, human_id: int,
                          session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await get_human_photo(client_token, human_id, session)
    return result


@router.get('/human_get/{client_token}/{human_id}', name='Получение данных человека')
async def get_human(client_token: str, human_id: int,
                    session: Annotated[AsyncSession, Depends(get_async_session)]):
    people_info = await human_get_service(client_token, human_id, session)
    logging.info(f'human {people_info.fullname} data received')
    return people_info


@router.get('/people_get/{client_token}', name='Получение данных людей')
async def get_people(client_token: str,
                     session: Annotated[AsyncSession, Depends(get_async_session)]):
    people_list = await people_get_service(client_token, session)
    return people_list


@router.put('/human_update/{client_token}/{human_id}', name='Обновление данных человека')
async def update_human(client_token: str,
                       human_id: int,
                       upd_worker: UpdateWorker,
                       file: Annotated[UploadFile, File],
                       session: Annotated[AsyncSession, Depends(get_async_session)]):
    await update_human_service(client_token, human_id, upd_worker, file, session)
    logging.info(f'Human with id {human_id} data updated')
    return {'status': 'success'}


@router.delete('/human_del/{client_token}/{human_id}', name='Удаление человека')
async def delete_human(client_token: str, human_id: int,
                       session: Annotated[AsyncSession, Depends(get_async_session)]):
    await delete_human_service(client_token, human_id, session)
    logging.info(f'Human with id {human_id} deleted')
    return True
