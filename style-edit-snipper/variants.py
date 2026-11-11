# Konfigurasi 3 video. segs: [audio_src_mula, audio_src_tamat, video_src|None(=sama), tag]
# ov: [src_anchor(perkataan), tempoh_s, teks, sub-line, L|R, sfx, zoom(in|out|punch|-)]
# fb: indeks segmen untuk frame break; pip: [video_src, src_anchor, tempoh_s, L|R]

HOOK_PILL_CSS = ""

V = {}

# ---------------- V1: DEMO AIR ----------------
V["v1"] = dict(
 segs=[
  [34.45,35.98,28.2,"hook"],        # "tengok dia tak tembus ke dalam" + b-roll air (stabil)
  [8.12,12.95,None,"intro"],        # "beg sekolah daripada Snipper ni setiap tahun repeat... tahan lasak"
  [22.72,25.02,None,"usp"],         # "saya suka sebab dia water resistant"
  [25.18,28.30,None,"usp"],         # "kalau kena air pun tak risau, dia lalu sahaja"
  [49.15,50.45,None,"usp"],         # "kompartmen dia begini"
  [52.15,53.50,None,"usp"],         # "ada kompartmen dekat dalam"
  [59.36,64.45,None,"usp"],         # design cantik, jahitan kemas
  [86.84,88.35,None,"usp"],         # pakai memang selesa
  [88.62,91.50,None,"usp"],         # span tebal tak nipis
  [103.86,106.75,72.0,"usp"],       # kualiti elok, cantik (b-roll close-up stabil)
  [113.84,117.40,None,"cta"],       # tengok bakul kuning, harga murah
  [77.95,82.10,None,"cta"],         # warna cantik masih ada, cepat grab
 ],
 ov=[
  [9.68,1.5,"Repeat Setiap Tahun","","R","ui_prompt1","in"],
  [11.96,1.0,"Tahan Lasak","","R","impact2","punch"],
  [24.22,1.6,"Water Resistant","Anti-Splash","R","droplet","in"],
  [26.98,1.3,"Air Terus Mengalir","","R","ui_prompt2","out"],
  [49.22,1.4,"Multiple Compartments","Kapasiti 20L","R","zip","in"],
  [52.56,1.2,"Internal Compartment","Muat Laptop 16 Inci","R","ui_prompt3","out"],
  [59.42,1.7,"Design Cantik","","R","shimmer","-"],
  [62.06,1.8,"Jahitan Kemas","Scratch Resistant","R","ting2","punch"],
  [87.92,1.0,"Selesa Dipakai","","R","pop2","in"],
  [89.04,2.0,"Span Tebal","Adjustable Shoulder Straps","R","click2","out"],
  [103.92,1.6,"Kualiti Elok","","R","ding2","punch"],
 ],
 fb=[4,9], pip=[[72.6,61.34,1.6,"L"]],
 bg="background:radial-gradient(120% 70% at 50% 38%,#26324e 0%,#101624 55%,#06080e 100%);",
 bgfx="opacity:.22;background-image:radial-gradient(rgba(255,255,255,.55) 1.2px,transparent 1.3px);background-size:36px 36px;",
 css='''.word{top:170px;} .word.L{left:96px;text-align:left;} .word.R{right:96px;text-align:right;}
.word .mk{display:inline-block;width:8px;height:8px;border-radius:50%;background:#fff;margin:0 12px 4px 0;vertical-align:middle;box-shadow:0 1px 4px rgba(0,0,0,.4);}
.word.R .mk{margin:0 12px 4px 0;}
#hook{top:205px;} #hook .pill{display:inline-block;padding:15px 28px 17px;border-radius:999px;background:rgba(12,16,26,.30);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1.5px solid rgba(255,255,255,.38);opacity:0;}
#hook .hw{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:700;font-size:31px;letter-spacing:-0.05em;color:#fff;margin:0 5px;opacity:0;text-shadow:0 2px 6px rgba(0,0,0,.35);}''',
 anim_in='tl.fromTo("#w{i} .mk",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:.25,ease:"back.out(3)"}},{s});'
         'tl.fromTo("#w{i} .tx",{{opacity:0,clipPath:"inset(0 100% 0 0)"}},{{opacity:1,clipPath:"inset(0 0% 0 0)",duration:.4,ease:"power3.out"}},{s});'
         'tl.fromTo("#w{i} .sb",{{opacity:0,y:6}},{{opacity:.92,y:0,duration:.3,ease:"expo.out"}},{s2});',
 hook=dict(sfx="hook1",
  html='<span class="pill"><span class="hw">Beg</span><span class="hw">Sekolah</span><span class="hw">Waterproof</span></span>',
  js='''tl.fromTo("#cam",{scale:1.16},{scale:1.03,duration:.8,ease:"power3.out"},0.0);
tl.to("#cam",{scale:1.08,duration:2.0,ease:"sine.inOut"},0.9);
tl.fromTo("#hook .pill",{opacity:0,scale:.7},{opacity:1,scale:1,duration:.42,ease:"back.out(2.2)"},0.25);
tl.fromTo("#hook .hw",{opacity:0,y:12},{opacity:1,y:0,duration:.3,ease:"expo.out",stagger:.13},0.36);
tl.to("#hook .pill",{opacity:0,y:-10,duration:.22,ease:"power2.in"},2.76);
tl.to("#cam",{scale:1.0,duration:.6,ease:"sine.inOut"},3.0);'''),
)

# ---------------- V2: BUKTI TAHAN 2 TAHUN ----------------
V["v2"] = dict(
 segs=[
  [37.80,41.98,None,"hook"],        # "tahan lasak dah dua tahun dah saya pakai bag daripada Snipper ni"
  [42.50,45.50,None,"intro"],       # "hari tu saya beli plain, kali ni corak-corak"
  [59.36,64.45,None,"usp"],         # design cantik, jahitan kemas
  [52.15,53.50,None,"usp"],         # ada kompartmen dekat dalam
  [55.36,57.68,None,"usp"],         # combo dapat sekali
  [22.72,25.02,None,"usp"],         # water resistant
  [109.76,110.60,None,"usp"],       # kena air pun tak risau
  [26.82,28.30,None,"usp"],         # dia lalu sahaja (demo air)
  [88.62,91.50,None,"usp"],         # span tebal tak nipis
  [102.26,103.40,None,"cta"],       # memang sangat-sangat recommend
  [113.84,117.40,None,"cta"],       # bakul kuning, harga murah
 ],
 ov=[
  [44.64,1.6,"Plain → Corak","","R","ui_prompt2","in"],
  [59.42,1.7,"Design Cantik","","R","shimmer","out"],
  [62.06,1.8,"Jahitan Kemas","","R","ting2","punch"],
  [52.56,1.3,"Internal Compartment","Front & Side Pocket","R","zip","in"],
  [56.68,1.6,"Combo + Pencil Box","","R","ding2","punch"],
  [24.22,1.9,"Water Resistant","Water-Resistant Zipper","R","droplet","in"],
  [89.04,2.2,"Span Tebal · Tak Nipis","","R","click2","out"],
 ],
 fb=[2,5,9], pip=[[28.4,23.04,1.8,"L"]],
 bg="background:linear-gradient(160deg,#1b2440 0%,#0d1222 60%,#05070d 100%);",
 bgfx="opacity:.16;background-image:repeating-linear-gradient(45deg,rgba(255,255,255,.35) 0 1px,transparent 1px 22px);",
 css='''.word{top:165px;} .word.L{left:90px;text-align:left;} .word.R{right:90px;text-align:right;}
.word .tx{padding:9px 18px 10px;border:1.5px solid rgba(255,255,255,.85);border-radius:999px;background:rgba(0,0,0,.22);}
.word .sb{margin-top:9px;padding:0 6px;}
#hook{top:190px;}
#hook .tag{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:500;font-size:17px;letter-spacing:-0.02em;color:#fff;padding:7px 15px;border:1.3px solid rgba(255,255,255,.8);border-radius:999px;opacity:0;}
#hook .box{display:block;width:max-content;margin:12px auto 0;padding:14px 26px 16px;border-radius:18px;background:rgba(8,10,18,.32);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);opacity:0;}
#hook .hw{display:inline-block;font-family:"Lexend Mega",sans-serif;font-weight:700;font-size:31px;letter-spacing:-0.05em;color:#fff;margin:0 5px;opacity:0;}''',
 anim_in='tl.fromTo("#w{i} .tx",{{opacity:0,scale:.82,y:8}},{{opacity:1,scale:1,y:0,duration:.36,ease:"back.out(2.4)"}},{s});'
         'tl.fromTo("#w{i} .sb",{{opacity:0,y:6}},{{opacity:.92,y:0,duration:.3,ease:"expo.out"}},{s2});',
 hook=dict(sfx="hook2",
  html='<span class="tag">Tahan Lasak · 2 Tahun</span><span class="box"><span class="hw">Beg</span><span class="hw">Sekolah</span><span class="hw">Waterproof</span></span>',
  js='''tl.fromTo("#cam",{scale:1.0},{scale:1.13,duration:.42,ease:"power2.in"},0.0);
tl.to("#cam",{scale:1.04,duration:.5,ease:"power3.out"},0.45);
tl.to("#cam",{scale:1.08,duration:2.0,ease:"sine.inOut"},1.0);
tl.fromTo("#hook .tag",{opacity:0,y:-10},{opacity:1,y:0,duration:.35,ease:"expo.out"},0.3);
tl.fromTo("#hook .box",{opacity:0,scale:.8},{opacity:1,scale:1,duration:.4,ease:"back.out(2)"},0.45);
tl.fromTo("#hook .hw",{opacity:0,y:12},{opacity:1,y:0,duration:.3,ease:"expo.out",stagger:.12},0.55);
tl.to("#hook .tag,#hook .box",{opacity:0,y:-10,duration:.22,ease:"power2.in"},2.76);
tl.to("#cam",{scale:1.0,duration:.6,ease:"sine.inOut"},3.0);'''),
)

# ---------------- V3: MAK & ANAK ----------------
V["v3"] = dict(
 segs=[
  [111.28,113.42,None,"hook"],      # "lagi-lagi anak kita tu memang seorang yang lasak"
  [82.20,83.98,None,"intro"],       # "saya suka sebab anak memang suka"
  [0.00,2.62,None,"intro"],         # "beg sekolah daripada Snipper ni"
  [13.06,14.76,29.4,"usp"],         # "saya suka dia water resistant" + b-roll air
  [34.45,35.98,None,"usp"],         # "tengok dia tak tembus ke dalam"
  [86.84,88.35,None,"usp"],         # selesa
  [91.68,93.98,None,"usp"],         # bila pakai memang elok
  [96.00,101.55,None,"usp"],        # sekolah rendah, menengah, travel, recommend
  [49.15,50.45,None,"usp"],         # kompartmen dia begini
  [52.15,53.50,None,"usp"],         # ada kompartmen dekat dalam
  [55.36,57.68,None,"usp"],         # combo dapat sekali
  [77.95,82.10,None,"cta"],         # warna cantik masih ada, cepat grab
 ],
 ov=[
  [13.84,1.4,"Water Resistant","Anti-Splash","L","droplet","in"],
  [35.02,1.3,"Tak Tembus Ke Dalam","","L","ui_prompt2","punch"],
  [87.36,1.1,"Selesa Dipakai","","L","pop2","out"],
  [96.88,0.85,"Sekolah Rendah","","L","ui_prompt3","in"],
  [97.70,1.0,"Sekolah Menengah","","L","click2","-"],
  [99.48,1.2,"Travel","","L","ting2","out"],
  [49.22,1.4,"Saiz 47 × 32 × 15 cm","Kapasiti 20L","L","zip","in"],
  [56.68,1.6,"Combo + Pencil Box","","L","ding2","punch"],
 ],
 fb=[3,7], pip=[[30.0,35.02,1.4,"R"],[50.4,52.56,1.3,"R"]],
 bg="background:radial-gradient(110% 80% at 30% 20%,#2a3a48 0%,#121a24 55%,#070a0f 100%);",
 bgfx="opacity:.15;background-image:linear-gradient(rgba(255,255,255,.14) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.14) 1px,transparent 1px);background-size:64px 64px;",
 css='''.word{top:172px;padding-left:18px;} .word.L{left:90px;text-align:left;} .word.R{right:90px;text-align:left;}
.word .mk{position:absolute;left:0;top:4px;width:3px;height:30px;background:#fff;border-radius:2px;transform-origin:50% 0;box-shadow:0 1px 4px rgba(0,0,0,.4);}
#hook{top:205px;}
#hook .pill{position:relative;display:inline-block;padding:15px 28px 17px;border-radius:16px;background:rgba(10,14,20,.28);border:1.5px solid rgba(255,255,255,.55);opacity:0;}
#hook .q,#hook .a{font-family:"Lexend Mega",sans-serif;font-weight:700;font-size:31px;letter-spacing:-0.05em;color:#fff;}
#hook .q{position:absolute;left:0;right:0;top:15px;opacity:0;} #hook .a{opacity:0;}
#hook .hw{display:inline-block;margin:0 5px;}''',
 anim_in='tl.fromTo("#w{i} .mk",{{opacity:0,scaleY:0}},{{opacity:1,scaleY:1,duration:.3,ease:"expo.out"}},{s});'
         'tl.fromTo("#w{i} .tx",{{opacity:0,x:-14}},{{opacity:1,x:0,duration:.36,ease:"expo.out"}},{s});'
         'tl.fromTo("#w{i} .sb",{{opacity:0,x:-10}},{{opacity:.92,x:0,duration:.3,ease:"expo.out"}},{s2});',
 hook=dict(sfx="hook3",
  html='<span class="pill"><span class="q">Anak Lasak?</span><span class="a"><span class="hw">Beg</span><span class="hw">Sekolah</span><span class="hw">Waterproof</span></span></span>',
  js='''tl.fromTo("#cam",{scale:1.14},{scale:1.04,duration:.6,ease:"power3.out"},0.0);
tl.to("#cam",{scale:1.08,duration:2.2,ease:"sine.inOut"},0.7);
tl.fromTo("#hook .pill",{opacity:0,y:14},{opacity:1,y:0,duration:.4,ease:"back.out(2)"},0.2);
tl.fromTo("#hook .q",{opacity:0,scale:.8},{opacity:1,scale:1,duration:.3,ease:"back.out(2.5)"},0.28);
tl.to("#hook .q",{opacity:0,y:-10,duration:.2,ease:"power2.in"},1.15);
tl.fromTo("#hook .a",{opacity:0},{opacity:1,duration:.01},1.3);
tl.fromTo("#hook .hw",{opacity:0,y:12},{opacity:1,y:0,duration:.3,ease:"expo.out",stagger:.12},1.3);
tl.to("#hook .pill",{opacity:0,y:-10,duration:.22,ease:"power2.in"},2.76);
tl.to("#cam",{scale:1.0,duration:.6,ease:"sine.inOut"},3.0);'''),
)
