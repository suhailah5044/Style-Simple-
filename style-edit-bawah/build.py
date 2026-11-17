# Style Bawah v2 — tiru penuh video rujukan:
#  - Tajuk KUNING besar tulisan tangan (melengkung/condong), muncul huruf demi huruf + bunyi "scribble"
#  - Perkataan PUTIH kecil condong di sisi kepala + "pop"
#  - Kapsyen putih kecil frasa demi frasa (diletak ATAS supaya tak tutup baju)
#  - Potongan zoom (dekat/jauh) + transisi blur + whoosh
#  - Muzik latar lofi perlahan, penutup gelap + boom
import json
FOOT=59.73          # panjang footage
END=2.9             # panjang penutup gelap
DUR=round(FOOT+END,2)

# ---------- KUMPULAN TAJUK (hook + penekanan) ----------
# item: [masa, "y"|"w", teks, x, y, rotate, saiz, arc]
G=[
 dict(s=0.0,e=1.46,items=[
   [0.0,"w","jangan jadi",205,330,-28,46,0],
   [0.48,"w","macam",880,330,16,46,0],
   [0.68,"y","Tahun Lepas",540,135,-3,112,44]]),
 dict(s=1.46,e=2.96,items=[
   [1.48,"w","tengah",170,440,-30,46,0],
   [1.62,"y","Fikir",290,250,-16,150,0],
   [2.04,"y","Fikir",815,250,14,104,0],
   [2.4,"w","fikir...",850,420,8,46,0]]),
 dict(s=2.96,e=5.40,items=[
   [2.98,"w","tup-tup",830,170,12,48,0],
   [3.74,"w","baju raya kita",235,470,-18,46,0],
   [4.54,"y","Sold",300,255,-14,175,0],
   [4.96,"y","Out",820,395,0,160,0]]),
 dict(s=5.40,e=7.02,items=[
   [5.42,"w","punyalah",235,205,-20,48,0],
   [6.0,"y","Berkenan",560,275,-2,130,38]]),
 dict(s=13.22,e=14.84,items=[
   [13.22,"w","ya Allah",290,165,-12,48,0],
   [13.7,"y","Sangat",420,285,-8,135,0],
   [14.04,"y","Cantik!",690,410,-4,145,0]]),
 dict(s=25.54,e=28.9,items=[
   [25.54,"w","material baju kurung ni",540,140,-3,44,0],
   [26.82,"y","Chiffon",540,290,0,155,32],
   [27.46,"w","+ lining dekat dalam",815,410,9,42,0]]),
 dict(s=35.4,e=37.62,items=[
   [35.4,"w","kain dia jenis",300,215,-14,46,0],
   [35.72,"y","Soft",370,345,-10,150,0],
   [35.94,"y","Brocade",610,500,-4,150,0],
   [36.88,"w","tak jarang langsung",820,640,6,42,0]]),
 dict(s=53.44,e=55.26,items=[
   [53.44,"w","sangat-sangat murah",540,145,-3,46,0],
   [54.36,"y","Bawah",315,285,-12,140,0],
   [54.56,"y","RM100",785,335,6,150,0]]),
 dict(s=57.84,e=FOOT,items=[
   [57.84,"y","Cepat-Cepat",540,205,-2,118,34],
   [58.3,"y","grab!",815,365,10,155,0],
   [58.48,"w","kita memang suka sangat",300,395,-10,42,0]]),
]

# ---------- KAPSYEN PUTIH (atas, frasa demi frasa) ----------
P=[
 [7.02,"tak ada rezeki"],[7.56,"nak grab tahun ni"],[8.32,"kakak grab"],[8.66,"awal-awal"],
 [9.6,"yang ini kakak grab"],[10.82,"daripada Sunset Closet"],[12.48,"korang tengok sendiri"],
 [14.84,"memang love"],[15.44,"sangat-sangat"],
 [16.04,"baju kurung"],[16.9,"daripada Sunset Closet"],[18.24,"dia punya koleksi"],
 [19.0,"semuanya cantik tau"],[19.98,"baju kurung"],[20.36,"yang kakak pakai ni"],
 [21.18,"cutting real"],[21.72,"korang tengok sendiri"],[22.36,"cutting dia"],
 [22.78,"memang sangat-sangat cantik"],[23.78,"sebab dia bagi kita"],[24.48,"efek yang kurus"],
 [28.9,"kurung ni ada pesak"],[29.94,"tapi jenis pesak"],[30.84,"yang tersorok"],
 [31.66,"sebab tu bila kita pakai"],[32.9,"dia memang flowy"],[33.88,"jatuh dia cantik"],
 [37.62,"tak gatal"],[38.52,"tak miang"],[38.98,"memang sangat-sangat selesa"],
 [40.9,"tak berat pun"],[41.7,"memang cantik"],[42.58,"sangat-sangat tau"],
 [43.6,"baju kurung ni"],[44.12,"memang kakak suka"],[44.72,"sebab dia bagi"],[45.3,"efek yang kurus"],
 [46.3,"bahagian belakang"],[46.98,"dia berzip"],[48.1,"bahagian lengan"],[48.64,"jenis lebar macam ni"],
 [50.0,"tinggi kakak"],[50.6,"165"],[51.74,"cantik"],[52.88,"ngam-ngam je"],
 [55.26,"korang akan dapat"],[56.16,"kurung yang cantik"],[56.92,"macam ni"],
]
starts=sorted([p[0] for p in P]+[g["s"] for g in G])

# ---------- KAMERA: potongan zoom (skala serta-merta) + transisi blur ----------
CUT=[(0,1.0),(2.98,1.1),(5.42,1.0),(9.6,1.15),(13.22,1.0),(16.9,1.15),(19.98,1.0),(22.36,1.15),
     (28.9,1.15),(31.66,1.0),(34.94,1.12),(37.62,1.0),(40.9,1.15),(46.3,1.15),(50.0,1.0),(55.26,1.12),(57.84,1.0)]
BLUR=[(7.02,1.0),(25.54,1.0),(43.6,1.0),(53.44,1.0)]

LETTER_GAP=0.045
html_items=[];js=[];au=[]
def esc(s): return s.replace("&","&amp;").replace("<","&lt;")
ai=0
def audio(src,t0,vol,d=1.0):
    global ai
    au.append(f'<audio id="s{ai}" src="sfx/{src}.wav" data-start="{max(0,t0):.2f}" data-duration="{d}" data-volume="{vol}"></audio>'); ai+=1

for gi,g in enumerate(G):
    inner=[]
    for ii,(t0,kind,txt,x,y,rot,size,arc) in enumerate(g["items"]):
        iid=f"g{gi}i{ii}"
        if kind=="y":
            n=len(txt); spans=[]
            for k,ch in enumerate(txt):
                if arc and n>1:
                    a=-arc/2+arc*k/(n-1)
                    import math
                    dy=size*2.2*(1-math.cos(math.radians(a)))
                    tr=f"translateY({dy:.1f}px) rotate({a:.1f}deg)"
                else: tr="none"
                c="&nbsp;" if ch==" " else esc(ch)
                spans.append(f'<span class="L" style="transform:{tr}"><b>{c}</b></span>')
            inner.append(f'<div id="{iid}" class="Y" style="left:{x}px;top:{y}px;font-size:{size}px;transform:translate(-50%,-50%) rotate({rot}deg)">{"".join(spans)}</div>')
            js.append(f'tl.fromTo("#{iid} b",{{opacity:0,scale:.3,y:size_y}},{{opacity:1,scale:1,y:0,duration:.22,ease:"back.out(2.2)",stagger:{LETTER_GAP}}},{t0});'.replace("size_y",str(round(size*0.12))))
            audio("scribble",t0-0.02,0.4,0.5)
        else:
            inner.append(f'<div id="{iid}" class="W" style="left:{x}px;top:{y}px;font-size:{size}px;transform:translate(-50%,-50%) rotate({rot}deg)"><b>{esc(txt)}</b></div>')
            js.append(f'tl.fromTo("#{iid} b",{{opacity:0,scale:.55}},{{opacity:1,scale:1,duration:.2,ease:"back.out(2.6)"}},{t0});')
            audio("pop",t0-0.01,0.35,0.2)
    d=round(g["e"]-g["s"],2)
    html_items.append(f'<div id="g{gi}" class="clip grp" data-start="{g["s"]}" data-duration="{d}">{"".join(inner)}</div>')

for i,(s,t) in enumerate(P):
    nxt=min([x for x in starts if x>s+0.001],default=FOOT)
    e=min(nxt,s+2.4); d=round(e-s,2)
    html_items.append(f'<div id="c{i}" class="clip cap" data-start="{s}" data-duration="{d}"><b>{esc(t)}</b></div>')
    js.append(f'tl.fromTo("#c{i} b",{{opacity:0,scale:.86,y:6}},{{opacity:1,scale:1,y:0,duration:.16,ease:"back.out(2)"}},{s});')

for t0,sc in CUT: js.append(f'tl.set("#cam",{{scale:{sc}}},{t0});')
for t0,sc in BLUR:
    js.append(f'tl.fromTo("#cam",{{scale:{sc*1.12:.3f},filter:"blur(16px)"}},{{scale:{sc},filter:"blur(0px)",duration:.32,ease:"power2.out",immediateRender:false}},{t0});')
    audio("whoosh",t0-0.2,0.35,0.6)

# penutup gelap
audio("boom",FOOT+0.3,0.85,END-0.3)
js.append(f'tl.fromTo("#endY b",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2.4)",stagger:.03}},{FOOT+0.3:.2f});')
js.append(f'tl.fromTo("#endW",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.3,ease:"expo.out"}},{FOOT+0.55:.2f});')
for k,c in enumerate(["#fff","#F5DE6E","#fff","#F5DE6E"]):
    js.append(f'tl.set("#endY",{{color:"{c}"}},{FOOT+0.3+0.35*k:.2f});')

endY="".join(f'<b>{"&nbsp;" if ch==" " else ch}</b>' for ch in "cepat grab!")
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Gochi Hand";src:url("assets/GochiHand.woff2") format("woff2");}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;transform-origin:50% 22%;}}
#cam video{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;}}
b{{font-weight:400;display:inline-block;}}
.grp{{position:absolute;inset:0;z-index:6;}}
.Y,.W{{position:absolute;white-space:nowrap;font-family:"Gochi Hand",cursive;line-height:1;}}
.Y{{color:#F5DE6E;letter-spacing:.02em;filter:url(#rough) drop-shadow(0 3px 4px rgba(0,0,0,.35));}}
.Y .L{{display:inline-block;transform-origin:50% 100%;}}
.Y b{{opacity:0;}}
.W{{color:#fff;letter-spacing:.07em;word-spacing:.15em;}}
.W b,.cap b{{opacity:0;-webkit-text-stroke:1.2px rgba(0,0,0,.45);paint-order:stroke fill;text-shadow:0 2px 3px rgba(0,0,0,.6),0 0 8px rgba(0,0,0,.3);}}
.cap{{position:absolute;left:80px;right:80px;top:205px;text-align:center;z-index:5;}}
.cap b{{font-family:"Gochi Hand",cursive;font-size:46px;line-height:1.1;letter-spacing:.07em;word-spacing:.18em;color:#fff;}}
#dark{{position:absolute;inset:0;background:#000;opacity:.7;z-index:8;}}
#endbox{{position:absolute;left:0;right:0;top:860px;text-align:center;z-index:9;}}
#endY{{font-family:"Gochi Hand",cursive;font-size:150px;line-height:1;color:#fff;filter:url(#rough);}}
#endY b{{opacity:0;}}
#endW{{font-family:"Gochi Hand",cursive;font-size:46px;letter-spacing:.08em;color:#fff;margin-top:22px;opacity:0;}}
</style></head>
<body>
<svg width="0" height="0" style="position:absolute"><filter id="rough" x="-10%" y="-10%" width="120%" height="120%">
<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="5" xChannelSelector="R" yChannelSelector="G" result="d"/>
<feComposite in="d" in2="d" operator="over"/></filter></svg>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam">
    <video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{FOOT}" data-has-audio="true" data-volume="1"></video>
    <video id="endv" class="clip" src="assets/footage.mp4" data-start="{FOOT}" data-duration="{END}" data-media-start="51.0" data-has-audio="true" data-volume="0"></video>
  </div>
{chr(10).join("  "+x for x in html_items)}
  <div id="dark" class="clip" data-start="{FOOT}" data-duration="{END}"></div>
  <div id="endbox" class="clip" data-start="{FOOT}" data-duration="{END}"><div id="endY">{endY}</div><div id="endW">sebelum sold out</div></div>
  <audio id="music" src="sfx/music.wav" data-start="0" data-duration="{FOOT}" data-volume="0.14"></audio>
{chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
open("index.html","w").write(html)
print("ok",DUR,len(au),"audio")
