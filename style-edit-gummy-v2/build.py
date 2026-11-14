# [start, end, text, side, sfx, zoom]
# [start, end, text, side, sfx, zoom, (optional) top px]
O=[
 [3.6,5.7,"Turkish Gummies","R","ui_blip","out"],
 [5.8,7.7,"Ramai Kata Sedap!","R","glass_ting","in"],
 [8.9,11.6,"Anak Dah Habis Separuh","R","ui_notif","out"],
 [12.3,14.9,"Buat Terliur","R","ui_tap","in"],
 [16.9,19.6,"Macam-Macam Ada","R","ui_blip","out"],
 [20.9,21.85,"Confirm Masam!","R","sub_boom","punch"],
 [21.9,24.9,"Anak Suka Sangat","R","glass_ting","in"],
 [28.6,30.0,"Macam-Macam Bentuk","L","ui_blip","out"],
 [30.1,31.7,"Bentuk Mangga","L","ui_tap","in"],
 [31.8,33.1,"Bentuk Gigi","L","ui_tap","out"],
 [37.3,38.8,"Ada Masam, Ada Manis","L","ui_blip","in"],
 [38.9,41.0,"Yang Penting Halal","L","ui_confirm","out"],
 [42.7,44.4,"Sedap!","L","riser_shimmer","in"],
 [46.6,48.2,"Ramai Cakap Masam","L","ui_notif","out"],
 [49.2,50.9,"Memang Masam!","L","sub_boom","punch"],
 [51.7,55.7,"Buat Ketagih","R","glass_ting","in"],
 [55.8,58.8,"Peminat Masam Wajib Try","R","ui_notif","out"],
 [58.9,60.4,"Lagi Masam Lagi Sedap","R","sub_boom","punch"],
 [60.5,62.9,"Tak Cukup Sekali","R","ui_tap","in"],
 [63.1,66.2,"Standby Masa Travel","L","swoosh","out"],
 [67.4,68.7,"1KG Puas Makan","L","coin","in"],
 [85.2,86.9,"Buat Ketagih!","L","glass_ting","in"],
 [87.1,90.1,"Siap Ada Penutup","L","ui_confirm","out",120],
 [90.2,91.8,"Free Pengepit","L","ui_tap","in",120],
 [91.9,93.7,"Mix Campur","L","ui_blip","out",120],
 [93.8,96.6,"3 Pilihan","L","ui_notif","in",120],
 [96.7,98.3,"Terus Beli 1KG","L","coin","out",120],
 [98.4,99.85,"Lebih Jimat","L","coin","in",120],
 [99.9,101.2,"Boleh Kongsi Ramai","L","ui_tap","out",120],
 [102.3,104.9,"Ambil Yang Mix","L","ui_blip","in",120],
 [105.4,107.0,"Serius Berbaloi!","L","riser_shimmer","punch",120],
 [108.6,110.8,"Banyak Lagi Tau","L","ui_tap","out"],
 [110.9,112.0,"Sangat Recommend!","L","sub_boom","punch"],
 [112.0,113.5,"Anak-Anak Suka","L","glass_ting","in"],
]
VOL={"sub_boom":0.5,"swoosh":0.3,"riser_shimmer":0.4,"coin":0.35,"ui_tap":0.45}
DUR=113.6
ov=[];au=[];js=[]
for i,(s,e,t,side,sfx,z,*rest) in enumerate(O):
    st=f' style="top:{rest[0]}px"' if rest else ''
    ov.append(f'<div id="w{i}" class="clip word {side}"{st} data-start="{s}" data-duration="{round(e-s,2)}"><span class="tx">{t}</span><i class="bar"></i></div>')
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
.word .tx{{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:800;font-size:34px;line-height:1.3;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 6px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);opacity:0;}}
.word .bar{{display:block;height:4px;width:60px;background:#fff;border-radius:2px;margin-top:10px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}}
#title{{position:absolute;top:230px;left:0;right:0;text-align:center;z-index:6;color:#fff;font-family:"Lexend Mega",sans-serif;font-weight:800;font-size:46px;line-height:1.25;letter-spacing:-0.03em;
  text-shadow:0 2px 8px rgba(0,0,0,.45);}}
#title span{{display:inline-block;opacity:0;}} #t2{{font-size:32px;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  <div id="title" class="clip" data-start="0" data-duration="3.5"><span id="t1">Turkish Gummies</span><br><span id="t2">masam tapi sedap!</span></div>
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
tl.to("#cam",{{scale:1.0,duration:0.2,ease:"sine.inOut"}},3.4);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
