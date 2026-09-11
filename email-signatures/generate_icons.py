# -*- coding: utf-8 -*-
"""Draw clean monochrome contact icons (phone, mail, linkedin, portfolio, web)
in each brand accent colour. Output small PNGs used in the signatures."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE=os.path.dirname(os.path.abspath(__file__)); LOGOS=os.path.join(HERE,"logos")
ICONS=os.path.join(LOGOS,"icons"); os.makedirs(ICONS,exist_ok=True)
FONT_BOLD=r"C:\Windows\Fonts\arialbd.ttf"

ACCENTS={"navy":(31,43,77),"red":(225,29,42),"purple":(124,58,237),"gray":(80,80,90)}

def newcanvas(O): return Image.new("RGBA",(O,O),(0,0,0,0))

def ic_phone(O,col):
    im=newcanvas(O); d=ImageDraw.Draw(im); t=max(2,int(O*0.07))
    w=O*0.44; h=O*0.80; x0=(O-w)/2; y0=(O-h)/2
    d.rounded_rectangle([x0,y0,x0+w,y0+h],radius=O*0.13,outline=col+(255,),width=t)
    d.line([x0+w*0.34,y0+h*0.08,x0+w*0.66,y0+h*0.08],fill=col+(255,),width=t)   # speaker
    d.ellipse([O/2-O*0.045,y0+h-O*0.15,O/2+O*0.045,y0+h-O*0.06],fill=col+(255,)) # home btn
    return im

def ic_mail(O,col):
    im=newcanvas(O); d=ImageDraw.Draw(im); t=max(2,int(O*0.07))
    w=O*0.82; h=O*0.60; x0=(O-w)/2; y0=(O-h)/2
    d.rounded_rectangle([x0,y0,x0+w,y0+h],radius=O*0.06,outline=col+(255,),width=t)
    d.line([x0,y0+h*0.08,O/2,y0+h*0.58],fill=col+(255,),width=t)
    d.line([x0+w,y0+h*0.08,O/2,y0+h*0.58],fill=col+(255,),width=t)
    return im

def ic_web(O,col):
    im=newcanvas(O); d=ImageDraw.Draw(im); t=max(2,int(O*0.06))
    m=O*0.12; box=[m,m,O-m,O-m]
    d.ellipse(box,outline=col+(255,),width=t)
    d.ellipse([O*0.32,m,O*0.68,O-m],outline=col+(255,),width=max(1,t-1))  # vertical meridian
    d.line([m,O/2,O-m,O/2],fill=col+(255,),width=max(1,t-1))              # equator
    d.line([O*0.18,O*0.33,O*0.82,O*0.33],fill=col+(255,),width=max(1,t-1))
    d.line([O*0.18,O*0.67,O*0.82,O*0.67],fill=col+(255,),width=max(1,t-1))
    return im

def ic_portfolio(O,col):
    # code </> glyph = developer portfolio
    im=newcanvas(O); d=ImageDraw.Draw(im); t=max(2,int(O*0.08))
    d.line([O*0.40,O*0.30,O*0.24,O*0.50],fill=col+(255,),width=t)
    d.line([O*0.24,O*0.50,O*0.40,O*0.70],fill=col+(255,),width=t)
    d.line([O*0.60,O*0.30,O*0.76,O*0.50],fill=col+(255,),width=t)
    d.line([O*0.76,O*0.50,O*0.60,O*0.70],fill=col+(255,),width=t)
    d.line([O*0.54,O*0.26,O*0.46,O*0.74],fill=col+(255,),width=t)
    return im

def ic_linkedin(O,col):
    im=newcanvas(O); d=ImageDraw.Draw(im)
    d.rounded_rectangle([O*0.05,O*0.05,O*0.95,O*0.95],radius=O*0.18,fill=col+(255,))
    try: f=ImageFont.truetype(FONT_BOLD,int(O*0.55))
    except: f=ImageFont.load_default()
    tw=d.textlength("in",font=f)
    d.text(((O-tw)/2,O*0.20),"in",font=f,fill=(255,255,255,255))
    return im

MAKERS={"phone":ic_phone,"mail":ic_mail,"web":ic_web,"portfolio":ic_portfolio,"linkedin":ic_linkedin}

def main():
    disp=20; ss=3; O=disp*ss
    for aname,col in ACCENTS.items():
        for iname,fn in MAKERS.items():
            im=fn(O,col).resize((disp*2,disp*2),Image.LANCZOS)  # 2x retina
            im.save(os.path.join(ICONS,f"{iname}_{aname}.png"))
    print("icons written to",ICONS, "->", len(os.listdir(ICONS)),"files")

if __name__=="__main__": main()
