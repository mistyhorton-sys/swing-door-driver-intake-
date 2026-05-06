# M365 Setup (No credit card, no blocked phishing relay)

Use this pattern instead of third-party form relays:

1. **Microsoft Form** (public) for driver details
2. **OneDrive Request files** link for photo uploads
3. Optional: **Power Automate** email notifications to `6077cro@walmart.com`

## Step 1 — Create Microsoft Form
- Create a Form with fields:
  - Language
  - Door Number
  - Driver Name (optional)
  - Trailer Number (optional)
- Form setting: **Anyone can respond**
- Copy the public form URL

## Step 2 — Create OneDrive Request Files link
- Create folder: `SwingDoorDriverIntake`
- Click **Request files**
- Ask uploaders for naming convention:
  - `Door-<door number>-<timestamp>`
  - `TrailerDisconnect-<door number>-<timestamp>`
  - `ChockedWheels-<door number>-<timestamp>`
- Copy the request files URL

## Step 3 — Paste links into docs/index.html
Replace constants:
- `DATA_FORM_URL`
- `FILE_UPLOAD_URL`

Commit and push. GitHub Pages will update.

## Step 4 — Optional automation
Use Power Automate:
- Trigger A: `When a new response is submitted` (Microsoft Forms)
- Trigger B: `When a file is created` (OneDrive folder)
- Action: `Send an email (V2)` to `6077cro@walmart.com`
