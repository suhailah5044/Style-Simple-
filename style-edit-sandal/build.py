import json
# Teks overlay: [mula, tamat, "Teks", "sfx"]  (masa ikut footage yang dah dipotong)
O=[
 [5.4,7.95,"Anti-Slip Sole","glass_ting"],
 [8.2,10.6,"Comfortable Fit","ui_confirm"],
 [10.7,12.5,"Simple &amp; Stylish","ui_blip"],
 [23.31,25.7,"Budget Friendly","coin"],
]
# B-roll produk penuh skrin 4s (tiada muka): [mula, fail]
B=[[5.3,"broll0"],[10.6,"broll1"],[23.11,"broll2"]]
PUNCH=[15.84,20.3,27.21]
VOL={"sub_boom":0.45,"coin":0.35,"ui_tap":0.4,"swoosh":0.25}
EDL=json.load(open("edl.json"))
DUR=30.040000
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
.hook{{position:absolute;top:235px;left:120px;right:120px;text-align:center;z-index:6;color:#fff;font-family:"Lexend Mega",sans-serif;font-weight:700;
  font-size:46px;line-height:1.2;letter-spacing:-0.04em;text-shadow:0 2px 8px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);}}
.hook span{{display:inline-block;opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="pz"><div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div></div>
  {chr(10).join("  "+x for x in br)}
  <div id="h0" class="clip hook" data-start="0.1" data-duration="1.75"><span>RACUN SANDAL<br>HARI NI!</span></div>
  <div id="h1" class="clip hook" data-start="1.85" data-duration="1.75"><span>LOOK MAHAL,<br>HARGA BAJET!</span></div>
  <div id="h2" class="clip hook" data-start="3.6" data-duration="1.35"><span>HARGA<br>TAK SANGKA!</span></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_cork" src="sfx/ui_blip.wav" data-start="0.1" data-duration="1.0" data-volume="0.35"></audio>
  <audio id="a_t3" src="sfx/glass_ting.wav" data-start="3.58" data-duration="0.9" data-volume="0.25"></audio>
  <audio id="a_t2" src="sfx/ui_blip.wav" data-start="1.83" data-duration="0.9" data-volume="0.28"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#pz",{{scale:1}},0);
tl.fromTo("#h0 span",{{opacity:0,y:18,scale:.96}},{{opacity:1,y:0,scale:1,duration:.4,ease:"expo.out"}},0.1);
tl.to("#h0 span",{{opacity:0,y:-12,duration:.22,ease:"power2.in"}},1.61);
tl.fromTo("#h1 span",{{opacity:0,y:18,scale:.96}},{{opacity:1,y:0,scale:1,duration:.4,ease:"expo.out"}},1.85);
tl.to("#h1 span",{{opacity:0,y:-12,duration:.22,ease:"power2.in"}},3.36);
tl.fromTo("#h2 span",{{opacity:0,y:18,scale:.96}},{{opacity:1,y:0,scale:1,duration:.4,ease:"expo.out"}},3.6);
tl.to("#h2 span",{{opacity:0,y:-12,duration:.22,ease:"power2.in"}},4.71);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
