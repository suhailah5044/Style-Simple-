# Style Edit — Kemeja Bazla Cotton Linen (TikTok 9:16, ±19s)

Pipeline ffmpeg + Python (Pillow). Warna footage asal dikekalkan.

## Warna (penting)
- B-roll iPhone = HDR HLG (bt2020). Tukar ke SDR bt709 guna tone-map:
  `zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv`
- Semua tukaran RGB guna matriks bt709 (`in_color_matrix=bt709` / `out_color_matrix=bt709`) dan output ditag bt709.

## Langkah
1. `tr.py` (faster-whisper, `ms`) → `words.json` untuk timing perkataan.
2. `base.py` — potong A-roll (`A`: buang pause/ulang, hook dulu) + B-roll skrin penuh fade 0.25s (`B`).
3. `music.py` — muzik latar 118bpm (dijana sendiri), ducking automatik bawah suara.
4. `render.py <skala> <out>` — zoom punch (`PUNCH`), teks Lexend Mega 30px putih + bayang (`O`), pill untuk fakta, SFX dari `style-edit-standphone-v2/sfx`.
   Preview: `python3 render.py 0.5 preview.mp4` · Final: `python3 render.py 1 final.mp4`

Teks diletak di ruang kosong (kiri/kanan atas kepala, `top:250px`, 70px dari tepi), dalam safe zone TikTok/IG, tak tutup baju/tangan.
