from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from typing import Optional

from services.image_service import compress_image, convert_image
from services.watermark_service import add_text_watermark, add_image_watermark

router = APIRouter(prefix="/api/image", tags=["image"])

MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB


@router.post("/compress")
async def image_compress(
    file: UploadFile = File(...),
    quality: int = Form(80),
    max_width: Optional[int] = Form(None),
    max_height: Optional[int] = Form(None),
):
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 15MB).")

    try:
        result_bytes, fmt = compress_image(file_bytes, quality=quality, max_width=max_width, max_height=max_height)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not process image: {str(e)}")

    media_type = f"image/{fmt if fmt != 'jpg' else 'jpeg'}"
    return Response(content=result_bytes, media_type=media_type)


@router.post("/convert")
async def image_convert(
    file: UploadFile = File(...),
    target_format: str = Form(...),
):
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 15MB).")

    try:
        result_bytes = convert_image(file_bytes, target_format)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not convert image: {str(e)}")

    media_type = f"image/{target_format if target_format != 'jpg' else 'jpeg'}"
    return Response(content=result_bytes, media_type=media_type)


@router.post("/watermark")
async def image_watermark(
    file: UploadFile = File(...),
    watermark_type: str = Form(...),  # "text" or "image"
    text: Optional[str] = Form(None),
    position: str = Form("bottom-right"),
    opacity: int = Form(128),
    watermark_image: Optional[UploadFile] = File(None),
):
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 15MB).")

    try:
        if watermark_type == "text":
            if not text or not text.strip():
                raise HTTPException(status_code=400, detail="Watermark text cannot be empty.")
            result_bytes = add_text_watermark(file_bytes, text=text, position=position, opacity=opacity)
        elif watermark_type == "image":
            if not watermark_image:
                raise HTTPException(status_code=400, detail="Watermark image file required.")
            watermark_bytes = await watermark_image.read()
            result_bytes = add_image_watermark(file_bytes, watermark_bytes, position=position, opacity=opacity)
        else:
            raise HTTPException(status_code=400, detail="watermark_type must be 'text' or 'image'.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not apply watermark: {str(e)}")

    return Response(content=result_bytes, media_type="image/png")
