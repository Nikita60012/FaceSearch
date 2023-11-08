import io
from typing import Annotated

import PIL
from fastapi import APIRouter, UploadFile, File

router = APIRouter(
    prefix='/identify_workers',
    tags=['Identificate']
)


@router.post('/identify')
async def Identify(file: Annotated[UploadFile, File()]):
    byte = bytearray(file.file.read())
    image = io.BytesIO(byte)
    image.seek(0)
    img = PIL.Image.open(image)
    return img.show()
