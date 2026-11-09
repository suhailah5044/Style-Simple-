"""Phone Holder v2 — susun semula footage + overlay kecil (gaya repo Kasut-Sekolah).
Guna:  python3 build.py SRC.mov OUT.mp4 [--preview]
--preview = 540x960 laju (jimat), tanpa --preview = 1080x1920 final.
Tiada muzik. Audio = suara asal (dibersihkan) + 'ting' perlahan.
"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "assets", "Cweyons-Regular.ttf")
SRC, OUT = sys.argv[1], sys.argv[2]
PREVIEW = "--preview" in sys.argv
W, H = (540, 960) if PREVIEW else (1080, 1920)
K = W / 1080

# Susunan baru (src_start, src_end, label)
SEG = [
    (58.10, 60.52, "HOOK: phone tergantung terbalik, memang melekat jangan risau jatuh"),
    (4.34, 7.10, "ramai tanya cara pasang"),
    (7.45, 16.90, "open = longgar, ketatkan balik"),
    (17.35, 29.25, "lekat, pusing, memang melekat"),
    (30.30, 35.95, "tarik sekuat hati, tak tercabut, so far okey"),
    (36.28, 39.45, "worth it, puas hati"),
    (39.68, 57.75, "tanggal, tangkai panjang, allen key, senang"),
    (60.96, 73.20, "casing magnetic"),
    (79.85, 84.95, "masa drive, pusing 360"),
    (73.40, 79.55, "nak dapatkan, harga murah"),
    (85.55, 92.45, "CTA: memang recommend, kuat"),
]
# jeda dalam segmen (silencedetect -32dB) -> dipendekkan ke 0.12s
SIL = [(9.923, 10.405), (12.953, 13.330), (18.306, 18.750), (19.532, 20.130), (21.063, 21.655),
       (26.796, 27.406), (48.635, 49.084), (49.330, 49.731), (54.466, 54.913), (60.517, 61.018),
       (64.876, 65.417), (68.844, 69.197), (81.504, 82.144), (90.778, 91.295)]
GAP = 0.12

R = []  # [s, e]
for s, e, _ in SEG:
    cur = s
    for a, b in SIL:
        if s < a and b < e:
            m = (a + b) / 2
            R.append([cur, round(m - GAP / 2, 3)]); cur = round(m + GAP / 2, 3)
    R.append([cur, e])
outs, t = [], 0.0
for s, e in R:
    outs.append(t); t += e - s
DUR = round(t, 3)


def o(src):
    for (s, e), os_ in zip(R, outs):
        if s - 1e-6 <= src <= e + 1e-6:
            return round(os_ + src - s, 3)
    return min(os_ for (s, e), os_ in zip(R, outs) if s > src)


HOOK = ("phone terbalik pun tak jatuh", 0.10, 2.40)
# overlay kecil: (src masa perkataan, teks)  — font tiada nombor / '&'
KW = [
    (4.58, "ramai tanya cara pasang"),
    (8.40, "pusing ke open"),
    (10.60, "longgarkan sambungan"),
    (13.50, "ketatkan balik"),
    (20.20, "lekat dulu"),
    (22.20, "pusing dan lekat"),
    (27.40, "memang melekat"),
    (31.60, "tarik kuat pun tak tercabut"),
    (36.32, "worth it, puas hati"),
    (39.70, "nak tanggal? tarik je"),
    (43.90, "tangkai dia panjang"),
    (46.60, "yang lain pendek"),
    (49.80, "siap ada allen key"),
    (55.80, "senang gila"),
    (61.10, "casing tak magnetic?"),
    (63.30, "dapat magnetic sekali"),
    (80.00, "senang masa drive"),
    (83.40, "boleh pusing penuh"),
    (77.84, "harga murah je"),
    (85.60, "memang recommend"),
    (88.40, "kuat dan steady"),
]
items = sorted((o(s), txt) for s, txt in KW)
ov = []
for i, (st, txt) in enumerate(items):
    nxt = items[i + 1][0] if i + 1 < len(items) else DUR
    ov.append((st, round(min(2.4, nxt - st - 0.15), 3), txt))

FS_HOOK, FS = round(50 * K), round(38 * K)
Y = round(250 * K)


def dt(txt, s, d, fs):
    e = s + d
    a = f"if(lt(t,{s}+0.4),(t-{s})/0.4,if(gt(t,{e}-0.3),({e}-t)/0.3,1))"
    yy = f"{Y}+{round(14*K)}*(1-min(1,(t-{s})/0.4))"
    return (f"drawtext=fontfile='{FONT}':text='{txt}':fontsize={fs}:fontcolor=white:"
            f"shadowcolor=black@0.35:shadowx=0:shadowy={max(1,round(2*K))}:"
            f"x=(w-text_w)/2:y='{yy}':alpha='{a}':enable='between(t,{s},{e})'")


# Langkah 1: potong satu-satu (jimat memori), punch-in selang-seli sembunyikan jump cut
import tempfile
TMP = tempfile.mkdtemp()
lst = []
for i, (s, e) in enumerate(R):
    z = 1.0 if i % 2 == 0 else 1.045
    sc = f"scale={round(W*z/2)*2}:{round(H*z/2)*2},crop={W}:{H}" if z != 1.0 else f"scale={W}:{H}"
    p = os.path.join(TMP, f"c{i:02d}.mkv")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s), "-to", str(e), "-i", SRC,
                    "-vf", f"{sc},setsar=1,fps=30", "-af", f"afade=t=in:d=0.008,afade=t=out:st={e-s-0.008:.3f}:d=0.008",
                    "-c:v", "libx264", "-preset", "ultrafast" if PREVIEW else "veryfast", "-crf", "28" if PREVIEW else "14",
                    "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", p], check=True)
    lst.append(f"file '{p}'")
open(os.path.join(TMP, "list.txt"), "w").write("\n".join(lst))
CUT = os.path.join(TMP, "cut.mkv")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(TMP, "list.txt"), "-c", "copy", CUT], check=True)
n = len(R)
fc = []
txt = [dt(HOOK[0], HOOK[1], HOOK[2] - HOOK[1], FS_HOOK)] + [dt(x, s, d, FS) for s, d, x in ov]
fc.append("[0:v]" + ",".join(txt) + "[vo]")
# suara: bersihkan + kuatkan; ting perlahan pada setiap overlay
fc.append("[0:a]highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150,loudnorm=I=-15:TP=-1.5:LRA=9,aresample=48000[voice]")
sfx = [(HOOK[1], "sfx_ting", 0.35)] + [(s, "sfx_ting" if i % 2 == 0 else "sfx_ting_hi", 0.22) for i, (s, d, x) in enumerate(ov)]
inputs = ["-i", CUT]
mixin = ["[voice]"]
for j, (s, name, vol) in enumerate(sfx):
    inputs += ["-i", os.path.join(HERE, "sfx", name + ".wav")]
    fc.append(f"[{j+1}:a]volume={vol},adelay={int(s*1000)}|{int(s*1000)}[s{j}]")
    mixin.append(f"[s{j}]")
fc.append("".join(mixin) + f"amix=inputs={len(mixin)}:normalize=0:duration=first[ao]")
open(os.path.join(HERE, "filter.txt"), "w").write(";\n".join(fc))
venc = ["-c:v", "libx264", "-preset", "ultrafast" if PREVIEW else "medium", "-crf", "28" if PREVIEW else "20",
        "-pix_fmt", "yuv420p", "-r", "30"]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "4", *inputs, "-filter_complex_script", os.path.join(HERE, "filter.txt"),
                "-map", "[vo]", "-map", "[ao]", *venc, "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", OUT], check=True)
print(f"durasi {DUR}s, {n} potongan, {len(ov)} overlay")
print(f"  0.10  hook: {HOOK[0]}")
for s, d, x in ov:
    print(f"  {s:6.2f} +{d:.2f}  {x}")
