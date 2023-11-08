import io

from PIL import Image
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.workersList_editing.models import worker
from src.workersList_editing.shemas import AddWorker, UpdateWorker
from src.workersList_editing.utils import reduce_image, bytes_to_image, make_descriptor

router = APIRouter(
    prefix='/edit_workers',
    tags=['Редактирование данных работников']
)


@router.post('/add', name='Добавление работника')
async def add_worker(new_worker: AddWorker, session: AsyncSession = Depends(get_async_session)):
    statement = insert(worker).values(**new_worker.model_dump())
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


@router.post('/reduce_image', name='Сжатие изображения')
async def reduce(path: str, file: UploadFile):
    image = bytearray(file.file.read())
    img = reduce_image(image)
    img.save(path, quality=95)
    return {'status': 'success'}


@router.get('/photo_get', name='Получение фотографии работника')
async def show_worker_photo(worker_id: int, session: AsyncSession = Depends(get_async_session)):
    statement = select(worker.c.photo).where(worker.c.id == worker_id)
    result = await session.execute(statement)
    await session.commit()

    img = io.BytesIO(result.first()[0])
    img.seek(0)
    image = Image.open(img)
    image.show()

    return {'status': 'success'}


@router.put('/photo', name='Установление фотографии работника')
async def photo(worker_id: int, file: UploadFile, session: AsyncSession = Depends(get_async_session)):
    byte = bytearray(file.file.read())
    statement = update(worker).where(worker.c.id == worker_id).values(photo=byte)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


@router.put('/upd', name='Обновление данных работника')
async def update_worker(
        upd_worker: UpdateWorker, session: AsyncSession = Depends(get_async_session)):
    statement = update(worker).where(worker.c.id == upd_worker.id) \
        .values(**upd_worker.model_dump())
    print(statement)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


@router.put('/descriptor_making', name='Создание дескрипторов фотографии')
async def descriptor_maker(worker_id: int,
                           landmarks_data: UploadFile,
                           data_model: UploadFile,
                           session: AsyncSession = Depends(get_async_session)):
    statement = select(worker.c.photo).where(worker.c.id == worker_id)
    result = await session.execute(statement)
    await session.commit()
    image = bytes_to_image(result)
    result = make_descriptor(image, landmarks_data, data_model)
    statement = update(worker).where(worker.c.id == worker_id).values(descriptor=str(result[0]))
    await session.execute(statement)
    await session.commit()
    return str(result[0])


@router.delete('/del', name='Удаление работника')
async def delete_worker(
        del_worker: str, session: AsyncSession = Depends(get_async_session)):
    statement = delete(worker).where(worker.c.fullname == del_worker)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}
