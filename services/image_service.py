"""
Image compression/resizing and format conversion using Pillow.
"""

import io
from PIL import Image

SUPPORTED_FORMATS = {"jpeg", "jpg", "png", "webp", "bmp"}


def compress_image(
    file_bytes: bytes,
    quality: int = 80,
    max_width: int | None = None,
    max_height: int | None = None,
) -> tuple[bytes, str]:
    """
    Compresses an image and optionally resizes it (maintaining aspect
    ratio if only one dimension is given). Returns (image_bytes, format).
    """
    image = Image.open(io.BytesIO(file_bytes))
    original_format = (image.format or "JPEG").upper()

    if max_width or max_height:
        image = _resize_maintaining_aspect(image, max_width, max_height)

    output = io.BytesIO()

    # PNG doesn't support a "quality" parameter the same way JPEG does -
    # use optimize instead. WEBP and JPEG both support quality directly.
    if original_format == "PNG":
        image.save(output, format="PNG", optimize=True)
    else:
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        image.save(output, format=original_format, quality=quality, optimize=True)

    return output.getvalue(), original_format.lower()


def convert_image(file_bytes: bytes, target_format: str) -> bytes:
    """
    Converts an image to the target format (jpeg, png, webp, bmp).
    """
    target_format = target_format.lower()
    if target_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported target format: {target_format}")

    image = Image.open(io.BytesIO(file_bytes))

    save_format = "JPEG" if target_format in ("jpeg", "jpg") else target_format.upper()

    # JPEG/BMP don't support transparency - flatten onto white if needed
    if save_format in ("JPEG", "BMP") and image.mode in ("RGBA", "P"):
        background = Image.new("RGB", image.size, "white")
        image = image.convert("RGBA")
        background.paste(image, mask=image.split()[-1])
        image = background

    output = io.BytesIO()
    image.save(output, format=save_format)
    return output.getvalue()


def _resize_maintaining_aspect(image: Image.Image, max_width: int | None, max_height: int | None) -> Image.Image:
    original_width, original_height = image.size

    if max_width and max_height:
        image.thumbnail((max_width, max_height))
        return image

    if max_width:
        ratio = max_width / original_width
        new_size = (max_width, int(original_height * ratio))
    else:
        ratio = max_height / original_height
        new_size = (int(original_width * ratio), max_height)

    return image.resize(new_size, Image.LANCZOS)
