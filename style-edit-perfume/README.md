# Perfume (VILILY Lover's Whisper) — TikTok 9:16, gaya "Luggage Bag Pack"

Footage asal (Drive): https://drive.google.com/drive/folders/12FDQEIZZjftJfslPThILUYfvVFTAeY6m
(`copy_6217E91F-4BAD-494C-957B-C9547604F4AF.mov`, 43s, 1080x1920)

## Status (latest)
- 5 versi PREVIEW siap (540x960) dalam `preview/`. **Belum render final 1080x1920.**
- Gaya ikut `style-edit-luggage-v4` (branch claude/dreamy-goodall-djn8tf): hook pill kaca kanan atas,
  teks putih kecil Lexend Mega (24px/15px + bar), zoom punch/in/out, SFX, whoosh setiap cut,
  frame break 2x, speed 1.1x, muzik 0.09. Warna footage asal tak diubah.
- Overlay semua di ruang kosong atas kepala (top 255px) — tak tutup muka/produk/baju.

| Versi | Hook pill | Ayat pembuka |
|---|---|---|
| V1 | Botol Kecil? / Rupanya Besar! | "Ingatkan botol kecil je, rupanya besarnya wih!" |
| V2 | 100ML Je? / Harga Tak Masuk Akal! | "100 ml je harga serius tak masuk akal" |
| V3 | Rasa Nak Spray / Banyak Kali! | "Macam nak spray banyak kali tau…" |
| V4 | Dah Repeat / Banyak Kali! | "Wangi dia tahan lama… dah beberapa kali repeat" |
| V5 | Harga Terlajak / Murah! | "Harga dia memang terlajak murah. Besar pula tu" |

Overlay (teks user): PERFUME 100ML · SWEET • FRUITY • FLORAL · DAILY WEAR FRIENDLY · BOLEH BAWA SOLAT ·
TOP/MIDDLE/BASE NOTES · 90% PERFUME CONCENTRATE. Overlay yang jatuh dalam hook (<2.15s) dianjak lepas hook pill.

## Cara build semula
```
mkdir -p src && curl -sSL -o src/raw.mov "https://drive.usercontent.google.com/download?id=1Ol9ZP3lO_sfkE9_MhhYdNOvXTULtnIq1&export=download&confirm=t"
ffmpeg -i src/raw.mov -ac 1 -ar 16000 audio.wav
VARIANT=V2 python3 build.py        # -> PREVIEW_V2.mp4 (W,H=540,960; tukar ke 1080,1920 untuk final)
```
`sfx/music.wav` dijana oleh `music.py`. `transcript.json` = transcribe faster-whisper (word timestamps).

## Nota / belum selesai
- Tiada b-roll dalam folder Drive (overlay full-screen b-roll belum ada).
- Transcribe kabur: "Wangi dia taklah lama" dianggap "tahan lama".
- Video rujukan TikTok tak dapat dimuat turun (hanya audio + thumbnail).
