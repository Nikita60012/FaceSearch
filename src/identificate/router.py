import io
from typing import Annotated

from PIL import Image
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.identificate.utils import comparison
from src.workersList_editing.models import worker
from src.workersList_editing.utils import make_descriptor

router = APIRouter(
    prefix='/identify_workers',
    tags=['Идентификация']
)


@router.post('/identify', name='Идентифицирование (в работе)')
async def identify(file: Annotated[UploadFile, File()],
                   landmarks_data: Annotated[UploadFile, File],
                   data_model: Annotated[UploadFile, File],
                   session: Annotated[AsyncSession, Depends(get_async_session)]):
    byte = bytearray(file.file.read())
    image = io.BytesIO(byte)
    image.seek(0)
    person_image = Image.open(image)
    person_descriptor = make_descriptor(person_image, landmarks_data, data_model)
    statement = select(worker.c.descriptor)
    worker_descriptors = await session.execute(statement)
    await session.commit()
    result = comparison(landmarks_data, data_model, worker_descriptors, person_descriptor)
    return result
