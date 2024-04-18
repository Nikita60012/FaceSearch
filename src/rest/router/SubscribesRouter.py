import logging
from datetime import date, timedelta
from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.ClientDAO import client
from src.dao.SubscribesDAO import subscribe
from src.database.connection.database import get_async_session
from src.dto.request.BuySubscribeDTO import BuySubscribe
from src.dto.request.UpdateSubscribeDTO import UpdateSubscribe

router = APIRouter(
    prefix='/subscribes',
    tags=['Подписки']
)


@router.post('/buy_subscribe/{client_email}', name='Оформление подписки')
async def buy(client_email: str, buy_subscribe: BuySubscribe,
              session: Annotated[AsyncSession, Depends(get_async_session)]):
    end_date_of_subscribe = date.today()
    end_date_of_subscribe = end_date_of_subscribe + timedelta(days=buy_subscribe.days)
    statement = select(client.c.id).where(client.c.email == client_email)
    result = await session.execute(statement)
    await session.commit()
    client_id = result.first()[0]
    statement = insert(subscribe).values(id_client=client_id,
                                         end_date_of_subscribe=end_date_of_subscribe,
                                         slots=buy_subscribe.slots,
                                         last_authorization=buy_subscribe.last_authorization)
    await session.execute(statement)
    await session.commit()
    logging.info(f'Subscribe was successfully bought by {client_email}')
    return True


@router.get('/subscribe_get/{email}', name='Получение данных о подписке клиента')
async def get_subscribe(email: str,
                        session: AsyncSession = Depends(get_async_session)):
    statement = select(subscribe).where(subscribe.c.email == email)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    logging.info(f'Subscribe data of {response[0]} received')
    return {'email': response[0],
            'end date of subscribe': response[1],
            'slots': response[2],
            'last authorization': response[3]}


@router.put('/subscribe_update/{email}', name='Обновление данных о подписке клиента')
async def update_client(upd_subscribe: UpdateSubscribe,
                        session: AsyncSession = Depends(get_async_session)):
    statement = update(subscribe).where(subscribe.c.email == upd_subscribe.email) \
        .values(**upd_subscribe.model_dump())
    await session.execute(statement)
    await session.commit()
    logging.info(f'Client data with email {upd_subscribe.email} updated')
    return {'status': 'success'}


@router.delete('/subscribe_delete/{email}', name='Удаление подписки клиента')
async def delete_client(email: str,
                        session: AsyncSession = Depends(get_async_session)):
    statement = select(client.c.id).where(client.c.email == email)
    print(statement)
    result = await session.execute(statement)
    await session.commit()
    client_id = result.first()[0]
    statement = delete(subscribe).where(subscribe.c.id_client == client_id)
    await session.execute(statement)
    await session.commit()
    logging.info(f'Client with email {email} deleted')
    return {'status': 'success'}
