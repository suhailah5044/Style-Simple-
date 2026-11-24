#!/bin/bash
# Render each variant, then re-encode to <100MB into ../video/
set -e
cd "$(dirname "$0")"
P=${PASSLOG:-/tmp/hf_pass}
for v in "$@"; do
  (cd $v && npx hyperframes render . -q delivery --video-frame-format png -o FINAL.mp4 > render.log 2>&1)
  ffmpeg -v error -y -i $v/FINAL.mp4 -c:v libx264 -preset slow -b:v 6000k -pass 1 -passlogfile $P-$v -an -f null /dev/null
  ffmpeg -v error -y -i $v/FINAL.mp4 -c:v libx264 -preset slow -b:v 6000k -pass 2 -passlogfile $P-$v -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart ../video/TurkishGummies_${v^^}.mp4
  rm -rf /tmp/hyperframes-extract-cache-0 $v/FINAL.mp4 $v/work-* $v/.*.hf-transaction-*
  echo "DONE $v $(stat -c %s ../video/TurkishGummies_${v^^}.mp4)"
done
