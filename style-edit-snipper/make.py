# python3 make.py v1|v2|v3 [--html]   (RAW & audio16k dari env RAW / AUD)
# 1) potong ayat + buang pause dalaman, b-roll stabil, speed 1.1, kuatkan suara -> vN/assets/footage.mp4
# 2) bina vN/index.html (HyperFrames): hook 0-3s, overlay kata, SFX, zoom, frame break, PiP
import numpy as np, wave, json, subprocess, sys, os, shutil
from variants import V
name=sys.argv[1]; only_html="--html" in sys.argv
RAW=os.environ.get("RAW","/tmp/claude-0/dl/raw.bin"); AUD=os.environ.get("AUD","/tmp/claude-0/w/a16.wav")
cfg=V[name]; SPEED=1.1; P=name
os.makedirs(f"{P}/assets",exist_ok=True)
for f in os.listdir("sfx"):
    os.makedirs(f"{P}/sfx",exist_ok=True); shutil.copy(f"sfx/{f}",f"{P}/sfx/{f}")
shutil.copy("assets/LexendMega.woff2",f"{P}/assets/")
if os.path.exists("assets/gsap.min.js"): shutil.copy("assets/gsap.min.js",f"{P}/assets/")

# ---------- audio analysis ----------
wf=wave.open(AUD); sr=wf.getframerate(); a=np.frombuffer(wf.readframes(wf.getnframes()),np.int16).astype(float)
hop=sr//100; rms=np.sqrt(np.convolve(a**2,np.ones(hop*2)/(hop*2),'same'))[::hop]
THR=np.percentile(rms,95)*0.07
def snap(t,lo,hi):
    i0,i1=max(0,int((t+lo)*100)),int((t+hi)*100); return (i0+int(np.argmin(rms[i0:i1])))/100
def split_pauses(s,e,minp=0.22,keep=0.07):
    """buang pause dalaman > minp (tinggal keep setiap sisi)"""
    i0,i1=int(s*100),int(e*100); sil=rms[i0:i1]<THR; out=[];cur=s;j=0
    while j<len(sil):
        if sil[j]:
            k=j
            while k<len(sil) and sil[k]: k+=1
            if (k-j)/100>minp and j>0 and k<len(sil):
                out.append([cur,(i0+j)/100+keep]); cur=(i0+k)/100-keep
            j=k
        else: j+=1
    out.append([cur,e]); return out

# ---------- pieces ----------
pieces=[]  # [a0,a1,v0,seg_idx]
for si,(s,e,v,tag) in enumerate(cfg["segs"]):
    s2=snap(s,-0.06,0.05); e2=snap(e,-0.05,0.08)
    parts=split_pauses(s2,e2)
    vt=v
    for p0,p1 in parts:
        pieces.append([p0,p1,(vt if v is not None else p0),si]);
        if v is not None: vt+=p1-p0
t=0; OUT=[]
for p in pieces: OUT.append(t/SPEED); t+=p[1]-p[0]
DUR=round(t/SPEED,3)
def m(src):  # src audio time -> output time
    for (a0,a1,v0,si),o in zip(pieces,OUT):
        if a0-0.05<=src<=a1+0.05: return round(o+max(0,src-a0)/SPEED,2)
    raise ValueError(f"{src} not in cut")
seg_start={}
for p,o in zip(pieces,OUT): seg_start.setdefault(p[3],o)

if not only_html:
    fv=[];fa=[]
    # potong setiap kepingan berasingan (jimat memori), kemudian sambung
    tmp=f"/tmp/claude-0/w/{P}_pcs"; os.makedirs(tmp,exist_ok=True); ins=[]
    for i,(s,e,v,_) in enumerate(pieces):
        d=e-s; fn=f"{tmp}/p{i}.mkv"
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{v:.3f}","-t",f"{d:.3f}","-i",RAW,"-ss",f"{s:.3f}","-t",f"{d:.3f}","-i",RAW,
          "-map","0:v","-map","1:a","-af",f"afade=t=in:d=0.012,afade=t=out:st={d-0.02:.3f}:d=0.02",
          "-c:v","libx264","-preset","veryfast","-crf","8","-pix_fmt","yuv420p","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
          "-r","30","-c:a","pcm_s16le","-ar","48000",fn],check=True)
        ins+=["-i",fn]
    n=len(pieces); cat="".join(f"[{i}:v][{i}:a]" for i in range(n))+f"concat=n={n}:v=1:a=1[cv][ca]"
    post=(f"[cv]setpts=PTS/{SPEED}[vo];[ca]atempo={SPEED},highpass=f=75,"
          "acompressor=threshold=-22dB:ratio=3.5:attack=4:release=110:makeup=3,loudnorm=I=-11:TP=-1.0:LRA=7,alimiter=limit=0.89[ao]")
    subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",cat+";"+post,
      "-map","[vo]","-map","[ao]","-c:v","libx264","-preset","medium","-threads","4","-crf","14","-pix_fmt","yuv420p",
      "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-r","30","-c:a","aac","-b:a","256k","-ar","48000",
      f"{P}/assets/footage.mp4"],check=True)
    for k,(vs,src,d,side) in enumerate(cfg.get("pip",[])):
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(vs),"-t",f"{d*SPEED+0.2:.2f}","-i",RAW,"-an","-vf",f"setpts=PTS/{SPEED},scale=360:-2",
          "-c:v","libx264","-crf","16","-pix_fmt","yuv420p","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-r","30",f"{P}/assets/pip{k}.mp4"],check=True)

# ---------- timeline ----------
ov=[];au=[];js=[];pipd=[]
VOL={"impact2":0.42,"ding2":0.3,"ting2":0.3,"shimmer":0.3,"droplet":0.4,"zip":0.32,"click2":0.42,"pop2":0.4,
     "ui_prompt1":0.36,"ui_prompt2":0.34,"ui_prompt3":0.36}
_st=sorted(m(o[0]) for o in cfg["ov"])+[DUR]
for i,(src,dur,tx,sub,side,sfx,z) in enumerate(cfg["ov"]):
    s=m(src); nx=min(x for x in _st if x>s+0.01); dur=round(min(dur,nx-s-0.08),2); cfg["ov"][i][1]=dur; e=round(s+dur,2)
    sb=f'<span class="sb">{sub}</span>' if sub else ""
    ov.append(f'<div id="w{i}" class="clip word {side}" data-start="{s}" data-duration="{dur}"><span class="mk"></span><span class="tx">{tx}</span>{sb}</div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.03):.2f}" data-duration="1.0" data-volume="{VOL.get(sfx,0.35)}"></audio>')
    js.append(cfg["anim_in"].format(i=i,s=s,s2=round(s+0.1,2)))
    js.append(f'tl.to("#w{i} > *",{{opacity:0,y:-6,duration:.18,ease:"power2.in"}},{e-0.2:.2f});')
    if z=="punch": js.append(f'tl.fromTo("#cam",{{scale:1.11}},{{scale:1.03,duration:.45,ease:"power3.out",overwrite:"auto"}},{s});')
    elif z=="in": js.append(f'tl.to("#cam",{{scale:1.07,duration:{dur},ease:"sine.inOut",overwrite:"auto"}},{s});')
    elif z=="out": js.append(f'tl.to("#cam",{{scale:1.0,duration:{dur},ease:"sine.inOut",overwrite:"auto"}},{s});')
# jump-cut punch (sorok potongan dlm segmen yg sama): selang-seli skala
k=0
for j in range(1,len(pieces)):
    if pieces[j][3]==pieces[j-1][3] and cfg["segs"][pieces[j][3]][2] is None:
        k+=1; js.append(f'tl.set("#cut",{{scale:{1.06 if k%2 else 1.0}}},{OUT[j]:.2f});')
    else:
        js.append(f'tl.set("#cut",{{scale:1.0}},{OUT[j]:.2f});')
# whoosh di tukar babak (segmen lompat jauh)
w=0
for j in range(1,len(cfg["segs"])):
    s0=cfg["segs"][j-1]; s1=cfg["segs"][j]
    if abs(s1[0]-s0[1])>3 or s1[2] is not None or s0[2] is not None:
        tt=seg_start[j]
        if tt<3.2: continue
        au.append(f'<audio id="wh{w}" src="sfx/{("whoosh_a","whoosh_b")[w%2]}.wav" data-start="{tt-0.18:.2f}" data-duration="0.5" data-volume="0.2"></audio>'); w+=1
# frame break
for k,si in enumerate(cfg["fb"]):
    tt=seg_start[si]
    au.append(f'<audio id="fb{k}" src="sfx/fbreak.wav" data-start="{tt-0.15:.2f}" data-duration="0.6" data-volume="0.36"></audio>')
    js.append(f'tl.to("#fb",{{scale:.84,rotation:{(-1.5,1.3,-1.1)[k%3]},borderRadius:44,duration:.16,ease:"power2.in"}},{tt-0.16:.2f});')
    js.append(f'tl.to("#fb",{{scale:1,rotation:0,borderRadius:0,duration:.44,ease:"back.out(1.5)"}},{tt:.2f});')
    js.append(f'tl.fromTo("#crk",{{opacity:.8}},{{opacity:0,duration:.28,ease:"power2.out",immediateRender:false}},{tt:.2f});')
# PiP (video atas video)
for k,(vs,src,d,side) in enumerate(cfg.get("pip",[])):
    s=m(src)
    pipd.append(f'<div id="p{k}" class="pip {side}"><video id="pv{k}" src="assets/pip{k}.mp4" data-start="{s}" data-duration="{d}" data-has-audio="false" muted></video></div>')
    au.append(f'<audio id="ps{k}" src="sfx/pip_swish.wav" data-start="{s:.2f}" data-duration="0.4" data-volume="0.26"></audio>')
    dx=60 if side=="R" else -60
    js.append(f'tl.fromTo("#p{k}",{{opacity:0,x:{dx},scale:.85,rotation:{dx/15}}},{{opacity:1,x:0,scale:1,rotation:{dx/30},duration:.4,ease:"back.out(1.8)"}},{s});')
    js.append(f'tl.to("#p{k}",{{opacity:0,scale:.9,duration:.2,ease:"power2.in"}},{s+d-0.22:.2f});')
# CTA: riser lembut, tiada teks
cta=[i for i,sg in enumerate(cfg["segs"]) if sg[3]=="cta"][0]
au.append(f'<audio id="acta" src="sfx/cta_rise.wav" data-start="{seg_start[cta]-0.1:.2f}" data-duration="1.6" data-volume="0.26"></audio>')
js.append(f'tl.to("#cam",{{scale:1.06,duration:{DUR-seg_start[cta]:.2f},ease:"sine.inOut",overwrite:"auto"}},{seg_start[cta]:.2f});')

NL=chr(10)
H=cfg["hook"]
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#0a0d14;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;{cfg["bg"]}}}
#bgfx{{position:absolute;inset:0;{cfg["bgfx"]}}}
#fb{{position:absolute;inset:0;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 0 4px rgba(255,255,255,.92);}}
#cut,#cam{{position:absolute;inset:0;transform-origin:50% 42%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
#crk{{position:absolute;inset:0;z-index:4;opacity:0;pointer-events:none;
  background:linear-gradient(115deg,transparent 47.6%,rgba(255,255,255,.95) 47.8%,transparent 48.1%),linear-gradient(64deg,transparent 60%,rgba(255,255,255,.7) 60.15%,transparent 60.4%);}}
.word{{position:absolute;z-index:5;width:440px;}}
.word .tx,.word .sb{{font-family:"Lexend Mega",sans-serif;color:#fff;opacity:0;}}
.word .tx{{display:inline-block;font-weight:600;font-size:27px;line-height:1.3;letter-spacing:-0.045em;text-shadow:0 2px 10px rgba(0,0,0,.55),0 0 3px rgba(0,0,0,.5);}}
.word .sb{{display:block;margin-top:7px;font-weight:400;font-size:16px;letter-spacing:-0.03em;text-shadow:0 1px 6px rgba(0,0,0,.7),0 0 2px rgba(0,0,0,.5);}}
.word .mk{{opacity:0;}}
{cfg["css"]}
#hook{{position:absolute;left:0;right:0;text-align:center;z-index:6;}}
.pip{{position:absolute;top:{cfg.get("pip_top",380)}px;width:270px;height:340px;border-radius:24px;overflow:hidden;z-index:5;border:4px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.45);opacity:0;}}
.pip.R{{right:60px;}} .pip.L{{left:60px;}}
.pip video{{width:100%;height:100%;object-fit:cover;display:block;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="bgfx"></div>
  <div id="fb"><div id="cut"><div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div></div><div id="crk"></div></div>
  <div id="hook" class="clip" data-start="0" data-duration="3.0">{H["html"]}</div>
  {(NL+"  ").join(pipd)}
  {(NL+"  ").join(ov)}
  <audio id="a_hook" src="sfx/{H["sfx"]}.wav" data-start="0" data-duration="1.6" data-volume="0.5"></audio>
  {(NL+"  ").join(au)}
</div>
<script src="assets/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);tl.set("#cut",{{scale:1}},0);
{H["js"]}
{NL.join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open(f"{P}/index.html","w").write(html)
ts=sorted((m(o[0]),m(o[0])+o[1],o[2]) for o in cfg["ov"])
for x,y in zip(ts,ts[1:]):
    if y[0]<x[1]: print("OVERLAP",x,y)
print(name,"DUR",DUR,"pieces",len(pieces),"overlays",len(cfg["ov"]))
for p,o in zip(pieces,OUT): print(f"  {o:6.2f}  src {p[0]:.2f}-{p[1]:.2f}  v{p[2]:.2f}  seg{p[3]} {cfg['segs'][p[3]][3]}")
