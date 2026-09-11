# -*- coding: utf-8 -*-
"""Gallery of 8 email-signature STYLES (with icons) using Chaitanya's real
details, so he can pick one. Assets embedded as base64."""
import os, base64
from PIL import Image, ImageDraw

HERE=os.path.dirname(os.path.abspath(__file__)); LOGOS=os.path.join(HERE,"logos")
ICONS=os.path.join(LOGOS,"icons")

NAME="Chaitanya Yelamasetty"; ROLE="Full Stack &amp; DevOps Engineer"
PHONE="+91-7993856293"; TEL="+917993856293"
EMAIL="chaitanya.yelamasetty@codesage.co.in"
LINKEDIN="https://www.linkedin.com/in/chaitanya-yelamasetty/"
PORTFOLIO="https://chaitanya.veltore.co.in/"
WEB="codesage.co.in"; WEBURL="https://codesage.co.in/"
A="#4f46e5"

def circ_photo(out=240):
    ss=3; O=out*ss
    src=Image.open(os.path.join(LOGOS,"photo_src.jpeg")).convert("RGB")
    w,h=src.size; side=int(min(w,h)*0.82); cx,cy=w//2,int(h*0.45)
    face=src.crop((cx-side//2,cy-side//2,cx+side//2,cy+side//2)).resize((O,O),Image.LANCZOS)
    rw=7*ss; pd=O-2*rw-2; face=face.resize((pd,pd),Image.LANCZOS)
    m=Image.new("L",(pd,pd),0); ImageDraw.Draw(m).ellipse((0,0,pd,pd),fill=255)
    cv=Image.new("RGBA",(O,O),(0,0,0,0)); cv.paste(face,(rw+1,rw+1),m)
    ImageDraw.Draw(cv).ellipse((rw//2,rw//2,O-rw//2,O-rw//2),outline=(79,70,229,255),width=rw)
    p=os.path.join(LOGOS,"_sample_photo.png"); cv.resize((out,out),Image.LANCZOS).save(p); return p

def b64(p):
    with open(p,"rb") as f: return "data:image/png;base64,"+base64.b64encode(f.read()).decode()

PHOTO=b64(circ_photo()); LOGO=b64(os.path.join(LOGOS,"codesage.png"))
IC={n:b64(os.path.join(ICONS,f"{n}_gray.png")) for n in ["phone","mail","linkedin","portfolio","web"]}

def ir(icon,inner,center=False):
    al="text-align:center;" if center else ""
    return (f'<div style="margin:3px 0;{al}"><img src="{IC[icon]}" width=14 height=14 '
            f'style="vertical-align:middle;">&nbsp;&nbsp;{inner}</div>')
def lk(href,text,bold=True):
    b="font-weight:bold;" if bold else ""
    return f'<a href="{href}" style="color:{A};text-decoration:none;{b}">{text}</a>'
def plain(href,text): return f'<a href="{href}" style="color:#333;text-decoration:none;">{text}</a>'

CONTACT = (ir("phone",plain('tel:'+TEL,PHONE))+ir("mail",plain('mailto:'+EMAIL,EMAIL))
          +ir("linkedin",lk(LINKEDIN,"LinkedIn"))+ir("portfolio",lk(PORTFOLIO,"Portfolio"))
          +ir("web",lk(WEBURL,WEB)))

def s_classic():
    return f"""<table cellpadding=0 cellspacing=0 style="font:13px Arial;color:#333;line-height:1.5;"><tr>
<td style="padding-right:16px;vertical-align:middle;"><img src="{PHOTO}" width=112 height=112 style="display:block"></td>
<td style="padding:0 16px;border-left:3px solid {A};vertical-align:middle;">
<div style="font-size:16px;font-weight:bold;color:#111;">{NAME}</div>
<div style="color:{A};font-weight:bold;margin:2px 0 8px;">{ROLE}</div>{CONTACT}
<div style="border-top:1px solid #e5e7eb;padding-top:8px;margin-top:6px;"><img src="{LOGO}" width=110 style="display:block"></div></td></tr></table>"""

def s_minimal():
    return f"""<table cellpadding=0 cellspacing=0 style="font:13px Arial;color:#333;line-height:1.6;"><tr>
<td style="padding-left:14px;border-left:4px solid {A};">
<div style="font-size:17px;font-weight:bold;color:#111;">{NAME}</div>
<div style="color:{A};font-weight:bold;margin:2px 0 6px;">{ROLE} &nbsp;|&nbsp; CodeSage</div>
<div>{PHONE} &nbsp;&#183;&nbsp; {EMAIL}</div>
<div>{lk(LINKEDIN,'LinkedIn')} &#183; {lk(PORTFOLIO,'Portfolio')} &#183; {lk(WEBURL,WEB)}</div></td></tr></table>"""

def s_logoleft():
    return f"""<table cellpadding=0 cellspacing=0 style="font:13px Arial;color:#333;line-height:1.5;"><tr>
<td style="padding-right:18px;border-right:2px solid #e5e7eb;vertical-align:middle;"><img src="{LOGO}" width=132 style="display:block"></td>
<td style="padding-left:18px;vertical-align:middle;">
<div style="font-size:16px;font-weight:bold;color:#111;">{NAME}</div>
<div style="color:{A};font-weight:bold;margin:2px 0 6px;">{ROLE}</div>{CONTACT}</td></tr></table>"""

def s_sidebar():
    return f"""<table cellpadding=0 cellspacing=0 style="font:13px Arial;color:#333;line-height:1.5;border-radius:10px;overflow:hidden;"><tr>
<td style="width:8px;background:{A};"></td>
<td style="background:#f7f7fb;padding:14px 18px;"><table cellpadding=0 cellspacing=0><tr>
<td style="padding-right:14px;vertical-align:middle;"><img src="{PHOTO}" width=96 height=96 style="display:block"></td>
<td style="vertical-align:middle;"><div style="font-size:16px;font-weight:bold;color:#111;">{NAME}</div>
<div style="color:{A};font-weight:bold;margin:2px 0 6px;">{ROLE}</div>{CONTACT}</td></tr></table></td></tr></table>"""

def s_centered():
    C=(ir("phone",plain('tel:'+TEL,PHONE),1)+ir("mail",plain('mailto:'+EMAIL,EMAIL),1)
       +ir("linkedin",lk(LINKEDIN,"LinkedIn"),1)+ir("portfolio",lk(PORTFOLIO,"Portfolio"),1)+ir("web",lk(WEBURL,WEB),1))
    return f"""<table cellpadding=0 cellspacing=0 style="font:13px Arial;color:#333;line-height:1.55;text-align:center;"><tr><td style="text-align:center;">
<img src="{PHOTO}" width=96 height=96 style="display:block;margin:0 auto 6px;">
<div style="font-size:16px;font-weight:bold;color:#111;">{NAME}</div>
<div style="color:{A};font-weight:bold;margin:2px 0 6px;">{ROLE}</div>{C}
<div style="margin-top:8px;"><img src="{LOGO}" width=100 style="display:inline-block;"></div></td></tr></table>"""

def s_icons():
    def chip(icon,href):
        return f'<a href="{href}"><img src="{IC[icon]}" width=22 height=22 style="vertical-align:middle;margin-right:8px;"></a>'
    return f"""<table cellpadding=0 cellspacing=0 style="font:13px Arial;color:#333;line-height:1.5;"><tr>
<td style="padding-right:16px;vertical-align:middle;"><img src="{PHOTO}" width=104 height=104 style="display:block"></td>
<td style="padding-left:16px;vertical-align:middle;">
<div style="font-size:16px;font-weight:bold;color:#111;">{NAME}</div>
<div style="color:{A};font-weight:bold;margin:2px 0 6px;">{ROLE} &#183; CodeSage</div>
<div style="margin-bottom:8px;">{PHONE} &nbsp;&#183;&nbsp; {EMAIL}</div>
<div>{chip('linkedin',LINKEDIN)}{chip('portfolio',PORTFOLIO)}{chip('web',WEBURL)}{chip('mail','mailto:'+EMAIL)}</div></td></tr></table>"""

def s_compact():
    return f"""<table cellpadding=0 cellspacing=0 style="font:13px Arial;color:#333;"><tr>
<td style="padding-right:12px;vertical-align:middle;"><img src="{PHOTO}" width=54 height=54 style="display:block"></td>
<td style="vertical-align:middle;line-height:1.45;">
<span style="font-weight:bold;color:#111;font-size:14px;">{NAME}</span> &nbsp;<span style="color:{A};font-weight:bold;">{ROLE}</span><br>
{PHONE} &#183; {EMAIL} &#183; {lk(LINKEDIN,'LinkedIn')}</td></tr></table>"""

def s_banner():
    return f"""<table cellpadding=0 cellspacing=0 style="font:13px Arial;color:#333;line-height:1.5;width:430px;">
<tr><td style="padding-bottom:10px;"><table cellpadding=0 cellspacing=0><tr>
<td style="padding-right:14px;vertical-align:middle;"><img src="{PHOTO}" width=96 height=96 style="display:block"></td>
<td style="vertical-align:middle;"><div style="font-size:16px;font-weight:bold;color:#111;">{NAME}</div>
<div style="color:{A};font-weight:bold;margin:2px 0 6px;">{ROLE}</div>{CONTACT}</td></tr></table></td></tr>
<tr><td style="background:{A};color:#fff;padding:8px 14px;border-radius:6px;font-style:italic;">Building reliable, human-centric software.</td></tr></table>"""

STYLES=[("1 · Classic (your current)","Photo left, icon rows, logo below.","Everyday use — safest all-rounder.",s_classic),
("2 · Minimalist (text only)","Clean accent bar, no images.","Formal / high-volume mail, or when images get blocked.",s_minimal),
("3 · Logo-left","Company logo leads, icon rows right.","When the brand matters more than your face.",s_logoleft),
("4 · Sidebar card","Soft grey card, colored side bar.","A modern, designed look that stands out.",s_sidebar),
("5 · Centered / stacked","Photo on top, centered rows.","Narrow layouts, mobile-first, personal touch.",s_centered),
("6 · Icon buttons","Photo + details + big tappable icons.","Social / networking-heavy roles.",s_icons),
("7 · Compact one-line","Tiny photo, single tidy block.","Replies & internal threads.",s_compact),
("8 · Banner + tagline","Icon rows + colored tagline strip.","Marketing / sales — adds a message.",s_banner)]

def main():
    cards="".join(f"""<div class="card"><div class="hd"><span class="num">{t}</span><span class="desc">{d}</span></div>
<div class="mail">{fn()}</div><div class="best"><b>Best for:</b> {b}</div></div>""" for t,d,b,fn in STYLES)
    html=f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Signature style samples</title>
<style>body{{background:#eef1f5;font-family:'Segoe UI',Arial;margin:0;padding:28px;color:#1f2937;}}
h1{{font-size:22px;margin:0 0 4px;}}p.sub{{color:#6b7280;margin:0 0 24px;font-size:14px;max-width:720px;}}
.card{{background:#fff;border-radius:14px;box-shadow:0 2px 10px rgba(0,0,0,.07);margin:0 0 22px;overflow:hidden;max-width:720px;}}
.hd{{padding:14px 20px;background:#f9fafb;border-bottom:1px solid #eef0f3;}}
.num{{font-weight:700;font-size:15px;color:#111;}}.desc{{color:#6b7280;font-size:13px;margin-left:10px;}}
.mail{{padding:26px 22px;background:#fff;}}.best{{padding:10px 20px;background:#fbfcfe;border-top:1px solid #eef0f3;font-size:12.5px;color:#4b5563;}}
</style></head><body>
<h1>Email signature styles &mdash; pick one</h1>
<p class="sub">8 layouts with your real details + icons (shown with CodeSage as the example; any style applies to all 3 mailboxes). Tell me the number and I'll apply it to Enable India, CodeSage &amp; Purple Aware in their brand colours (navy / red / purple).</p>
{cards}</body></html>"""
    out=os.path.join(HERE,"signature_samples.html"); open(out,"w",encoding="utf-8").write(html)
    print("wrote",out,"(",len(html)//1024,"KB )")

if __name__=="__main__": main()
