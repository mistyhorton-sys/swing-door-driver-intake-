# M365 Setup — Option 1 (Upload-only for drivers)

This approach avoids anonymous Forms requirements and avoids blocked third-party relays.

## Flow
1. Driver scans QR and opens GitHub Pages landing page.
2. Driver taps **Open Photo Upload** and uploads 3 photos via OneDrive Request Files.
3. Driver shows generated Intake ID to Walmart associate.
4. Associate records door/trailer/language internally (Microsoft Form or SharePoint list).

## Step 1 — Create OneDrive Request Files link
1. In OneDrive or SharePoint, create folder: `SwingDoorDriverIntake`.
2. Click **Request files** on that folder.
3. Title it: `6077 Inbound Driver Safety Photos`.
4. Copy the Request Files link.

## Step 2 — Add upload link to public page
In `docs/index.html`, replace:

```js
const FILE_UPLOAD_URL = "REPLACE_WITH_ONEDRIVE_REQUEST_FILES_LINK";
```

Then commit and push.

## Step 3 — Internal associate metadata form
Create an internal-only Microsoft Form (or SharePoint list) with fields:
- Intake ID
- Door Number
- Trailer Number (optional)
- Driver Name (optional)
- Language
- Timestamp
- Associate name

## Step 4 — (Optional) Power Automate email to 6077cro@walmart.com
Automations:
- Trigger A: `When a file is created` in intake folder
- Trigger B: `When a form response is submitted` in internal form
- Action: send summary email to `6077cro@walmart.com`

## Recommended naming guidance for associates/drivers
Ask associates to tell drivers to include Intake ID in upload name if prompted, e.g.:
- `6077-20260506-1430-321-door.jpg`
- `6077-20260506-1430-321-trailer.jpg`
- `6077-20260506-1430-321-chocks.jpg`
