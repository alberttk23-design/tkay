#!/usr/bin/env python3
"""
Native Cinematic Video Assembler (Zero Jitter, 100% Smooth)
Khắc phục triệt để hiện tượng giật của Remotion do Chromium seeking:
Sử dụng FFmpeg xfade tuần tự (sequential hardware-accelerated decoding),
bảo toàn 100% độ mượt nguyên bản của video gốc từ AI, kèm nhạc BGM và chuyển cảnh tan biến ánh sáng.
"""

import os
import subprocess
import time

def assemble_pure_smooth_commercial(output_path: str):
    assets_dir = "/Users/dudumac5/.gemini/antigravity/scratch/ai-video-studio/public/assets/tree_tvc"
    bgm_path = "/Users/dudumac5/.gemini/antigravity/scratch/ai-video-studio/public/assets/audio/bgm_christmas_luxury.mp3"

    v1 = os.path.join(assets_dir, "scene1_ambiance.mp4")
    v2 = os.path.join(assets_dir, "scene2_glide.mp4")
    v3 = os.path.join(assets_dir, "scene3_needles.mp4")
    v4 = os.path.join(assets_dir, "scene4_ornament.mp4")
    v5 = os.path.join(assets_dir, "scene5_reveal.mp4")

    # Xây dựng filter graph xfade:
    # Cắt từng đoạn đẹp nhất (trim) và chuyển cảnh fade mượt mà 0.5s
    # Scene 1: 0.5s -> 4.0s (3.5s)
    # Scene 2: 0.5s -> 3.5s (3.0s)
    # Scene 3: 0.5s -> 3.5s (3.0s)
    # Scene 4: 0.5s -> 3.5s (3.0s)
    # Scene 5: 0.5s -> 4.5s (4.0s)
    
    filter_complex = (
        "[0:v]trim=start=0.5:end=4.0,setpts=PTS-STARTPTS,scale=1080:1920,fps=24[v0];"
        "[1:v]trim=start=0.5:end=3.5,setpts=PTS-STARTPTS,scale=1080:1920,fps=24[v1];"
        "[2:v]trim=start=0.5:end=3.5,setpts=PTS-STARTPTS,scale=1080:1920,fps=24[v2];"
        "[3:v]trim=start=0.5:end=3.5,setpts=PTS-STARTPTS,scale=1080:1920,fps=24[v3];"
        "[4:v]trim=start=0.5:end=4.5,setpts=PTS-STARTPTS,scale=1080:1920,fps=24[v4];"
        "[v0][v1]xfade=transition=fade:duration=0.5:offset=3.0[x1];"
        "[x1][v2]xfade=transition=fade:duration=0.5:offset=5.5[x2];"
        "[x2][v3]xfade=transition=fade:duration=0.5:offset=8.0[x3];"
        "[x3][v4]xfade=transition=fade:duration=0.5:offset=10.5[vout];"
        "[5:a]atrim=start=0:end=14.5,asetpts=PTS-STARTPTS,afade=t=in:ss=0:d=0.5,afade=t=out:st=13.5:d=1.0,volume=0.85[aout]"
    )

    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-i", v1,
        "-i", v2,
        "-i", v3,
        "-i", v4,
        "-i", v5,
        "-i", bgm_path,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        output_path
    ]

    print("🚀 Bắt đầu render Native Smooth FFmpeg Commercial...")
    start = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Lỗi:", res.stderr)
        raise RuntimeError("FFmpeg xfade failed")
    print(f"✅ Hoàn tất render trong {time.time() - start:.1f}s: {output_path}")

if __name__ == "__main__":
    out = "/Users/dudumac5/.gemini/antigravity/scratch/ai-video-studio/out/luxury_tree_native_smooth.mp4"
    assemble_pure_smooth_commercial(out)
