# Style Edit v2 — Phone Holder (susun semula + overlay kecil)

Ikut gaya repo **Kasut-Sekolah** (tak tiru sebiji):
- **Hook 0–2.4s (baru):** phone tergantung terbalik pada holder, "memang melekat, jangan risau jatuh" → teks "phone terbalik pun tak jatuh". (Video 1 guna ujian tarik sebagai hook; di sini ujian tarik dipindah ke tengah.)
- **Susunan:** cara pasang → open/ketat → lekat → ujian tarik → worth it → tangkai panjang, allen key → casing magnetic → masa drive, pusing → harga murah → recommend.
- **Potongan:** jeda dipendekkan ke 0.12s, take berulang dibuang, punch-in 1.045 selang-seli pada setiap potongan.
- **Overlay:** 21 teks kecil Cweyons putih (38px, hook 50px), huruf kecil, tengah ruang kosong atas (y=250) — tak kacau produk. Fade + naik 14px, "ting" perlahan.
- **Tiada muzik.** Suara asal dibersihkan (-15 LUFS).

## Cara guna
```
python3 build.py input.mov preview.mp4 --preview   # 540p laju untuk semak
python3 build.py input.mov ../video/PhoneHolder_v2_FINAL.mp4   # final 1080p
```
Edit `SEG` (susunan), `HOOK` dan `KW` (overlay) dalam `build.py`. Font tiada nombor / '&'.
