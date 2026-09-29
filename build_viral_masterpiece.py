#!/usr/bin/env python3
"""
Viral Christmas Tree Commercial Generator
- Hook: Santa fainting outside window in shock/awe
- Reveal: Hosts dramatically pulling curtain off tree to cheering crowd
- Feature 1: Macro hand touching lush evergreen foliage (realism proof)
- Feature 2: Twinkling fairy lights & delicate Christmas ornament
- Payoff: Full luxury Christmas tree glowing in festive living room
Dynamic Context-Aware Transitions:
- Window -> Interior: zoomin (push through glass)
- Unveil -> Detail: smoothleft (whip pan)
- Needles -> Ornament: fadewhite (golden light burst)
- Ornament -> Hero: fade (cinematic dissolve)
"""

import os
import subprocess
import time

def build_viral_masterpiece():
    santa = "/Users/dudumac5/Downloads/Santa_dropping_sack_and_fainting_20260926161809.mp4"
    hosts = "/Users/dudumac5/Downloads/Hosts_revealing_Christmas_tree_p…_20260928103722.mp4"
    needles = "/Users/dudumac5/Downloads/Hand_touching_evergreen_needles_1080p_20260928135000.mp4"
    ornament = "/Users/dudumac5/Downloads/Hand_touching_Christmas_tree_orn…_20260928100424.mp4"
    hero = "/Users/dudumac5/Downloads/Christmas_tree_product_reveal_video_20260928103007.mp4"
    bgm = "/Users/dudumac5/.gemini/antigravity/scratch/ai-video-studio/public/assets/audio/bgm_christmas_luxury.mp3"
    out = "/Users/dudumac5/.gemini/antigravity/scratch/ai-video-studio/out/viral_christmas_tree_masterpiece.mp4"

    # Scale all to 1080x1920 24fps
    filter_complex = (
        "[0:v]trim=start=0:end=3.2,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=24[v0];"
        "[1:v]trim=start=0.3:end=3.8,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=24[v1];"
        "[2:v]trim=start=0.5:end=3.3,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=24[v2];"
        "[3:v]trim=start=0.5:end=3.3,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=24[v3];"
        "[4:v]trim=start=0.5:end=4.7,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=24[v4];"
        "[v0][v1]xfade=transition=zoomin:duration=0.5:offset=2.7[x1];"
        "[x1][v2]xfade=transition=smoothleft:duration=0.5:offset=5.7[x2];"
        "[x2][v3]xfade=transition=fadewhite:duration=0.4:offset=8.1[x3];"
        "[x3][v4]xfade=transition=fade:duration=0.5:offset=10.5[vout];"
        "[5:a]atrim=start=0:end=14.7,asetpts=PTS-STARTPTS,afade=t=in:ss=0:d=0.3,afade=t=out:st=13.7:d=1.0,volume=0.9[aout]"
    )

    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-i", santa,
        "-i", hosts,
        "-i", needles,
        "-i", ornament,
        "-i", hero,
        "-i", bgm,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        out
    ]

    print("🎬 Đang render TVC Viral Cây Thông Giáng Sinh đỉnh cao...")
    start = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Lỗi:", res.stderr)
        raise RuntimeError("Render failed")
    print(f"🎉 Hoàn thành trong {time.time() - start:.1f}s: {out}")
    return out

if __name__ == "__main__":
    build_viral_masterpiece()
