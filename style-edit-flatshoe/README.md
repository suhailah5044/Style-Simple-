# Style Edit v3 — Flat Shoe (Creato + Subtitle UI Prompt)

Template HyperFrames 9:16 (1080x1920). Footage asal tak diubah warna, tiada filter.

## Gaya
- **Intro 0–3.35s**: "Flat shoe / paling selesa" — *Creato Display* (Medium 40px + Bold 50px), putih, kiri atas (`top:290px; left:64px`), di ruang siling kosong. SFX **pop cork** + bunyi angin lembut. Zoom-out 1.1→1.0, kemudian zoom-in perlahan.
- **Subtitle kata kunci** (lain daripada v2): *Lexend Mega* 500, 24px, putih, ada titik putih kecil.
  - Masuk: titik pop (`back.out`), kemudian setiap perkataan **blur→jelas** satu-satu (stagger 0.06s).
  - Keluar: blur + fade 0.2s.
  - Letak sudut atas (`top:300px`, 64px dari tepi, lebar 300px), sebelah yang kosong — tak tutup produk/muka.
- **Zoom**: `in` (→1.07), `out` (→1.0), `punch` (1.09→1.02) untuk perkataan kuat.
- **SFX UI prompt** (dijana `sfx3.py`): `prompt`, `bubble`, `tingting`, `pluck`, `click`, `sparkle_up` (pilihan warna), `success` (anti slip), `heartpop` (penutup), `air`; `cork` (intro).

## Preview
`preview/contact-sheet.jpg` — gambar sahaja, belum render.

## Cara guna
`python3 tr.py` → edit `O` dalam `build.py` → `python3 build.py` → `npx hyperframes snapshot . --at ...` → final: `npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`.

Lesen font: Creato Display (Anugrah Pasau) & Lexend Mega — SIL OFL.
