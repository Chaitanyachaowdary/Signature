# -*- coding: utf-8 -*-
"""Final signatures: CRISP static circular photo (2x, full colour) + solid brand
ring + updated logos. All static (sharp everywhere, incl. desktop Outlook)."""
import os, shutil, base64
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
LOGOS = os.path.join(HERE, "logos")
STANDALONE = os.path.join(HERE, "standalone")
SIG_DIR = os.path.join(os.environ["APPDATA"], "Microsoft", "Signatures")

NAME="Chaitanya Yelamasetty"; ROLE="Full Stack &amp; DevOps Engineer"
PHONE="+91-7993856293"; PHONE_TEL="+917993856293"
LINKEDIN="https://www.linkedin.com/in/chaitanya-yelamasetty/"
PORTFOLIO="https://chaitanya.veltore.co.in/"

COMPANIES = {
    "Enable India": dict(logo="enableindia.png", logo_w=118, accent=(124,58,237), ickey="purple",
                         email="chaitanya.csv@enableindia.org",
                         website="enableindia.org", website_url="https://www.enableindia.org/"),
    "CodeSage":     dict(logo="codesage.png", logo_w=112, accent=(124,58,237), ickey="purple",
                         email="chaitanya.yelamasetty@codesage.co.in",
                         website="codesage.co.in", website_url="https://codesage.co.in/"),
    "Purple Aware": dict(logo="purpleaware.png", logo_w=172, accent=(124,58,237), ickey="purple",
                         email="chaitanya@purpleaware.com",
                         website="purpleaware.com", website_url="https://purpleaware.com/"),
}
FMAP = {"Enable India":"Enable-India","CodeSage":"CodeSage","Purple Aware":"Purple-Aware"}
ICON_NAMES = ["phone","mail","linkedin","portfolio","web"]

def make_photo_png(accent, out_path, disp=120):
    """Crisp circular headshot rendered at 2x with a solid accent ring."""
    OUT = disp*2          # retina: 240px file shown at 120
    ss = 3; O = OUT*ss
    src = Image.open(os.path.join(LOGOS,"photo_src.jpeg")).convert("RGB")
    w,h = src.size
    side = int(min(w,h)*0.82); cx,cy = w//2, int(h*0.45)
    face = src.crop((cx-side//2, cy-side//2, cx+side//2, cy+side//2)).resize((O,O), Image.LANCZOS)
    ring_w = 7*ss
    pd = O - 2*ring_w - 2                      # inner photo diameter
    face = face.resize((pd,pd), Image.LANCZOS)
    mask = Image.new("L",(pd,pd),0); ImageDraw.Draw(mask).ellipse((0,0,pd,pd),fill=255)
    canvas = Image.new("RGBA",(O,O),(0,0,0,0))
    canvas.paste(face,(ring_w+1,ring_w+1),mask)
    d = ImageDraw.Draw(canvas)
    d.ellipse((ring_w//2, ring_w//2, O-ring_w//2, O-ring_w//2), outline=accent+(255,), width=ring_w)
    canvas.resize((OUT,OUT), Image.LANCZOS).save(out_path)

def sig_html(company, c, photo_ref, logo_ref, ic):
    r,g,b = c["accent"]; a=f"#{r:02x}{g:02x}{b:02x}"
    def ico(name):
        return (f'<img src="{ic[name]}" width="15" height="15" '
                f'style="vertical-align:middle;border:0;display:inline-block;">')
    L=f'color:{a};text-decoration:none;'
    B=f'color:{a};text-decoration:none;font-weight:bold;'
    ph=f'<a href="tel:{PHONE_TEL}" style="{L}">{PHONE}</a>'
    em=f'<a href="mailto:{c["email"]}" style="{L}">{c["email"]}</a>'
    li=f'<a href="{LINKEDIN}" style="{B}">LinkedIn</a>'
    pf=f'<a href="{PORTFOLIO}" style="{B}">Portfolio</a>'
    rows = (f'<div style="margin:3px 0;">{ico("phone")}&nbsp;&nbsp;{ph}</div>'
            f'<div style="margin:3px 0;">{ico("mail")}&nbsp;&nbsp;{em}</div>'
            f'<div style="margin:3px 0;">{ico("linkedin")}&nbsp;&nbsp;{li}'
            f'&nbsp;&nbsp;&nbsp;&nbsp;{ico("portfolio")}&nbsp;&nbsp;{pf}</div>')
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<table cellpadding="0" cellspacing="0" border="0" style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#333;line-height:1.5;">
 <tr>
  <td width="120" style="padding:0;vertical-align:middle;"><img src="{photo_ref}" width="120" height="120" alt="{NAME}" style="display:block;border:0;"></td>
  <td style="padding:0 16px 0 16px;vertical-align:middle;">
   <div style="font-size:16px;font-weight:bold;color:#111;">{NAME}</div>
   <div style="color:{a};font-weight:bold;margin:3px 0 8px 0;">{ROLE}</div>
   {rows}
   <div style="margin-top:11px;"><a href="{c['website_url']}" style="text-decoration:none;border:0;" title="{c['website']}"><img src="{logo_ref}" width="{c['logo_w']}" alt="{company} &#8212; {c['website']}" style="display:block;border:0;"></a></div>
  </td>
 </tr>
</table></body></html>"""

def b64(p):
    with open(p,"rb") as f: return base64.b64encode(f.read()).decode()

def main():
    os.makedirs(SIG_DIR,exist_ok=True); os.makedirs(STANDALONE,exist_ok=True)
    ICONDIR = os.path.join(LOGOS,"icons")
    for company,c in COMPANIES.items():
        photo = os.path.join(LOGOS, f"photo_{FMAP[company]}.png")
        make_photo_png(c["accent"], photo)
        fdir = os.path.join(SIG_DIR, company+"_files"); os.makedirs(fdir,exist_ok=True)
        old = os.path.join(fdir,"photo.gif")
        if os.path.exists(old): os.remove(old)
        shutil.copyfile(photo, os.path.join(fdir,"photo.png"))
        shutil.copyfile(os.path.join(LOGOS,c["logo"]), os.path.join(fdir,"logo.png"))
        # copy this brand's icon set + build ref dicts
        ic_rel={}; ic_b64={}
        for n in ICON_NAMES:
            src=os.path.join(ICONDIR,f"{n}_{c['ickey']}.png")
            shutil.copyfile(src, os.path.join(fdir,f"ic_{n}.png"))
            ic_rel[n]=f"{company}_files/ic_{n}.png"
            ic_b64[n]=f"data:image/png;base64,{b64(src)}"
        with open(os.path.join(SIG_DIR,company+".htm"),"w",encoding="utf-8") as f:
            f.write(sig_html(company,c,f"{company}_files/photo.png",f"{company}_files/logo.png",ic_rel))
        with open(os.path.join(SIG_DIR,company+".txt"),"w",encoding="utf-8") as f:
            f.write(f"{NAME}\n{ROLE} | {company}\nT: {PHONE}\nE: {c['email']}\nLinkedIn: {LINKEDIN}\nPortfolio: {PORTFOLIO}\nWeb: {c['website_url']}\n")
        html = sig_html(company,c,f"data:image/png;base64,{b64(photo)}",
                        f"data:image/png;base64,{b64(os.path.join(LOGOS,c['logo']))}", ic_b64)
        with open(os.path.join(STANDALONE,f"{FMAP[company]}-signature.html"),"w",encoding="utf-8") as f:
            f.write(html)
        print(f"{company}: crisp photo + icons + logo -> installed")
    print("Signatures:", SIG_DIR)

if __name__=="__main__":
    main()
