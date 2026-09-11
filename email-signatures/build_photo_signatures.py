# -*- coding: utf-8 -*-
"""Build circular photo + animated accent-ring GIFs (per brand colour),
rebuild the 3 signatures with a photo layout, install to Outlook, and emit
self-contained standalone files."""
import os, shutil, base64, math
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
LOGOS = os.path.join(HERE, "logos")
STANDALONE = os.path.join(HERE, "standalone")
SIG_DIR = os.path.join(os.environ["APPDATA"], "Microsoft", "Signatures")

NAME = "Chaitanya Yelamasetty"
ROLE = "Full Stack Developer"
PHONE = "+91-7993856293"; PHONE_TEL = "+917993856293"
LINKEDIN = "https://www.linkedin.com/in/chaitanya-yelamasetty/"
PORTFOLIO = "https://chaitanya.veltore.co.in/"

COMPANIES = {
    "Enable India": dict(logo="enableindia.png", logo_w=118, accent=(31,43,77),
                         email="chaitanya.csv@enableindia.org",
                         website="enableindia.org", website_url="https://www.enableindia.org/"),
    "CodeSage":     dict(logo="codesage.png", logo_w=112, accent=(225,29,42),
                         email="chaitanya.yelamasetty@codesage.co.in",
                         website="codesage.co.in", website_url="https://codesage.co.in/"),
    "Purple Aware": dict(logo="purpleaware.png", logo_w=172, accent=(124,58,237),
                         email="chaitanya@purpleaware.com",
                         website="purpleaware.com", website_url="https://purpleaware.com/"),
}

def circular_photo(size=100, ss=3):
    """Return an RGBA circular headshot at `size` px."""
    src = Image.open(os.path.join(LOGOS, "photo_src.jpeg")).convert("RGB")
    w, h = src.size
    # crop a square focused slightly above centre (on the face)
    side = int(min(w, h) * 0.86)
    cx, cy = w // 2, int(h * 0.46)
    box = (cx - side//2, cy - side//2, cx + side//2, cy + side//2)
    face = src.crop(box).resize((size*ss, size*ss), Image.LANCZOS)
    mask = Image.new("L", (size*ss, size*ss), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size*ss, size*ss), fill=255)
    out = Image.new("RGBA", (size*ss, size*ss), (0,0,0,0))
    out.paste(face, (0,0), mask)
    return out.resize((size, size), Image.LANCZOS)

def make_ring_gif(accent, path, D=120, frames=16, ss=3):
    photo_d = 100
    ring_w = 6
    pd = photo_d * ss; Dd = D * ss; ctr = Dd//2; off = (Dd - pd)//2
    photo = circular_photo(photo_d, ss=1).resize((pd, pd), Image.LANCZOS)
    light = tuple(int(a + (255-a)*0.55) for a in accent)   # highlight tint
    base  = tuple(int(a + (255-a)*0.15) for a in accent)   # base ring tint
    bbox = (ring_w*ss//2, ring_w*ss//2, Dd-ring_w*ss//2, Dd-ring_w*ss//2)
    imgs = []
    for i in range(frames):
        theta = (i/frames)*360
        cv = Image.new("RGB", (Dd, Dd), (255,255,255))
        d = ImageDraw.Draw(cv)
        d.arc(bbox, 0, 360, fill=base, width=ring_w*ss)
        d.arc(bbox, theta, theta+95, fill=light, width=ring_w*ss)   # sweeping highlight
        cv.paste(photo, (off, off), photo)
        imgs.append(cv.resize((D, D), Image.LANCZOS).convert("P", palette=Image.ADAPTIVE, colors=64))
    imgs[0].save(path, save_all=True, append_images=imgs[1:], duration=90, loop=0, optimize=True, disposal=2)
    return os.path.getsize(path)

def sig_html(company, c, photo_ref, logo_ref):
    r,g,b = c["accent"]; a = f"#{r:02x}{g:02x}{b:02x}"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<table cellpadding="0" cellspacing="0" border="0" style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#333;line-height:1.5;">
 <tr>
  <td style="padding-right:16px;vertical-align:middle;"><img src="{photo_ref}" width="120" height="120" alt="{NAME}" style="display:block;border:0;border-radius:60px;"></td>
  <td style="padding:0 18px;border-left:3px solid {a};vertical-align:middle;">
   <div style="font-size:16px;font-weight:bold;color:#111;">{NAME}</div>
   <div style="color:{a};font-weight:bold;margin:2px 0 8px 0;">{ROLE}</div>
   <div style="margin:1px 0;"><span style="color:{a};font-weight:bold;">T</span>&nbsp;&nbsp;<a href="tel:{PHONE_TEL}" style="color:#333;text-decoration:none;">{PHONE}</a></div>
   <div style="margin:1px 0;"><span style="color:{a};font-weight:bold;">E</span>&nbsp;&nbsp;<a href="mailto:{c['email']}" style="color:#333;text-decoration:none;">{c['email']}</a></div>
   <div style="margin:5px 0 0 0;"><a href="{LINKEDIN}" style="color:{a};text-decoration:none;font-weight:bold;">LinkedIn</a>&nbsp;&#183;&nbsp;<a href="{PORTFOLIO}" style="color:{a};text-decoration:none;font-weight:bold;">Portfolio</a>&nbsp;&#183;&nbsp;<a href="{c['website_url']}" style="color:{a};text-decoration:none;font-weight:bold;">{c['website']}</a></div>
  </td>
  <td style="padding-left:18px;vertical-align:middle;"><img src="{logo_ref}" width="{c['logo_w']}" alt="{company}" style="display:block;border:0;"></td>
 </tr>
</table></body></html>"""

def b64(path):
    with open(path, "rb") as f: return base64.b64encode(f.read()).decode()

def main():
    os.makedirs(SIG_DIR, exist_ok=True); os.makedirs(STANDALONE, exist_ok=True)
    fmap = {"Enable India":"Enable-India","CodeSage":"CodeSage","Purple Aware":"Purple-Aware"}
    for company, c in COMPANIES.items():
        gif = os.path.join(LOGOS, f"ring_{fmap[company]}.gif")
        sz = make_ring_gif(c["accent"], gif)
        # install version (relative refs in _files)
        fdir = os.path.join(SIG_DIR, company + "_files"); os.makedirs(fdir, exist_ok=True)
        shutil.copyfile(gif, os.path.join(fdir, "photo.gif"))
        shutil.copyfile(os.path.join(LOGOS, c["logo"]), os.path.join(fdir, "logo.png"))
        with open(os.path.join(SIG_DIR, company + ".htm"), "w", encoding="utf-8") as f:
            f.write(sig_html(company, c, f"{company}_files/photo.gif", f"{company}_files/logo.png"))
        with open(os.path.join(SIG_DIR, company + ".txt"), "w", encoding="utf-8") as f:
            f.write(f"{NAME}\n{ROLE} | {company}\nT: {PHONE}\nE: {c['email']}\nLinkedIn: {LINKEDIN}\nPortfolio: {PORTFOLIO}\nWeb: {c['website_url']}\n")
        # standalone self-contained
        html = sig_html(company, c, f"data:image/gif;base64,{b64(gif)}",
                        f"data:image/png;base64,{b64(os.path.join(LOGOS,c['logo']))}")
        with open(os.path.join(STANDALONE, f"{fmap[company]}-signature.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"{company}: ring gif {sz//1024} KB -> installed + standalone")
    print("\nSignatures:", SIG_DIR)

if __name__ == "__main__":
    main()
