from datetime import date, timedelta

from fastapi import Depends
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from src.dao.SubscribeDAO import subscribe
from src.database.connection.database import get_async_session
from src.dto.request.BuySubscribeDTO import BuySubscribe
from src.dto.request.UpdateSubscribeDTO import UpdateSubscribe
from src.service.client.ClientService import get_client_token2id_service


async def buy_subscribe_service(client_token: str,
                                buy_subscribe: BuySubscribe,
                                session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = get_client_token2id_service(client_token, session)
    end_date_of_subscribe = date.today() + timedelta(days=buy_subscribe.days)
    statement = insert(subscribe).values(id_client=client_id,
                                         end_date_of_subscribe=end_date_of_subscribe,
                                         slots=buy_subscribe.slots,
                                         last_authorization=buy_subscribe.last_authorization)
    await session.execute(statement)
    await session.commit()


async def get_subscribe_service(client_token: str,
                                session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = get_client_token2id_service(client_token, session)
    statement = select(subscribe).where(subscribe.c.id == client_id)
    result = await session.execute(statement)
    await session.commit()
    return result.first()[0]


async def subscribe_update_service(client_token: str,
                                   upd_subscribe: UpdateSubscribe,
                                   session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = get_client_token2id_service(client_token, session)
    statement = update(subscribe).where(subscribe.c.id_client == client_id) \
        .values(**upd_subscribe.model_dump())
    await session.execute(statement)
    await session.commit()


async def delete_subscribe_service(client_token: str,
                                   session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = get_client_token2id_service(client_token, session)
    statement = delete(subscribe).where(subscribe.c.id_client == client_id)
    await session.execute(statement)
    await session.commit()
