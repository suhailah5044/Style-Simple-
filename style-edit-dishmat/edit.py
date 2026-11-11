# Edit decision list. Masa dalam saat sumber (main = video utama, broll = B-roll).
SPEED=1.1
# Segmen ucapan yang disimpan (buang senyap, gagap, ayat ulang)
SEGS=[(5.95,10.95),(11.15,18.15),(30.75,44.70),(44.75,49.35),(53.0,57.2),(57.25,62.85),(76.85,85.65),(88.9,113.95)]
# Cutaway visual (masa sumber main ucapan mula, tamat) -> (fail, masa mula visual). Audio tetap suara utama.
CUT=[((14.5,18.15),("main",23.0)),     # countertop basah -> tunjuk mat atas counter
     ((44.75,49.35),("broll",30.0)),   # tak rosak / berkulat -> demo atas counter
     ((55.96,57.2),("broll",11.0)),    # design -> close-up alur
     ((57.25,60.45),("broll",15.2)),   # design kemas -> tunjuk mat
     ((98.7,101.9),("broll",38.0)),    # letak sebelah sinki
     ((104.32,107.1),("broll",20.5))]  # harga murah, banyak kegunaan
def cut_t(t):
    c=0
    for a,b in SEGS:
        if a<=t<=b: return c+(t-a)
        c+=b-a
    raise ValueError(t)
def out_t(t): return round(cut_t(t)/SPEED,3)
TOTAL_CUT=sum(b-a for a,b in SEGS)
DUR=round(TOTAL_CUT/SPEED,2)
