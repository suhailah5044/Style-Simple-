# Usage: python3 build.py v1  -> writes v1/index.html (style v2 + hook Baloo 2 besar dengan grafik + Lexend Mega subtitle UI + UI SFX)
import sys,os,shutil
from videos import VIDEOS
name=sys.argv[1]; cfg=VIDEOS[name]; O=cfg["O"]; DUR=cfg["dur"]; H1,H2=cfg["hook"]
FS=int(min(100,1800/len(H1)))
H1W="".join(f'<span class="w">{w}</span>' for w in H1.split())
STAR='<svg class="sp" id="sp{i}" style="{pos}" viewBox="0 0 24 24"><path d="M12 0 C13 8 16 11 24 12 C16 13 13 16 12 24 C11 16 8 13 0 12 C8 11 11 8 12 0Z" fill="{c}"/></svg>'
SPK="".join(STAR.format(i=i,pos=p,c=c) for i,(p,c) in enumerate([
 ("left:-46px;top:-30px","#FFE27A"),("right:-50px;top:-14px","#9EEBD6"),("right:-20px;bottom:-44px;width:34px;height:34px","#FFB3D1"),("left:-14px;bottom:-40px;width:30px;height:30px","#fff")]))
os.makedirs(f"{name}/assets",exist_ok=True)
for d in ("assets","sfx"):
    for f in os.listdir(d): 
        os.makedirs(f"{name}/{d}",exist_ok=True); shutil.copy(f"{d}/{f}",f"{name}/{d}/{f}")
VOL={"sub_boom":0.5,"swoosh":0.3,"riser_shimmer":0.4,"coin":0.35,"ui_tap":0.45}
ov=[];au=[];js=[]
for i,(s,e,t,side,sfx,z) in enumerate(O):
    t=t.replace("&","&amp;")
    ov.append(f'<div id="w{i}" class="clip word {side}" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{t}</span><i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.45)}"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:22}},{{opacity:1,y:0,duration:0.38,ease:"expo.out"}},{s});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s+0.08:.2f});')
    js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,y:-10,duration:0.2,ease:"power2.in"}},{e-0.22:.2f});')
    if z=="punch":
        js.append(f'tl.fromTo("#cam",{{scale:1.1}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s});')
    elif z=="in":
        js.append(f'tl.to("#cam",{{scale:1.07,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
    else:
        js.append(f'tl.to("#cam",{{scale:1.0,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Baloo2";src:url("assets/Baloo2-ExtraBold.woff2") format("woff2");font-weight:800;}}
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.word{{position:absolute;top:240px;width:420px;z-index:5;}}
.word.L{{left:170px;text-align:left;}}
.word.R{{right:170px;text-align:right;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:30px;line-height:1.3;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);opacity:0;}}
.word .bar{{display:block;height:3px;width:56px;background:#fff;border-radius:2px;margin-top:10px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}}
#title{{position:absolute;top:190px;left:40px;right:40px;text-align:center;z-index:6;}}
#title .h1{{position:relative;display:inline-block;font-family:"Baloo2",sans-serif;font-weight:800;font-size:{FS}px;line-height:1.05;color:#fff;letter-spacing:-0.01em;
  text-shadow:0 4px 14px rgba(0,0,0,.45),0 0 3px rgba(0,0,0,.3);}}
#title .h1 .w{{display:inline-block;opacity:0;margin:0 .14em;}}
#title svg.sw{{position:absolute;left:50%;bottom:-26px;width:78%;height:40px;transform:translateX(-50%);overflow:visible;}}
#title .pill{{display:inline-block;margin-top:34px;background:#fff;border-radius:999px;padding:12px 34px 8px;box-shadow:0 6px 18px rgba(0,0,0,.35);transform:scaleX(0);}}
#title .pill span{{display:inline-block;font-family:"Baloo2",sans-serif;font-weight:800;font-size:46px;line-height:1.1;color:#3a2a55;opacity:0;}}
#title .sp{{position:absolute;width:54px;height:54px;opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="title" class="clip" data-start="0" data-duration="3.5">
    <div class="h1">{H1W}<svg class="sw" viewBox="0 0 600 40" preserveAspectRatio="none"><path id="swp" d="M8 26 C 150 6, 300 34, 440 16 S 580 14, 592 20" fill="none" stroke="#FFE27A" stroke-width="9" stroke-linecap="round"/></svg>
      {SPK}
    </div><br><div class="pill"><span>{H2}</span></div>
  </div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_cork" src="sfx/cork.wav" data-start="0.12" data-duration="1.0" data-volume="0.55"></audio>
  <audio id="a_sw" src="sfx/swoosh.wav" data-start="0.78" data-duration="0.5" data-volume="0.35"></audio>
  <audio id="a_t2" src="sfx/glass_ting.wav" data-start="0.5" data-duration="0.9" data-volume="0.3"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#title .h1 .w",{{opacity:0,scale:.3,y:40,rotation:-8}},{{opacity:1,scale:1,y:0,rotation:0,duration:.5,ease:"back.out(2.2)",stagger:.09}},0.12);
tl.fromTo("#swp",{{strokeDasharray:700,strokeDashoffset:700}},{{strokeDashoffset:0,duration:.55,ease:"power2.out"}},0.55);
tl.fromTo("#title .sp",{{opacity:0,scale:0,rotation:-90}},{{opacity:1,scale:1,rotation:0,duration:.45,ease:"back.out(3)",stagger:.08}},0.5);
tl.to("#title .sp",{{rotation:45,scale:.85,duration:1.6,ease:"sine.inOut",stagger:.08}},1.0);
tl.fromTo("#title .pill",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"expo.out"}},0.8);
tl.fromTo("#title .pill span",{{opacity:0,y:12}},{{opacity:1,y:0,duration:.35,ease:"power2.out"}},0.9);
tl.fromTo("#cam",{{scale:1.1}},{{scale:1.0,duration:1.0,ease:"power3.out"}},0.12);
tl.to("#cam",{{scale:1.06,duration:2.0,ease:"sine.inOut"}},1.2);
tl.to("#title",{{opacity:0,y:-24,scale:.94,duration:.3,ease:"power2.in"}},3.12);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open(f"{name}/index.html","w").write(html)
print("built",name)
