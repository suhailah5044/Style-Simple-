# Style Bawah — Kapsyen Tulisan Tangan (Baju Kurung)

Template HyperFrames 9:16 (1080x1920). Footage asal tak diubah warna, tiada filter, tiada zoom, tiada SFX — gaya minimal ikut rujukan.

## Gaya
- **Kapsyen bawah-tengah**: font *Gochi Hand* 50px, putih, huruf kecil, `letter-spacing:.06em` (rupa tulisan tangan jarang macam rujukan).
- Garis luar hitam nipis (`-webkit-text-stroke 1.5px`) + bayang lembut supaya jelas atas corak bunga.
- Letak `top:1330px` (~70% tinggi), tengah, kiri/kanan 90px.
- **Frasa demi frasa** 2–4 perkataan ikut timing suara (whisper medium, `words_m.json`).
- Masuk: pop kecil `scale .86→1`, `back.out(2)`, 0.16s. Keluar: potong terus bila frasa seterusnya masuk (maks 2.4s atas skrin).

## Cara guna
1. `ffmpeg -i in.mov -vn -ac 1 -ar 16000 audio.wav` → `python3 tr.py` (tukar model ke `medium` untuk ketepatan lebih baik).
2. Edit senarai `P` dalam `build.py`: `[mula, "teks"]`. Betulkan ejaan whisper secara manual.
3. Letak footage di `assets/footage.mp4`, set `DUR` → `python3 build.py`.
4. `npx hyperframes snapshot . --at 1,10,30` untuk semak → `npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`.

Lesen font: Gochi Hand — SIL OFL (Google Fonts).
