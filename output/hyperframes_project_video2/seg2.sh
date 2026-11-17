#!/bin/bash
# usage: seg2.sh out src start dur(out) speed
TM="zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
GR="eq=contrast=0.98:saturation=0.96:brightness=0.025:gamma=1.04,colorbalance=rs=0.025:gs=0.005:bs=-0.025:rm=0.02:bm=-0.015,unsharp=5:5:0.35,format=yuv420p"
OUT="-colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:v libx264 -preset medium -crf 16 -an"
out=$1; src=$2; ss=$3; d=$4; sp=$5
srcd=$(python3 -c "print(round($d*$sp+0.05,3))")
if python3 -c "import sys; sys.exit(0 if $sp<0.99 else 1)"; then
 ff=$(python3 -c "print(round(30/$sp))")
 VF="$TM,scale=1080:1920:flags=lanczos,fps=30,minterpolate=fps=$ff:mi_mode=mci:mc_mode=aobmc:vsbmc=1,setpts=PTS/$sp,fps=30,$GR"
else
 VF="$TM,setpts=PTS/$sp,scale=1080:1920:flags=lanczos,fps=30,$GR"
fi
ffmpeg -v error -y -ss $ss -t $srcd -i $src -vf "$VF" -t $d $OUT $out
