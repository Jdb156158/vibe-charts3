#!/bin/sh
set -eu
cd "$(dirname "$0")"
ffmpeg -y -framerate 60 -i frames/frame-%04d.jpg -i assets/sound.wav -vf 'scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p' -af 'loudnorm=I=-16:TP=-2.5:LRA=9' -c:v libx264 -preset medium -crf 18 -profile:v main -level:v 4.2 -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -g 60 -c:a aac -b:a 192k -ar 48000 -t 20 -movflags +faststart -video_track_timescale 60000 controls-knowledge-20s.mp4
