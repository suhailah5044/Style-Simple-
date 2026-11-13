# 4 versi situasi — guna footage & gaya sama, hook + susunan berbeza
import subprocess,sys,os,json
SRC=sys.argv[1]; ONLY=sys.argv[2:] 
# babak: (masuk_sumber, teks overlay, sisi, sfx, zoom P/S)
SC={
 "pack":(1.0,"SILKELLE<br>Creator Exclusive 3.0","R","ui_notif","S"),
 "cup":(27.3,"3D Fit Cup","R","ui_blip","P"),
 "w":(36.5,"W-Shaped<br>Upper Support","L","ui_confirm","S"),
 "push":(45.5,"Push Up &amp;<br>Natural Lift","L","sub_boom","P"),
 "strap":(86.0,"Wide Anti-Slip<br>Shoulder Strap","R","swoosh","S"),
 "fabric":(42.3,"Soft &amp; Breathable<br>Material","R","glass_ting","S"),
 "hook":(66.5,"4 Rows<br>Hook &amp; Eye","R","ui_tap","P"),
 "light":(51.4,"Lightweight<br>&amp; Comfy","R","ui_blip","S"),
 "every":(120.4,"Perfect For<br>Everyday Wear","C","ui_confirm","S"),
 "every2":(93.2,"Perfect For<br>Everyday Wear","C","ui_confirm","S"),
 "back":(108.4,"More Comfort,<br>Better Support","R","sub_boom","P"),
 "size":(126.4,"Available Size<br>M – 4XL","C","coin","S"),
 "col":(129.5,"5 Colours<br>Available","C","ui_notif","S"),
 "end":(133.4,"Your Everyday<br>Comfort Bra 🤎","C","riser_shimmer","S"),
}
V={
 "V1_Student":dict(hook=(120.0,"Budak student","Kena ada bra ni!"),d=2.1,
   order=["light","fabric","cup","push","strap","hook","w","every2","back","size","col","pack","end"]),
 "V2_ContentCreator":dict(hook=(93.0,"Content creator","Shooting seharian pun selesa!"),d=2.1,
   order=["pack","cup","push","w","strap","fabric","light","hook","back","every","size","col","end"]),
 "V3_TakdaBesi":dict(hook=(12.0,"Bra berbesi sakit?","Try yang takda besi!"),d=2.1,
   order=["cup","w","push","fabric","light","strap","hook","back","every","pack","size","col","end"]),
 "V4_Unboxing":dict(hook=(0.6,"Unboxing","Silkelle Creator Exclusive 3.0"),d=2.3,
   order=["cup","w","push","strap","fabric","hook","light","every","back","size","col","end"]),
}
VOL={"sub_boom":0.45,"swoosh":0.3,"riser_shimmer":0.4,"coin":0.35,"ui_tap":0.45}
HD=2.8
def build(name,cfg):
    d=f"variants/{name}";os.makedirs(d+"/assets",exist_ok=True)
    for f in ["Italianno.woff2","LexendMega.woff2"]:
        p=f"{d}/assets/{f}"; os.path.exists(p) or os.symlink(os.path.abspath(f"assets/{f}"),p)
    os.path.exists(d+"/sfx") or os.symlink(os.path.abspath("sfx"),d+"/sfx")
    h0,h1,h2=cfg["hook"];D=cfg["d"]
    seg=[(h0,h0+HD)]+[(SC[k][0],SC[k][0]+D) for k in cfg["order"]]
    if seg[-1][1]-seg[-1][0]<2.2: seg[-1]=(seg[-1][0],seg[-1][0]+2.2)
    f="".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];" for i,(a,b) in enumerate(seg))
    f+="".join(f"[v{i}][a{i}]" for i in range(len(seg)))+f"concat=n={len(seg)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",f,"-map","[v]","-map","[a]","-c:v","libx264","-crf","16","-preset","fast",
     "-pix_fmt","yuv420p","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-c:a","aac","-b:a","192k",d+"/assets/footage.mp4"],check=True)
    T=[];t=0
    for a,b in seg: T.append(round(t,2)); t+=b-a
    DUR=round(t,2);ov=[];au=[];js=[]
    for i,k in enumerate(cfg["order"]):
        _,txt,side,sfx,z=SC[k];s=T[i+1]+0.05;e=(T[i+2]-0.1) if i+2<len(T) else DUR-0.15
        ov.append(f'<div id="w{i}" class="clip word {side}" style="top:250px" data-start="{s:.2f}" data-duration="{e-s:.2f}"><span class="tx">{txt}</span><i class="bar"></i></div>')
        au.append(f'<audio src="sfx/{sfx}.wav" data-start="{max(0,s-0.02):.2f}" data-duration="1.1" data-volume="{VOL.get(sfx,0.4)}"></audio>')
        js.append(f'tl.fromTo("#w{i} .tx",{{opacity:0,y:22,scale:.92}},{{opacity:1,y:0,scale:1,duration:0.38,ease:"back.out(2)"}},{s:.2f});')
        js.append(f'tl.fromTo("#w{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"expo.out"}},{s+0.08:.2f});')
        js.append(f'tl.to("#w{i} .tx,#w{i} .bar",{{opacity:0,y:-10,duration:0.2,ease:"power2.in"}},{e-0.22:.2f});')
        if z=="P": js.append(f'tl.fromTo("#cam",{{scale:1.1}},{{scale:1.02,duration:0.45,ease:"power3.out"}},{s:.2f});')
    for c in T[1:]:
        js.append(f'tl.set("#cam",{{scale:1}},{c});tl.fromTo("#flash",{{opacity:.35}},{{opacity:0,duration:.25,ease:"power2.out",immediateRender:false}},{c});')
        au.append(f'<audio src="sfx/swoosh.wav" data-start="{c-0.12:.2f}" data-duration="0.6" data-volume="0.12"></audio>')
    tpl=open("index.html").read()
    head=tpl.split("<body>")[0]
    html=head+f'''<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="footage" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-has-audio="true" data-volume="0.35"></video></div>
  <div id="flash"></div>
  <div id="title" class="clip" data-start="0" data-duration="{HD}"><span id="t1">{h1}</span><br><span id="t2">{h2}</span></div>
  {chr(10).join("  "+x for x in ov)}
  <audio src="sfx/cork.wav" data-start="0.15" data-duration="1.0" data-volume="0.5"></audio>
  <audio src="sfx/sub_boom.wav" data-start="0.7" data-duration="1.0" data-volume="0.4"></audio>
  {chr(10).join("  "+x for x in au)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
tl.set("#cam",{{scale:1}},0);
tl.fromTo("#t1",{{opacity:0,scale:.6,y:10}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2.6)"}},0.15);
tl.fromTo("#t2",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.4,ease:"expo.out"}},0.7);
tl.fromTo("#cam",{{scale:1.12}},{{scale:1.02,duration:.5,ease:"power3.out"}},0.7);
tl.to("#t1,#t2",{{opacity:0,y:-10,duration:.22,ease:"power2.in"}},{HD-0.25});
{chr(10).join(js)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
    open(d+"/index.html","w").write(html);print(name,DUR)
for n,c in V.items():
    if not ONLY or n in ONLY: build(n,c)
