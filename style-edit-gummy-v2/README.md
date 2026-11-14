# Style Edit v2 — Gummy Turkey

Sama gaya dengan `style-edit-standphone-v2/` (intro Italianno + subtitle kata kunci Lexend Mega + garis putih, zoom, SFX UI). Footage 9:16 1080x1920, 113.6s, tiada filter warna.

## Beza dari v2 asal
- Intro (hook): "Gummy Turkey / masam tapi sedap!" guna Lexend Mega 800 (46px + 32px), bukan Italianno.
- 34 overlay kata kunci dari transkrip (lihat senarai `O` dalam `build.py`).
- Medan ke-7 pilihan dalam `O` = `top` px. Shot close-up 87–107s guna `top:120px` supaya teks tak kena muka.
- Subtitle lebih tebal: Lexend Mega 800, 34px, garis 60x4px.
- Zoom keluar intro dipendekkan (0.2s) supaya tak bertindih dengan overlay pertama.

## Cara guna
`python3 tr.py` → edit `O` dalam `build.py` → `python3 build.py` → `npx hyperframes lint .` → `npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`.

`assets/footage.mp4` (188MB) tak dicommit — tukar dari .mov asal: `ffmpeg -i in.mov -c:v libx264 -crf 15 -pix_fmt yuv420p -c:a aac assets/footage.mp4`.
