# Teks: [mula, tamat, "teks", sfx, zoom]  (masa dalam footage yang dah dipotong)
O=[
 [3.9,5.5,"Gummy Turkey","ui_blip","in"],
 [5.6,6.75,"Ramai Kata Sedap","ui_notif","out"],
 [8.2,9.6,"Confirm Masam!","sub_boom","punch"],
 [9.85,13.55,"Macam-Macam Bentuk","glass_ting",None],
 [17.3,19.1,"Confirm Ketagih!","sub_boom","punch"],
 [20.2,22.9,"Lagi Masam Lagi Sedap","ui_confirm","in"],
 [24.3,26.85,"Wajib Bawa Travel","swoosh","out"],
 [27.3,28.65,"1KG Puas Makan","sub_boom","punch"],
 [30.0,33.7,"Siap Penutup & Pengepit","ui_tap",None],
 [34.5,37.55,"Mix · 3 Pilihan","ui_notif","in"],
 [38.45,41.55,"1KG Lebih Jimat","coin",None],
 [41.95,43.45,"Sangat Recommend!","riser_shimmer","punch"],
]
BR=[["A",9.69],["B",29.85],["D",38.25]]   # B-roll 4s penuh skrin, produk sahaja
HALAL=[14.8,17.1]
VOL={"sub_boom":0.45,"swoosh":0.3,"riser_shimmer":0.38,"coin":0.35,"ui_tap":0.45,"glass_ting":0.35}
DUR=43.54
def words(t): return " ".join(f'<span class="k">{w}</span>' for w in t.split(" "))
ov=[];au=[];js=[];br=[]
for n,s in BR:
    br.append(f'<div id="br{n}" class="broll"><video id="vbr{n}" src="assets/broll{n}.mp4" data-start="{s}" data-duration="4" muted></video></div>')
    js.append(f'tl.fromTo("#br{n}",{{opacity:0}},{{opacity:1,duration:0.35,ease:"sine.out"}},{s});')
    js.append(f'tl.fromTo("#br{n} video",{{scale:1.0}},{{scale:1.02,duration:4,ease:"none"}},{s});')
    js.append(f'tl.to("#br{n}",{{opacity:0,duration:0.35,ease:"sine.in"}},{s+3.65:.2f});')
for i,(s,e,t,sfx,z) in enumerate(O):
    ov.append(f'<div id="w{i}" class="clip word" data-start="{s}" data-duration="{round(e-s,2)}"><div class="tx">{words(t)}</div><i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.42)}"></audio>')
    js.append(f'tl.fromTo("#w{i} .k",{{opacity:0,y:26,scale:.7}},{{opacity:1,y:0,scale:1,duration:0.34,ease:"back.out(2.2)",stagger:0.07}},{s});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s+0.12:.2f});')
    js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,y:-10,duration:0.2,ease:"power2.in"}},{e-0.22:.2f});')
    if z=="punch": js.append(f'tl.fromTo("#cam",{{scale:1.035}},{{scale:1.0,duration:0.5,ease:"power2.out"}},{s});')
    elif z=="in": js.append(f'tl.to("#cam",{{scale:1.02,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
    elif z=="out": js.append(f'tl.to("#cam",{{scale:1.0,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.broll{{position:absolute;inset:0;z-index:3;opacity:0;overflow:hidden;}}
.broll video{{width:100%;height:100%;object-fit:cover;display:block;}}
/* safe zone TikTok/Reels: atas 220px, kanan 140px, bawah 420px */
.word{{position:absolute;top:250px;left:170px;right:170px;text-align:center;z-index:5;}}
.word .tx{{font-family:"Lexend Mega",sans-serif;font-weight:600;font-size:32px;line-height:1.3;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);}}
.word .k{{display:inline-block;opacity:0;}}
.word .bar{{display:block;height:3px;width:56px;margin:10px auto 0;background:#fff;border-radius:2px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
#title{{position:absolute;top:240px;left:150px;right:150px;text-align:center;z-index:6;color:#fff;font-family:"Lexend Mega",sans-serif;font-weight:700;letter-spacing:-0.04em;text-shadow:0 2px 8px rgba(0,0,0,.45);}}
#title .l1{{font-size:26px;font-weight:500;}} #title .l2{{font-size:44px;line-height:1.15;margin-top:6px;}}
#title .k{{display:inline-block;opacity:0;}}
#halal{{position:absolute;top:240px;right:150px;width:96px;height:96px;z-index:6;opacity:0;filter:drop-shadow(0 2px 5px rgba(0,0,0,.45));}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  {chr(10).join("  "+x for x in br)}
  <div id="title" class="clip" data-start="0" data-duration="3.2"><div class="l1">{words("Suka benda masam?")}</div><div class="l2">{words("Kena try ni!")}</div></div>
  <img id="halal" class="clip" src="assets/halal.svg" data-start="{HALAL[0]}" data-duration="{round(HALAL[1]-HALAL[0],2)}">
  <div id="w_h" class="clip word" data-start="{HALAL[0]}" data-duration="{round(HALAL[1]-HALAL[0],2)}"><div class="tx">{words("Yang Penting Halal")}</div><i class="bar"></i></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="ai1" src="sfx/riser_shimmer.wav" data-start="0.05" data-duration="1.0" data-volume="0.3"></audio>
  <audio id="ai2" src="sfx/sub_boom.wav" data-start="1.3" data-duration="1.0" data-volume="0.4"></audio>
  <audio id="ai3" src="sfx/ui_confirm.wav" data-start="{HALAL[0]-0.02:.2f}" data-duration="1.0" data-volume="0.42"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#title .l1 .k",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.35,ease:"expo.out",stagger:.08}},0.1);
tl.fromTo("#title .l2 .k",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2.8)",stagger:.1}},1.3);
tl.fromTo("#cam",{{scale:1.035}},{{scale:1.0,duration:.5,ease:"power2.out"}},1.3);
tl.to("#title .k",{{opacity:0,y:-10,duration:.22,ease:"power2.in"}},2.95);
tl.to("#cam",{{scale:1.0,duration:.8,ease:"sine.inOut"}},3.1);
tl.fromTo("#halal",{{opacity:0,scale:.3,rotate:-25}},{{opacity:1,scale:1,rotate:0,duration:.45,ease:"back.out(2.4)"}},{HALAL[0]});
tl.to("#halal",{{opacity:0,scale:.8,duration:.22}},{HALAL[1]-0.22:.2f});
tl.fromTo("#w_h .k",{{opacity:0,y:26,scale:.7}},{{opacity:1,y:0,scale:1,duration:.34,ease:"back.out(2.2)",stagger:.07}},{HALAL[0]+0.1});
tl.fromTo("#w_h .bar",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"expo.out"}},{HALAL[0]+0.2});
tl.to("#w_h .tx,#w_h .bar",{{opacity:0,y:-10,duration:.2}},{HALAL[1]-0.22:.2f});
tl.fromTo("#cam",{{scale:1.035}},{{scale:1.0,duration:.5,ease:"power2.out"}},{HALAL[0]});
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
