# Outlook Email Signatures — Setup Guide

**Owner:** Chaitanya Yelamasetty
**Prepared:** 2026-09-10
**Purpose:** How the 3 branded email signatures (Enable India, CodeSage, Purple Aware) were built and installed into Outlook, so it can be repeated on any machine.

---

## 1. What was created

Three signatures, one per mailbox — each has: a circular photo with a purple ring, name, role (**Full Stack & DevOps Engineer**), purple contact lines with icons (phone, email, LinkedIn, Portfolio), and the company logo below (the logo is a clickable link to the company website).

| Signature | Email account | Logo links to |
|---|---|---|
| Enable India | chaitanya.csv@enableindia.org | enableindia.org |
| CodeSage | chaitanya.yelamasetty@codesage.co.in | codesage.co.in |
| Purple Aware | chaitanya@purpleaware.com | purpleaware.com |

**Shared details:** Phone +91-7993856293 · LinkedIn linkedin.com/in/chaitanya-yelamasetty · Portfolio chaitanya.veltore.co.in

---

## 2. Project files (source)

Located at: `D:\EI_Official\email-signatures\`

| File / folder | What it is |
|---|---|
| `build_final_signatures.py` | Main builder — makes the signatures and installs them into Outlook's folder |
| `generate_icons.py` | Draws the contact icons (phone, mail, LinkedIn, portfolio, web) in each colour |
| `build_samples.py` | Builds `signature_samples.html`, a gallery of 8 style options |
| `logos\` | Company logos + the photo (`photo_src.jpeg`) + `icons\` |
| `standalone\` | Self-contained `.html` copies of each final signature (open in a browser to preview) |
| `signature_samples.html` | The 8-style gallery for choosing a design |

---

## 3. Where Outlook stores signatures

```
%APPDATA%\Microsoft\Signatures\
= C:\Users\<you>\AppData\Roaming\Microsoft\Signatures\
```

Each signature = a `.htm` + `.txt` file plus a `<Name>_files\` folder holding its images.

---

## 4. Install steps

### Step A — Generate + copy the signature files into Outlook's folder
Run (needs Python with the Pillow library):
```bash
cd D:\EI_Official\email-signatures
python generate_icons.py          # only needed once (or if icons change)
python build_final_signatures.py  # builds + installs the 3 signatures
```
This writes `Enable India.htm`, `CodeSage.htm`, `Purple Aware.htm` (+ `.txt` + `_files\`) into `%APPDATA%\Microsoft\Signatures\`.

### Step B — Make Outlook use LOCAL signatures (not cloud/roaming)
Modern Outlook (Microsoft 365) defaults to **cloud signatures** and ignores the folder above. Force it to read local files by setting one registry value (PowerShell):
```powershell
New-ItemProperty -Path "HKCU:\Software\Microsoft\Office\16.0\Outlook\Setup" `
  -Name "DisableRoamingSignaturesTemporaryToggle" -Value 1 -PropertyType DWord -Force
```
> `16.0` = Office 2016/2019/2021/365. This is user-scope and reversible.

### Step C — Restart Outlook COMPLETELY
- Close all Outlook windows, **and**
- System tray (bottom-right, click the `^`) → right-click Outlook icon → **Close / Exit**.
- Reopen Outlook. *(The registry change only takes effect on a fresh start.)*

### Step D — Assign each signature as its account default (in Outlook, one-time)
`File → Options → Mail → Signatures…`
1. The three signatures now appear in the **"Select signature to edit"** list.
2. Under **"Choose default signature"**:
   - **E-mail account** = CodeSage account → **New messages** = `CodeSage`, **Replies/forwards** = `CodeSage`
   - Switch account to Enable India → set both to `Enable India`
   - Switch account to Purple Aware → set both to `Purple Aware`
3. Click **OK**.

Open a new email in each account — the correct signature appears automatically.

---

## 5. "New Outlook" app (different — no File menu)
The new Outlook does **not** read the local folder. Instead:
1. Open a `standalone\*.html` file in a browser → **Ctrl+A**, **Ctrl+C**.
2. Outlook: **Settings ⚙ → Accounts → Signatures → + New signature** → paste (**Ctrl+V**).
3. Set it as the default for that account. Repeat per mailbox.

---

## 6. Troubleshooting

| Problem | Fix |
|---|---|
| Signatures don't appear in the list | You skipped Step B, or didn't fully exit Outlook (check the system tray). Redo B + C. |
| A blue "…-signature.html" link appears in an email | You copied the *file* — instead open the `.html` in a **browser** and copy the rendered page. |
| "Convert File" popup | You dragged the `.html` into Outlook — don't; use the folder-install method (Steps A–D). |
| Photo looks blurry | Don't put the photo inside an animated GIF (colour limit blurs it). Use the static PNG build (this project already does). |
| Images blocked for the recipient | Normal — some mail servers hide images until the reader clicks "show images." The alt text still shows. |

---

## 7. How to UNDO everything
```powershell
# revert Outlook to cloud signatures
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Office\16.0\Outlook\Setup" -Name "DisableRoamingSignaturesTemporaryToggle" -Value 0
```
Then delete `Enable India*`, `CodeSage*`, `Purple Aware*` from `%APPDATA%\Microsoft\Signatures\`.

---

## 8. Notes
- Signatures animate/render everywhere; in **classic Outlook desktop** they show as a clean static image (no motion needed — the design is static by choice for sharpness + accessibility).
- Logos keep their brand colour; the accent (ring, role, contact text, icons) is purple across all three.
- To change anything (title, colours, add an address line): edit `build_final_signatures.py` and re-run it, then restart Outlook.
