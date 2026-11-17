# Style Menu Card — Tajuk Serif Elegan (Baju Kurung)

Template HyperFrames 9:16 (1080x1920), ikut gaya video rujukan kafe (kad menu). Warna footage asal tak diubah. Tiada muzik, tiada nama brand.

## Gaya
- **Tajuk 3 lapis** per bahagian, *Playfair Display*, putih, bayang lembut, tengah atas (`top:95px`; bahagian pertama `40px` sebab shot dekat):
  - atas kecil (50px, rapat kiri) · **besar** (124px, 600) · bawah kecil (44px, rapat kanan).
  - Angka biasa (`lnum`) supaya "RM100" tak jadi "RM1oo".
- **Animasi "zap-zup" lembut (~30%)**:
  - Tajuk masuk: blur 8px→0 + fade + naik 18px, berperingkat 0.09s; tajuk besar `scaleX 1.05→1`.
  - Tajuk keluar: blur + naik 10px, 0.25s.
  - Kamera: tolak zoom kecil 3% + blur 3px → jelas (0.4s) setiap tukar tajuk, kemudian hanyut perlahan (±2.5%).
  - SFX: `swish` perlahan (vol 0.25) setiap tukar tajuk, `glint` kilau kecil untuk harga.
- **Penutup**: pudar ke hitam + kad "Kurung / Raya / Bawah RM100".

## Cara guna
1. Edit senarai `S` dalam `build.py`: `[mula, "atas", "BESAR", "bawah", "glint"|""]`.
2. `python3 sfx.py` → `python3 build.py` → `npx hyperframes snapshot . --at 1,30` → render.
3. Kuatkan/lemahkan kesan: `PUSH` (zoom), blur dalam tween `#cam`, volume `swish`.

Lesen font: Playfair Display — SIL OFL (Google Fonts). SFX dijana sendiri.
