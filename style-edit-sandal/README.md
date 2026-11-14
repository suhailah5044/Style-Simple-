# Style Edit — Sandal Utune (gaya v2 + B-roll)

HyperFrames 9:16 (1080x1920), 53s. Footage asal tak diubah warna.

- Sumber: Drive folder "Sandal 2" (5 klip). `cut.py` buang pause/ayat ulang → `assets/footage.mp4`, b-roll 4s → `assets/broll0-3.mp4`.
- Hook 0–3s: "Siapa dekat sini teringin nak pakai brand C tapi tengok harga..." + tajuk Italianno "Rupa brand C, harga budget!".
- Teks: Lexend Mega 600, 30px putih, tengah atas (`top:250px`) atas kepala, garis bawah kecil.
- B-roll full screen 4s, fade 0.35s, muted (suara asal jalan terus).
- Zoom selang-seli tiap cut (sorok jump cut) + punch pada fakta penting.

Cara guna: `python3 cut.py <folder_sumber>` → `python3 build.py` → `npx hyperframes lint .` → draft: `npx hyperframes render . -q draft -o draft.mp4` → final: `npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4`
