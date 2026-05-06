import io
import os
from datetime import datetime
from email.message import EmailMessage
from typing import Annotated

import qrcode
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import smtplib

MAX_FILE_SIZE = 8 * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"}

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.office365.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
MAIL_FROM = os.getenv("MAIL_FROM", SMTP_USER)
MAIL_TO = os.getenv("MAIL_TO", "6077cro@walmart.com")
PUBLIC_URL = os.getenv("PUBLIC_URL", "http://127.0.0.1:8000")

app = FastAPI(title="Swing Door Driver Intake")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


def _validate_and_read(upload: UploadFile) -> bytes:
    if upload.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {upload.content_type}")

    data = upload.file.read()
    if len(data) == 0:
        raise HTTPException(status_code=400, detail=f"{upload.filename} is empty")

    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"{upload.filename} exceeds 8MB")

    return data


def _send_email(
    language: str,
    driver_name: str,
    trailer_number: str,
    door_number: str,
    submitted_at: str,
    attachments: list[tuple[str, str, bytes]],
) -> None:
    if not SMTP_USER or not SMTP_PASSWORD or not MAIL_FROM:
        raise HTTPException(
            status_code=500,
            detail="Email settings are not configured. Set SMTP_USER, SMTP_PASSWORD, and MAIL_FROM.",
        )

    msg = EmailMessage()
    msg["Subject"] = f"Door Safety Intake - Door {door_number} - {submitted_at}"
    msg["From"] = MAIL_FROM
    msg["To"] = MAIL_TO
    msg.set_content(
        "\n".join(
            [
                "A new inbound truck driver intake was submitted.",
                f"Submitted at (UTC): {submitted_at}",
                f"Language: {language}",
                f"Driver Name: {driver_name or 'Not provided'}",
                f"Trailer Number: {trailer_number or 'Not provided'}",
                f"Door Number: {door_number}",
            ]
        )
    )

    for label, content_type, data in attachments:
        ext = content_type.split("/")[-1].replace("jpeg", "jpg")
        file_name = f"{label}.{ext}"
        msg.add_attachment(data, maintype="image", subtype=ext, filename=file_name)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
        if SMTP_USE_TLS:
            smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html", {"request": request, "public_url": PUBLIC_URL})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/qr")
async def qr_code(url: str | None = None) -> Response:
    target = url or PUBLIC_URL
    qr = qrcode.QRCode(border=2, box_size=10)
    qr.add_data(target)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return Response(content=buffer.getvalue(), media_type="image/png")


@app.post("/submit")
async def submit(
    language: Annotated[str, Form(...)],
    door_number: Annotated[str, Form(...)],
    driver_name: Annotated[str, Form()] = "",
    trailer_number: Annotated[str, Form()] = "",
    door_photo: UploadFile = File(...),
    disconnected_trailer_photo: UploadFile = File(...),
    chocked_wheels_photo: UploadFile = File(...),
) -> JSONResponse:
    if not door_number.strip():
        raise HTTPException(status_code=400, detail="Door number is required")

    door_data = _validate_and_read(door_photo)
    trailer_data = _validate_and_read(disconnected_trailer_photo)
    chock_data = _validate_and_read(chocked_wheels_photo)

    submitted_at = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    _send_email(
        language=language.strip(),
        driver_name=driver_name.strip(),
        trailer_number=trailer_number.strip(),
        door_number=door_number.strip(),
        submitted_at=submitted_at,
        attachments=[
            ("door_photo", door_photo.content_type or "image/jpeg", door_data),
            (
                "disconnected_trailer_photo",
                disconnected_trailer_photo.content_type or "image/jpeg",
                trailer_data,
            ),
            ("chocked_wheels_photo", chocked_wheels_photo.content_type or "image/jpeg", chock_data),
        ],
    )

    return JSONResponse({"message": "Submission sent successfully"})
