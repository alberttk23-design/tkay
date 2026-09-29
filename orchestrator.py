#!/usr/bin/env python3
"""
AI Video Studio - Master Orchestrator
Kết nối toàn bộ chuỗi tự động hoá:
1. Veo Browser Agent (Playwright điều khiển Google Gemini Ultra)
2. Remaster & Anti-Jitter Engine (Khử giật, nâng lên 60fps mượt mà, khử nhấp nháy đèn)
3. CapCut Mac Draft Exporter (Tự động đưa clip & BGM vào timeline CapCut Mac)
"""

import os
import sys
import glob
import argparse
from capcut_draft_generator import create_capcut_project
from remaster_pipeline import remaster_video

def main():
    parser = argparse.ArgumentParser(description="AI Commercial Video Studio Orchestrator")
    parser.add_argument("--mode", choices=["capcut", "remaster", "all"], default="capcut",
                        help="Chế độ xử lý: capcut (tạo project CapCut), remaster (khử giật 60fps), all (tất cả)")
    parser.add_argument("--name", type=str, default="AI Christmas Commercial 2026",
                        help="Tên Project CapCut")
    args = parser.parse_args()

    # Tìm các clip gần nhất trong thư mục Downloads
    recent_clips = sorted(glob.glob(os.path.expanduser("~/Downloads/*20260928*.mp4")), key=os.path.getmtime)
    if not recent_clips:
        recent_clips = sorted(glob.glob(os.path.expanduser("~/Downloads/*20260926*.mp4")), key=os.path.getmtime)

    print("=" * 60)
    print("🎬 AI VIDEO STUDIO MASTER ORCHESTRATOR")
    print(f"📌 Chế độ: {args.mode}")
    print(f"📂 Tìm thấy: {len(recent_clips)} clip video gần đây")
    print("=" * 60)

    if not recent_clips:
        print("❌ Không tìm thấy video clip nào trong ~/Downloads.")
        return

    selected_clips = recent_clips[-5:] # Lấy 5 clip mới nhất

    if args.mode in ["remaster", "all"]:
        remastered_clips = []
        out_dir = os.path.expanduser("~/.gemini/antigravity/scratch/ai-video-studio/out/remastered")
        os.makedirs(out_dir, exist_ok=True)
        for clip in selected_clips:
            base_name = os.path.basename(clip)
            target = os.path.join(out_dir, f"smooth_{base_name}")
            if not os.path.exists(target):
                res = remaster_video(clip, target, target_fps=60)
                remastered_clips.append(res)
            else:
                remastered_clips.append(target)
        selected_clips = remastered_clips

    if args.mode in ["capcut", "all"]:
        bgm = os.path.expanduser("~/.gemini/antigravity/scratch/ai-video-studio/public/assets/audio/jingle_bells_cozy.mp3")
        if not os.path.exists(bgm):
            bgm = None
        create_capcut_project(args.name, selected_clips, bgm)

if __name__ == "__main__":
    main()
