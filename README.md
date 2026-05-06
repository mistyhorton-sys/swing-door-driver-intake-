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

## Deploy for off-network access (Azure App Service)
This project is prepped for Azure Linux Web App deployment.

### Prerequisites
- Azure subscription access
- Azure CLI installed and logged in: `az login`

### Option A: guided script (PowerShell)
Run:

```powershell
./azure-deploy.ps1 \
  -ResourceGroup rg-swing-door-intake \
  -Location eastus \
  -AppName swing-door-driver-intake-<unique> \
  -PlanName plan-swing-door-intake \
  -SmtpUser "<smtp-user>" \
  -SmtpPassword "<smtp-password>" \
  -MailFrom "<from-email>"
```

Then deploy your source (recommended from Azure Portal Deployment Center using this GitHub repo).

### Option B: Azure Portal only
1. Create **Web App** (Linux, Python 3.12)
2. In Configuration → General settings:
   - Startup Command: `bash startup.sh`
3. In Configuration → Application settings, add:
   - `SCM_DO_BUILD_DURING_DEPLOYMENT=true`
   - `ENABLE_ORYX_BUILD=true`
   - `SMTP_HOST=smtp.office365.com`
   - `SMTP_PORT=587`
   - `SMTP_USE_TLS=true`
   - `SMTP_USER=<secret>`
   - `SMTP_PASSWORD=<secret>`
   - `MAIL_FROM=<secret>`
   - `MAIL_TO=6077cro@walmart.com`
   - `PUBLIC_URL=https://<app-name>.azurewebsites.net`
4. Connect GitHub repo in Deployment Center and deploy.

### Verify
- Health: `https://<app-name>.azurewebsites.net/health`
- Form: `https://<app-name>.azurewebsites.net/`
- QR: `https://<app-name>.azurewebsites.net/qr`

Use the **Form URL** as your QR destination for drivers.
