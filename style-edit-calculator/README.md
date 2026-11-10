# Style Edit — Calculator Solar (Overlay UI Prompt, Putih Kecil)

HyperFrames 9:16 (1080x1920), 23s. Footage asal tak diubah warna, tiada filter
(B-roll iPhone HDR/HLG ditukar ke SDR biasa supaya warna nampak sama macam kat telefon).

## Potongan (raw → footage.mp4)
Segmen sumber: `0.40–6.50 | 6.92–16.95 | 23.88–26.85 | 29.72–32.05 | 32.36–33.90`
- Buang pause panjang (16.9–18.8s) & pause kecil.
- Buang ayat berulang: "Mula-mula saya ingatkan mahal… murah aja", "Bila kita tekan ni, best",
  "Nampak tak? Ya ini… tak ada bateri" (kekal satu versi sahaja).
- B-roll (bahagian stabil sahaja, dianalisis guna vidstabdetect): A = 3.5–6.6s (tekan butang) di atas "tekan-tekan ni best gila",
  B = 8.0–10.4s (panel solar) di atas "dia hanya gunakan solar".

## Gaya
- **Hook 0–3s**: "Calculator Solar" (Plus Jakarta Sans 700, 44px) + "ada button [%]" — butang % kecil animasi ditekan. SFX stereo `hook_shimmer` + `key_triple` + `ding_soft`.
- **Overlay**: Lexend Mega 600, 27px, putih, tengah atas (ruang kosong bumbung kereta, tak tutup muka/produk). Animasi wipe kiri→kanan + kursor (gaya UI prompt).
  Atas B-roll (latar bunga) guna pil gelap lut sinar kecil supaya teks jelas.
- **Ikon**: troli (bakul kuning), matahari (solar). Putih sahaja.
- **SFX baru** (`sfx3.py`, lain dari video sebelum): `ui_prompt`, `ui_select`, `key_tick`, `key_triple`, `ding_glass`, `ding_soft`, `whoosh_lr/rl`, `soft_impact`, `bubble_pop`, `sparkle_lr`, `hook_shimmer`, `bgm` (lo-fi lembut, vol 0.09).
- **Zoom**: punch pada jump cut & penekanan, zoom perlahan selebihnya; B-roll settle 1.06→1.0.

## Cara guna
`python3 sfx3.py` → `python3 build.py` → `npx hyperframes lint .` → `npx hyperframes snapshot . --at 1.3,6.7,...`
Render final (selepas preview diluluskan): `npx hyperframes render . -q delivery --video-frame-format png -o ../video/CalculatorSolar_FINAL.mp4`
