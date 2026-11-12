import json
J=json.load(open("cuts.json")); DUR=J["dur"]; CUTS=J["cuts"]
def T(src):   # masa sumber (saat aku sebut) -> masa output
    for s,e,o,l in CUTS:
        if s-0.05<=src<=e+0.05: return round(o+(src-s)/1.1,2)
    raise SystemExit(f"src {src} tiada dalam potongan")
# [src mula, tempoh, "Tajuk", "sub", "L|R", sfx, zoom]
OS=[
 [45.85,2.6,"USB Charging Port","Tak Payah Pegang Powerbank Dah","L","impact","punch"],
 [54.45,2.4,"Waterproof Material","Tahan Percikan Air","R","ding","punch"],
 [0.60,2.4,"Backpack + Luggage","Luar Backpack, Dalam Macam Luggage","L","pop","in"],
 [3.80,2.0,"Ruang Dalam Luas","Muat Baju 3–4 Hari","L","click","out"],
 [10.35,2.2,"Expandable Design","Barang Sikit Slim, Barang Banyak Expand","L","ding","punch"],
 [36.10,2.0,"3 Zip Utama","Banyak Ruang Simpanan","L","pop","out"],
 [19.20,1.6,"Multiple Compartments","Barang Mudah Asingkan","L","click","in"],
 [21.55,2.3,"Tali Pengikat Dalam","Baju Kekal Kemas & Secure","L","click","out"],
 [92.60,1.8,"Laptop Compartment","Sesuai Untuk Outstation","L","ding","punch"],
 [83.25,2.4,"Hidden Back Compartment","Letak Passport, Wallet & Phone","L","click","in"],
 [99.30,0.85,"Front Compartment","Poket Pen & Tempat Letak Kunci","L","pop","in"],
 [70.20,1.6,"3-in-1 Carrying Style","Backpack | Hand Carry | Luggage Style","L","click","in"],
 [73.40,1.9,"Thick Padded Shoulder","Span Bahu Tebal & Selesa","L","pop","out"],
 [65.85,1.5,"Travel Friendly","Sesuai Untuk Flight & Road Trip","L","sparkle","out"],
 [102.70,9.0,"Spacious & Practical","Besar, Banyak Ruang & Berbaloi","L","riser","in"],
]
O=[]
for s,d,tx,sub,side,sfx,z in OS:
    a=T(s); O.append([a,round(min(a+d,DUR),2),tx,side,sfx,z,sub])
O.sort()
FACT=[T(28.45),"16 cm","24 cm"]             # pop-up fakta
BR=[["b1",T(49.0),2.4],["b2",T(36.9),2.4],["b3",T(57.4),2.2]]   # b-roll full screen
FB=[T(53.65),T(89.5)]                         # frame break
WH=[o for s,e,o,l in CUTS[1:]]
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
    js.append(f'tl.to("#fb",{{scale:.86,rotation:{(-1.6,1.4)[k]},borderRadius:40,duration:.16,ease:"power2.in"}},{t-0.16:.2f});')
    js.append(f'tl.to("#fb",{{scale:1,rotation:0,borderRadius:0,duration:.42,ease:"back.out(1.6)"}},{t:.2f});')
    ir=",immediateRender:false"; js.append(f'tl.fromTo("#crk",{{opacity:.85}},{{opacity:0,duration:.28,ease:"power2.out"{ir}}},{t:.2f});')
for k,t in enumerate(WH):
    au.append(f'<audio id="wh{k}" src="sfx/whoosh.wav" data-start="{t-0.2:.2f}" data-duration="0.5" data-volume="0.22"></audio>')
pip=[]
for k,(n,s,d) in enumerate(BR):
    pip.append(f'<div id="br{k}" class="br"><video id="bv{k}" src="assets/{n}.mp4" data-start="{s}" data-duration="{d}" data-has-audio="false" muted></video></div>')
    js.append(f'tl.fromTo("#br{k}",{{opacity:0}},{{opacity:1,duration:.35,ease:"sine.out"}},{s});')
    js.append(f'tl.to("#br{k}",{{opacity:0,duration:.4,ease:"sine.in"}},{s+d-0.4:.2f});')
fs=FACT[0]
pip.append(f'<div id="fact" class="clip" data-start="{fs}" data-duration="2.2"><span class="fp"><b class="fa">{FACT[1]}</b><i class="ar">→</i><b class="fb2">{FACT[2]}</b></span></div>')
au.append(f'<audio id="fs1" src="sfx/tick_a.wav" data-start="{fs:.2f}" data-duration="0.3" data-volume="0.35"></audio>')
au.append(f'<audio id="fs2" src="sfx/tick_c.wav" data-start="{fs+0.9:.2f}" data-duration="0.3" data-volume="0.35"></audio>')
js.append(f'tl.fromTo("#fact .fp",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2.4)"}},{fs});')
js.append(f'tl.fromTo("#fact .fa",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.3}},{fs+0.1:.2f});')
js.append(f'tl.fromTo("#fact .ar",{{opacity:0,x:-10}},{{opacity:1,x:0,duration:.3}},{fs+0.6:.2f});')
js.append(f'tl.fromTo("#fact .fb2",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2)"}},{fs+0.9:.2f});')
js.append(f'tl.fromTo("#cam",{{scale:1.12}},{{scale:1.03,duration:.45,ease:"power3.out",overwrite:"auto"}},{fs+0.9:.2f});')
js.append(f'tl.to("#fact .fp",{{opacity:0,y:-8,duration:.2}},{fs+2.0:.2f});')
for k,(n,s,d,side) in enumerate([]):
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
.word{{position:absolute;top:255px;width:400px;z-index:5;}}
.word.L{{left:80px;text-align:left;}} .word.R{{right:150px;text-align:right;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:24px;line-height:1.3;letter-spacing:-0.04em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.35);opacity:0;}}
.word .sb{{display:block;margin-top:6px;font-family:"Lexend Mega",sans-serif;font-weight:400;font-size:15px;letter-spacing:-0.03em;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.55);opacity:0;}}
.word .bar{{display:block;height:3px;width:46px;background:#fff;border-radius:2px;margin-top:9px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}}
#hook{{position:absolute;top:255px;left:80px;text-align:left;z-index:6;}}
#hook .pill{{display:inline-block;padding:14px 28px 16px;border-radius:34px;line-height:1.35;background:rgba(10,14,24,.34);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
  border:1.5px solid rgba(255,255,255,.35);box-shadow:0 10px 30px rgba(0,0,0,.25);opacity:0;}}
#hook .hw{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:700;font-size:26px;letter-spacing:-0.05em;color:#fff;margin:0 5px;opacity:0;text-shadow:0 2px 6px rgba(0,0,0,.35);}}
.br{{position:absolute;inset:0;z-index:3;opacity:0;}} .br video{{width:100%;height:100%;object-fit:cover;display:block;}}
#fact{{position:absolute;top:255px;left:80px;z-index:6;}}
#fact .fp{{display:inline-flex;align-items:center;gap:12px;padding:12px 22px;border-radius:999px;background:rgba(10,14,24,.34);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1.5px solid rgba(255,255,255,.35);opacity:0;}}
#fact b,#fact i{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-style:normal;font-weight:700;font-size:26px;letter-spacing:-0.05em;color:#fff;}}
.pip{{position:absolute;top:400px;width:300px;height:375px;border-radius:26px;overflow:hidden;z-index:5;border:4px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.45);opacity:0;}}
.pip.R{{right:70px;}} .pip.L{{left:70px;}}
.pip video{{width:100%;height:100%;object-fit:cover;display:block;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="grid"></div>
  <div id="fb"><div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div><div id="crk"></div></div>
  <div id="hook" class="clip" data-start="0" data-duration="2.05"><span class="pill"><span class="hw">Backpack</span><span class="hw">Ni</span><br><span class="hw">Ada</span><span class="hw">USB</span><span class="hw">Port?!</span></span></div>
  {(NL+"  ").join(pip)}
  {(NL+"  ").join(ov)}
  <audio id="music" src="sfx/music.wav" data-start="0" data-duration="{DUR}" data-volume="0.09"></audio>
  <audio id="a_hook" src="sfx/hook.wav" data-start="0" data-duration="1.4" data-volume="0.5"></audio>
  <audio id="a_hp" src="sfx/pop.wav" data-start="0.62" data-duration="0.2" data-volume="0.3"></audio>
  {(NL+"  ").join(au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#cam",{{scale:1.14}},{{scale:1.02,duration:.9,ease:"power3.out"}},0.3);
tl.to("#cam",{{scale:1.05,duration:0.8,ease:"sine.inOut"}},1.2);
tl.fromTo("#hook .pill",{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.45,ease:"back.out(2.2)"}},0.3);
tl.fromTo("#hook .hw",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.32,ease:"expo.out",stagger:.12}},0.42);
tl.to("#hook .pill",{{opacity:0,y:-10,duration:.22,ease:"power2.in"}},1.82);

{NL.join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
print("ok",DUR,len(O),"overlays")
