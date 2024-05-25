import logging
from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection.database import get_async_session
from src.dto.request.BuySubscribeDTO import BuySubscribe
from src.dto.request.UpdateSubscribeDTO import UpdateSubscribe
from src.service.subscribe.SubscribeService import buy_subscribe_service, get_subscribe_service, \
    subscribe_update_service, delete_subscribe_service

router = APIRouter(
    prefix='/subscribe',
    tags=['Подписки']
)


@router.post('/buy_subscribe/{client_token}', name='Оформление подписки')
async def buy(client_token: str, buy_subscribe: BuySubscribe,
              session: Annotated[AsyncSession, Depends(get_async_session)]):
    await buy_subscribe_service(client_token, buy_subscribe, session)
    logging.info(f'Subscribe was successfully bought by client with token {client_token}')
    return True


@router.get('/subscribe_get/{client_token}', name='Получение данных о подписке клиента')
async def get_subscribe(client_token: str,
                        session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await get_subscribe_service(client_token, session)
    logging.info(f'Subscribe data of {result[0]} received')
    return {'email': result[0],
            'end date of subscribe': result[1],
            'slots': result[2],
            'last authorization': result[3]}


@router.put('/subscribe_update/{client_token}', name='Обновление данных о подписке клиента')
async def update_subscribe(client_token: str,
                           upd_subscribe: UpdateSubscribe,
                           session: Annotated[AsyncSession, Depends(get_async_session)]):
    await subscribe_update_service(client_token, upd_subscribe, session)
    logging.info(f'Client data with token {client_token} updated')
    return {'status': 'success'}


@router.delete('/subscribe_delete/{client_token}', name='Удаление подписки клиента')
async def delete_subscribe(client_token: str,
                           session: Annotated[AsyncSession, Depends(get_async_session)]):
    await delete_subscribe_service(client_token, session)
    logging.info(f'Client with token {client_token} deleted')
    return {'status': 'success'}
