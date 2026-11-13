# Perfume — ikut gaya "style-edit-luggage-v4" (bag pack)
import os, subprocess, numpy as np, math, wave, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SFX="sfx/"
FINAL=os.environ.get('FINAL')=='1'
W,H,FPS=(1080,1920,30) if FINAL else (540,960,30); S=W/1080; SPEED=1.1
import os
A=(0.00,3.95,"botol kecil besar");B=(4.15,6.98,"price");C=(7.30,10.90,"100ml harga tak masuk akal")
D=(10.95,16.25,"sweet fruity feminine");E=(16.28,19.15,"kerja/dating");F_=(19.38,22.95,"daily")
G=(23.95,25.40,"wangi");Hh=(27.70,30.25,"nak spray banyak kali");I=(30.60,35.85,"cta")
J=(35.90,39.15,"terlajak murah besar");K=(39.50,43.20,"tahan lama, dah repeat")
VAR={
 "V1":([A,B,C,D,E,F_,G,Hh,I,J,K],[["Botol","Kecil?"],["Rupanya","Besar!"]]),
 "V2":([C,A,B,D,E,F_,G,Hh,K,J,I],[["100ML","Je?"],["Harga","Tak","Masuk","Akal!"]]),
 "V3":([Hh,D,A,C,E,F_,G,J,K,I],[["Rasa","Nak","Spray"],["Banyak","Kali!"]]),
 "V4":([K,A,C,D,E,F_,G,Hh,J,I],[["Dah","Repeat"],["Banyak","Kali!"]]),
 "V5":([J,A,C,D,E,F_,G,Hh,K,I],[["Harga","Terlajak"],["Murah!"]]),
}
VN=os.environ.get("VARIANT","V1");SEG,HOOKW=VAR[VN]
# snap ke titik paling senyap (macam prep.py luggage)
wf=wave.open("audio.wav");sr=wf.getframerate();a=np.frombuffer(wf.readframes(wf.getnframes()),np.int16).astype(float)
hop=sr//100;rms=np.sqrt(np.convolve(a**2,np.ones(hop*2)/(hop*2),'same'))[::hop]
def snap(t,lo,hi):
    i0,i1=max(0,int((t+lo)*100)),min(len(rms),int((t+hi)*100));return (i0+int(np.argmin(rms[i0:i1])))/100
SEG=[(snap(s,-0.10,0.04),snap(e,-0.04,0.12),l) for s,e,l in SEG]
CUTS=[];t=0
for s,e,l in SEG: CUTS.append((s,e,t/SPEED)); t+=e-s
DUR=round(t/SPEED,3)
def T(src):
    for s,e,o in CUTS:
        if s-0.06<=src<=e+0.06: return o+max(0,src-s)/SPEED
    raise SystemExit(f"src {src}")
fv=[];fa=[]
for i,(s,e,l) in enumerate(SEG):
    d=e-s
    fv.append(f"[0:v]trim=start={s}:duration={d:.3f},setpts=PTS-STARTPTS,scale={W}:{H}[v{i}]")
    fa.append(f"[0:a]atrim=start={s}:duration={d:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={d-0.025:.3f}:d=0.025[a{i}]")
n=len(SEG);fc=";".join(fv+fa)+";"+"".join(f"[v{i}][a{i}]" for i in range(n))+f"concat=n={n}:v=1:a=1[cv][ca];"
fc+=(f"[cv]setpts=PTS/{SPEED}[vo];[ca]atempo={SPEED},highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,loudnorm=I=-13:TP=-1.2:LRA=9[ao]")
import sys,os
AUDIO_ONLY=len(sys.argv)>1
if not AUDIO_ONLY: subprocess.run(["ffmpeg","-v","error","-y","-i","src/raw.mov","-filter_complex",fc,"-map","[vo]","-map","[ao]","-r","30",
  "-c:v","libx264","-crf","16","-preset","fast","-c:a","pcm_s16le","-ar","48000",f"footage_{VN}.mov"],check=True)
# ---- overlay list: [src, tempoh, tajuk, sub, L|R, sfx, zoom]
OS=[
 [7.40,2.6,"PERFUME 100ML","Saiz besar, harga bajet!","L","pop","punch"],
 [12.55,2.8,"SWEET • FRUITY • FLORAL","Bau manis dan feminin","L","sparkle","in"],
 [16.30,2.4,"DAILY WEAR FRIENDLY","Work • Casual • Dating","L","click","out"],
 [19.70,2.6,"BOLEH BAWA SOLAT","Mengikut keterangan listing","L","ding","punch"],
 [23.95,1.35,"TOP NOTES","Berry & Pineapple","L","pop","in"],
 [27.75,1.1,"MIDDLE NOTES","Rose & Violet","L","click","out"],
 [28.90,1.25,"BASE NOTES","Patchouli & Musk","L","pop","in"],
 [39.60,3.0,"90% PERFUME CONCENTRATE","Mengikut keterangan seller","L","impact","punch"],
]
O=sorted([[T(s),min(T(s)+d,DUR),tx,sub,side,sfx,z] for s,d,tx,sub,side,sfx,z in OS])
if VN=="V3":
    t0=T(23.95);seq={"TOP NOTES":(t0,t0+1.3),"MIDDLE NOTES":(t0+1.35,t0+2.55),"BASE NOTES":(t0+2.6,t0+3.85)}
    O=sorted([[*seq[r[2-2+0]],*r] if False else ([*seq[o[2]],*o[2:]] if o[2] in seq else o) for o in O for r in [o]])
O2=[];nxt=2.15
for s,e,*r in O:   # overlay dalam hook -> keluar lepas hook pill, satu-satu, min 1.4s
    if s<2.15: s=max(s,nxt); e=max(e,s+1.4); nxt=e+0.05
    O2.append([round(s,2),round(min(e,DUR),2),*r])
O=sorted(O2)
FB=[T(4.25),T(36.0)] if VN=="V1" else [CUTS[1][2]+0.05,CUTS[-2][2]+0.05]
WH=[o for s,e,o in CUTS[1:]]              # whoosh setiap cut
# ---- easing
def clamp(x):return min(1,max(0,x))
def p3o(x):x=clamp(x);return 1-(1-x)**3
def expo(x):x=clamp(x);return 1 if x>=1 else 1-2**(-10*x)
def p2i(x):x=clamp(x);return x*x
def sio(x):x=clamp(x);return -(math.cos(math.pi*x)-1)/2
def backo(x,c=1.70158):x=clamp(x);c3=c+1;return 1+c3*(x-1)**3+c*(x-1)**2
# ---- tween kamera (GSAP-style, overwrite)
TW=[(0,0,1.0,1.0,p3o),(0.3,0.9,1.14,1.02,p3o),(1.2,0.8,None,1.05,sio)]
for s,e,tx,sub,side,sfx,z in O:
    if z=="punch":TW.append((s,0.45,1.12,1.03,p3o))
    elif z=="in":TW.append((s,e-s,None,1.07,sio))
    elif z=="out":TW.append((s,e-s,None,1.0,sio))
TW.sort(key=lambda x:x[0])
def cam(t):
    v=1.0
    for st,d,fr,to,ez in TW:
        if t<st:break
        f0=v if fr is None else fr
        if d<=0 or t>=st+d: v=to
        else: return f0+(to-f0)*ez((t-st)/d)
    return v
# ---- background (radial navy + grid) untuk frame break
yy,xx=np.mgrid[0:H,0:W];r=np.sqrt(((xx-W*.5)/(W*1.2))**2+((yy-H*.35)/(H*.7))**2)
c0=np.array([0x24,0x30,0x4d]);c1=np.array([0x0e,0x14,0x24]);c2=np.array([0x07,0x0a,0x12])
bg=np.where((r<.55)[...,None],c0+(c1-c0)*(r/.55)[...,None],c1+(c2-c1)*np.clip((r-.55)/.45,0,1)[...,None])
g=int(72*S);grid=((xx%g==0)|(yy%g==0));bg[grid]=bg[grid]*0.95+255*0.05
BG=Image.fromarray(bg.astype(np.uint8)).convert("RGBA")
# ---- fonts
def F(sz,wt):
    f=ImageFont.truetype("assets/LexendMega.ttf",max(6,round(sz*S)));f.set_variation_by_axes([wt]);return f
FT,FS,FH=F(24,600),F(15,400),F(26,700)
def track(d,xy,txt,font,ls,fill,anchor_right=False):
    # letter-spacing negatif (-0.04em) macam CSS
    ws=[d.textlength(c,font=font)+ls for c in txt];tw=sum(ws)-ls;x,y=xy
    if anchor_right:x-=tw
    for c,w in zip(txt,ws):d.text((x,y),c,font=font,fill=fill);x+=w
    return tw
def twidth(d,txt,font,ls):return sum(d.textlength(c,font=font)+ls for c in txt)-ls
def shadowed(base,drawfn,blur,alpha):
    sh=Image.new("RGBA",base.size,(0,0,0,0));drawfn(ImageDraw.Draw(sh),(0,0,0,int(255*alpha)),int(2*S))
    sh=sh.filter(ImageFilter.GaussianBlur(blur));base.alpha_composite(sh)
    lay=Image.new("RGBA",base.size,(0,0,0,0));drawfn(ImageDraw.Draw(lay),None,0);base.alpha_composite(lay)
TOP=int(255*S)
def word(img,t,s,e,tx,sub,side):
    # .tx: opacity 0,y14,scale.92 -> 1 (0.34 back.out(2)); .sb at s+.12; .bar scaleX at s+.06; out e-0.2 (0.18 power2.in)
    p=backo((t-s)/0.34,2);a1=clamp((t-s)/0.34)
    outp=p2i((t-(e-0.2))/0.18) if t>=e-0.2 else 0
    ao=1-outp;dy=-8*outp*S
    a_tx=a1*ao;y_tx=(1-p)*14*S+dy
    ps=expo((t-s-0.12)/0.3);a_sb=0.92*clamp((t-s-0.12)/0.3)*ao;y_sb=(1-ps)*8*S+dy
    pb=expo((t-s-0.06)/0.38)*(1 if outp<1 else 0)
    d0=ImageDraw.Draw(img);ls=-0.04*24*S;ls2=-0.03*15*S
    x0=int(80*S) if side=="L" else W-int(150*S)
    R=side=="R"
    def dt(dr,col,off):
        c=(255,255,255,int(255*a_tx)) if col is None else col[:3]+(int(col[3]*a_tx),)
        track(dr,(x0+off,TOP+y_tx+off),tx,FT,ls,c,R)
        if sub:
            c2=(255,255,255,int(255*a_sb)) if col is None else col[:3]+(int(col[3]*a_sb*0.9),)
            track(dr,(x0+off,TOP+int(37*S)+y_sb+off),sub,FS,ls2,c2,R)
        bw=46*S*pb;by=TOP+int((37+(30 if sub else 0))*S)+dy
        if bw>0.5:
            ca=int(255*ao) if col is None else int(col[3]*0.7*ao)
            cc=(255,255,255,ca) if col is None else (0,0,0,ca)
            xs=(x0-bw if R else x0)+off
            dr.rounded_rectangle([xs,by+off,xs+bw,by+3*S+off],radius=1,fill=cc)
    shadowed(img,dt,3*S,0.5)
def hook(img,frame,t):
    # pill 0.3 (opacity/scale .7->1 back.out(2.2) .45s), words stagger .12 from .42, out at 1.82 (.22s)
    if not (0.3<=t<2.05):return
    ps=backo((t-0.3)/0.45,2.2);ap=clamp((t-0.3)/0.45)
    if t>=1.82:o=p2i((t-1.82)/0.22);ap*=1-o;dy=-10*o*S
    else:dy=0
    d=ImageDraw.Draw(img);ls=-0.05*26*S;gap=10*S
    lines=[[twidth(d,w,FH,ls) for w in L] for L in HOOKW]
    lw=[sum(l)+gap*(len(l)-1) for l in lines];lh=26*S*1.35
    pw=max(lw)+56*S;ph=lh*2+30*S
    sc=0.7+0.3*ps;pw2,ph2=pw*sc,ph*sc
    x1=W-150*S;x0=x1-pw2;y0=TOP+dy;rad=34*S*sc
    box=(int(x0),int(y0),int(x1),int(y0+ph2))
    # backdrop blur + tint .34 + border
    m=Image.new("L",img.size,0);ImageDraw.Draw(m).rounded_rectangle(box,radius=rad,fill=int(255*ap))
    bl=frame.filter(ImageFilter.GaussianBlur(10*S));tint=Image.new("RGBA",img.size,(10,14,24,255))
    bl=Image.blend(bl,tint,0.34);bl.putalpha(m);img.alpha_composite(bl)
    ImageDraw.Draw(img).rounded_rectangle(box,radius=rad,outline=(255,255,255,int(255*.35*ap)),width=max(1,round(1.5*S)))
    k=0
    for li,L in enumerate(HOOKW):
        xr=x1-28*S*sc;ws=lines[li];x=xr-(sum(ws)+gap*(len(ws)-1))*sc
        for wi,wd in enumerate(L):
            st=0.42+0.12*k;pw_=expo((t-st)/0.32);aw=clamp((t-st)/0.32)*(ap if t>=1.82 else 1)
            y=y0+(14*S+li*lh)*sc+(1-pw_)*14*S
            f=F(26*sc,700)
            def dw(dr,col,off,x=x,y=y,wd=wd,f=f,aw=aw):
                c=(255,255,255,int(255*aw)) if col is None else (0,0,0,int(90*aw))
                track(dr,(x+off,y+off),wd,f,ls*sc,c)
            shadowed(img,dw,3*S,0.35)
            x+=ws[wi]*sc+gap*sc;k+=1
def fbreak(t):
    # scale .86 rotate (in .16 power2.in), back to 1 (.42 back.out(1.6)); crack flash
    for k,tb in enumerate(FB):
        rot=(-1.6,1.4)[k]
        if tb-0.16<=t<tb:x=p2i((t-(tb-0.16))/0.16);return 1-0.14*x,rot*x,40*x,0
        if tb<=t<tb+0.42:x=backo((t-tb)/0.42,1.6);return 0.86+0.14*x,rot*(1-x),40*(1-x),0.85*(1-p3o((t-tb)/0.28))
    return 1,0,0,0
# ---- render
if AUDIO_ONLY: dec=None
else: dec=subprocess.Popen(["ffmpeg","-v","error","-i",f"footage_{VN}.mov","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
if not AUDIO_ONLY: enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","30","-i","-",
  "-c:v","libx264","-crf","18" if FINAL else "20","-preset","medium" if FINAL else "fast","-pix_fmt","yuv420p",f"vid_{VN}.mp4"],stdin=subprocess.PIPE)
fi=0
while not AUDIO_ONLY:
    buf=dec.stdout.read(W*H*3)
    if len(buf)<W*H*3:break
    t=fi/FPS;fr=Image.frombuffer("RGB",(W,H),buf)
    z=cam(t)
    if abs(z-1)>1e-3:
        cw,ch=W/z,H/z;cx,cy=W*.5,H*.45;x0,y0=cx-cw*.5,cy-ch*.45*2  # transform-origin 50% 45%
        x0=cx-cw/2;y0=cy-ch*0.45
        fr=fr.resize((W,H),Image.BICUBIC,box=(x0,y0,x0+cw,y0+ch))
    fr=fr.convert("RGBA")
    sc,rot,rad,crk=fbreak(t)
    if sc<0.999:
        sw,sh=int(W*sc),int(H*sc);sm=fr.resize((sw,sh),Image.BICUBIC)
        m=Image.new("L",(sw,sh),0);ImageDraw.Draw(m).rounded_rectangle([0,0,sw-1,sh-1],radius=int(rad*S),fill=255)
        brd=Image.new("RGBA",(sw+4,sh+4),(0,0,0,0));ImageDraw.Draw(brd).rounded_rectangle([0,0,sw+3,sh+3],radius=int(rad*S)+2,fill=(255,255,255,230))
        brd.paste(sm,(2,2),m);brd=brd.rotate(-rot,Image.BICUBIC,expand=True)
        base=BG.copy();base.alpha_composite(brd,((W-brd.width)//2,(H-brd.height)//2));fr=base
    if crk>0:
        cl=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(cl)
        d.line([(W*0.62,0),(W*0.30,H)],fill=(255,255,255,int(242*crk)),width=2)
        d.line([(W*0.30,0),(W*0.78,H)],fill=(255,255,255,int(180*crk)),width=1);fr.alpha_composite(cl)
    ov=Image.new("RGBA",(W,H),(0,0,0,0))
    hook(ov,fr,t)
    for s,e,tx,sub,side,sfx,zz in O:
        if s<=t<e:word(ov,t,s,e,tx,sub,side)
    fr.alpha_composite(ov);enc.stdin.write(fr.convert("RGB").tobytes());fi+=1
if not AUDIO_ONLY: enc.stdin.close();enc.wait()
# ---- audio: suara + muzik 0.09 + sfx (volume sama macam luggage)
VOL={"impact":0.45,"riser":0.4,"sparkle":0.35,"ding":0.32,"pop":0.45,"click":0.45}
ev=[("music",0,0.09,DUR),("hook",0,0.5,1.4),("pop",0.62,0.3,0.2)]
for s,e,tx,sub,side,sfx,z in O:ev.append((sfx,max(0,s-0.03),VOL[sfx],1.2))
for tb in FB:ev.append(("snap",tb-0.16,0.4,0.6))
for w in WH:ev.append(("whoosh",max(0,w-0.2),0.22,0.5))
inp=["-i",f"footage_{VN}.mov"];fl=[]
for i,(nm,st,vol,d) in enumerate(ev):
    inp+=["-i",SFX+nm+".wav"]
    fl.append(f"[{i+2}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{d},volume={vol},adelay={int(st*1000)}|{int(st*1000)}[s{i}]")
fl.append("[1:a]aformat=channel_layouts=stereo[vo]")
fl.append("[vo]"+"".join(f"[s{i}]" for i in range(len(ev)))+f"amix=inputs={len(ev)+1}:duration=first:normalize=0,alimiter=limit=0.95[aout]")
subprocess.run(["ffmpeg","-v","error","-y","-i",f"vid_{VN}.mp4"]+inp+["-filter_complex",";".join(fl),"-map","0:v","-map","[aout]",
  "-c:v","copy","-c:a","aac","-b:a","256k" if FINAL else "160k","-shortest","-movflags","+faststart",(f"final/FINAL_{VN}.mp4" if FINAL else f"PREVIEW_{VN}.mp4")],check=True)
print("DUR",DUR,"frames",fi)
for s,e,tx,*_ in O:print(f"{s:6.2f}-{e:6.2f} {tx}")
