# Storyboard — CCTV Murah (HyperFrames 9:16, 82s)

Footage: `copy_5A33A620….mov` (1080x1920, 30fps, 82.0s, HEVC)
Gambar overlay: IMG_4057, IMG_4060, IMG_4061, IMG_4062

## Gaya overlay gambar
- Kad gambar putih bucu bulat (radius 28px), bayang lembut, lebar ~620px, di ruang kosong atas (top ~260px).
- Masuk: pop `scale .6→1` + `y:40→0`, `back.out(1.8)`, 0.4s + SFX `ui_notif`/`swoosh`. Keluar: `scale→.9` + fade 0.25s.
- Zoom perlahan dalam gambar (Ken Burns 1.0→1.06) sepanjang tayangan.
- Subtitle kata kunci ikut style v2 (Lexend Mega putih + garis kecil). Disorok semasa gambar keluar.

## Timeline

| # | Masa | Skrip (VO) | Visual footage | Overlay teks | Overlay gambar | SFX / Zoom |
|---|------|-----------|----------------|--------------|----------------|-----------|
| 1 | 0.0–3.3 | "Saya ada grab lagi CCTV yang murah…" | Pegang CCTV + kotak | **Intro:** "CCTV Murah / tapi worth it!" (Italianno) | — | cork + glass_ting · zoom-out |
| 2 | 3.3–8.7 | "…letak kat bilik anak, senang nak pantau anak…" | Sama | "Untuk Bilik Anak" → "Pantau Anak" | — | ui_blip · in |
| 3 | 8.9–13.5 | "Harga dia betul-betul murah, boleh pantau dari telefon" | Skrin telefon + CCTV | "Harga Murah!" → "Pantau Dari Telefon" | — | coin · punch / ui_tap |
| 4 | 13.5–20.2 | "Android, iPhone, iPad dua-dua pun tak ada masalah" | Pegang iPad | "Android & iPhone" → "iPad Pun Boleh" | — | ui_confirm · in/out |
| 5 | 20.6–27.8 | "Nampak tak saya tengah tengok anak… kualiti jelas" | Live view di iPad | "Live View" → "Kualiti Jelas!" | — | glass_ting · punch |
| 6 | 27.8–30.5 | "Nak install senang, just scan je" | CCTV atas meja | "Install Senang" | **IMG_4062** — 3 cara sambung WiFi/AP Hotspot | ui_notif · in |
| 7 | 30.5–36.3 | "Ada buku panduan… boleh dengar & cakap dua hala" | Tunjuk kotak / cakap dekat CCTV | "Ada Buku Panduan" → "Cakap 2 Hala" | — | ui_tap / ui_blip |
| 8 | 36.3–38.4 | "Ada pergerakan je akan hantar notification" | Pegang CCTV | — | **IMG_4060** — Movement & AI Human Detection | swoosh · punch |
| 9 | 38.4–42.8 | "Rakaman pun ada simpan dalam memory card…" | Pegang CCTV + telefon | "Simpan Dalam Memory Card" | **IMG_4061** — Auto Tracking + Notification (38.4–40.6) | ui_notif · in |
| 10 | 42.8–51.0 | "Pilih setting je… guna power bank je, bawa mana-mana mudah" | Close-up CCTV | "Setting Senang" → "Guna Power Bank" → "Bawa Mana-Mana" | — | ui_confirm / swoosh |
| 11 | 51.0–59.0 | "Letak bilik anak ke ruang tamu… budget tapi kualiti okey" | Talking head | "Bilik / Ruang Tamu" → "Budget Tapi Berkualiti" | — | glass_ting · sub_boom punch |
| 12 | 59.0–68.5 | "Nak tinggal rumah, pergi holiday… harga murah tapi worth it" | Skrin telefon live view | "Pergi Holiday Pun Tenang" → "Worth It!" | — | riser_shimmer · in |
| 13 | 68.5–75.2 | "Dekat setting boleh share dengan banyak device" | Talking head + CCTV | "Share Banyak Device" | **IMG_4057** — Share kamera dengan family (70.4–75.2) | ui_notif · in |
| 14 | 75.2–82.0 | "Isteri, suami, nenek kat kampung… pantau mak ayah" | Talking head | "Satu Family Boleh Tengok" → "Pantau Mak Ayah" → CTA "Tekan Bakul Kuning!" | — | ui_confirm → coin · punch |

## Nota
- Gambar dipotong (crop) bahagian penting sahaja jika teks dalam gambar terlalu kecil.
- Suara asal 1.0, SFX 0.3–0.5. Tiada filter/warna footage.
