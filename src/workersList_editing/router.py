import io
from typing import Annotated

import PIL
from PIL.Image import Image
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.workersList_editing.models import worker
from src.workersList_editing.shemas import AddWorker, UpdateWorker
from src.workersList_editing.utils import reduce_image, upload_image

router = APIRouter(
    prefix='/edit_workers',
    tags=['Add_Edit_Delete_Workers']
)


@router.post('/add')
async def add_worker(
        new_worker: Annotated[AddWorker, Form()],
        file: Annotated[UploadFile, File()],
        session: Annotated[AsyncSession, Depends(get_async_session)]):
    byte = upload_image(file)
    statement = insert(worker).values(photo=byte, **new_worker.model_dump())
    await session.execute(statement)
    await session.commit()
    return {'form': new_worker.model_dump(), 'photo': file.filename}


@router.post('/photo')
async def photo(worker_id: int, file: UploadFile, session: AsyncSession = Depends(get_async_session)):
    byte = bytearray(file.file.read())
    statement = update(worker).where(worker.c.id == worker_id).values(photo=byte)
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


@router.post('/reduce_image')
async def reduce(path: str, file: UploadFile):
    image = bytearray(file.file.read())
    img = reduce_image(image)
    img.save(f'{path}new_image.jpg', quality=95)
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
