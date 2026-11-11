# Style Edit — Silicone Dish Mat (HyperFrames)

Video jualan TikTok 9:16 (1080x1920), **67.5s**. Status: **PREVIEW sahaja — belum render.**
Warna footage asal dikekalkan (bt709, tiada filter/grade).

## Suntingan (`edit.py` + `build_base.py`)
- Buang senyap/pause, gagap & ayat ulang:
  - "kadang-kadang barang dapur" (sebut 2x) → simpan sekali
  - "sebab tu kita kena ada…" (3x) → simpan sekali
  - "lepas basuh…" (4–5 cubaan, 63–77s sumber) → simpan ambilan terakhir
  - Senyap 18–30s, 85–89s dibuang
- **Speed 1.1x** (video + `atempo`), **suara dikuatkan**: highpass 80Hz → compressor → loudnorm -13 LUFS.
- **B-roll / cutaway** (overlay video penuh skrin, suara utama berterusan) — hanya bahagian B-roll yang **tak goyang** (diukur dengan phase-correlation, `shake.py`): 6 cutaway, ~25% masa.
- Bahagian "bakul kuning": footage sahaja, **tiada teks**.

## Overlay (`build.py`)
- **Hook 0–2.9s**: "Silicone Dish Mat" (Lexend Mega 600, 40px) + garis + "Cepat kering & mudah guna" (300, 21px). Frame break + zoom-out + impact/ting-ting.
- **Subtitle kata kunci**: Lexend Mega 500, **26px**, putih, titik putih kecil di depan; perkataan masuk satu-satu (blur→jelas). Ruang kosong atas (`top:255px`, kabinet), tak tutup produk.
- **Digital zoom**: in / out / punch. **Frame break**: 3 jalur video teranjak & snap balik (0s, 7.6s, 23.6s, 53.6s).
- **SFX baru** (`sfx3.py`, stereo — sedap dengan headphone, lain dari video sebelum): `prompt_up`/`prompt_soft` (UI prompt subtitle), `pop_bubble`, `click_soft`, `ding_usp`, `tingting`, `whoosh_air` (pan kiri→kanan, setiap cutaway), `impact_soft`, `sparkle_up`, `cash_tick` (harga).
- **BGM** lofi lembut (`bgm_lofi.wav`) ~18 dB bawah suara.

## Cara guna
```
python3 build_base.py MAIN.mov BROLL.mov assets/footage.mp4   # footage asas
python3 sfx3.py                                              # SFX + BGM
python3 build.py && hyperframes lint .
hyperframes preview . --no-open                              # preview
# bila OK: hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4
```
Font Lexend Mega — SIL OFL.
