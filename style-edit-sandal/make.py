# Jana video tambahan dari footage "Sandal 2" — satu klip cakap setiap video.
# Guna: python3 make.py <folder_sumber> <nama_video>
# Masa dalam CONF = masa dalam klip asal; dipetakan automatik ke timeline lepas potong.
import subprocess,sys,json,os,wave,shutil
import numpy as np
SRC=sys.argv[1]; NAME=sys.argv[2]
F={"A":"10OOMKGa_pmPillbprIcGOxYurIiuUHir","B":"1Sf4y1GUM5VA57OxTK8Yzu5kKX_kmlX67","C":"1WjczG8ICgiP68pfT1AOo4WAhw5EWZJVk","D":"1wNTB8uK78Tt4wdcLureW522Et2Ah-fol","E":"1zTGiPwrS4hr5TFxpn7MzpFj61G6APyGI"}
# B-roll produk sahaja (crop 9:16 penuh skrin, tiada muka)
K={"hitam":("C",15.1,"675:1200:202:720",4.0),"kaki":("C",64.0,"432:768:330:1152",4.0),
   "maroon":("E",21.1,"512:910:134:1010",2.9)}  # crop center pada sandal, tiada muka
CONF={
 "v2_selesa":dict(clip="C",
   cuts=[(8.5,11.15),(29.4,34.25),(35.1,35.98),(45.9,52.55),(57.35,66.15)],
   hook="SANDAL PILIHAN<br>WANITA!",anim="up",
   texts=[(47.1,49.8,"Comfortable Fit"),(51.75,52.55,"Everyday Sandals")],
   broll=[(31.2,"kaki"),(58.1,"maroon")]),
 "v3_murah":dict(clip="B",
   cuts=[(9.6,14.72),(20.45,22.6),(24.1,26.02),(28.05,34.2)],
   hook="MURAH TAPI<br>CANTIK!",anim="scale",
   texts=[(28.1,30.7,"Simple &amp; Stylish"),(31.1,34.1,"Budget Friendly")],
   broll=[(24.75,"hitam")]),
 "v4_antirugi":dict(clip="E",
   cuts=[(17.6,23.05),(23.35,25.0),(40.4,50.8)],
   hook="SANDAL<br>ANTI RUGI!",anim="words",
   texts=[(21.85,23.05,"Simple &amp; Stylish"),(49.0,50.8,"Comfortable Fit")],
   broll=[(21.5,"maroon"),(42.7,"hitam")]),
}
C=CONF[NAME]; OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"more",NAME)
os.makedirs(OUT+"/assets",exist_ok=True); os.makedirs(OUT+"/sfx",exist_ok=True)
HERE=os.path.dirname(os.path.abspath(__file__))
shutil.copy(HERE+"/assets/LexendMega.woff2",OUT+"/assets/"); shutil.copy(HERE+"/sfx/ui_blip.wav",OUT+"/sfx/")
def run(a): subprocess.run(["ffmpeg","-v","error","-y"]+a,check=True)
# --- snap titik potong ke celah senyap ---
w=wave.open(f"{SRC}/{F[C['clip']]}.wav"); A=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
def db(t): i=int(t*16000); return 20*np.log10(np.sqrt(np.mean(A[i:i+640]**2))+1e-9)  # 40ms
def snap_in(t):
    c=[x for x in np.arange(t-0.25,t+0.04,0.01) if db(x)<-33]; return round(float(c[-1]) if c else t,2)
def snap_out(t):
    c=[x for x in np.arange(t-0.04,t+0.3,0.01) if db(x)<-33]; return round(float(c[0])+0.04 if c else t,2)
CUTS=[(snap_in(a),snap_out(b)) for a,b in C["cuts"]]
X=0.08; VF="scale=1080:1920:flags=lanczos,setsar=1,fps=30"
ins=[];fc=[];edl=[];acc=0
for i,(s,e) in enumerate(CUTS):
    ins+=["-ss",str(s),"-to",str(e),"-i",f"{SRC}/{F[C['clip']]}.mov"]
    fc.append(f"[{i}:v]{VF},setpts=PTS-STARTPTS[v{i}];[{i}:a]asetpts=PTS-STARTPTS[a{i}]")
pv,pa="v0","a0";acc=CUTS[0][1]-CUTS[0][0];edl.append((CUTS[0][0],CUTS[0][1],0.0))
for i in range(1,len(CUTS)):
    off=acc-X; edl.append((CUTS[i][0],CUTS[i][1],round(off,3)))
    fc.append(f"[{pv}][v{i}]xfade=transition=fade:duration={X}:offset={off:.3f}[xv{i}];[{pa}][a{i}]acrossfade=d={X}[xa{i}]")
    pv,pa=f"xv{i}",f"xa{i}"; acc=off+(CUTS[i][1]-CUTS[i][0])
run(ins+["-filter_complex",";".join(fc),"-map",f"[{pv}]","-map",f"[{pa}]","-c:v","libx264","-crf","15","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",OUT+"/assets/footage.mp4"])
DUR=round(acc,2)
def T(src):  # masa klip asal -> masa timeline
    for s,e,t0 in edl:
        if s-0.05<=src<=e+0.05: return round(t0+max(0,src-s),2)
    raise SystemExit(f"masa {src} tiada dalam potongan")
for j,(src,key) in enumerate(C["broll"]):
    k,s,cr,bd=K[key]
    run(["-ss",str(s),"-t",str(bd),"-i",f"{SRC}/{F[k]}.mov","-vf",f"scale=1080:1920,crop={cr},scale=1080:1920:flags=lanczos,setsar=1,fps=30","-an","-c:v","libx264","-crf","15","-pix_fmt","yuv420p",f"{OUT}/assets/broll{j}.mp4"])
# --- HTML ---
el=[];js=[]
for j,(src,key) in enumerate(C["broll"]):
    bd=K[key][3]; s=min(T(src),round(DUR-bd,2))
    el.append(f'<video id="b{j}" class="broll" src="assets/broll{j}.mp4" data-start="{s}" data-duration="{bd}" muted playsinline></video>')
    js.append(f'tl.fromTo("#b{j}",{{opacity:0}},{{opacity:1,duration:0.5,ease:"sine.inOut"}},{s});tl.to("#b{j}",{{opacity:0,duration:0.5,ease:"sine.inOut"}},{s+bd-0.5:.2f});')
for j,(a,b,txt) in enumerate(C["texts"]):
    s,e=T(a),T(b); e=max(e,s+1.4)
    el.append(f'<div id="w{j}" class="clip word" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{txt}</span><i class="bar"></i></div>')
    js.append(f'tl.fromTo("#w{j} .tx",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.45,ease:"power2.out"}},{s});tl.fromTo("#w{j} .bar",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"power2.out"}},{s+0.08:.2f});tl.to("#w{j} .tx,#w{j} .bar",{{opacity:0,duration:0.25}},{e-0.25:.2f});')
H=C["hook"]; HD=2.8
if C["anim"]=="words":
    parts=H.replace("<br>"," <br> ").split(" "); hk="".join(p if p=="<br>" else f'<span class="hw">{p}</span> ' for p in parts)
    js.insert(0,f'tl.fromTo("#hook .hw",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.35,stagger:0.18,ease:"power2.out"}},0.1);tl.to("#hook",{{opacity:0,duration:0.3}},{HD-0.3});')
elif C["anim"]=="scale":
    hk=f'<span class="hw">{H}</span>'
    js.insert(0,f'tl.fromTo("#hook .hw",{{opacity:0,scale:0.92}},{{opacity:1,scale:1,duration:0.6,ease:"power2.out"}},0.1);tl.to("#hook",{{opacity:0,duration:0.3}},{HD-0.3});')
else:
    hk=f'<span class="hw">{H}</span>'
    js.insert(0,f'tl.fromTo("#hook .hw",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},0.1);tl.to("#hook",{{opacity:0,duration:0.3}},{HD-0.3});')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%;}}
#cam video,.broll{{width:100%;height:100%;object-fit:cover;display:block;}}
.broll{{position:absolute;inset:0;z-index:3;opacity:0;}}
.word{{position:absolute;top:250px;left:0;right:0;text-align:center;z-index:5;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:30px;line-height:1.3;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);opacity:0;}}
.word .bar{{display:block;height:3px;width:56px;background:#fff;border-radius:2px;margin:10px auto 0;transform:scaleX(0);}}
#hook{{position:absolute;top:235px;left:120px;right:120px;text-align:center;z-index:6;color:#fff;font-family:"Lexend Mega",sans-serif;font-weight:700;
  font-size:46px;line-height:1.2;letter-spacing:-0.04em;text-shadow:0 2px 8px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);}}
#hook .hw{{display:inline-block;opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  {chr(10).join("  "+x for x in el)}
  <div id="hook" class="clip" data-start="0" data-duration="{HD}">{hk}</div>
  <audio id="a_hook" src="sfx/ui_blip.wav" data-start="0.1" data-duration="1.0" data-volume="0.25"></audio>
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.fromTo("#cam",{{scale:1.0}},{{scale:1.04,duration:{DUR},ease:"none"}},0);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open(OUT+"/index.html","w").write(html)
json.dump({"cuts":CUTS,"edl":edl,"dur":DUR},open(OUT+"/edl.json","w"))
print(NAME,"DUR",DUR,"CUTS",CUTS)
