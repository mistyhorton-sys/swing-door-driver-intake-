# Swing Door Driver Intake

Mobile-friendly intake form for inbound drivers to submit three required safety photos:
1. Door photo
2. Disconnected trailer photo
3. Chocked wheels photo

Submissions are emailed to `6077cro@walmart.com`.

## Features
- Language selector (English, Spanish, French, Haitian Creole)
- Camera-first file inputs for mobile devices
- FastAPI backend with email attachments
- Built-in QR endpoint (`/qr`) to generate QR code for the form URL

## Run locally (Walmart-friendly)

```bash
uv venv
.venv\Scripts\activate
uv sync --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com
```

Set environment variables before running:

- `SMTP_HOST` (default: `smtp.office365.com`)
- `SMTP_PORT` (default: `587`)
- `SMTP_USER` (required)
- `SMTP_PASSWORD` (required)
- `SMTP_USE_TLS` (default: `true`)
- `MAIL_FROM` (default: `SMTP_USER`)
- `MAIL_TO` (default: `6077cro@walmart.com`)
- `PUBLIC_URL` (public URL used for QR code image)

Start app:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open: http://127.0.0.1:8000

## Production note
To support drivers off Walmart network, deploy this app to an internet-accessible host with HTTPS.
Use the deployed URL as `PUBLIC_URL`, then print/display the QR code from `/qr`.
