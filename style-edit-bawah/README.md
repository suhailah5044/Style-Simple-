# Style Bawah v2 — Tiru Penuh Gaya Rujukan (Baju Kurung)

Template HyperFrames 9:16 (1080x1920). Warna footage asal tak diubah.

## Gaya
- **Tajuk kuning besar** (`#F5DE6E`, *Gochi Hand* 110–175px, tekstur kasar guna SVG `feTurbulence`):
  - Muncul **huruf demi huruf** (`stagger .045s`, `scale .3→1`, `back.out(2.2)`), ada yang **melengkung** (`arc`) atau **condong** (`rotate`).
  - Diletak keliling kepala / ruang kosong atas. Bunyi **scribble** (pen menulis) setiap kali keluar.
  - Hook (0–7s) = tajuk jualan baru: *baju raya → Bawah RM100* · *tapi nampak → Mahal, gila!* · *siap buat badan → Nampak Kurus!* · *jangan sampai → Sold Out*. Penekanan lain: *Sangat Cantik*, *Chiffon*, *Soft Brocade*, *Bawah RM100*, *Cepat-Cepat grab!*
- **Perkataan putih kecil condong** di sisi (46px) — pop `scale .55→1` + bunyi **pop**.
- **Kapsyen putih kecil** frasa demi frasa, diletak **ATAS** (`top:205px`) supaya tak tutup baju.
- **Kamera**: statik — tiada zoom / blur / potongan laju (atas permintaan).
- **Muzik latar** lofi lembut (Rhodes + bass + hat, 78 BPM) volume 0.14, berhenti bila cakap habis.
- **Penutup**: video gelap 70%, senyap sekejap → **boom** dalam, tajuk "cepat grab!" berkelip putih/kuning + "sebelum sold out".
- Tiada ikon IG / nama brand (atas permintaan).

> Huruf besar "G" dalam Gochi Hand nampak macam "6" — guna "g" kecil.

## Cara guna
1. Audio → `python3 tr.py` (model `medium`) → `words_m.json`.
2. Edit dalam `build.py`: `G` (kumpulan tajuk: `[masa, "y"|"w", teks, x, y, rotate, saiz, arc]`), `P` (kapsyen), `CUT`, `BLUR`.
3. `python3 sfx3.py` (jana SFX + muzik) → `python3 build.py`.
4. `npx hyperframes snapshot . --at 1,7.1,30` untuk semak → `npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`.

Lesen font: Gochi Hand — SIL OFL (Google Fonts). SFX & muzik dijana sendiri (`sfx3.py`), bebas guna.

## Varian hook "cold open" (momen paling kuat di depan)
`HOOK=A python3 build.py` / `HOOK=B python3 build.py` (tanpa `HOOK` = v2). Salinan disimpan `index_A.html`, `index_B.html`.
- **A — Harga**: klip 53.44–57.84s diletak depan ("sangat-sangat murah, bawah RM100 je… kurung yang cantik macam ni") → *Murah!* · *Bawah RM100* · *Secantik Ini!* → video penuh dari 0s.
- **B — Badan kurus**: klip 22.36–25.54s di depan ("cutting dia memang sangat-sangat cantik sebab dia bagi kita efek yang kurus") → *Cantik gila!* · *Nampak Kurus!* → video penuh.
- Dalam A/B, 0–7s video asal guna kapsyen biasa + tajuk kuning *Sold Out*.
