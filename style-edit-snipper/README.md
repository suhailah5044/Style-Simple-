# Snipper — Beg Sekolah Waterproof (3 versi, HyperFrames 9:16)

Footage sama dengan session "SNIPPER - Beg Sekolah". Warna footage TAK diubah, tiada filter (bt709, crf 14).
Fail `*/assets/footage.mp4` & `pip*.mp4` tak masuk git (besar) — jana semula dengan `make.py`.

| | V1 – Demo Air | V2 – Bukti 2 Tahun | V3 – Mak & Anak |
|---|---|---|---|
| Hook 0–3s | "Tengok dia tak tembus ke dalam" + b-roll air | "Tahan lasak, dah dua tahun saya pakai" | "Anak kita memang lasak" |
| Teks hook | Pill kaca: *Beg Sekolah Waterproof* | Tag *Tahan Lasak · 2 Tahun* + kotak *Beg Sekolah Waterproof* | *Anak Lasak?* → *Beg Sekolah Waterproof* |
| Intro | Snipper, repeat setiap tahun | Plain → corak | Anak memang suka → Snipper |
| USP | Water resistant, kompartmen, jahitan, span | Design, kompartmen, Combo + Pencil Box, water resistant | Water resistant, selesa, sekolah/travel, saiz, combo |
| CTA (tiada overlay) | Bakul kuning harga murah → warna masih ada, grab | Sangat recommend → harga murah | Warna cantik masih ada, cepat grab |
| Gaya overlay | Titik + wipe | Chip outline | Bar tegak kiri |
| Frame break bg | Navy dot | Navy garis serong | Slate grid |

Semua: Lexend Mega kecil (27px, sub 16px) putih, di ruang kosong kabinet atas, tak tutup produk. ~50% ayat sahaja diberi overlay.

## Audio
Speed 1.1, pause dalaman > 0.22s dibuang, gagap/ayat ulang dipotong, highpass + compressor + loudnorm -11 LUFS (suara lebih kuat).

## SFX (`sfx4.py`, set baru stereo)
hook1/2/3 (lain setiap video), whoosh_a/b (tukar footage), ui_prompt1/2/3 (overlay), pop2, click2, ting2/ding2 (USP), impact2 (soft impact), droplet (air), zip (kompartmen), shimmer (design), pip_swish, fbreak, cta_rise.

## Cara guna
```
python3 sfx4.py
RAW=raw.mov AUD=audio16k.wav python3 make.py v1   # (v2, v3)
cd v1 && npx hyperframes lint . && npx hyperframes preview .
npx hyperframes render . -q delivery --video-frame-format png -o ../../video/Snipper_V1_FINAL.mp4
```
Ubah ayat/overlay dalam `variants.py`, kemudian `python3 make.py v1 --html` (tanpa potong semula footage).
