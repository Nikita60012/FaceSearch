from fastapi import APIRouter, Depends
from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.workersList_editing.models import worker
from src.workersList_editing.shemas import AddWorker, UpdateWorker

router = APIRouter(
    prefix='/edit_workers',
    tags=['Add_Edit_Delete_Workers']
)


@router.post('/add')
async def add_worker(
        new_worker: AddWorker, session: AsyncSession = Depends(get_async_session)):
    statement = insert(worker).values(**new_worker.model_dump())
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


@router.post('/del')
async def delete_worker(
        del_worker: str, session: AsyncSession = Depends(get_async_session)):
    statement = delete(worker).where(worker.c.fullname == del_worker)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


@router.post('/upd')
async def update_worker(
        upd_worker: UpdateWorker, session: AsyncSession = Depends(get_async_session)):
    statement = update(worker).where(worker.c.id == upd_worker.id) \
        .values(**upd_worker.model_dump())
    print(statement)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}
