from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from typing import Optional

from services.qr_service import generate_qr, scan_qr

router = APIRouter(prefix="/api/qr", tags=["qr"])


@router.post("/generate")
async def qr_generate(
    data: str = Form(...),
    fill_color: str = Form("black"),
    back_color: str = Form("white"),
    box_size: int = Form(10),
    logo: Optional[UploadFile] = File(None),
):
    if not data.strip():
        raise HTTPException(status_code=400, detail="Data cannot be empty.")

    logo_bytes = await logo.read() if logo else None

    try:
        image_bytes = generate_qr(
            data=data,
            fill_color=fill_color,
            back_color=back_color,
            box_size=box_size,
            logo_bytes=logo_bytes,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not generate QR code: {str(e)}")

    return Response(content=image_bytes, media_type="image/png")


@router.post("/scan")
async def qr_scan(file: UploadFile = File(...)):
    image_bytes = await file.read()

    try:
        results = scan_qr(image_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not results:
        return {"found": False, "results": []}

    return {"found": True, "results": results}
