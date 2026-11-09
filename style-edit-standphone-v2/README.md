# Style Edit v2 — Intro Script + Subtitle UI (Stand Phone)

Template HyperFrames 9:16 (1080x1920). Footage asal tak diubah warna, tiada filter.

## Gaya
- **Intro 0–3.4s**: "Content creator / wajib ada benda ni!" — font *Italianno* 78px, putih, tengah atas (`top:230px`). SFX **cork pop** + glass ting perlahan. Zoom-out 1.1→1.0.
- **Subtitle kata kunci**: font *Lexend Mega* 600, 30px, `letter-spacing:-0.03em`, putih, bayang nipis.
  - Garis putih kecil (56x3px) di bawah teks, animasi `scaleX 0→1`.
  - Masuk: naik `y:22→0`, `expo.out` 0.38s. Keluar: naik sikit + fade 0.2s.
  - Letak ruang kosong atas (`top:240px`), sebelah bertentangan produk, 170px dari tepi, lebar 420px.
- **Zoom**: `in` (→1.07), `out` (→1.0), `punch` (1.1→1.02).
- **SFX UI** (dijana `sfx2.py`): `ui_blip`, `ui_notif`, `ui_confirm`, `ui_tap`, `glass_ting`, `coin` (harga), `sub_boom` (solid/berat + punch zoom), `riser_shimmer` (worth it), `swoosh` (naik/turun), `cork` (intro).

## Cara guna
Sama macam `style-edit-standphone/`: transcribe (`tr.py`) → edit senarai `O` dalam `build.py` → `python3 build.py` → `npx hyperframes snapshot . --at ...` untuk preview gambar → `npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`.

Lesen font: Italianno & Lexend Mega — SIL OFL (Google Fonts).
