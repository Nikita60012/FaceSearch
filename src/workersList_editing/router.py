import base64
import io

import PIL
import cv2
from PIL.Image import Image
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

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
    # byte_code = file.file.read()
    # new_worker.photo = str(byte_code)
    # print(byte_code)
    statement = insert(worker).values(**new_worker.model_dump())
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


@router.post('/photo')
async def photo(worker_id: int, file: UploadFile, session: AsyncSession = Depends(get_async_session)):
    byte = bytearray(file.file.read())
    statement = update(worker).where(worker.c.id == worker_id).values(photo=byte)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}
    # img = io.BytesIO(byte)
    # return str(byte)


@router.post('/del')
async def delete_worker(
        del_worker: str, session: AsyncSession = Depends(get_async_session)):
    statement = delete(worker).where(worker.c.fullname == del_worker)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


@router.get("/photo_get")
async def download_file(session: AsyncSession = Depends(get_async_session)):
    statement = select(worker.c.photo)
    result = await session.execute(statement)
    await session.commit()

    img = io.BytesIO(result.first()[0])
    img.seek(0)
    image = PIL.Image.open(img)
    image.show()
    image.save('C:\\search\\5.jpg')

    return img


@router.post('/upd')
async def update_worker(
        upd_worker: UpdateWorker, session: AsyncSession = Depends(get_async_session)):
    statement = update(worker).where(worker.c.id == upd_worker.id) \
        .values(**upd_worker.model_dump())
    print(statement)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}

# @router.g
