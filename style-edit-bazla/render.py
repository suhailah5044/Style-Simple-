import subprocess,sys,math,numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
K=float(sys.argv[1]);OUT=sys.argv[2];W,H=int(1080*K),int(1920*K);FPS=30;DUR=19.15
def font(sz):
    f=ImageFont.truetype("lexend.ttf",int(sz*K))
    try:f.set_variation_by_axes([600])
    except Exception:pass
    return f
F=font(30);FK=font(20);FT=font(36)
# [start,end,text,side,kind]  kind: t=text, p=pill(fact)
O=[[3.10,4.45,"LOOSE CUTTING","L","t"],
   [4.50,6.00,"CUTTING LABUH","L","t"],
   [6.05,7.70,"KEMEJA BAZLA","L","t"],
   [7.75,9.10,"MATERIAL\nCOTTON LINEN","L","t"],
   [9.15,10.25,"RINGAN &\nBREATHABLE","R","t"],
   [10.30,11.35,"FULL BUTTON","R","p"],
   [12.00,12.95,"SIDE SLIT\nKIRI KANAN","L","t"],
   [13.00,14.40,"FREE SIZE\nDADA ±50 INCI","L","p"],
   [14.45,15.55,"COLOUR LILAC","L","t"],
   [15.60,16.55,"TAK MELEKAT\nBADAN","L","t"],
   [16.60,17.55,"SENANG\nMIX & MATCH","L","t"],
   [17.60,18.40,"DAILY WEAR &\nOUTFIT KERJA","L","t"],
   [18.45,19.15,"DAPATKAN SEKARANG","L","t"]]
PUNCH=[0.0,1.62,7.75,10.39,12.13,14.49]
X0,X1,Y=70*K,1010*K,250*K
def eo(x):return 1-2**(-10*max(0,min(1,x)))
def layer(t):
    im=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    items=[]
    if t<3.0:
        a=eo((t-0.15)/0.4)*(1-max(0,min(1,(t-2.8)/0.2)));items.append((FK,"KEMEJA BAZLA",X0,Y+(1-eo((t-.15)/.4))*22*K,a,"L","k"))
        a2=eo((t-0.45)/0.4)*(1-max(0,min(1,(t-2.8)/0.2)));items.append((FT,"COTTON LINEN",X0,Y+34*K+(1-eo((t-.45)/.4))*22*K,a2,"L","t"))
    for s,e,tx,side,k in O:
        if s<=t<e:
            p=(t-s)/0.38;a=eo(p)*(1-max(0,min(1,(t-(e-0.2))/0.2)));dy=(1-eo(p))*22*K-max(0,(t-(e-0.2))/0.2)*10*K
            items.append((F,tx,None,Y+dy,a,side,k,(t-s)))
    for it in items:
        f,tx,x,y,a,side,k=it[:7]
        if a<=0:continue
        bb=d.multiline_textbbox((0,0),tx,font=f,spacing=int(8*K),align="left" if side=="L" else "right")
        tw,th=bb[2],bb[3]
        x=X0 if side=="L" else X1-tw
        lay=Image.new("RGBA",(W,H),(0,0,0,0));ld=ImageDraw.Draw(lay)
        sh=Image.new("RGBA",(W,H),(0,0,0,0));sd=ImageDraw.Draw(sh)
        al="left" if side=="L" else "right"
        if k=="p":
            pad=14*K;sc=eo((it[7])/0.3) if len(it)>7 else 1
            ld.rounded_rectangle((x-pad,y-pad*.8,x+tw+pad,y+th+pad),radius=int(18*K),outline=(255,255,255,255),width=max(1,int(2*K)))
            sd.rounded_rectangle((x-pad,y-pad*.8,x+tw+pad,y+th+pad),radius=int(18*K),outline=(0,0,0,110),width=max(1,int(3*K)))
        sd.multiline_text((x,y+2*K),tx,font=f,fill=(0,0,0,170),spacing=int(8*K),align=al)
        ld.multiline_text((x,y),tx,font=f,fill=(255,255,255,255),spacing=int(8*K),align=al)
        if k=="t" and len(it)>7:
            bw=56*K*eo((it[7]-0.08)/0.4);by=y+th+10*K
            bx=x if side=="L" else x+tw-bw
            if bw>0:ld.rectangle((bx,by,bx+bw,by+3*K),fill=(255,255,255,255));sd.rectangle((bx,by+1*K,bx+bw,by+4*K),fill=(0,0,0,90))
        sh=sh.filter(ImageFilter.GaussianBlur(3*K))
        comb=Image.alpha_composite(sh,lay)
        if a<1:comb.putalpha(comb.getchannel("A").point(lambda v:int(v*a)))
        im=Image.alpha_composite(im,comb)
    return im
def zoom(t):
    z=1.0;p=max([q for q in PUNCH if q<=t],default=None)
    if p is not None:z+=0.09*math.exp(-(t-p)/0.28)
    return z+0.015*math.sin(t*0.6)**2
dec=subprocess.Popen(["ffmpeg","-v","error","-i","base.mp4","-vf",f"scale={W}:{H}:in_color_matrix=bt709:in_range=tv:flags=bicubic","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
# audio: voice + ducked music + sfx
sfx=[(s,"ui_blip",.25) for s,*_ in O]+[(p,"sub_boom",.3) for p in PUNCH[1:]]+[(0.15,"swoosh",.3)]
S="/home/user/Style-Simple-/style-edit-standphone-v2/sfx/"
ain=["-i","base.mp4","-i","music.wav"];af=[]
for i,(s,n,v) in enumerate(sfx):
    ain+=["-i",S+n+".wav"];af.append(f"[{i+3}:a]adelay={int(s*1000)}|{int(s*1000)},volume={v}[s{i}]")
af.append("[1:a]asplit[v1][v2]");af.append("[2:a]volume=0.22[m];[m][v2]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md]")
af.append("[v1][md]"+"".join(f"[s{i}]" for i in range(len(sfx)))+f"amix=inputs={len(sfx)+2}:normalize=0:duration=first,alimiter=limit=0.95[a]")
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-"]+ain+["-filter_complex",";".join(af),"-map","0:v","-map","[a]","-vf","scale=out_color_matrix=bt709:out_range=tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-c:v","libx264","-crf","18" if K==1 else "24","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest",OUT],stdin=subprocess.PIPE)
i=0;fs=W*H*3
while True:
    b=dec.stdout.read(fs)
    if len(b)<fs:break
    t=i/FPS;fr=Image.frombytes("RGB",(W,H),b);z=zoom(t)
    if z>1.001:
        zw,zh=int(W*z),int(H*z);fr=fr.resize((zw,zh),Image.BILINEAR);ox=(zw-W)//2;oy=int((zh-H)*0.4);fr=fr.crop((ox,oy,ox+W,oy+H))
    fr=Image.alpha_composite(fr.convert("RGBA"),layer(t)).convert("RGB")
    enc.stdin.write(fr.tobytes());i+=1
enc.stdin.close();enc.wait();print("frames",i)
