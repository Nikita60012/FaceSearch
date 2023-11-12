import io
from typing import Annotated

from PIL import Image
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.identificate.models import worker_identifications
from src.identificate.utils import comparison
from src.workersList_editing.models import worker
from src.workersList_editing.utils import make_descriptor, bytes_to_image

router = APIRouter(
    prefix='/identify_workers',
    tags=['Идентификация']
)


@router.post('/identify', name='Идентифицирование (в работе)')
async def identify(file: Annotated[UploadFile, File()],
                   landmarks_data: Annotated[UploadFile, File],
                   data_model: Annotated[UploadFile, File],
                   session: Annotated[AsyncSession, Depends(get_async_session)]):
    byte_image = bytearray(file.file.read())
    person_image = bytes_to_image(byte_image)
    person_descriptor = make_descriptor(person_image, landmarks_data, data_model)
    statement = select(worker.c.descriptor)
    descriptor = await session.execute(statement)
    await session.commit()
    worker_descriptor = descriptor.fetchall()
    result = comparison(landmarks_data, data_model, worker_descriptor, person_descriptor[0])
    statement = insert(worker_identifications).values()
    return result
