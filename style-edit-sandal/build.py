import json
# Teks overlay: [mula, tamat, "Teks", "sfx"]  (masa ikut footage yang dah dipotong)
O=[
 [11.3,13.95,"Budget Friendly","coin"],
 [19.85,22.1,"Soft &amp; Flexible","ui_blip"],
 [22.15,23.7,"Comfortable Fit","ui_confirm"],
 [26.3,29.3,"Lightweight Design","ui_tap"],
 [31.3,32.95,"Everyday Sandals","ui_notif"],
 [33.0,34.25,"Waterproof","ui_blip"],
 [34.3,37.0,"Anti-Slip Sole","glass_ting"],
 [43.6,45.6,"Simple &amp; Stylish","ui_confirm"],
]
# B-roll full screen 4s: [mula, fail]
B=[[14.2,"broll0"],[19.85,"broll1"],[30.0,"broll3"],[43.6,"broll2"]]
PUNCH=[2.3,13.56,34.36,38.94]
VOL={"sub_boom":0.45,"coin":0.35,"ui_tap":0.4,"swoosh":0.25}
EDL=json.load(open("edl.json"))
DUR=49.7
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
    js.append(f'tl.fromTo("#b{i}",{{opacity:0}},{{opacity:1,duration:0.6,ease:"sine.inOut"}},{s});')
    js.append(f'tl.fromTo("#b{i}",{{scale:1.03}},{{scale:1.0,duration:4,ease:"none"}},{s});')
    js.append(f'tl.to("#b{i}",{{opacity:0,duration:0.6,ease:"sine.inOut"}},{s+3.4:.2f});')
js.append(f'tl.fromTo("#cam",{{scale:1.0}},{{scale:1.04,duration:{DUR},ease:"none"}},0);')
for p in PUNCH:
    js.append(f'tl.fromTo("#pz",{{scale:1.045}},{{scale:1.0,duration:0.6,ease:"power2.out"}},{p});')
    au.append(f'<audio id="p{int(p*100)}" src="sfx/sub_boom.wav" data-start="{p-0.02:.2f}" data-duration="1.1" data-volume="0.2"></audio>')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
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
#title{{position:absolute;top:240px;left:0;right:0;text-align:center;z-index:6;color:#fff;font-family:"Lexend Mega",sans-serif;font-weight:600;letter-spacing:-0.03em;line-height:1.35;
  text-shadow:0 2px 8px rgba(0,0,0,.45);}}
#title span{{display:inline-block;opacity:0;}} #t1{{font-size:22px;font-weight:500;}} #t2{{font-size:36px;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="pz"><div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div></div>
  {chr(10).join("  "+x for x in br)}
  <div id="title" class="clip" data-start="0" data-duration="3.2"><span id="t1">Rupa ala brand C,</span><br><span id="t2">harga budget!</span></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_cork" src="sfx/ui_blip.wav" data-start="0.1" data-duration="1.0" data-volume="0.35"></audio>
  <audio id="a_t2" src="sfx/glass_ting.wav" data-start="0.55" data-duration="0.9" data-volume="0.28"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#pz",{{scale:1}},0);
tl.fromTo("#t1",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.4,ease:"expo.out"}},0.1);
tl.fromTo("#t2",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},0.55);

tl.to("#title span",{{opacity:0,y:-10,duration:.25,ease:"power2.in"}},2.9);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
