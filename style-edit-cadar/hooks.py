# Versi "hook paling kuat di depan": footage sama, disusun semula (V3-V6).
# python3 hooks.py cut v3   -> assets/footage_v3.mp4 (potong + sambung, fade audio 20ms)
# build.py v3 guna plan() dari sini.
import subprocess, sys

# Sempadan segmen (ikut senyap antara ayat & cut asal footage)
B = [0, 4.80, 9.43, 14.23, 19.70, 23.23, 27.70, 30.10, 35.20, 37.58, 41.45, 45.05, 49.30, 50.73]
# Teks kata kunci untuk setiap segmen (posisi = ruang kosong yang disemak pada setiap shot)
TXT = {
 1: ("Premium Soft Fabric", "L:470"),
 2: ("Sejuk &amp; Lembut!", "L:380"),
 3: ("Floral Design,<br>So Aesthetic!", "L:380"),
 4: ("Warna Tak<br>Mudah Luntur", "L:560"),
 5: ("Tak Berbulu!", "L:400"),
 6: ("Getah 360°<br>Keliling", "R:300"),
 7: ("Machine Wash<br>Friendly", "L:430"),
 10: ("Fit Kemas,<br>Tak Mudah Tercabut", "L:600"),
 11: ("Easy Care,<br>Tahan Lama", "L:470"),
 12: ("Bilik Terus<br>Nampak Classy!", "C:410"),
}
INNER_CUTS = [6.90, 10.93, 25.10, 27.93, 45.13]  # cut asal di dalam segmen

# Segmen 8 (test fit) & 9 (seriously cantik) dibuang supaya lebih padat.
VAR = {
 # hook (2 baris), top px, susunan segmen
 "v3": (("Beli kat mall pun", "tak dapat harga ni!"), 420, [3, 1, 2, 4, 5, 6, 7, 10, 11, 12, 13]),
 "v4": (("Pasang je, terus", "fit &amp; kemas!"), 420, [10, 1, 2, 3, 4, 5, 6, 7, 11, 12, 13]),
 "v5": (("1 set dapat", "3 helai terus!"), 280, [6, 7, 1, 2, 3, 4, 5, 10, 11, 12, 13]),
 "v6": (("Dah basuh,", "warna tak luntur!"), 420, [4, 1, 2, 3, 5, 6, 7, 10, 11, 12, 13]),
}

def seg(k): return B[k - 1], B[k]

def plan(v):
    hook, htop, order = VAR[v]
    t = 0.0; O = []; cuts = []; prev = None; sfx = ["soft_chime", "soft_tap"]
    for n, k in enumerate(order):
        a, b = seg(k); d = b - a
        if prev is not None and seg(prev)[1] != a:
            cuts.append(round(t, 2))  # sambungan baru = tukar scene
        cuts += [round(t + c - a, 2) for c in INNER_CUTS if a + 0.15 < c < b - 0.15]
        if n > 0 and k in TXT:
            end = t + d
            if k == 12 and n + 1 < len(order) and order[n + 1] == 13:
                end += B[13] - B[12]
            s = "soft_sparkle" if k == 12 else sfx[len(O) % 2]
            O.append([round(t + 0.15, 2), round(end - 0.1, 2), TXT[k][0], TXT[k][1], s])
        t += d; prev = k
    hend = 3.0
    if v == "v5":  # close-up bucu (cut 1.87s) penuh dengan produk: hook hanya dalam shot katil penuh
        hend = 1.6
        O.insert(0, [2.02, round(B[6] - B[5] - 0.1, 2), TXT[6][0], "R:220", "soft_tap"])
    return round(t, 2), hook, htop, O, cuts, hend

def cut(v):
    order = VAR[v][2]; f = []; parts = []
    for i, k in enumerate(order):
        a, b = seg(k); d = b - a
        f.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];"
                 f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={d-0.02:.3f}:d=0.02[a{i}];")
        parts.append(f"[v{i}][a{i}]")
    fc = "".join(f) + "".join(parts) + f"concat=n={len(order)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/footage.mp4", "-filter_complex", fc,
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "15", "-preset", "fast",
                    "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", f"assets/footage_{v}.mp4"], check=True)

if __name__ == "__main__" and sys.argv[1] == "cut":
    cut(sys.argv[2])
