# Style Bawah — kapsyen kecil tulisan tangan putih, bawah-tengah, frasa demi frasa.
# [mula, teks]  (tamat = mula frasa seterusnya, atau +gap jika senyap)
P=[
 [0.0,"jangan jadi macam"],[0.68,"tahun lepas ya"],[1.48,"tengah fikir-fikir"],[2.4,"fikir..."],
 [2.98,"tup-tup"],[3.74,"baju raya kita"],[4.54,"sold out"],
 [5.42,"punyalah berkenan"],[7.02,"tak ada rezeki"],[7.56,"nak grab tahun ni"],
 [8.32,"kakak grab"],[8.66,"awal-awal"],
 [9.6,"yang ini kakak grab"],[10.82,"daripada Sunset Closet"],[12.48,"korang tengok sendiri"],
 [13.22,"ya Allah"],[13.7,"sangat-sangat cantik"],[14.84,"memang love"],[15.44,"sangat-sangat"],
 [16.04,"baju kurung"],[16.9,"daripada Sunset Closet"],[18.24,"dia punya koleksi"],
 [19.0,"semuanya cantik tau"],[19.98,"baju kurung"],[20.36,"yang kakak pakai ni"],
 [21.18,"cutting real"],[21.72,"korang tengok sendiri"],[22.36,"cutting dia"],
 [22.78,"memang sangat-sangat cantik"],[23.78,"sebab dia bagi kita"],[24.48,"efek yang kurus"],
 [25.54,"material baju kurung ni"],[26.82,"chiffon"],[27.46,"siap ada lining"],[28.06,"lagi dekat dalam"],
 [28.9,"kurung ni ada pesak"],[29.94,"tapi jenis pesak"],[30.84,"yang tersorok"],
 [31.66,"sebab tu bila kita pakai"],[32.9,"dia memang flowy"],[33.88,"jatuh dia cantik"],
 [34.94,"kain dia pula"],[35.4,"jenis soft brocade"],[36.88,"tak jarang langsung"],
 [37.62,"tak gatal"],[38.52,"tak miang"],[38.98,"memang sangat-sangat selesa"],
 [40.9,"tak berat pun"],[41.7,"memang cantik"],[42.58,"sangat-sangat tau"],
 [43.6,"baju kurung ni"],[44.12,"memang kakak suka"],[44.72,"sebab dia bagi"],[45.3,"efek yang kurus"],
 [46.3,"bahagian belakang"],[46.98,"dia berzip"],[48.1,"bahagian lengan"],[48.64,"jenis lebar macam ni"],
 [50.0,"tinggi kakak"],[50.6,"165"],[51.74,"cantik"],[52.88,"ngam-ngam je"],
 [53.44,"sangat-sangat murah"],[54.36,"bawah RM100 je"],[55.26,"korang akan dapat"],
 [56.16,"kurung yang cantik"],[56.92,"macam ni"],
 [57.84,"cepat-cepat grab"],[58.48,"kita memang suka sangat"],[59.22,"dengan baju kurung ni"],
]
DUR=59.73
ov=[];js=[]
for i,(s,t) in enumerate(P):
    e=P[i+1][0] if i+1<len(P) else DUR
    e=min(e,s+2.4)  # jangan duduk lama sangat semasa senyap
    d=round(e-s,2)
    ov.append(f'<div id="c{i}" class="clip cap" data-start="{s}" data-duration="{d}"><span>{t}</span></div>')
    # masuk: pop kecil, keluar: hilang serta-merta (macam rujukan, potong terus)
    js.append(f'tl.fromTo("#c{i} span",{{opacity:0,scale:.86,y:6}},{{opacity:1,scale:1,y:0,duration:.16,ease:"back.out(2)"}},{s});')
html=f'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{{font-family:"Gochi Hand";src:url("assets/GochiHand.woff2") format("woff2");}}
html,body{{margin:0;background:#000;}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;}}
#cam{{position:absolute;inset:0;}}
#cam video{{width:100%;height:100%;object-fit:cover;display:block;}}
.cap{{position:absolute;left:90px;right:90px;top:1330px;text-align:center;z-index:5;}}
.cap span{{display:inline-block;font-family:"Gochi Hand",cursive;font-size:50px;line-height:1.1;letter-spacing:.06em;word-spacing:.18em;color:#fff;
  -webkit-text-stroke:1.5px rgba(0,0,0,.55);paint-order:stroke fill;
  text-shadow:0 2px 3px rgba(0,0,0,.7),0 0 10px rgba(0,0,0,.35);opacity:0;}}
</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="1"></video></div>
{chr(10).join("  "+x for x in ov)}
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
