import json,sys
STAR='<svg class="ico" viewBox="0 0 24 24" width="0.9em" height="0.9em"><path fill="#fff" d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6L2.5 9.4l6.6-.8z"/></svg>'
BAG='<svg class="ico" viewBox="0 0 24 24" width="1.05em" height="1.05em"><path fill="#FFC21A" d="M5 7.5h14l-1.1 12.2a2 2 0 0 1-2 1.8H8.1a2 2 0 0 1-2-1.8z"/><path d="M8.6 9.5V7a3.4 3.4 0 0 1 6.8 0v2.5" fill="none" stroke="#FFC21A" stroke-width="1.8" stroke-linecap="round"/></svg>'
TAP='<span class="tapwrap"><span id="ripple"></span><svg id="bagbig" viewBox="0 0 24 24" width="128" height="128"><path fill="#FFC21A" d="M5 7.5h14l-1.1 12.2a2 2 0 0 1-2 1.8H8.1a2 2 0 0 1-2-1.8z"/><path d="M8.6 9.5V7a3.4 3.4 0 0 1 6.8 0v2.5" fill="none" stroke="#FFC21A" stroke-width="1.8" stroke-linecap="round"/></svg><svg id="hand" viewBox="0 0 24 24" width="104" height="104"><path fill="#fff" stroke="rgba(0,0,0,.35)" stroke-width="0.6" d="M10 7.5c0-.83.67-1.5 1.5-1.5S13 6.67 13 7.5v6h.76c.19 0 .37.04.54.11l4.54 2.26c.53.22.91.76.91 1.38 0 .06-.01.13-.02.2l-.75 5.27c-.11.73-.69 1.28-1.44 1.28h-6.79c-.41 0-.79-.17-1.06-.44L4.75 18.62l.79-.8c.2-.2.48-.33.79-.33.09 0 .16.02.24.03l3.43.72z"/></svg></span>'
G=[ # start,end,line1,line2,big
 (0.10,1.42,"Earbuds ni tahan","100 JAM?!",True),
 (1.55,2.92,"8 jam sekali cas,","100 jam + casing",False),
 (3.05,4.18,"Call selalu bising?","",False),
 (4.25,5.42,"Quad-Mic ENC","suara jelas, bising hilang",False),
 (5.55,6.95,"Bluetooth 5.4","pair laju & stabil",False),
 (7.05,8.42,"Gaming mode","main game tak lag",False),
 (8.55,9.95,"Ringan 3.0g sebelah","selesa pakai lama",False),
 (10.05,11.42,"IPX5","kalis peluh & hujan",False),
 (11.55,12.92,"Dalam kotak siap","ear tips spare",False),
 (13.05,14.42,"+ kabel cas","boleh wireless charging",False),
 (14.55,15.95,"[STAR] 4.6 rating","12.7K terjual",False),
 (16.05,18.0,"[TAP]","ada 5 warna tau!",False),
]
CUTS=[0,1.5,3.0,5.5,8.5,11.5,13.0,14.5,18.0]
PUNCH=[0.60,4.25,16.05]
def words(s): return [w for w in s.split(' ') if w]
html=[];js=[]
for gi,(a,b,l1,l2,big) in enumerate(G):
    t=a; spans=[]
    for li,line in enumerate([l1,l2]):
        if not line: continue
        if li==1: t+=0.04
        ws=words(line)
        if big and li==1: ws=[line]  # chunk emphasis
        parts=[]
        for w in ws:
            inner=w.replace('[STAR]',STAR).replace('[BAG]',BAG).replace('[TAP]',TAP)
            wid=f"w{gi}_{len(spans)}"; spans.append((wid,round(t,3)))
            parts.append(f'<span class="w" id="{wid}">{inner}</span>')
            t+=0.06
        cls="l1" if li==0 else ("l2 big" if big else "l2")
        if li==0 and big: cls="l1"
        parts=" ".join(parts)
        html.append(None) if False else None
        spans_html=parts
        if li==0: g1=f'<div class="{cls}">{spans_html}</div>'
        else: g2=f'<div class="{cls}">{spans_html}</div>'
    body=g1+(g2 if l2 else '')
    if not l2: g2=''
    html.append(f'<div id="g{gi}" class="cap clip" data-start="{a}" data-duration="{round(b-a,3)}" data-track-index="2">{body}</div>')
    for wid,wt in spans:
        js.append(f'tl.fromTo("#{wid}",{{opacity:0,y:22,scale:0.82}},{{opacity:1,y:0,scale:1,duration:0.2,ease:"back.out(2.6)"}},{wt});')
    if b<17.9: js.append(f'tl.to("#g{gi}",{{opacity:0,y:-10,duration:0.12,ease:"power2.in"}},{round(b-0.12,3)});')
for tt in (16.45,17.0,17.55):
    js.append(f'tl.fromTo("#hand",{{x:0,y:0,scale:1}},{{x:-10,y:-12,scale:0.86,duration:0.1,ease:"power2.in"}},{tt});')
    js.append(f'tl.to("#hand",{{x:0,y:0,scale:1,duration:0.18,ease:"power2.out"}},{round(tt+0.1,2)});')
    js.append(f'tl.fromTo("#bagbig",{{scale:1}},{{scale:0.9,duration:0.1,yoyo:true,repeat:1,ease:"power1.inOut"}},{tt});')
    js.append(f'tl.fromTo("#ripple",{{scale:0.5,opacity:0.9}},{{scale:1.5,opacity:0,duration:0.45,ease:"power2.out"}},{round(tt+0.08,2)});')
# camera: snap on cuts, slow drift per seg, punches
for i in range(len(CUTS)-1):
    a,b=CUTS[i],CUTS[i+1]
    js.append(f'tl.fromTo("#drift",{{scale:1}},{{scale:1.045,duration:{b-a},ease:"none"}},{a});')
    if i>0:
        js.append(f'tl.fromTo("#snap",{{scale:1.09}},{{scale:1,duration:0.34,ease:"power3.out"}},{a});')
        js.append(f'tl.fromTo("#flash",{{opacity:0.32}},{{opacity:0,duration:0.14,ease:"power1.out"}},{a});')
for p in PUNCH:
    end=min(c for c in CUTS if c>p)
    js.append(f'tl.fromTo("#punch",{{scale:1}},{{scale:1.06,duration:0.22,ease:"power2.out"}},{p});')
    if end<18: js.append(f'tl.set("#punch",{{scale:1}},{end});')
tpl=open(sys.argv[1]).read()
open(sys.argv[2],'w').write(tpl.replace('<!--CAPS-->',"\n      ".join(html)).replace('//JS',"\n      ".join(js)))
