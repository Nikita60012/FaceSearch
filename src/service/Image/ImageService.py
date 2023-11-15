import io
import zlib

from PIL import Image


def compress_image(file: bytes):
    compressed_image = zlib.compress(file, zlib.Z_BEST_COMPRESSION)
    return compressed_image


def decompress_image(file: bytes):
    decompressed_image = zlib.decompress(file)
    return decompressed_image


def bytes_to_image(byte_code: bytes):
    image = io.BytesIO(byte_code)
    image.seek(0)
    image = Image.open(image)
    return image
