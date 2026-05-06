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

## Deploy for off-network access (Render)
This project includes `render.yaml` and a `Dockerfile` so you can deploy quickly.

### 1) Push this repo to GitHub

```bash
git remote add origin <your-github-repo-url>
git push -u origin master
```

### 2) Create the Render web service
1. Sign in to Render
2. New + → Blueprint
3. Select your GitHub repo
4. Render will detect `render.yaml`

### 3) Set secret environment variables in Render
- `SMTP_USER`
- `SMTP_PASSWORD`
- `MAIL_FROM`

Already preconfigured in blueprint:
- `SMTP_HOST=smtp.office365.com`
- `SMTP_PORT=587`
- `SMTP_USE_TLS=true`
- `MAIL_TO=6077cro@walmart.com`

### 4) Set `PUBLIC_URL`
After deploy, set `PUBLIC_URL` to your Render app URL, for example:
`https://swing-door-driver-intake.onrender.com`

### 5) Verify
- Health: `https://<your-url>/health`
- Form: `https://<your-url>/`
- QR image: `https://<your-url>/qr`

Use the final `https://<your-url>/` in printed QR codes for drivers.
