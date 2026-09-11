# -*- coding: utf-8 -*-
"""Generate 3 Outlook HTML email signatures and install them into the
Windows Outlook Signatures folder. Re-runnable."""
import os, shutil, base64

HERE = os.path.dirname(os.path.abspath(__file__))
LOGOS = os.path.join(HERE, "logos")
SIG_DIR = os.path.join(os.environ["APPDATA"], "Microsoft", "Signatures")

# ---- shared details ----
NAME = "Chaitanya Yelamasetty"
ROLE = "Full Stack Developer"
PHONE = "+91-7993856293"
PHONE_TEL = "+917993856293"
LINKEDIN = "https://www.linkedin.com/in/chaitanya-yelamasetty/"
PORTFOLIO = "https://chaitanya.veltore.co.in/"

COMPANIES = {
    "Enable India": {
        "logo": "enableindia.png", "logo_w": 150,
        "accent": "#1f2b4d",
        "email": "chaitanya.csv@enableindia.org",
        "website": "enableindia.org", "website_url": "https://www.enableindia.org/",
    },
    "CodeSage": {
        "logo": "codesage.png", "logo_w": 124,
        "accent": "#e11d2a",
        "email": "chaitanya.yelamasetty@codesage.co.in",
        "website": "codesage.co.in", "website_url": "https://codesage.co.in/",
    },
    "Purple Aware": {
        "logo": "purpleaware.png", "logo_w": 200,
        "accent": "#7c3aed",
        "email": "chaitanya@purpleaware.com",
        "website": "purpleaware.com", "website_url": "https://purpleaware.com/",
    },
}

def sig_html(company, c, img_ref):
    a = c["accent"]
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head>
<body>
<table cellpadding="0" cellspacing="0" border="0" style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#333333;line-height:1.5;">
 <tr>
  <td style="padding:2px 18px 2px 0;border-right:3px solid {a};vertical-align:middle;">
   <img src="{img_ref}" alt="{company}" width="{c['logo_w']}" style="display:block;border:0;">
  </td>
  <td style="padding-left:18px;vertical-align:middle;">
   <div style="font-size:16px;font-weight:bold;color:#111111;">{NAME}</div>
   <div style="color:{a};font-weight:bold;margin:2px 0 8px 0;">{ROLE}</div>
   <div style="margin:1px 0;"><span style="color:{a};font-weight:bold;">T</span>&nbsp;&nbsp;<a href="tel:{PHONE_TEL}" style="color:#333333;text-decoration:none;">{PHONE}</a></div>
   <div style="margin:1px 0;"><span style="color:{a};font-weight:bold;">E</span>&nbsp;&nbsp;<a href="mailto:{c['email']}" style="color:#333333;text-decoration:none;">{c['email']}</a></div>
   <div style="margin:1px 0;"><a href="{LINKEDIN}" style="color:{a};text-decoration:none;font-weight:bold;">LinkedIn</a>&nbsp;&nbsp;&#183;&nbsp;&nbsp;<a href="{PORTFOLIO}" style="color:{a};text-decoration:none;font-weight:bold;">Portfolio</a>&nbsp;&nbsp;&#183;&nbsp;&nbsp;<a href="{c['website_url']}" style="color:{a};text-decoration:none;font-weight:bold;">{c['website']}</a></div>
  </td>
 </tr>
</table>
</body></html>"""

def sig_txt(company, c):
    return (f"{NAME}\n{ROLE} | {company}\n"
            f"T: {PHONE}\nE: {c['email']}\n"
            f"LinkedIn: {LINKEDIN}\nPortfolio: {PORTFOLIO}\nWeb: {c['website_url']}\n")

def main():
    os.makedirs(SIG_DIR, exist_ok=True)
    preview_blocks = []
    for company, c in COMPANIES.items():
        files_dir = os.path.join(SIG_DIR, company + "_files")
        os.makedirs(files_dir, exist_ok=True)
        # copy logo into the _files folder
        src_logo = os.path.join(LOGOS, c["logo"])
        dst_logo = os.path.join(files_dir, "logo.png")
        shutil.copyfile(src_logo, dst_logo)
        img_ref = f"{company}_files/logo.png"
        # write .htm (Outlook) and .txt
        with open(os.path.join(SIG_DIR, company + ".htm"), "w", encoding="utf-8") as f:
            f.write(sig_html(company, c, img_ref))
        with open(os.path.join(SIG_DIR, company + ".txt"), "w", encoding="utf-8") as f:
            f.write(sig_txt(company, c))
        # preview block with base64 image so preview.html is self-contained
        with open(src_logo, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode()
        preview_blocks.append(sig_html(company, c, f"data:image/png;base64,{b64}"))
        print("installed:", company)

    # build a self-contained preview
    body = "".join(f'<div style="background:#fff;padding:24px;margin:18px 0;'
                   f'box-shadow:0 1px 4px rgba(0,0,0,.1);border-radius:10px;max-width:640px;">'
                   f'<div style="font:700 11px Arial;color:#9ca3af;letter-spacing:.08em;'
                   f'margin-bottom:14px;">SIGNATURE {i+1}</div>{b}</div>'
                   for i, b in enumerate(preview_blocks))
    with open(os.path.join(HERE, "preview.html"), "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8">'
                f'<title>Signatures preview</title></head>'
                f'<body style="background:#f3f4f6;padding:28px;font-family:Arial;">'
                f'<h1 style="font-size:20px;">Final signatures preview</h1>{body}</body></html>')
    print("\nSignatures folder:", SIG_DIR)
    print("preview:", os.path.join(HERE, "preview.html"))

if __name__ == "__main__":
    main()
