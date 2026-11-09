# [start, end, text, side, sfx, zoom]
O=[
 [5.15,8.3,"Jenis Pengepit","R","ui_blip","out"],
 [8.4,11.9,"Ada 2 Jenis","R","ui_notif","in"],
 [12.2,15.2,"Pemberat Super Berat","R","sub_boom","punch"],
 [15.3,16.6,"Takkan Mudah Jatuh","R","ui_tap","out"],
 [16.7,18.8,"Memang Solid!","R","sub_boom","punch"],
 [18.9,20.0,"Boleh Tinggikan","R","swoosh","in"],
 [20.05,21.9,"Atau Rendahkan","R","swoosh","out"],
 [22.2,24.9,"Anti Slip","L","glass_ting","in"],
 [25.0,26.7,"Tak Bergerak","L","sub_boom","punch"],
 [26.85,29.8,"Bawah RM20!","L","coin","in"],
 [29.9,31.3,"Betul Betul Solid","L","sub_boom","punch"],
 [31.4,33.6,"Black & White","L","ui_confirm","out"],
 [33.7,35.3,"Worth It!","L","riser_shimmer","in"],
 [35.4,38.0,"Tengok Bakul Kuning","L","ui_notif","out"],
 [38.1,40.4,"Jenis Pengepit","L","ui_blip","in"],
 [40.45,41.6,"Letak Dalam Kereta","L","ui_tap","out"],
 [41.65,43.1,"Lebih Secure","L","ui_confirm","in"],
 [43.15,45.5,"Worth It Untuk Grab!","L","riser_shimmer","out"],
 [45.6,46.85,"Solid & Berkualiti","L","sub_boom","punch"],
 [46.9,48.0,"Harga Serius Murah!","L","coin","in"],
 [48.1,49.6,"Senang Bawa <span style=\"white-space:nowrap\">Mana-Mana</span>","L","glass_ting","out"],
]
VOL={"sub_boom":0.5,"swoosh":0.3,"riser_shimmer":0.4,"coin":0.35,"ui_tap":0.45}
DUR=49.6
ov=[];au=[];js=[]
for i,(s,e,t,side,sfx,z) in enumerate(O):
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
@font-face{{font-family:"Italianno";src:url("assets/Italianno.woff2") format("woff2");}}
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
#title{{position:absolute;top:230px;left:0;right:0;text-align:center;z-index:6;color:#fff;font-family:"Italianno",cursive;font-size:78px;line-height:.95;
  text-shadow:0 2px 8px rgba(0,0,0,.45);}}
#title span{{display:inline-block;opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="title" class="clip" data-start="0" data-duration="3.5"><span id="t1">Content creator</span><br><span id="t2">wajib ada benda ni!</span></div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_cork" src="sfx/cork.wav" data-start="0.15" data-duration="1.0" data-volume="0.55"></audio>
  <audio id="a_t2" src="sfx/glass_ting.wav" data-start="0.6" data-duration="0.9" data-volume="0.3"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#t1",{{opacity:0,scale:.6,y:10}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2.6)"}},0.15);
tl.fromTo("#t2",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},0.6);
tl.fromTo("#cam",{{scale:1.1}},{{scale:1.0,duration:1.0,ease:"power3.out"}},0.15);
tl.to("#cam",{{scale:1.06,duration:2.2,ease:"sine.inOut"}},1.2);
tl.to("#title span",{{opacity:0,y:-10,duration:.25,ease:"power2.in"}},3.2);
tl.to("#cam",{{scale:1.0,duration:1.6,ease:"sine.inOut"}},3.4);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
