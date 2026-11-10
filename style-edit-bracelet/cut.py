# Edit decision list: buang ulangan/gagap + auto buang pause > 0.4s
import json,subprocess,sys
W=json.load(open(sys.argv[1]))
KEEP=[(1.2,8.5),(14.7,18.4),(18.4,23.65),(28.9,32.35),(43.3,51.3),(51.6,55.58),
      (60.1,65.0),(66.7,72.9),(75.3,77.9),(84.1,86.9),(90.7,94.3),(97.45,101.6),
      (102.1,106.9),(110.4,115.5)]
segs=[]
for a,b in KEEP:
    ws=[w for w in W if w[0]>=a-0.05 and w[0]<b]
    cur=[ws[0][0],ws[0][1]]
    for s,e,_ in ws[1:]:
        if s-cur[1]>0.4: segs.append(cur); cur=[s,e]
        else: cur[1]=e
    segs.append(cur)
segs=[(max(0,s-0.08),e+0.12) for s,e in segs]
json.dump(segs,open("segs.json","w"))
print(len(segs),round(sum(e-s for s,e in segs),2))
