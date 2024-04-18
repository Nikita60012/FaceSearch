import logging
from typing import Annotated

from fastapi import Form, Depends, APIRouter
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection.database import get_async_session
from src.dao.IdentificateDAO import worker_identifications
from src.dto.request.AddClientDTO import AddClient
from src.dto.request.AuthClientDTO import AuthClient
from src.dto.request.UpdateClientDTO import UpdateClient
from src.dto.response.getClientDTO import GetClient
from src.service.Image.ImageService import decompress_image
from src.dao.ClientDAO import client
from src.service.Image.ImageService import bytes_to_image

router = APIRouter(
    prefix='/client',
    tags=['Клиент']
)


@router.post('/registration', name='Регистрация')
async def registration(new_client: AddClient,
                       session: Annotated[AsyncSession, Depends(get_async_session)]):
    email = new_client.email
    statement = select(client).where(client.c.email == email)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    if response is None:
        statement = insert(client).values(**new_client.model_dump())
        await session.execute(statement)
        await session.commit()
        logging.info(f'Client {new_client.email} successfully added')
        return True
    else:
        return False


@router.get('/client_get/{client_email}', name='Получение данных клиента')
async def get_client_email(client_email: str,
                           session: AsyncSession = Depends(get_async_session)):
    statement = select(client).where(client.c.email == client_email)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    logging.info(f'Client data {response[1]} received')
    get_client = GetClient(email=response[1], phone=response[3])
    return get_client


@router.post('/client_authentication/', name='Авторизация клиента')
async def authentication(auth_data: AuthClient, session: AsyncSession = Depends(get_async_session)):
    statement = select(client).where(client.c.email == auth_data.email)
    try:
        result = await session.execute(statement)
        await session.commit()
        response = result.first()
        if auth_data.password == response[2]:
            return True
        else:
            return False
    except TypeError:
        return False


@router.put('/client_update/{client_email}', name='Обновление данных клиента')
async def update_client(client_email: str, upd_client: UpdateClient,
                        session: AsyncSession = Depends(get_async_session)):
    statement = select(client).where(client.c.email == client_email)
    result = await session.execute(statement)
    await session.commit()
    email = upd_client.email
    response = result.first()
    changed_data = []
    if upd_client.email != "":
        changed_data.append(upd_client.email)
    else:
        changed_data.append(response[1])
    if upd_client.new_password != "":
        changed_data.append(upd_client.new_password)
    else:
        changed_data.append(response[2])
    if upd_client.phone != "":
        changed_data.append(upd_client.phone)
    else:
        changed_data.append(response[3])
    statement = select(client).where(client.c.email == email)
    result = await session.execute(statement)
    await session.commit()
    email_exists_check = result.first()
    if email_exists_check[1] == response[1]:
        email_exists_check = None
    if upd_client.old_password == response[2] and email_exists_check is None:
        update_data = AddClient(email=changed_data[0], password=changed_data[1], phone=changed_data[2])
        statement = update(client).where(client.c.email == client_email) \
            .values(**update_data.model_dump())
        await session.execute(statement)
        await session.commit()
        logging.info(f'Client data with id {client_email} updated')
        return True
    else:
        return False


@router.delete('/client_delete/{client_id}', name='Удаление клиента')
async def delete_client(client_id: int,
                        session: AsyncSession = Depends(get_async_session)):
    statement = delete(client).where(client.c.id == client_id)
    await session.execute(statement)
    await session.commit()
    logging.info(f'Client with id {client_id} deleted')
    return {'status': 'success'}
