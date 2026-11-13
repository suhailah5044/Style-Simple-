# Kemeja Cotton Umi — preview build (HyperFrames 9:16, 1080x1920)
# Footage dah dipotong oleh cut.py (hook depan, pause & ayat ulang dibuang). Warna asal, tiada filter.
# Overlay: [mula, tamat, "TEKS", "L|R", "sfx"]  — masa ikut timeline baru (lepas potong)
O=[
 [0.10,1.90,"ONE SIZE FIT","R","sub_boom"],          # hook: "didi besar pun muat tau"
 [2.00,4.40,"BAGGY GIRL ERA","L","ui_blip"],          # "siapa je yang tak suka kemeja ni"
 [12.50,14.10,"COMFY FIT CHECK","R","ui_notif"],      # "sangat-sangat selesa"
 [14.20,15.50,"LOOSE BUT STILL CUTE","L","ui_tap"],   # "loose, cantik"
 [15.60,16.90,"COTTON TOP 🤎","R","glass_ting"],      # "material dia cotton"
 [17.20,19.90,"SIMPLE BUT CLASSY","L","ui_confirm"],  # "belakang labuh, depan labuh"
 [21.10,24.40,"EASY OOTD","R","swoosh"],              # "mix dengan jeans / skirt"
 [25.40,27.10,"HALF BUTTON DETAIL","L","ui_blip"],    # "half button berkolar"
 [31.90,34.60,"BLACK TOP NEVER FAILS","R","sub_boom"],# "hitam ni lagi senang"
 [39.10,43.00,"DAILY OUTFIT APPROVED","L","riser_shimmer"], # "pergi kerja, OT, holiday"
]
# zoom punch pada setiap cut (sorok jump cut) + point penting
CUTS=[1.94,6.56,11.11,14.16,14.77,16.97,21.01,24.54,27.21,29.11,31.83,35.79,37.56,39.03,43.16]
VOL={"sub_boom":0.4,"swoosh":0.25,"riser_shimmer":0.3,"coin":0.3,"ui_tap":0.35}
DUR=44.96

def chars(t):
    out=[]
    for word in t.split(" "):
        out.append('<span class="wd">'+"".join(f'<span class="ch">{c}</span>' for c in word)+'</span>')
    return " ".join(out)

ov=[];au=[];js=[]
for i,(s,e,t,side,sfx) in enumerate(O):
    ov.append(f'<div id="w{i}" class="clip word {side}" data-start="{s}" data-duration="{round(e-s,2)}"><div class="tx">{chars(t)}</div><i class="bar"></i></div>')
    au.append(f'<audio id="a{i}" src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.35)}"></audio>')
    # kinetic type: huruf masuk satu-satu (stagger), pop kecil
    js.append(f'tl.fromTo("#w{i} .ch",{{opacity:0,y:18,scale:.6}},{{opacity:1,y:0,scale:1,duration:0.32,ease:"back.out(2.2)",stagger:0.022}},{s});')
    js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s+0.15:.2f});')
    js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,y:-10,duration:0.2,ease:"power2.in"}},{e-0.22:.2f});')
    js.append(f'tl.fromTo("#cam",{{scale:1.09}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s});')
for c in CUTS:
    if any(abs(c-o[0])<0.4 for o in O): continue
    js.append(f'tl.fromTo("#cam",{{scale:1.06}},{{scale:1.0,duration:0.4,ease:"power3.out"}},{c});')
# drift perlahan balik ke 1.0 selepas setiap punch
js.sort(key=lambda x: float(x.rsplit(",",1)[1].rstrip(");")))

html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Lexend Mega";src:url("assets/LexendMega.woff2") format("woff2");font-weight:100 900;}}
@font-face{{font-family:"Noto Color Emoji";src:url("assets/NotoColorEmoji.ttf") format("truetype");}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
/* safe zone TikTok/Reels: atas >=250px, tepi >=120px, jauh dari ikon kanan & caption bawah.
   Teks duduk atas kepala (ruang dinding kosong), tak sentuh baju. */
.word{{position:absolute;top:270px;width:400px;z-index:5;}}
.word.L{{left:130px;text-align:left;}}
.word.R{{right:130px;text-align:right;}}
.word .tx{{font-family:"Lexend Mega","Noto Color Emoji",sans-serif;font-weight:600;font-size:28px;line-height:1.35;letter-spacing:-0.03em;color:#fff;
  text-shadow:0 2px 10px rgba(0,0,0,.55),0 0 3px rgba(0,0,0,.45);}}
.wd{{display:inline-block;white-space:nowrap;}}
.ch{{display:inline-block;opacity:0;}}
.word .bar{{display:block;height:3px;width:52px;background:#fff;border-radius:2px;margin-top:10px;box-shadow:0 1px 4px rgba(0,0,0,.35);transform:scaleX(0);}}
.word.L .bar{{transform-origin:0 50%;}} .word.R .bar{{margin-left:auto;transform-origin:100% 50%;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
  {chr(10).join("  "+x for x in ov)}
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
