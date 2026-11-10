# Komposisi HyperFrames: Sabun Basuh Baju. Footage asal (tiada filter/warna diubah).
import json
E=json.load(open("edl.json")); DUR=E["dur"]; SP=E["speed"]
CUTS=[round(t,3) for a,b,t in E["edl"]]           # masa mula setiap segmen (output)
# [mula, tamat, teks, sfx, gaya]  gaya: "" biasa | "pill" (hook, ada bg)
O=[
 [0.05,2.70,"Baju Takkan Bau Hapak!","hook_hit","pill"],
 [4.12,4.95,"Paling Wangi","bell_ding",""],
 [5.20,7.95,"Dah Berkali-kali Repeat","soft_click",""],
 [10.40,11.80,"Wangi Semerbak","sparkle_rise",""],
 [12.40,14.90,"Sesuai Sidai Lambat","soft_click",""],
 [16.42,18.10,"Basuh Waktu Malam","bubble_pop",""],
 [18.26,20.20,"Kena Cuba!","bubble_pop","pill"],
 [20.60,22.45,"Wangi Melekat","sparkle_rise",""],
 [23.90,25.00,"Floral Perfume","bell_ding",""],
 [26.50,29.15,"Tadah &amp; Pam Je","soft_click",""],
 [29.25,30.90,"Tak Perlu Angkat Berat","air_whoosh",""],
 [31.05,32.65,"5 Liter","soft_impact","pill"],
 [32.83,34.80,"Harga Sangat Murah!","cash_ting","pill"],
 [37.23,39.30,"Hilang Bau Kepam","bubble_pop",""],
 [39.60,DUR-0.05,"Memang Recommend!","sparkle_rise",""],
]
# digital zoom: setiap potongan + titik tambahan dalam take panjang. h=1.0 z=1.08 p=push k=punch
ZPTS=sorted([(c,l) for c,l in zip(CUTS,"kzhpzhpzpzk")]+[(31.05,"k"),(32.83,"z"),(37.2,"h")])
FB={CUTS[3],CUTS[5],CUTS[7],CUTS[9]}   # frame break pada potongan ini
VOL={"soft_impact":0.5,"hook_hit":0.55,"air_whoosh":0.28,"sparkle_rise":0.3,"bell_ding":0.28,"cash_ting":0.32,"soft_click":0.4,"bubble_pop":0.38}
ov=[];au=[];js=[]
for i,(s,e,t,sfx,st) in enumerate(O):
    ov.append(f'<div id="w{i}" class="clip word {st}" data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{t}</span></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.03):.2f}" data-duration="1.1" data-volume="{VOL[sfx]}"></audio>')
    if st=="pill":
        js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,scale:.6,y:8}},{{opacity:1,scale:1,y:0,duration:.42,ease:"back.out(2.2)"}},{s});')
    else:
        js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:18,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.36,ease:"expo.out"}},{s});')
    js.append(f'tl.to("#w{i} .tx",{{opacity:0,y:-8,duration:.18,ease:"power2.in"}},{e-0.2:.2f});')
for k,(c,z) in enumerate(ZPTS):
    nxt=ZPTS[k+1][0] if k+1<len(ZPTS) else DUR; d=round(nxt-c,3)
    if z=="h": js.append(f'tl.set("#cam",{{scale:1}},{c});')
    elif z=="z": js.append(f'tl.set("#cam",{{scale:1.08}},{c});')
    elif z=="p": js.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.05,duration:{d-.04:.3f},ease:"none",immediateRender:false}},{c});')
    else: js.append(f'tl.fromTo("#cam",{{scale:1.12}},{{scale:1.03,duration:.5,ease:"power3.out",immediateRender:false}},{c});tl.to("#cam",{{scale:1.0,duration:{max(.1,d-.56):.2f},ease:"sine.inOut"}},{c+.5:.2f});')
    if c in FB:
        js.append(f'tl.fromTo("#fb",{{x:-34,rotation:-.6,skewX:-3}},{{x:0,rotation:0,skewX:0,duration:.26,ease:"power3.out",immediateRender:false}},{c});')
        js.append(f'tl.fromTo("#fbl",{{opacity:.9,scaleY:1}},{{opacity:0,scaleY:.2,duration:.16,ease:"power2.out",immediateRender:false}},{c});')
        au.append(f'<audio id="fbs{k}" src="sfx/air_whoosh.wav" data-start="{max(0,c-0.12):.2f}" data-duration="0.6" data-volume="0.22"></audio>')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#fb{{position:absolute;inset:0;}}
#cam{{position:absolute;inset:0;transform-origin:50% 42%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
#fbl{{position:absolute;left:0;right:0;top:46%;height:6px;background:#fff;opacity:0;z-index:4;mix-blend-mode:overlay;}}
.word{{position:absolute;top:300px;left:90px;right:90px;text-align:center;z-index:5;}}
.word .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:30px;line-height:1.3;letter-spacing:-0.035em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.5),0 0 2px rgba(0,0,0,.35);opacity:0;}}
.word.pill .tx{{font-size:32px;padding:14px 26px;border-radius:999px;background:rgba(20,20,22,.42);
  -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);border:1.5px solid rgba(255,255,255,.55);text-shadow:none;
  box-shadow:0 6px 18px rgba(0,0,0,.18);}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="fb"><div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div></div>
  <div id="fbl"></div>
  {chr(10).join("  "+x for x in ov)}
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);tl.set("#fb",{{x:0,rotation:0,skewX:0}},0);tl.set("#fbl",{{opacity:0}},0);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
print("ok",DUR,len(CUTS))
