#!/bin/bash
# 将 WEBM 转换为 MP4 和 GIF

# 转换为 MP4
ffmpeg -i web_demo.webm -c:v libx264 -crf 23 -pix_fmt yuv420p web_demo.mp4

# 转换为 GIF
ffmpeg -i web_demo.webm -vf "fps=12,scale=1000:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3" -loop 0 web_demo.gif

echo "转换完成！"
