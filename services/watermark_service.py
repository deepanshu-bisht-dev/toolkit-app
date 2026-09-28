"""
Adds text or image watermarks to an image, with configurable
position and opacity.
"""

import io
from PIL import Image, ImageDraw, ImageFont

POSITIONS = {
    "top-left": lambda w, h, ww, wh: (20, 20),
    "top-right": lambda w, h, ww, wh: (w - ww - 20, 20),
    "bottom-left": lambda w, h, ww, wh: (20, h - wh - 20),
    "bottom-right": lambda w, h, ww, wh: (w - ww - 20, h - wh - 20),
    "center": lambda w, h, ww, wh: ((w - ww) // 2, (h - wh) // 2),
}


def add_text_watermark(
    image_bytes: bytes,
    text: str,
    position: str = "bottom-right",
    opacity: int = 128,
    font_size: int = 36,
) -> bytes:
    base = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    pos_fn = POSITIONS.get(position, POSITIONS["bottom-right"])
    x, y = pos_fn(base.width, base.height, text_width, text_height)

    draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))

    watermarked = Image.alpha_composite(base, overlay).convert("RGB")
    output = io.BytesIO()
    watermarked.save(output, format="PNG")
    return output.getvalue()


def add_image_watermark(
    image_bytes: bytes,
    watermark_bytes: bytes,
    position: str = "bottom-right",
    opacity: int = 128,
    scale: float = 0.2,
) -> bytes:
    base = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    watermark = Image.open(io.BytesIO(watermark_bytes)).convert("RGBA")

    # Scale watermark relative to base image width
    target_width = int(base.width * scale)
    ratio = target_width / watermark.width
    watermark = watermark.resize((target_width, int(watermark.height * ratio)))

    # Apply opacity to the watermark's alpha channel
    alpha = watermark.split()[3].point(lambda p: int(p * (opacity / 255)))
    watermark.putalpha(alpha)

    pos_fn = POSITIONS.get(position, POSITIONS["bottom-right"])
    x, y = pos_fn(base.width, base.height, watermark.width, watermark.height)

    base.paste(watermark, (x, y), watermark)
    result = base.convert("RGB")
    output = io.BytesIO()
    result.save(output, format="PNG")
    return output.getvalue()
