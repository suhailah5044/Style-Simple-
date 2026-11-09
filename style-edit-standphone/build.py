# [start, end, text, side, sfx, zoom]
O=[
 [3.6, 5.1,"Wajib Ada!","R","tingting","in"],
 [5.15,8.3,"Jenis Pengepit","R","pop","out"],
 [8.4,11.9,"Ada 2 Jenis","R","ting","in"],
 [12.2,15.2,"Pemberat Super Berat","R","impact","punch"],
 [15.3,16.6,"Takkan Mudah Jatuh","R","pop","out"],
 [16.7,18.8,"Memang Solid!","R","impact","punch"],
 [18.9,20.0,"Boleh Tinggikan","R","whoosh","in"],
 [20.05,21.9,"Atau Rendahkan","R","whoosh","out"],
 [22.2,24.9,"Anti Slip","L","tingting","in"],
 [25.0,26.7,"Tak Bergerak","L","impact","punch"],
 [26.85,29.8,"Bawah RM20!","L","kaching","in"],
 [29.9,31.3,"Betul Betul Solid","L","impact","punch"],
 [31.4,33.6,"Black dan White","L","ting","out"],
 [33.7,35.3,"Worth It!","L","sparkle","in"],
 [35.4,38.0,"Tengok Bakul Kuning","L","tingting","out"],
 [38.1,40.4,"Jenis Pengepit","L","pop","in"],
 [40.45,41.6,"Letak Dalam Kereta","L","pop","out"],
 [41.65,43.1,"Lebih Secure","L","ting","in"],
 [43.15,45.5,"Worth It Untuk Grab!","L","sparkle","out"],
 [45.6,46.85,"Solid dan Berkualiti","L","impact","punch"],
 [46.9,48.0,"Harga Serius Murah!","L","kaching","in"],
 [48.1,49.6,"Senang Bawa Mana Mana","L","tingting","out"],
]
DUR=49.6
ov=[];au=[];js=[]
for i,(s,e,t,side,sfx,z) in enumerate(O):
    ov.append(f'<div id="w{i}" class="clip word {side}" data-start="{s}" data-duration="{round(e-s,2)}"><span>{t}</span></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.03):.2f}" data-duration="1.2" data-volume="{0.35 if sfx in ("impact","whoosh") else 0.45}"></audio>')
    js.append(f'tl.fromTo("#w{i} span",{{opacity:0,scale:0.55,y:14}},{{opacity:1,scale:1,y:0,duration:0.32,ease:"back.out(2.4)"}},{s});')
    js.append(f'tl.to("#w{i} span",{{opacity:0,scale:0.9,duration:0.18,ease:"power2.in"}},{e-0.2:.2f});')
    if z=="punch":
        js.append(f'tl.fromTo("#cam",{{scale:1.12}},{{scale:1.03,duration:0.5,ease:"power3.out"}},{s});')
    elif z=="in":
        js.append(f'tl.to("#cam",{{scale:1.08,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
    else:
        js.append(f'tl.to("#cam",{{scale:1.0,duration:{round(e-s,2)},ease:"sine.inOut"}},{s});')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Cweyons";src:url("assets/Cweyons-Regular.ttf") format("truetype");}}
@font-face{{font-family:"FredokaD";src:url("assets/Fredoka.woff2") format("woff2");font-weight:600;}}
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.word{{position:absolute;top:235px;width:400px;z-index:5;}}
.word.L{{left:170px;text-align:left;}}
.word.R{{right:170px;text-align:right;}}
.word span{{display:inline-block;font-family:"Cweyons","FredokaD",sans-serif;font-size:56px;line-height:1.05;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.35);transform-origin:50% 60%;opacity:0;}}
.word.L span{{transform-origin:0% 60%;}} .word.R span{{transform-origin:100% 60%;}}
#title{{position:absolute;top:255px;left:0;right:0;text-align:center;z-index:6;color:#fff;font-family:"Lexend Mega",sans-serif;
  text-shadow:0 2px 6px rgba(0,0,0,.45);}}
#title .k{{display:block;font-size:20px;font-weight:600;letter-spacing:.06em;opacity:.95;margin-bottom:10px;}}
#title .t1,#title .t2{{display:block;font-weight:700;font-size:34px;line-height:1.25;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="title" class="clip" data-start="0" data-duration="3.1">
    <span class="k">STAND PHONE</span><span class="t1">Stand Phone Holder</span><span class="t2">Murah Padu</span>
  </div>
  {chr(10).join("  "+x for x in ov)}
  <audio id="a_in" src="sfx/whoosh.wav" data-start="0" data-duration="0.5" data-volume="0.3"></audio>
  <audio id="a_in2" src="sfx/tingting.wav" data-start="0.35" data-duration="1.2" data-volume="0.45"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#title .k",{{opacity:0,y:-12}},{{opacity:.95,y:0,duration:.35,ease:"power2.out"}},0.05);
tl.fromTo("#title .t1",{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2.2)"}},0.25);
tl.fromTo("#title .t2",{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2.2)"}},0.45);
tl.fromTo("#cam",{{scale:1.12}},{{scale:1.0,duration:1.2,ease:"power3.out"}},0);
tl.to("#cam",{{scale:1.06,duration:1.8,ease:"sine.inOut"}},1.2);
tl.to("#title",{{opacity:0,duration:.25}},2.85);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
