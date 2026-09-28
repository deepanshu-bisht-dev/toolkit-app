"""
QR code generation (with optional color + logo) and scanning.
Scanning uses OpenCV's built-in QRCodeDetector - no external zbar
library needed, which avoids native-dependency install issues.
"""

import io
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
import numpy as np
import cv2


def generate_qr(
    data: str,
    fill_color: str = "black",
    back_color: str = "white",
    box_size: int = 10,
    border: int = 4,
    logo_bytes: bytes | None = None,
) -> bytes:
    """
    Generates a QR code PNG. If logo_bytes is provided, embeds it in
    the center (uses high error-correction so the code stays scannable).
    """
    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECT_H if logo_bytes else qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    if logo_bytes:
        logo = Image.open(io.BytesIO(logo_bytes)).convert("RGBA")
        qr_width, qr_height = img.size

        # Logo should be roughly 1/4 the width of the QR code
        logo_size = qr_width // 4
        logo.thumbnail((logo_size, logo_size))

        # White backing behind the logo so it stays readable against the code
        pad = 8
        backing = Image.new("RGBA", (logo.width + pad, logo.height + pad), "white")
        backing.paste(logo, (pad // 2, pad // 2), logo)

        position = ((qr_width - backing.width) // 2, (qr_height - backing.height) // 2)
        img.paste(backing, position, backing)

    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()


def scan_qr(image_bytes: bytes) -> list[str]:
    """
    Decodes any QR codes found in the given image bytes.
    Returns a list of decoded strings (empty list if none found).
    """
    np_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Could not read the uploaded image.")

    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, _ = detector.detectAndDecodeMulti(image)

    if not retval:
        return []

    return [text for text in decoded_info if text]
