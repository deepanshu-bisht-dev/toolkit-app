"""
PDF <-> Image conversion and PDF merge/split.

Uses PyMuPDF (fitz) for PDF<->image rendering instead of pdf2image,
because pdf2image needs the external "poppler" binary installed
separately on the system - PyMuPDF is pure pip-install, no extra
system dependency, which avoids the install headaches we've hit
with other native libraries before.
"""

import io
import zipfile
import pymupdf as fitz  # PyMuPDF's new import name (fitz is deprecated)
from PIL import Image
from pypdf import PdfReader, PdfWriter


def pdf_to_images(pdf_bytes: bytes, dpi: int = 150) -> bytes:
    """
    Renders every page of a PDF as a PNG image and returns them
    bundled in a ZIP file.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    zoom = dpi / 72  # PDF default is 72 DPI
    matrix = fitz.Matrix(zoom, zoom)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for page_num, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=matrix)
            zf.writestr(f"page_{page_num}.png", pix.tobytes("png"))

    doc.close()
    return zip_buffer.getvalue()


def images_to_pdf(image_bytes_list: list[bytes]) -> bytes:
    """
    Combines multiple images into a single multi-page PDF, in the
    order they were provided.
    """
    if not image_bytes_list:
        raise ValueError("No images provided.")

    images = []
    for img_bytes in image_bytes_list:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        images.append(img)

    output = io.BytesIO()
    first_image, remaining_images = images[0], images[1:]
    first_image.save(output, format="PDF", save_all=True, append_images=remaining_images)
    return output.getvalue()


def merge_pdfs(pdf_bytes_list: list[bytes]) -> bytes:
    """
    Merges multiple PDFs into one, in the order provided.
    """
    writer = PdfWriter()

    for pdf_bytes in pdf_bytes_list:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


def split_pdf(pdf_bytes: bytes) -> bytes:
    """
    Splits a PDF into individual single-page PDFs, bundled in a ZIP file.
    """
    reader = PdfReader(io.BytesIO(pdf_bytes))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, page in enumerate(reader.pages, start=1):
            writer = PdfWriter()
            writer.add_page(page)

            page_buffer = io.BytesIO()
            writer.write(page_buffer)
            zf.writestr(f"page_{i}.pdf", page_buffer.getvalue())

    return zip_buffer.getvalue()
