import io
from typing import Annotated

from PIL import Image
from fastapi import APIRouter, UploadFile, File

router = APIRouter(
    prefix='/identify_workers',
    tags=['Идентификация']
)


@router.post('/identify', name='Идентифицирование (в работе)')
async def identify(file: Annotated[UploadFile, File()]):
    byte = bytearray(file.file.read())
    image = io.BytesIO(byte)
    image.seek(0)
    img = Image.open(image)
    return img.show()
