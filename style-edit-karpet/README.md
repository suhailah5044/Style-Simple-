# Style Edit — Karpet Luar Anti Slip (B-roll + Phone Mockup)

Template HyperFrames 9:16 (1080x1920), ~26.3s. B-roll sahaja (tiada VO) + muzik latar sintetik.
Footage iPhone HDR (HLG) ditukar ke SDR bt709 dengan tonemap *mobius* sahaja — **tiada filter / grade warna**.

## Susunan scene (klip asal Drive)
| Masa | Klip | Overlay | Efek |
|---|---|---|---|
| 0–3.0 | IMG_1968 (gulung karpet) | Hook: COVER STORY / Karpet Luar / Anti Slip | zoom-out, soft impact + pop |
| 3.0–5.6 | IMG_1970 (bentang) | Outdoor Mat / Upgrade! | zoom-in, ding |
| 5.6–8.6 | IMG_1969 dalam **phone mockup** + latar pro (gradient + spotlight + dot grid) | Biggest Size / 80 × 120 cm | zoom skrin penuh → phone |
| 8.6–11.4 | IMG_1982 (close-up bulu) | 400 GSM / Coarse Fiber | **digital zoom** punch |
| 11.4–14.4 | IMG_1976 (pijak) | Scrape Off / Dirt & Sand | zoom-in |
| 14.4–16.3 | IMG_1981 | Water / Resistant | zoom-out |
| 16.3–16.6 | — | — | **frame break** (3 jalur pecah) + flash |
| 16.3–18.4 | IMG_1972 (selak bawah) | TPE Anti-Slip / Base | punch zoom |
| 18.4–21.1 | IMG_1973 (pan corak) | Minimalist / Embossed Design | zoom-in |
| 21.1–23.3 | IMG_1977 | (tiada — ruang bernafas) | zoom-out |
| 23.3–26.3 | IMG_1970 akhir (depan pintu) | Perfect for / Home Entrance | zoom-in, ting2 |

Klip goyang diukur (phase-correlation jitter); hujung klip yang goyang dipotong.

## Gaya teks
Lexend Mega, putih sahaja. Baris 1: 600 30px · baris 2: 400 21px · garis 48x2px. Animasi *mask reveal* naik (expo.out), keluar naik ke atas.
Letak di ruang kosong atas, tak tutup produk. `dk` = bayang lebih tebal untuk latar cerah.

## Bunyi (`sfx3.py`, baru — lain dari v1/v2)
`air_whoosh` (tukar footage) · `bubble_pop` (teks/produk muncul) · `ui_click` (perubahan visual) · `bell_ding` (USP) ·
`soft_impact` (visual penting) · `frame_break` · `ting2` · `ui_prompt` (subtitle) · `music.wav` 116bpm house ringan, stereo lebar.
Volume SFX 0.22–0.4, muzik 0.55 + fade-out.

## Cara guna
`python3 build.py` → `npx hyperframes lint .` → preview: `npx hyperframes preview .` atau `npx hyperframes snapshot . --at 1.5,7.4,...`
Render (bila diluluskan): `npx hyperframes render . -q delivery --video-frame-format png -o Karpet_FINAL.mp4`
