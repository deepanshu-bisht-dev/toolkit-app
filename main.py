"""
ToolBox - Multipurpose utility toolkit.
QR generation/scanning, image compression/conversion/watermarking,
and PDF tools - all built with FastAPI.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers import qr, image, pdf

app = FastAPI(title="ToolBox")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(qr.router)
app.include_router(image.router)
app.include_router(pdf.router)

PAGES = [
    "index", "qr_generate", "qr_scan", "image_compress", "image_convert",
    "pdf_to_image", "image_to_pdf", "pdf_merge", "pdf_split", "watermark",
]


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/qr-generator")
async def qr_generator_page(request: Request):
    return templates.TemplateResponse(request, "qr_generate.html")


@app.get("/qr-scanner")
async def qr_scanner_page(request: Request):
    return templates.TemplateResponse(request, "qr_scan.html")


@app.get("/image-compress")
async def image_compress_page(request: Request):
    return templates.TemplateResponse(request, "image_compress.html")


@app.get("/image-convert")
async def image_convert_page(request: Request):
    return templates.TemplateResponse(request, "image_convert.html")


@app.get("/pdf-to-image")
async def pdf_to_image_page(request: Request):
    return templates.TemplateResponse(request, "pdf_to_image.html")


@app.get("/image-to-pdf")
async def image_to_pdf_page(request: Request):
    return templates.TemplateResponse(request, "image_to_pdf.html")


@app.get("/pdf-merge")
async def pdf_merge_page(request: Request):
    return templates.TemplateResponse(request, "pdf_merge.html")


@app.get("/pdf-split")
async def pdf_split_page(request: Request):
    return templates.TemplateResponse(request, "pdf_split.html")


@app.get("/watermark")
async def watermark_page(request: Request):
    return templates.TemplateResponse(request, "watermark.html")


@app.get("/health")
async def health():
    return {"status": "ok"}
