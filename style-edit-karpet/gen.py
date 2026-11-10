# Enjin variasi V2-V5: susunan klip, transisi, gaya teks, grafik & SFX berbeza.
# Footage karpet sahaja (tiada orang), warna asal, tiada filter. Font Lexend Mega putih kecil.
# Guna: python3 gen.py  -> variants/vN/index.html (assets/ & sfx/ = symlink)
import json
SRC = "assets/src/"

# Scene: dict(t=jenis, src=[(id, media_start)], d=durasi, z=zoom, tr=transisi masuk, ov=(baris1, baris2) atau None)
# jenis: v | split | phone3d | polaroid | collage | letterbox
# transisi: cut | slide | zoomthru | circle | wipe | break | flash
V = {
 "v2": dict(name="Slide Clean", text="A", pos="L",
   hook=("OUTDOOR MAT", "Depan Pintu", "Terus Nampak Kemas"),
   sfx=dict(text="glass_pluck", usp="sparkle_tail", hook=["thump_low", "glass_pluck"]),
   scenes=[
    dict(t="v", src=[("1983", 0.2)], d=3.0, z="out", tr="cut", ov=None),
    dict(t="v", src=[("1981", 0.0)], d=2.0, z="in", tr="slide", ov=("Outdoor Mat", "Upgrade!"), usp=1),
    dict(t="v", src=[("1976", 0.0)], d=2.0, z="in", tr="slide", ov=("Biggest Size", "80 × 120 cm")),
    dict(t="v", src=[("1973", 0.4)], d=2.3, z="punch", tr="slide", ov=("400 GSM", "Coarse Fiber")),
    dict(t="v", src=[("1976", 3.0)], d=1.7, z="in", tr="cut", ov=("Scrape Off", "Dirt & Sand")),
    dict(t="v", src=[("1979", 0.2)], d=2.0, z="out", tr="slide", ov=("Water", "Resistant")),
    dict(t="v", src=[("1972", 0.0)], d=1.9, z="punch", tr="flash", ov=("TPE Anti-Slip", "Base")),
    dict(t="split", src=[("1974", 0.3), ("1982", 1.0)], d=2.6, z="in", tr="slide", ov=("Minimalist", "Embossed Design")),
    dict(t="v", src=[("1978", 0.5)], d=2.0, z="out", tr="slide", ov=None),
    dict(t="v", src=[("1970t", 0.1)], d=2.4, z="in", tr="slide", ov=("Perfect for", "Home Entrance"), usp=1),
   ]),
 "v3": dict(name="Typewriter UI", text="B", pos="C",
   hook=("NEW", "Upgrade", "Karpet Depan Rumah"),
   sfx=dict(text="type_burst", usp="bell_ding", hook=["soft_impact", "type_burst"]),
   scenes=[
    dict(t="v", src=[("1982", 0.8)], d=3.0, z="punch", tr="cut", ov=None),
    dict(t="v", src=[("1970t", 0.0)], d=2.2, z="in", tr="zoomthru", ov=("Outdoor Mat", "Upgrade!"), usp=1),
    dict(t="phone3d", src=[("1976", 0.0)], d=2.8, z="none", tr="zoomthru", ov=("Biggest Size", "80 × 120 cm")),
    dict(t="v", src=[("1974", 0.0)], d=2.1, z="punch", tr="zoomthru", ov=("400 GSM", "Coarse Fiber")),
    dict(t="v", src=[("1976", 3.0)], d=1.7, z="in", tr="cut", ov=("Scrape Off", "Dirt & Sand")),
    dict(t="v", src=[("1981", 1.6)], d=1.9, z="out", tr="zoomthru", ov=("Water", "Resistant")),
    dict(t="v", src=[("1972", 0.0)], d=1.9, z="punch", tr="cut", ov=("TPE Anti-Slip", "Base")),
    dict(t="v", src=[("1979", 0.3)], d=2.3, z="in", tr="zoomthru", ov=("Minimalist", "Embossed Design")),
    dict(t="v", src=[("1971", 1.4)], d=2.5, z="out", tr="zoomthru", ov=("Perfect for", "Home Entrance"), usp=1),
   ]),
 "v4": dict(name="Kinetic Blur", text="C", pos="R",
   hook=("ANTI SLIP", "Karpet Luar", "Untuk Pintu Rumah"),
   sfx=dict(text="chime_soft", usp="ting2", hook=["thump_low", "chime_soft"]),
   scenes=[
    dict(t="v", src=[("1978", 0.2)], d=3.0, z="in", tr="cut", ov=None),
    dict(t="v", src=[("1983", 0.5)], d=2.0, z="out", tr="circle", ov=("Outdoor Mat", "Upgrade!"), usp=1),
    dict(t="polaroid", src=[("1970t", 0.0)], d=2.6, z="none", tr="circle", ov=("Biggest Size", "80 × 120 cm"), count=1),
    dict(t="v", src=[("1982", 2.0)], d=2.4, z="punch", tr="circle", ov=("400 GSM", "Coarse Fiber"), count=1),
    dict(t="v", src=[("1976", 3.0)], d=1.7, z="in", tr="cut", ov=("Scrape Off", "Dirt & Sand")),
    dict(t="v", src=[("1980", 0.0)], d=1.75, z="out", tr="circle", ov=("Water", "Resistant")),
    dict(t="v", src=[("1972", 0.0)], d=1.9, z="punch", tr="cut", ov=("TPE Anti-Slip", "Base")),
    dict(t="v", src=[("1973", 1.5)], d=2.3, z="in", tr="circle", ov=("Minimalist", "Embossed Design")),
    dict(t="v", src=[("1981", 0.0)], d=1.6, z="out", tr="cut", ov=None),
    dict(t="v", src=[("1976", 0.0)], d=2.0, z="in", tr="circle", ov=("Perfect for", "Home Entrance"), usp=1),
   ]),
 "v5": dict(name="Editorial Index", text="D", pos="L",
   hook=("01 — 08", "Outdoor Mat", "Anti Slip"),
   sfx=dict(text="tick_index", usp="sparkle_tail", hook=["thump_low", "tick_index"]),
   scenes=[
    dict(t="letterbox", src=[("1971", 0.0)], d=3.0, z="in", tr="cut", ov=None),
    dict(t="v", src=[("1979", 0.0)], d=2.0, z="out", tr="wipe", ov=("Outdoor Mat", "Upgrade!"), usp=1),
    dict(t="v", src=[("1983", 0.5)], d=2.4, z="in", tr="wipe", ov=("Biggest Size", "80 × 120 cm")),
    dict(t="v", src=[("1974", 0.4)], d=2.2, z="punch", tr="break", ov=("400 GSM", "Coarse Fiber")),
    dict(t="v", src=[("1976", 3.0)], d=1.7, z="in", tr="wipe", ov=("Scrape Off", "Dirt & Sand")),
    dict(t="v", src=[("1981", 0.2)], d=1.9, z="out", tr="wipe", ov=("Water", "Resistant")),
    dict(t="v", src=[("1972", 0.0)], d=1.9, z="punch", tr="break", ov=("TPE Anti-Slip", "Base")),
    dict(t="v", src=[("1982", 3.0)], d=2.3, z="in", tr="wipe", ov=("Minimalist", "Embossed Design")),
    dict(t="collage", src=[("1970t", 0.0), ("1978", 0.5), ("1983", 1.0), ("1971", 1.5)], d=2.8, z="none", tr="wipe", ov=("Perfect for", "Home Entrance"), usp=1),
   ]),
}
TD = dict(cut=0, flash=0, slide=0.35, zoomthru=0.4, circle=0.45, wipe=0.4, break_=0, **{"break": 0})
TRSFX = dict(slide="swish_fast", zoomthru="rise_sweep", circle="blip_up", wipe="paper_slide", flash="thump_low", cut="ui_click")
SFXV = dict(swish_fast=.28, rise_sweep=.25, blip_up=.22, paper_slide=.3, thump_low=.4, ui_click=.28, camera_shutter=.35,
            glass_pluck=.22, type_burst=.3, chime_soft=.2, tick_index=.3, sparkle_tail=.2, bell_ding=.2, ting2=.22, soft_impact=.35)

CSS = open("gen_style.css").read()

def build(key, cfg):
    sc = cfg["scenes"]; H = []; A = []; J = []; mid = [0]
    def media(tag_id, src, ms, start, dur, extra=""):
        mid[0] += 1
        return f'<video id="m{mid[0]}_{tag_id}" src="{SRC}{src}.mp4" data-start="{start:.3f}" data-duration="{dur:.3f}" data-media-start="{ms:.3f}" muted playsinline{extra}></video>'
    def sfx(t, name, v=None):
        A.append(f'<audio id="a{len(A)}" src="sfx/{name}.wav" data-start="{max(0,t):.2f}" data-duration="0.9" data-volume="{v if v is not None else SFXV.get(name,.25)}"></audio>')
    # masa scene
    st = []; t = 0.0
    for i, s in enumerate(sc):
        td = TD[s["tr"]] if i else 0
        t = t - td if i else 0.0
        st.append(t); t += s["d"]
    DUR = round(t, 2)
    for i, s in enumerate(sc):
        s0, d, z = st[i], s["d"], s["z"]
        W = f"sc{i}"
        style = f"z-index:{10+i};visibility:hidden"
        if s["t"] == "v" or s["t"] == "letterbox":
            (src, ms), = s["src"]
            inner = f'<div class="cam">{media(W, src, ms, s0, d)}</div>'
            if s["t"] == "letterbox":
                inner += '<i class="lb t"></i><i class="lb b"></i>'
        elif s["t"] == "split":
            (a, ma), (b, mb) = s["src"]
            inner = (f'<div class="half top"><div class="cam">{media(W+"a", a, ma, s0, d)}</div></div>'
                     f'<div class="half bot"><div class="cam">{media(W+"b", b, mb, s0, d)}</div></div><i class="seam"></i>')
        elif s["t"] == "phone3d":
            (src, ms), = s["src"]
            inner = f'<div class="bg bg3"><i class="streak"></i></div><div class="stage"><div class="phone p3">{"<div class=scr>"+media(W, src, ms, s0, d)+"</div>"}<i class="isl"></i></div></div>'
        elif s["t"] == "polaroid":
            (src, ms), = s["src"]
            inner = f'<div class="bg bg4"><i class="dots"></i></div><div class="pol"><div class="ph">{media(W, src, ms, s0, d)}</div></div>'
        elif s["t"] == "collage":
            cells = "".join(f'<div class="cell c{k}"><div class="cam">{media(W+str(k), a, m, s0, d)}</div></div>' for k, (a, m) in enumerate(s["src"]))
            inner = f'<div class="bg bg5"></div><div class="grid4">{cells}</div>'
        H.append(f'<div id="{W}" class="scene" style="{style}">{inner}</div>')
        J.append(f'tl.set("#{W}",{{visibility:"visible"}},{s0:.3f});tl.set("#{W}",{{visibility:"hidden"}},{s0+d:.3f});')
        # zoom digital
        cam = f"#{W} > .cam"
        if s["t"] in ("v", "letterbox"):
            if z == "punch": J.append(f'tl.fromTo("{cam}",{{scale:1.16}},{{scale:1.04,duration:.5,ease:"power3.out"}},{s0:.3f});tl.to("{cam}",{{scale:1.1,duration:{d-0.5:.2f},ease:"sine.inOut"}},{s0+0.5:.3f});')
            elif z == "in": J.append(f'tl.fromTo("{cam}",{{scale:1.0}},{{scale:1.07,duration:{d:.2f},ease:"sine.inOut"}},{s0:.3f});')
            elif z == "out": J.append(f'tl.fromTo("{cam}",{{scale:1.08}},{{scale:1.0,duration:{d:.2f},ease:"sine.out"}},{s0:.3f});')
        if s["t"] == "letterbox":
            J.append(f'tl.fromTo("#{W} .lb",{{scaleY:.55}},{{scaleY:0,duration:.9,ease:"power3.inOut"}},{s0:.3f});')
        if s["t"] == "split":
            J.append(f'tl.fromTo("#{W} .top",{{xPercent:-100}},{{xPercent:0,duration:.5,ease:"power3.out"}},{s0:.3f});')
            J.append(f'tl.fromTo("#{W} .bot",{{xPercent:100}},{{xPercent:0,duration:.5,ease:"power3.out"}},{s0+0.08:.3f});')
            J.append(f'tl.fromTo("#{W} .seam",{{scaleX:0}},{{scaleX:1,duration:.5,ease:"expo.out"}},{s0+0.3:.3f});')
            J.append(f'tl.fromTo("#{W} .half .cam",{{scale:1.0}},{{scale:1.08,duration:{d:.2f},ease:"sine.inOut"}},{s0:.3f});')
            sfx(s0 + 0.08, "swish_fast", .2)
        if s["t"] == "phone3d":
            J.append(f'tl.fromTo("#{W} .p3",{{rotationY:-28,rotationX:8,scale:.82,y:80}},{{rotationY:-12,rotationX:4,scale:.95,y:0,duration:.8,ease:"power3.out"}},{s0:.3f});')
            J.append(f'tl.to("#{W} .p3",{{rotationY:8,rotationX:2,duration:{d-0.8:.2f},ease:"sine.inOut"}},{s0+0.8:.3f});')
            J.append(f'tl.fromTo("#{W} .streak",{{xPercent:-120}},{{xPercent:120,duration:{d:.2f},ease:"none"}},{s0:.3f});')
            sfx(s0 + 0.1, "soft_impact", .3)
        if s["t"] == "polaroid":
            J.append(f'tl.fromTo("#{W} .pol",{{rotation:-14,scale:.6,y:260,opacity:0}},{{rotation:-4,scale:1,y:0,opacity:1,duration:.7,ease:"back.out(1.6)"}},{s0:.3f});')
            J.append(f'tl.to("#{W} .pol",{{rotation:2,duration:{d-0.7:.2f},ease:"sine.inOut"}},{s0+0.7:.3f});')
            J.append(f'tl.fromTo("#{W} .ph video",{{scale:1}},{{scale:1.08,duration:{d:.2f},ease:"sine.inOut"}},{s0:.3f});')
            sfx(s0 + 0.15, "camera_shutter", .3)
        if s["t"] == "collage":
            for k in range(4):
                J.append(f'tl.fromTo("#{W} .c{k}",{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:"back.out(1.4)"}},{s0+0.1+0.1*k:.3f});')
                J.append(f'tl.fromTo("#{W} .c{k} .cam",{{scale:1.12}},{{scale:1,duration:{d:.2f},ease:"sine.out"}},{s0:.3f});')
            for k in range(4): sfx(s0 + 0.1 + 0.1 * k, "blip_up", .14)
        # transisi masuk
        tr = s["tr"]; td = TD[tr]
        if i:
            P = f"#sc{i-1}"
            if tr == "slide":
                J.append(f'tl.fromTo("#{W}",{{xPercent:100}},{{xPercent:0,duration:{td},ease:"power3.inOut"}},{s0:.3f});')
                J.append(f'tl.fromTo("{P}",{{xPercent:0}},{{xPercent:-35,duration:{td},ease:"power3.inOut"}},{s0:.3f});')
            elif tr == "zoomthru":
                J.append(f'tl.fromTo("{P}",{{scale:1,opacity:1}},{{scale:1.45,opacity:0,duration:{td},ease:"power2.in"}},{s0:.3f});')
                J.append(f'tl.fromTo("#{W}",{{scale:.8,opacity:0}},{{scale:1,opacity:1,duration:{td},ease:"power2.out"}},{s0:.3f});')
                J.append(f'tl.set("#{W}",{{zIndex:{10+i}}},{s0:.3f});')
            elif tr == "circle":
                J.append(f'tl.fromTo("#{W}",{{clipPath:"circle(0% at 50% 52%)"}},{{clipPath:"circle(80% at 50% 52%)",duration:{td},ease:"power2.inOut"}},{s0:.3f});')
            elif tr == "wipe":
                J.append(f'tl.fromTo("#{W}",{{clipPath:"inset(100% 0% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:{td},ease:"power3.inOut"}},{s0:.3f});')
                H.append(f'<i id="wl{i}" class="wline" style="z-index:{30+i}"></i>')
                J.append(f'tl.fromTo("#wl{i}",{{y:1920,opacity:1}},{{y:0,duration:{td},ease:"power3.inOut"}},{s0:.3f});tl.set("#wl{i}",{{opacity:0}},{s0+td:.3f});')
            elif tr == "flash":
                H.append(f'<i id="fl{i}" class="flash" style="z-index:{30+i}"></i>')
                J.append(f'tl.fromTo("#fl{i}",{{opacity:.7}},{{opacity:0,duration:.25,ease:"power2.out",immediateRender:false}},{s0:.3f});')
            elif tr == "break":
                p = sc[i-1]; (psrc, pms), = p["src"]; po = pms + (s0 - 0.3 - st[i-1])
                for k, (a, b, dx) in enumerate([(0, 34, -1), (33, 67, 1), (66, 100, -1)]):
                    H.append(f'<div id="br{i}_{k}" class="scene" style="z-index:{30+i};visibility:hidden;clip-path:polygon(0 {a}%,100% {a+2*dx}%,100% {b+2*dx}%,0 {b}%)"><div class="cam">{media(f"br{i}{k}", psrc, po, s0-0.3, 0.3+0.01*k)}</div></div>')
                    J.append(f'tl.set("#br{i}_{k}",{{visibility:"visible"}},{s0-0.3:.3f});tl.set("#br{i}_{k}",{{visibility:"hidden"}},{s0:.3f});')
                    J.append(f'tl.fromTo("#br{i}_{k}",{{x:0,rotation:0}},{{x:{dx*1150},rotation:{dx*4},duration:.3,ease:"power3.in"}},{s0-0.3+0.02*k:.3f});')
                # scene baru mesti kelihatan di bawah jalur
                J.append(f'tl.set("#{W}",{{visibility:"visible"}},{s0-0.3:.3f});')
            sfx(s0 - (0.3 if tr == "break" else 0.05), "camera_shutter" if tr == "break" else TRSFX[tr])
        # overlay
        if s.get("ov"):
            l1, l2 = s["ov"]
            a0 = s0 + td + 0.12; nxt = sc[i+1] if i + 1 < len(sc) else None
            e0 = (st[i+1] - (0.3 if nxt and nxt["tr"] == "break" else 0) if nxt else DUR) - 0.12
            top = 150 if s["t"] in ("phone3d", "polaroid", "collage") else (210 if cfg["pos"] == "C" else 225)
            pos = "C" if s["t"] in ("phone3d", "polaroid", "collage", "split") else cfg["pos"]
            H.append(overlay(i, cfg["text"], pos, top, l1, l2, i))
            J.extend(text_anim(cfg["text"], f"#w{i}", a0, e0, l1, l2, s.get("count")))
            sfx(a0, cfg["sfx"]["text"])
            if s.get("usp"): sfx(a0 + 0.2, cfg["sfx"]["usp"])
    # hook
    k, h1, h2 = cfg["hook"]
    H.append(hook_html(cfg["text"], k, h1, h2))
    J.extend(text_anim(cfg["text"], "#hook", 0.25, 2.75, h1, h2, None, hook=True))
    sfx(0.05, cfg["sfx"]["hook"][0], .38); sfx(0.3, cfg["sfx"]["hook"][1])
    html = f'''<!doctype html>
<html><head><meta charset="utf-8"><title>Karpet {key.upper()} — {cfg["name"]}</title>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{DUR}" data-fps="30">
{chr(10).join(H)}
{chr(10).join(A)}
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script>
const tl=gsap.timeline({{paused:true}});
gsap.set(".tx .ch,.tx .wd",{{opacity:0}});
{chr(10).join(J)}
tl.set({{}},{{}},{DUR});
window.__timelines=window.__timelines||{{}};window.__timelines["root"]=tl;
</script>
</body></html>'''
    import os
    d = f"variants/{key}"; os.makedirs(d, exist_ok=True)
    for l in ("assets", "sfx"):
        if not os.path.islink(f"{d}/{l}"): os.symlink(f"../../{l}", f"{d}/{l}")
    open(f"{d}/index.html", "w").write(html)
    return DUR

def chars(s):  # untuk gaya B (taip)
    return "".join(f'<span class="ch">{c if c != " " else "&nbsp;"}</span>' for c in s)
def words(s):
    return " ".join((f'<span class="wd" data-n="{w}">{w}</span>' if w.isdigit() else f'<span class="wd">{w}</span>') for w in s.split(" "))

def overlay(i, style, pos, top, l1, l2, idx):
    if style == "A":
        body = f'<i class="vl"></i><div class="l1"><span class="tx">{l1}</span></div><div class="l2"><span class="tx">{l2}</span></div>'
    elif style == "B":
        body = f'<div class="l1"><span class="tx">{chars(l1)}</span></div><div class="l2"><span class="tx">{chars(l2)}</span><i class="cur"></i></div>'
    elif style == "C":
        body = f'<div class="l1"><span class="tx">{words(l1)}</span></div><div class="l2"><span class="tx">{words(l2)}</span></div>'
    else:
        body = f'<div class="ix"><b class="num">{idx:02d}</b><i class="hl"></i></div><div class="l1 m"><span class="tx">{l1}</span></div><div class="l2 m"><span class="tx">{l2}</span></div>'
    return f'<div id="w{i}" class="word st{style} {pos}" style="top:{top}px;visibility:hidden"><b class="gl"></b>{body}</div>'

def hook_html(style, k, h1, h2):
    if style == "B": l1, l2 = chars(h1), chars(h2)
    elif style == "C": l1, l2 = words(h1), words(h2)
    else: l1, l2 = h1, h2
    cur = '<i class="cur"></i>' if style == "B" else ""
    vl = '<i class="vl"></i>' if style == "A" else ""
    cls = "L" if style in ("A", "D") else "C"
    m = " m" if style == "D" else ""
    return (f'<div id="hook" class="hook st{style} {cls}"><b class="gl"></b>{vl}'
            f'<div class="l1 big{m}"><span class="tx">{l1}</span></div><div class="l2 big{m}"><span class="tx">{l2}</span>{cur}</div></div>')

def text_anim(style, sel, a, e, l1, l2, count, hook=False):
    J = []
    J.append(f'tl.fromTo("{sel} .gl",{{opacity:0}},{{opacity:1,duration:.35}},{a-0.05:.2f});tl.to("{sel} .gl",{{opacity:0,duration:.3}},{e-0.3:.2f});')
    if style == "A":
        J.append(f'tl.fromTo("{sel} .vl",{{scaleY:0}},{{scaleY:1,duration:.4,ease:"expo.out"}},{a:.2f});')
        J.append(f'tl.fromTo("{sel} .tx",{{opacity:0,x:-28}},{{opacity:1,x:0,duration:.5,ease:"expo.out",stagger:.1}},{a+0.08:.2f});')
        J.append(f'tl.to("{sel} .tx",{{opacity:0,x:16,duration:.22,ease:"power2.in",stagger:.04}},{e-0.28:.2f});tl.to("{sel} .vl",{{scaleY:0,duration:.25,ease:"power2.in"}},{e-0.25:.2f});')
    elif style == "B":
        n1 = len(l1); n2 = len(l2)
        J.append(f'tl.set("{sel} .tx",{{opacity:1}},{a:.2f});')
        J.append(f'tl.fromTo("{sel} .l1 .ch",{{opacity:0}},{{opacity:1,duration:.01,stagger:.035}},{a:.2f});')
        J.append(f'tl.fromTo("{sel} .l2 .ch",{{opacity:0}},{{opacity:1,duration:.01,stagger:.035}},{a+n1*0.035+0.05:.2f});')
        J.append(f'tl.fromTo("{sel} .cur",{{opacity:0}},{{opacity:1,duration:.01}},{a:.2f});')
        k = a + 0.1
        while k < e - 0.3:
            J.append(f'tl.to("{sel} .cur",{{opacity:0,duration:.01}},{k+0.3:.2f});tl.to("{sel} .cur",{{opacity:1,duration:.01}},{k+0.55:.2f});'); k += 0.5
        J.append(f'tl.to("{sel} .ch,{sel} .cur",{{opacity:0,duration:.01,stagger:{{each:.012,from:"end"}}}},{e-0.35:.2f});')
    elif style == "C":
        J.append(f'tl.fromTo("{sel} .wd",{{opacity:0,filter:"blur(14px)",scale:1.25}},{{opacity:1,filter:"blur(0px)",scale:1,duration:.45,ease:"power3.out",stagger:.09}},{a:.2f});')
        J.append(f'tl.to("{sel} .wd",{{opacity:0,filter:"blur(10px)",duration:.25,ease:"power2.in",stagger:.03}},{e-0.3:.2f});')
        if count:
            J.append(f'(function(){{const els=[...document.querySelectorAll("{sel} [data-n]")];const o={{p:0}};tl.fromTo(o,{{p:0}},{{p:1,duration:.9,ease:"power2.out",onUpdate:()=>els.forEach(el=>el.textContent=Math.round(+el.dataset.n*o.p))}},{a:.2f});}})();')
    else:
        J.append(f'tl.fromTo("{sel} .num",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.35,ease:"expo.out"}},{a:.2f});')
        J.append(f'tl.fromTo("{sel} .hl",{{scaleX:0}},{{scaleX:1,duration:.5,ease:"expo.out"}},{a+0.05:.2f});')
        J.append(f'tl.fromTo("{sel} .m .tx",{{opacity:1,yPercent:110}},{{opacity:1,yPercent:0,duration:.5,ease:"expo.out",stagger:.1}},{a+0.12:.2f});')
        J.append(f'tl.to("{sel} .m .tx",{{yPercent:-110,duration:.25,ease:"power2.in",stagger:.04}},{e-0.3:.2f});tl.to("{sel} .num,{sel} .hl",{{opacity:0,duration:.25}},{e-0.28:.2f});')
    if hook:
        J.append(f'tl.set("{sel}",{{visibility:"hidden"}},{e+0.05:.2f});')
    else:
        J.append(f'tl.set("{sel}",{{visibility:"visible"}},{a-0.05:.2f});tl.set("{sel}",{{visibility:"hidden"}},{e+0.02:.2f});')
    return J

if __name__ == "__main__":
    for k, c in V.items():
        print(k, c["name"], build(k, c), "s")
