import datetime

from fastapi import Depends
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from src.dao.AuthorizationSessionDAO import authSessions
from src.dao.ClientDAO import client
from src.dao.HumanDAO import human
from src.dao.SubscribeDAO import subscribe
from src.database.connection.database import get_async_session
from src.dto.request.AddClientDTO import AddClient
from src.dto.request.AuthClientDTO import AuthClient
from src.dto.request.UpdateClientDTO import UpdateClient
from src.dto.request.UpdateDataClientDTO import UpdateDataClient
from src.service.token.TokenService import create_access_token


async def is_client_exist_service(email: str,
                                  session: Annotated[AsyncSession, Depends(get_async_session)]):
    statement = select(client).where(client.c.email == email)
    result = await session.execute(statement)
    await session.commit()
    return result.first()


async def add_client_service(new_client: AddClient,
                             session: Annotated[AsyncSession, Depends(get_async_session)]):
    statement = insert(client).values(email=new_client.email, password=new_client.password, phone=new_client.phone)
    result = await session.execute(statement)
    await session.commit()
    return result.first()


async def client_auth_service(auth_data: AuthClient,
                              session: Annotated[AsyncSession, Depends(get_async_session)]):
    statement = select(client).where(client.c.email == auth_data.email)
    result = await session.execute(statement)
    await session.commit()
    return result.first()


async def get_client_token2id_service(client_token: str,
                                      session: Annotated[AsyncSession, Depends(get_async_session)]):
    statement = select(authSessions.c["id_client", "actual"]).where(authSessions.c.token == client_token)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    if response[1]:
        return response[0]
    else:
        return -1


async def get_client_service(client_token: str,
                             session: Annotated[AsyncSession, Depends(get_async_session)]):

    client_id = await get_client_token2id_service(client_token, session)
    statement = select(client.c['email', 'phone']).where(client.c.id == client_id)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    data = [response[0], response[1]]
    statement = select(subscribe.c['slots', 'end_date_of_subscribe']).where(subscribe.c.id_client == client_id)
    result = await session.execute(statement)
    await session.commit()
    response = result.first()
    days = response[1] - datetime.date.today()
    data += [response[0], days.days]
    statement = select(human.c.id).where(human.c.id_client == client_id)
    result = await session.execute(statement)
    await session.commit()
    response = result.all()
    data += [len(response)]
    return data


async def update_client_service(client_token: str, upd_client: UpdateClient,
                                session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = select(client).where(client.c.id == client_id)
    result = await session.execute(statement)
    await session.commit()
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
    if (await is_client_exist_service(upd_client.email, session) is None) & (upd_client.old_password == response[2]):
        update_data = UpdateDataClient(email=changed_data[0], password=changed_data[1], phone=changed_data[2])
        statement = update(client).where(client.c.id == client_id) \
            .values(**update_data.model_dump())
        await session.execute(statement)
        await session.commit()
        return True
    else:
        return False


async def client_exit_service(client_token: str,
                              session: Annotated[AsyncSession, Depends(get_async_session)]):
    statement = update(authSessions).where(authSessions.c.token == client_token).\
        values(out_date=datetime.datetime.today(), actual=False)
    await session.execute(statement)
    await session.commit()


async def client_delete_service(client_token: str,
                                session: Annotated[AsyncSession, Depends(get_async_session)]):
    client_id = await get_client_token2id_service(client_token, session)
    statement = delete(client).where(client.c.id == client_id)
    await session.execute(statement)
    await session.commit()


async def create_session_service(client_email: str, password: str, ip: str,
                                 session: Annotated[AsyncSession, Depends(get_async_session)]):
    token = create_access_token(
        {
            "email": client_email,
            "ip": ip,
            "password": password,
            "date": str(datetime.datetime.now())
        }
    )
    statement = select(client.c.id).where(client.c.email == client_email)
    result = await session.execute(statement)
    await session.commit()
    statement = insert(authSessions).values(id_client=result.first()[0],
                                            token=token,
                                            enter_date=datetime.datetime.today(),
                                            out_date=None,
                                            ip=ip,
                                            actual=True)
    await session.execute(statement)
    await session.commit()
    return token
