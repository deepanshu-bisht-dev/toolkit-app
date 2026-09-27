<div align="center">

# 🧰 ToolBox — Multipurpose File Utility Web App

### QR codes, image tools, and PDF tools — all in one place, no signup.

A free, self-hosted set of everyday file utilities — built with **FastAPI**,
each tool on its own dedicated page. No paid APIs, no heavy ML dependencies.

![Python](https://img.shields.io/badge/Python-3.10--3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-Image%20Processing-3776AB?style=for-the-badge)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-PDF%20Engine-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

---

## ⚡ Why this project?

Most portfolio projects are demos nobody actually opens twice. **ToolBox** is
built to be genuinely useful — the kind of thing you'd bookmark and use
yourself. Nine real tools, each with its own clean page, all running locally
with no file ever leaving your machine.

Built with **FastAPI** instead of Flask — async-ready, automatic interactive
API docs at `/docs`, and request validation baked in via Pydantic.

---

## 🖼️ Screenshots

> _Add your own screenshots here after running the app._

<div align="center">

<!-- ![Homepage](docs/screenshot-home.png) -->
<!-- ![QR Generator](docs/screenshot-qr.png) -->

**📸 Homepage — _add screenshot here_**

</div>

---

## ✨ Tools Included

| Tool | What it does |
|---|---|
| 🔗 **QR Generator** | Custom QR codes with your own colors and an embedded logo |
| 📷 **QR Scanner** | Upload an image, decode any QR code inside it |
| 🗜️ **Image Compressor** | Reduce file size, optionally resize dimensions |
| 🔄 **Image Converter** | Convert between PNG, JPG, WEBP, BMP |
| 📄 **PDF → Image** | Every page of a PDF rendered as a PNG, delivered as a ZIP |
| 🖼️ **Image → PDF** | Combine multiple images into one PDF |
| 📑 **PDF Merge** | Combine multiple PDFs into one |
| ✂️ **PDF Split** | Split a PDF into individual single-page files |
| 💧 **Watermark** | Add a text or image watermark, with position/opacity control |

---

## 🛠️ Tech Stack

| Layer          | Technology                          |
|----------------|----------------------------------------|
| Backend        | Python, FastAPI, Uvicorn             |
| Image Processing| Pillow, OpenCV (QR scanning only)   |
| PDF Engine     | PyMuPDF (no external Poppler binary needed), pypdf |
| QR             | `qrcode` (generation), OpenCV (scanning) |
| Frontend       | HTML, CSS, JavaScript (vanilla)      |

---

## 📂 Project Structure

```
toolkit-app/
├── main.py                    # FastAPI app - mounts routers, serves pages
├── routers/
│   ├── qr.py                   # QR generate/scan endpoints
│   ├── image.py                  # Compress/convert/watermark endpoints
│   └── pdf.py                     # PDF conversion/merge/split endpoints
├── services/
│   ├── qr_service.py             # QR generation + OpenCV-based scanning
│   ├── image_service.py            # Compression, resizing, format conversion
│   ├── watermark_service.py         # Text/image watermarking
│   └── pdf_service.py                # PDF<->image, merge, split
├── templates/                        # One HTML page per tool + shared base layout
├── static/css/style.css               # Shared styling
├── static/js/main.js                   # Shared generic form-handling logic
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/deepanshu-bisht-dev/toolbox-app.git
cd toolbox-app

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run it
uvicorn main:app --reload
```

Open **`http://localhost:8000`** — every tool is linked from the homepage.
Interactive API docs are auto-generated at **`http://localhost:8000/docs`**.

> If you're on a very new Python version and a dependency fails to install
> from source, use `py -3.12 -m venv venv` instead — see this repo's other
> projects for the full Python-version-mismatch troubleshooting steps.

---

## 🔍 How It Works

Each tool page posts a form (multipart file upload + options) to its own
API endpoint under `/api/...`. The backend processes the file entirely in
memory — nothing is written to disk — and streams the result straight back
as a downloadable file or image. No database, no persistent storage.

```
  Browser Form          FastAPI Router          Service Layer
──────────────►     ──────────────────►     ──────────────────►
 multipart upload      validates + routes       Pillow / PyMuPDF /
                                                  OpenCV / pypdf do
                                                  the actual work
```

---

## 📈 Roadmap

- [ ] Batch processing (zip upload → process every file → zip download)
- [ ] Drag-and-drop reordering for PDF merge / Image-to-PDF page order
- [ ] Dark mode

---

<div align="center">

Built by **[Deepanshu Bisht](https://github.com/deepanshu-bisht-dev)**
as part of the Python Developer Internship at Codec Technologies.

⭐ If this helped you, consider starring the repo!

</div>
