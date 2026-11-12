import subprocess,sys,math,numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
K=float(sys.argv[1]);OUT=sys.argv[2];W,H=int(1080*K),int(1920*K);FPS=30;DUR=20.339999999999996
def font(sz):
    f=ImageFont.truetype("lexend.ttf",int(sz*K))
    try:f.set_variation_by_axes([600])
    except Exception:pass
    return f
F=font(30);FK=font(20);FT=font(36)
# [start,end,text,side,kind]  kind: t=text, p=pill(fact)
O=[[2.15, 4.01, 'COLOUR LILAC', 'L', 't'], [4.19, 5.19, 'MATERIAL\nCOTTON LINEN', 'L', 't'], [5.24, 6.05, 'RINGAN &\nBREATHABLE', 'L', 't'], [6.22, 8.08, 'SIDE SLIT\nKIRI KANAN', 'L', 't'], [8.26, 10.12, 'LOOSE CUTTING\nCUTTING LABUH', 'R', 't'], [12.32, 14.18, 'FREE SIZE\nDADA ±50 INCI', 'L', 'p'], [14.36, 15.31, 'FULL BUTTON', 'L', 'p'], [15.36, 16.22, 'TAK MELEKAT\nBADAN', 'L', 't'], [18.43, 19.38, 'SENANG\nMIX & MATCH', 'L', 't'], [19.43, 20.29, 'DAILY WEAR &\nOUTFIT KERJA', 'L', 't']]
PUNCH=[0.0,1.62,7.75,10.39,12.13,14.49]
X0,X1,Y=70*K,1010*K,250*K
def eo(x):return 1-2**(-10*max(0,min(1,x)))
def layer(t):
    im=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    items=[]
    if t<1.95:
        a=eo((t-0.15)/0.4)*(1-max(0,min(1,(t-1.75)/0.2)));items.append((FK,"KEMEJA BAZLA",X0,Y+(1-eo((t-.15)/.4))*22*K,a,"L","k"))
        a2=eo((t-0.45)/0.4)*(1-max(0,min(1,(t-1.75)/0.2)));items.append((FT,"COTTON LINEN",X0,Y+34*K+(1-eo((t-.45)/.4))*22*K,a2,"L","t"))
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
L=2.034;Z=[(1.06, 0.5, 0.45), (1.18, 0.5, 0.6), (1.32, 0.45, 0.5), (1.18, 0.5, 0.8), (1.06, 0.5, 0.45), (1.3, 0.5, 0.55), (1.12, 0.5, 0.5), (1.22, 0.45, 0.55), (1.06, 0.5, 0.45), (1.05, 0.5, 0.45)]
def zoom(t):
    k=min(9,int(t/L));p=(t-k*L)/L;ze,cx,cy=Z[k]
    e=p*p*(3-2*p)
    return 1+(ze-1)*e+0.05*math.exp(-(t-k*L)/0.18),cx,cy
dec=subprocess.Popen(["ffmpeg","-v","error","-i","base2.mp4","-vf",f"scale={W}:{H}:in_color_matrix=bt709:in_range=tv:flags=bicubic","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
# audio: voice + ducked music + sfx
sfx=[(s,"ui_blip",.22) for s,*_ in O]+[(0.12,"swoosh",.3)]
S="/home/user/Style-Simple-/style-edit-standphone-v2/sfx/"
ain=["-i","music2.wav"];af=[]
for i,(s,n,v) in enumerate(sfx):
    ain+=["-i",S+n+".wav"];af.append(f"[{i+2}:a]adelay={int(s*1000)}|{int(s*1000)},volume={v}[s{i}]")
af.append("[1:a]volume=0.8[m]")
af.append("[m]"+"".join(f"[s{i}]" for i in range(len(sfx)))+f"amix=inputs={len(sfx)+1}:normalize=0:duration=first,alimiter=limit=0.95[a]")
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-"]+ain+["-filter_complex",";".join(af),"-map","0:v","-map","[a]","-vf","scale=out_color_matrix=bt709:out_range=tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-c:v","libx264","-crf","18" if K==1 else "24","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest",OUT],stdin=subprocess.PIPE)
i=0;fs=W*H*3
while True:
    b=dec.stdout.read(fs)
    if len(b)<fs:break
    t=i/FPS;fr=Image.frombytes("RGB",(W,H),b);z,cx,cy=zoom(t)
    if z>1.001:
        zw,zh=int(W*z),int(H*z);fr=fr.resize((zw,zh),Image.BILINEAR);ox=int((zw-W)*cx);oy=int((zh-H)*cy);fr=fr.crop((ox,oy,ox+W,oy+H))
    fr=Image.alpha_composite(fr.convert("RGBA"),layer(t)).convert("RGB")
    enc.stdin.write(fr.tobytes());i+=1
enc.stdin.close();enc.wait();print("frames",i)
