import json
# Teks overlay: [mula, tamat, "Teks", "sfx"]  (masa ikut footage yang dah dipotong)
O=[
 [6.0,7.9,"Budget Friendly","coin"],
 [19.9,22.1,"Soft &amp; Flexible","ui_blip"],
 [22.15,23.9,"Comfortable Fit","ui_confirm"],
 [25.0,27.9,"Lightweight Design","ui_tap"],
 [31.0,33.3,"Everyday Sandals","ui_notif"],
 [36.4,37.85,"Waterproof","sub_boom"],
 [37.95,41.0,"Anti-Slip Sole","glass_ting"],
 [47.6,49.2,"Simple &amp; Stylish","ui_confirm"],
]
# B-roll full screen 4s: [mula, fail]
B=[[14.0,"broll0"],[19.9,"broll1"],[31.0,"broll3"],[37.95,"broll2"]]
PUNCH=[7.34,8.35,36.8,43.05,49.2]
VOL={"sub_boom":0.45,"coin":0.35,"ui_tap":0.4,"swoosh":0.25}
EDL=json.load(open("edl.json"))
DUR=53.2
ov=[];au=[];js=[];br=[]
for i,(s,e,t,sfx) in enumerate(O):
    ov.append(f'<div id="w{i}" class="clip word" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{t}</span><i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.4)}"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:22}},{{opacity:1,y:0,duration:0.38,ease:"expo.out"}},{s});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s+0.08:.2f});')
    js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,y:-10,duration:0.2,ease:"power2.in"}},{e-0.22:.2f});')
for i,(s,f) in enumerate(B):
    br.append(f'<video id="b{i}" class="broll" src="assets/{f}.mp4" data-start="{s}" data-duration="4" muted playsinline></video>')
    au.append(f'<audio id="ab{i}" src="sfx/swoosh.wav" data-start="{s-0.1:.2f}" data-duration="1.1" data-volume="0.22"></audio>')
    js.append(f'tl.fromTo("#b{i}",{{opacity:0}},{{opacity:1,duration:0.35,ease:"sine.out"}},{s});')
    js.append(f'tl.fromTo("#b{i}",{{scale:1.06}},{{scale:1.0,duration:4,ease:"none"}},{s});')
    js.append(f'tl.to("#b{i}",{{opacity:0,duration:0.35,ease:"sine.in"}},{s+3.65:.2f});')
# zoom selang-seli setiap cut (sorok jump cut) + drift perlahan
for i,(_,a,b,t0) in enumerate(EDL):
    d=round(b-a,2); z=1.0 if i%2==0 else 1.07
    js.append(f'tl.set("#cam",{{scale:{z}}},{t0});tl.to("#cam",{{scale:{z+0.025:.3f},duration:{d},ease:"none"}},{t0});')
for p in PUNCH:
    js.append(f'tl.fromTo("#pz",{{scale:1.09}},{{scale:1.0,duration:0.45,ease:"power3.out"}},{p});')
    au.append(f'<audio id="p{int(p*100)}" src="sfx/sub_boom.wav" data-start="{p-0.02:.2f}" data-duration="1.1" data-volume="0.3"></audio>')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Italianno";src:url("assets/Italianno.woff2") format("woff2");}}
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#pz,#cam{{position:absolute;inset:0;transform-origin:50% 40%;}}
#cam video,.broll{{width:100%;height:100%;object-fit:cover;display:block;}}
.broll{{position:absolute;inset:0;z-index:3;opacity:0;}}
.word{{position:absolute;top:250px;left:0;right:0;text-align:center;z-index:5;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:30px;line-height:1.3;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);opacity:0;}}
.word .bar{{display:block;height:3px;width:56px;background:#fff;border-radius:2px;margin:10px auto 0;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
#title{{position:absolute;top:230px;left:0;right:0;text-align:center;z-index:6;color:#fff;font-family:"Italianno",cursive;font-size:78px;line-height:.95;
  text-shadow:0 2px 8px rgba(0,0,0,.45);}}
#title span{{display:inline-block;opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="pz"><div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div></div>
  {chr(10).join("  "+x for x in br)}
  <div id="title" class="clip" data-start="0" data-duration="3.2"><span id="t1">Rupa brand C,</span><br><span id="t2">harga budget!</span></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_cork" src="sfx/cork.wav" data-start="0.1" data-duration="1.0" data-volume="0.5"></audio>
  <audio id="a_t2" src="sfx/glass_ting.wav" data-start="0.55" data-duration="0.9" data-volume="0.28"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#pz",{{scale:1}},0);
tl.fromTo("#t1",{{opacity:0,scale:.6,y:10}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2.6)"}},0.1);
tl.fromTo("#t2",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},0.55);
tl.fromTo("#pz",{{scale:1.1}},{{scale:1.0,duration:0.9,ease:"power3.out"}},0.1);
tl.to("#title span",{{opacity:0,y:-10,duration:.25,ease:"power2.in"}},2.9);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
