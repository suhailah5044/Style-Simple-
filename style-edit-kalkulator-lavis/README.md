# Style Edit — Kalkulator Solar + Bracelet Lavis (3 video)

Gaya sama macam `style-edit-standphone-v2` (hook Italianno, subtitle Lexend Mega + garis putih, SFX UI, zoom in/out/punch). Footage asal tiada filter.

| Video | Footage | Hook 0–3s |
|---|---|---|
| v1 | Footage 1 (kalkulator) | *Tak payah beli bateri / lagi dah lepas ni!* |
| v2 | Footage 2 (bracelet Lavis) | *Pakai hari-hari pun / tak hitam langsung!* |
| v3 | Combine 1+2 | *2 barang murah / yang saya tak menyesal beli!* |

## Aliran
1. `cut.py work/vN.json work/vN.mp4` — buang pause (silencedetect −32dB) & take gagap/ulang (senarai `keep`), titik potong di-snap ke tenaga audio paling rendah, fade audio 12ms, zoom selang-seli 1.00/1.07 sorok jump cut.
2. Salin `work/vN.mp4` → `vN/assets/footage.mp4`.
3. Edit overlay dalam `videos.py` → `python3 build.py`.
4. Preview: `npx hyperframes render vN -q draft -o preview/vN_PREVIEW.mp4`
5. Final: `npx hyperframes render vN -q delivery --video-frame-format png -o ../video/...FINAL.mp4`
