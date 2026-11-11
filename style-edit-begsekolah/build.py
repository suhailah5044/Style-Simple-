import json
DUR=json.load(open("cuts.json"))["dur"]
# [mula, tamat, "Teks", "L|R", sfx, zoom(in|out|punch|-), sub-line]
O=[
 [3.05,4.55,"Repeat Setiap Tahun","R","click","in",""],
 [4.66,5.50,"Tahan Lasak","R","impact","punch",""],
 [5.95,7.00,"Water Resistant","L","ding","out","Anti-Splash"],
 [7.30,8.80,"Kena Air Pun Tak Risau","R","pop","in",""],
 [10.70,11.50,"Tak Tembus Ke Dalam","L","pop","-",""],
 [12.70,15.00,"Dah 2 Tahun Pakai","R","ding","in",""],
 [17.60,18.50,"Design Bercorak","R","pop","out",""],
 [18.75,19.95,"Multiple Compartments","R","click","in","20L · Muat Laptop 16\""],
 [20.15,21.40,"Internal Compartment","R","pop","out",""],
 [22.00,23.20,"Combo Dapat Pencil Box","R","ding","in",""],
 [24.40,25.80,"Design Cantik","R","sparkle","-",""],
 [26.10,28.20,"Jahitan Kemas","R","click","punch",""],
 [29.35,30.30,"Anak Pun Suka","R","pop","in",""],
 [31.00,31.90,"Selesa Dipakai","R","ding","out",""],
 [32.35,34.40,"Strap Span Tebal","R","click","in","Adjustable Shoulder Straps"],
 [37.55,38.55,"Sekolah Rendah","R","tick_a","out",""],
 [38.60,39.60,"Sekolah Menengah","R","tick_b","-",""],
 [39.65,40.55,"Travel","R","tick_c","in",""],
 [40.70,41.65,"Highly Recommended","R","ding","punch",""],
 [42.20,44.40,"Kualiti Elok","R","pop","out",""],
 [46.30,47.50,"Sesuai Untuk Anak Lasak","R","impact","punch",""],
 [48.80,50.55,"Harga Murah!","R","cash","in",""],
 [51.80,54.20,"Warna Cantik Masih Ada","R","pop","-",""],
 [54.90,DUR,"Grab Sekarang!","R","riser","in",""],
]
FB=[7.02,23.29,50.63]                       # frame break (tukar babak)
WH=[11.45,15.22,18.53,28.27,36.75,41.65,44.62]  # whoosh di potongan babak
PIP=[["pip1",5.55,1.6,"R"],["pip2",10.05,1.5,"R"]]
VOL={"impact":0.45,"riser":0.4,"cash":0.4,"sparkle":0.35,"ding":0.32,"pop":0.45,"click":0.45}
ov=[];au=[];js=[]
for i,(s,e,tx,side,sfx,z,sub) in enumerate(O):
    sb=f'<span class="sb">{sub}</span>' if sub else ""
    ov.append(f'<div id="w{i}" class="clip word {side}" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{tx}</span>{sb}<i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.03):.2f}" data-duration="{min(1.2,round(DUR-max(0,s-0.03),2))}" data-volume="{VOL.get(sfx,0.4)}"></audio>')
    js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:14,scale:.92}},{{opacity:1,y:0,scale:1,duration:.34,ease:"back.out(2)"}},{s});')
    if sub: js.append(f'tl.fromTo("#w{i} .sb",{{opacity:0,y:8}},{{opacity:.92,y:0,duration:.3,ease:"expo.out"}},{s+0.12:.2f});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:.38,ease:"expo.out"}},{s+0.06:.2f});')
    if e<DUR-0.05: js.append(f'tl.to("#w{i} > *",{{opacity:0,y:-8,duration:.18,ease:"power2.in"}},{e-0.2:.2f});')
    if z=="punch": js.append(f'tl.fromTo("#cam",{{scale:1.12}},{{scale:1.03,duration:.45,ease:"power3.out",overwrite:"auto"}},{s});')
    elif z=="in": js.append(f'tl.to("#cam",{{scale:1.07,duration:{round(e-s,2)},ease:"sine.inOut",overwrite:"auto"}},{s});')
    elif z=="out": js.append(f'tl.to("#cam",{{scale:1.0,duration:{round(e-s,2)},ease:"sine.inOut",overwrite:"auto"}},{s});')
for k,t in enumerate(FB):
    au.append(f'<audio id="fb{k}" src="sfx/snap.wav" data-start="{t-0.16:.2f}" data-duration="0.6" data-volume="0.4"></audio>')
    js.append(f'tl.to("#fb",{{scale:.86,rotation:{(-1.6,1.4,-1.2)[k]},borderRadius:40,duration:.16,ease:"power2.in"}},{t-0.16:.2f});')
    js.append(f'tl.to("#fb",{{scale:1,rotation:0,borderRadius:0,duration:.42,ease:"back.out(1.6)"}},{t:.2f});')
    ir=",immediateRender:false"; js.append(f'tl.fromTo("#crk",{{opacity:.85}},{{opacity:0,duration:.28,ease:"power2.out"{ir}}},{t:.2f});')
for k,t in enumerate(WH):
    au.append(f'<audio id="wh{k}" src="sfx/whoosh.wav" data-start="{t-0.2:.2f}" data-duration="0.5" data-volume="0.22"></audio>')
pip=[]
for k,(n,s,d,side) in enumerate(PIP):
    pip.append(f'<div id="p{k}" class="pip {side}"><video id="pv{k}" src="assets/{n}.mp4" data-start="{s}" data-duration="{d}" data-has-audio="false" muted></video></div>')
    au.append(f'<audio id="ps{k}" src="sfx/swipe.wav" data-start="{s:.2f}" data-duration="0.4" data-volume="0.3"></audio>')
    js.append(f'tl.fromTo("#p{k}",{{opacity:0,x:{60 if side=="R" else -60},scale:.85,rotation:{4 if side=="R" else -4}}},{{opacity:1,x:0,scale:1,rotation:{2 if side=="R" else -2},duration:.4,ease:"back.out(1.8)"}},{s});')
    js.append(f'tl.to("#p{k}",{{opacity:0,scale:.9,duration:.2,ease:"power2.in"}},{s+d-0.22:.2f});')
NL=chr(10)
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#0b0f1a;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;
  background:radial-gradient(120% 70% at 50% 35%,#24304d 0%,#0e1424 55%,#070a12 100%);}}
#grid{{position:absolute;inset:0;opacity:.18;background-image:linear-gradient(rgba(255,255,255,.12) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.12) 1px,transparent 1px);background-size:72px 72px;}}
#fb{{position:absolute;inset:0;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 0 4px rgba(255,255,255,.9);}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
#crk{{position:absolute;inset:0;z-index:4;opacity:0;pointer-events:none;
  background:linear-gradient(112deg,transparent 47.6%,rgba(255,255,255,.95) 47.8%,transparent 48.1%),linear-gradient(68deg,transparent 61%,rgba(255,255,255,.7) 61.15%,transparent 61.4%);}}
.word{{position:absolute;top:225px;width:470px;z-index:5;}}
.word.L{{left:120px;text-align:left;}} .word.R{{right:120px;text-align:right;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:28px;line-height:1.3;letter-spacing:-0.04em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.35);opacity:0;}}
.word .sb{{display:block;margin-top:6px;font-family:"Lexend Mega",sans-serif;font-weight:400;font-size:16px;letter-spacing:-0.03em;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.55);opacity:0;}}
.word .bar{{display:block;height:3px;width:46px;background:#fff;border-radius:2px;margin-top:9px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}}
#hook{{position:absolute;top:200px;left:0;right:0;text-align:center;z-index:6;}}
#hook .pill{{display:inline-block;padding:16px 30px 18px;border-radius:999px;background:rgba(10,14,24,.34);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
  border:1.5px solid rgba(255,255,255,.35);box-shadow:0 10px 30px rgba(0,0,0,.25);opacity:0;}}
#hook .hw{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:700;font-size:34px;letter-spacing:-0.05em;color:#fff;margin:0 6px;opacity:0;text-shadow:0 2px 6px rgba(0,0,0,.35);}}
.pip{{position:absolute;top:400px;width:300px;height:375px;border-radius:26px;overflow:hidden;z-index:5;border:4px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.45);opacity:0;}}
.pip.R{{right:70px;}} .pip.L{{left:70px;}}
.pip video{{width:100%;height:100%;object-fit:cover;display:block;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="grid"></div>
  <div id="fb"><div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div><div id="crk"></div></div>
  <div id="hook" class="clip" data-start="0" data-duration="3.0"><span class="pill"><span class="hw">Beg</span><span class="hw">Sekolah</span><span class="hw">Tahan</span><span class="hw">Lasak</span></span></div>
  {(NL+"  ").join(pip)}
  {(NL+"  ").join(ov)}
  <audio id="a_hook" src="sfx/hook.wav" data-start="0" data-duration="1.4" data-volume="0.5"></audio>
  <audio id="a_hp" src="sfx/pop.wav" data-start="0.62" data-duration="0.2" data-volume="0.3"></audio>
  {(NL+"  ").join(au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#cam",{{scale:1.14}},{{scale:1.02,duration:.9,ease:"power3.out"}},0.3);
tl.to("#cam",{{scale:1.07,duration:2.0,ease:"sine.inOut"}},1.2);
tl.fromTo("#hook .pill",{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.45,ease:"back.out(2.2)"}},0.3);
tl.fromTo("#hook .hw",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.32,ease:"expo.out",stagger:.12}},0.42);
tl.to("#hook .pill",{{opacity:0,y:-10,duration:.22,ease:"power2.in"}},2.78);
tl.to("#cam",{{scale:1.0,duration:.6,ease:"sine.inOut"}},3.0);
{NL.join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
print("ok",DUR,len(O),"overlays")
