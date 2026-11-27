# Style Edit — Flower Bracelet v2 (intro lain dari v1)

Gaya Misty sama macam `style-edit-flower/`, tapi intro berbeza:
- **Intro suara**: buka dengan ayat "Nampak mahal. Harga murah je tapi bila kita pakai terus nampak look yang mahal awak" (asal 22.10–27.45s), bukan "awak cantik…" macam v1.
- **Hook teks**: "Nampak mahal, / harga murah je!" — bawah kanan (top 1460px), masuk slide dari kanan + pop.
- **SFX intro**: swoosh + coin (v1: cork + glass ting). Swoosh + punch zoom di setiap potongan (5.35s, 26.1s).
- "Classy & Timeless Look" naik terus selepas hook (3.4s).

Susunan footage (`assets/footage.mp4`, tak di-commit) dipotong dari footage asal v1:
22.10–27.45 → 1.30–22.05 → 27.60–66.40 (lihat arahan ffmpeg dalam commit / sesi).
Render: `python3 build.py && npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`
