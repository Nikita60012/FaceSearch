import logging
from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection.database import get_async_session
from src.dto.request.AddClientDTO import AddClient
from src.dto.request.AuthClientDTO import AuthClient
from src.dto.request.UpdateClientDTO import UpdateClient
from src.dto.response.GetTokenClientDTO import GetTokenClientDTO
from src.service.client.ClientService import create_session_service, is_client_exist_service, add_client_service, \
    client_auth_service, update_client_service, client_delete_service, get_client_service, client_exit_service

router = APIRouter(
    prefix='/client',
    tags=['Клиент']
)


@router.post('/registration/', name='Регистрация')
async def registration(new_client: AddClient,
                       session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await is_client_exist_service(new_client.email, session)
    if result is None:
        await add_client_service(new_client, session)
        logging.info(f'Client {new_client.email} successfully added')
        token = await create_session_service(new_client.email, new_client.password, new_client.ip, session)
        return GetTokenClientDTO(enter=True, token=token)
    else:
        return GetTokenClientDTO(enter=False, token="empty")


@router.get('/client_get/{client_token}', name='Получение данных клиента')
async def get_client_email(client_token: str,
                           session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await get_client_service(client_token, session)
    logging.info(f'Client data {result[1]} received')
    return {"email": result[0],
            "phone": result[1],
            "slots": result[2],
            "days": result[3],
            "slots_occupied": result[4]}


@router.post('/client_authentication/', name='Авторизация клиента')
async def authentication(auth_data: AuthClient,
                         session: Annotated[AsyncSession, Depends(get_async_session)]):
    try:
        response = await client_auth_service(auth_data, session)
        if auth_data.password == response[2]:
            token = await create_session_service(auth_data.email,
                                                 auth_data.password,
                                                 auth_data.ip,
                                                 session)
            return GetTokenClientDTO(enter=True, token=token)
        else:
            return GetTokenClientDTO(enter=False, token="empty")
    except TypeError:
        return GetTokenClientDTO(enter=False, token="empty")


@router.put('/client_update/{client_token}', name='Обновление данных клиента')
async def update_client(client_token: str, upd_client: UpdateClient,
                        session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await update_client_service(client_token, upd_client, session)
    logging.info(f'Client data with token {client_token} updated')
    return result


@router.put('/client_exit/{client_token}', name='Завершение сессии')
async def exit_client(client_token: str,
                      session: Annotated[AsyncSession, Depends(get_async_session)]):
    await client_exit_service(client_token, session)
    logging.info(f'Client with token {client_token} exit')
    return {'status': 'success'}


@router.delete('/client_delete/{client_token}', name='Удаление клиента')
async def delete_client(client_token: str,
                        session: Annotated[AsyncSession, Depends(get_async_session)]):
    await client_delete_service(client_token, session)
    logging.info(f'Client with token {client_token} deleted')
    return {'status': 'success'}



