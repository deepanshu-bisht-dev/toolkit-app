from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from typing import List

from services.pdf_service import pdf_to_images, images_to_pdf, merge_pdfs, split_pdf

router = APIRouter(prefix="/api/pdf", tags=["pdf"])

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB


@router.post("/to-images")
async def pdf_to_images_route(file: UploadFile = File(...)):
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 25MB).")

    try:
        zip_bytes = pdf_to_images(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not convert PDF: {str(e)}")

    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=pdf_pages.zip"},
    )


@router.post("/from-images")
async def images_to_pdf_route(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="At least one image is required.")

    image_bytes_list = []
    for f in files:
        content = await f.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"{f.filename} is too large (max 25MB).")
        image_bytes_list.append(content)

    try:
        pdf_bytes = images_to_pdf(image_bytes_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not create PDF: {str(e)}")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=combined.pdf"},
    )


@router.post("/merge")
async def merge_pdfs_route(files: List[UploadFile] = File(...)):
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="At least two PDFs are required to merge.")

    pdf_bytes_list = []
    for f in files:
        content = await f.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"{f.filename} is too large (max 25MB).")
        pdf_bytes_list.append(content)

    try:
        merged_bytes = merge_pdfs(pdf_bytes_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not merge PDFs: {str(e)}")

    return Response(
        content=merged_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=merged.pdf"},
    )


@router.post("/split")
async def split_pdf_route(file: UploadFile = File(...)):
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 25MB).")

    try:
        zip_bytes = split_pdf(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not split PDF: {str(e)}")

    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=split_pages.zip"},
    )
