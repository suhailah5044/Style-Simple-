# Style Edit — Karpet Luar Anti Slip (B-roll + Phone Mockup)

Template HyperFrames 9:16 (1080x1920), ~26.3s. B-roll sahaja (tiada VO, tiada muzik) — SFX sahaja.
Footage iPhone HDR (HLG) ditukar ke SDR bt709 dengan tonemap *mobius* sahaja — **tiada filter / grade warna**.

## Susunan scene (footage karpet sahaja, tiada orang) — ~24.2s
| Masa | Klip | Overlay |
|---|---|---|
| 0–3.0 | IMG_1978 | Hook: COVER STORY / Karpet Luar / Anti Slip |
| 3.0–5.0 | IMG_1971 | Outdoor Mat / Upgrade! |
| 5.0–7.6 | IMG_1983 dalam **phone mockup** + latar pro | Biggest Size / 80 × 120 cm |
| 7.6–10.0 | IMG_1982 close-up (**digital zoom**) | 400 GSM / Coarse Fiber |
| 10.0–11.6 | IMG_1979 | — |
| 11.6–13.3 | IMG_1976 (kaki pijak) | Scrape Off / Dirt & Sand |
| 13.3–15.0 | IMG_1980 → **frame break** | Water / Resistant |
| 14.7–16.5 | IMG_1972 (bawah) | TPE Anti-Slip / Base |
| 16.5–18.7 | IMG_1974 | Minimalist / Embossed Design |
| 18.7–21.9 | IMG_1973, IMG_1981 | — |
| 21.9–24.2 | IMG_1970 akhir | Perfect for / Home Entrance |

Klip goyang diukur (phase-correlation jitter); hujung klip yang goyang dipotong.

## Gaya teks
Lexend Mega, putih sahaja. Baris 1: 600 30px · baris 2: 400 21px · garis 48x2px. Animasi *mask reveal* naik (expo.out), keluar naik ke atas.
Letak di ruang kosong atas, tak tutup produk. `dk` = bayang lebih tebal untuk latar cerah.

## Bunyi (`sfx3.py`, baru — lain dari v1/v2)
`air_whoosh` (tukar footage) · `bubble_pop` (teks/produk muncul) · `ui_click` (perubahan visual) · `bell_ding` (USP) ·
`soft_impact` (visual penting) · `frame_break` · `ting2` · `ui_prompt` (subtitle)
Volume SFX 0.22–0.4. **Tiada muzik** (dibuang atas permintaan); footage senyap.

## Cara guna
`python3 build.py` → `npx hyperframes lint .` → preview: `npx hyperframes preview .` atau `npx hyperframes snapshot . --at 1.5,7.4,...`
Render (bila diluluskan): `npx hyperframes render . -q delivery --video-frame-format png -o Karpet_FINAL.mp4`

---
# Variasi V2–V5 (`gen.py` → `v2.html`…`v5.html`)
Footage sama (karpet sahaja, tiada orang), klip sumber penuh di `assets/src/` (dipotong guna `data-media-start`). Setiap variasi berbeza susunan klip, gaya teks, transisi, grafik dan SFX (`sfx4.py`).

| Variasi | Gaya teks | Transisi | Grafik khas | SFX teks / USP |
|---|---|---|---|---|
| **V2 Slide Clean** (19.5s) | garis menegak + teks luncur dari kiri | slide/whip, flash | split-screen 2 footage | glass_pluck / sparkle_tail |
| **V3 Typewriter UI** (18s) | taip huruf demi huruf + kursor berkelip | zoom-through | phone mockup 3D senget + light streak | type_burst / bell_ding |
| **V4 Kinetic Blur** (18.5s) | perkataan muncul dari blur, nombor mengira | iris bulatan | bingkai polaroid | chime_soft / ting2 |
| **V5 Editorial Index** (17.8s) | indeks 01–08 + garis, mask reveal | wipe menegak + garis cahaya, frame break | intro letterbox, kolaj 2×2 | tick_index / sparkle_tail |

Render satu variasi: salin `vN.html` jadi `index.html` dalam folder lain (symlink `assets/` & `sfx/`), kemudian `npx hyperframes render <folder> -q delivery --video-frame-format png -o Karpet_vN_FINAL.mp4`.
