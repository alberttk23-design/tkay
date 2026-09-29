#!/usr/bin/env python3
"""
CapCut Mac Draft Project Generator
Tự động tạo project CapCut hoàn chỉnh với Timeline, Video Tracks, Audio, Tỷ lệ 9:16
trực tiếp trong thư mục lưu trữ của CapCut trên macOS:
~/Movies/CapCut/User Data/Projects/com.lveditor.draft/
"""

import os
import sys
import json
import uuid
import time
import subprocess
from typing import List, Dict, Any

CAPCUT_DRAFT_ROOT = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")

def get_media_info(file_path: str) -> Dict[str, Any]:
    cmd = [
        "/opt/homebrew/bin/ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,duration",
        "-of", "json",
        file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        data = json.loads(res.stdout)
        stream = data.get("streams", [{}])[0]
        width = int(stream.get("width", 1080))
        height = int(stream.get("height", 1920))
        dur_sec = float(stream.get("duration", 5.0))
        # CapCut uses microseconds (1s = 1,000,000 us)
        dur_us = int(dur_sec * 1_000_000)
        return {"width": width, "height": height, "duration_us": dur_us, "duration_sec": dur_sec}
    return {"width": 1080, "height": 1920, "duration_us": 5_000_000, "duration_sec": 5.0}

def create_capcut_project(project_name: str, video_paths: List[str], audio_path: str = None) -> str:
    os.makedirs(CAPCUT_DRAFT_ROOT, exist_ok=True)
    project_dir = os.path.join(CAPCUT_DRAFT_ROOT, project_name)
    os.makedirs(project_dir, exist_ok=True)

    project_id = str(uuid.uuid4()).upper()
    now_us = int(time.time() * 1_000_000)
    now_sec = int(time.time())

    # Build materials and timeline segments
    video_materials = []
    video_segments = []
    draft_materials_meta = []

    current_target_start = 0

    for idx, vpath in enumerate(video_paths):
        abs_vpath = os.path.abspath(vpath)
        if not os.path.exists(abs_vpath):
            print(f"⚠️ Bỏ qua file không tồn tại: {abs_vpath}")
            continue

        info = get_media_info(abs_vpath)
        mat_id = str(uuid.uuid4()).upper()
        seg_id = str(uuid.uuid4()).upper()
        dur_us = info["duration_us"]

        # Material entry for draft_info.json
        video_materials.append({
            "id": mat_id,
            "unique_id": uuid.uuid4().hex,
            "type": "video",
            "duration": dur_us,
            "path": abs_vpath,
            "media_path": "",
            "local_id": "",
            "has_audio": True,
            "reverse_path": "",
            "intensifies_path": "",
            "reverse_intensifies_path": "",
            "intensifies_audio_path": "",
            "cartoon_path": "",
            "width": info["width"],
            "height": info["height"],
            "category_id": "",
            "category_name": "local",
            "material_id": "",
            "material_name": os.path.basename(abs_vpath),
            "material_url": "",
            "crop": {
                "upper_left_x": 0.0, "upper_left_y": 0.0,
                "upper_right_x": 1.0, "upper_right_y": 0.0,
                "lower_left_x": 0.0, "lower_left_y": 1.0,
                "lower_right_x": 1.0, "lower_right_y": 1.0
            },
            "crop_ratio": "free",
            "audio_fade": None,
            "crop_scale": 1.0,
            "extra_type_option": 0,
            "stable": {"stable_level": 0, "matrix_path": "", "time_range": {"start": 0, "duration": 0}},
            "source": 0,
            "source_platform": 0,
            "check_flag": 62978047
        })

        # Segment entry for timeline track
        video_segments.append({
            "id": seg_id,
            "source_timerange": {"start": 0, "duration": dur_us},
            "target_timerange": {"start": current_target_start, "duration": dur_us},
            "render_timerange": {"start": 0, "duration": 0},
            "desc": "",
            "state": 0,
            "speed": 1.0,
            "is_loop": False,
            "is_tone_modify": False,
            "reverse": False,
            "intensifies_audio": False,
            "cartoon": False,
            "volume": 1.0,
            "last_nonzero_volume": 1.0,
            "clip": {
                "scale": {"x": 1.0, "y": 1.0},
                "rotation": 0.0,
                "transform": {"x": 0.0, "y": 0.0},
                "flip": {"vertical": False, "horizontal": False},
                "alpha": 1.0
            },
            "uniform_scale": {"on": True, "value": 1.0},
            "material_id": mat_id,
            "extra_material_refs": [],
            "render_index": 0,
            "visible": True,
            "group_id": ""
        })

        # Material entry for draft_meta_info.json
        draft_materials_meta.append({
            "ai_group_type": "",
            "create_time": now_sec,
            "duration": dur_us,
            "enter_from": 0,
            "extra_info": os.path.basename(abs_vpath),
            "file_Path": abs_vpath,
            "height": info["height"],
            "id": str(uuid.uuid4()).lower(),
            "import_time": now_sec,
            "import_time_ms": now_us,
            "item_source": 1,
            "material_color_tag": "",
            "md5": "",
            "metetype": "video",
            "roughcut_time_range": {"duration": dur_us, "start": 0},
            "sub_time_range": {"duration": -1, "start": -1},
            "type": 0,
            "width": info["width"]
        })

        current_target_start += dur_us

    total_duration_us = current_target_start

    # Build tracks
    tracks = [
        {
            "id": str(uuid.uuid4()).upper(),
            "type": "video",
            "segments": video_segments,
            "flag": 0,
            "attribute": 1,
            "name": "Main Video Track",
            "is_default_name": True
        }
    ]

    audio_materials = []
    if audio_path and os.path.exists(audio_path):
        abs_apath = os.path.abspath(audio_path)
        audio_mat_id = str(uuid.uuid4()).upper()
        audio_seg_id = str(uuid.uuid4()).upper()
        audio_materials.append({
            "id": audio_mat_id,
            "type": "audio",
            "path": abs_apath,
            "duration": total_duration_us,
            "material_name": os.path.basename(abs_apath)
        })
        tracks.append({
            "id": str(uuid.uuid4()).upper(),
            "type": "audio",
            "segments": [
                {
                    "id": audio_seg_id,
                    "source_timerange": {"start": 0, "duration": total_duration_us},
                    "target_timerange": {"start": 0, "duration": total_duration_us},
                    "volume": 0.8,
                    "material_id": audio_mat_id
                }
            ],
            "flag": 0,
            "attribute": 0,
            "name": "BGM Track",
            "is_default_name": True
        })

    # 1. Write draft_info.json
    draft_info = {
        "id": project_id,
        "version": 360000,
        "new_version": "185.0.0",
        "name": project_name,
        "duration": total_duration_us,
        "create_time": now_sec,
        "update_time": now_sec,
        "fps": 30.0,
        "is_drop_frame_timecode": False,
        "color_space": 0,
        "config": {
            "video_mute": False,
            "subtitle_sync": True,
            "lyrics_sync": True,
            "use_float_render": False,
            "hdr_vivid": False
        },
        "canvas_config": {
            "ratio": "9:16",
            "width": 1080,
            "height": 1920,
            "background": None
        },
        "tracks": tracks,
        "materials": {
            "videos": video_materials,
            "audios": audio_materials,
            "texts": [],
            "stickers": [],
            "transitions": []
        }
    }

    # 2. Write draft_meta_info.json
    draft_meta_info = {
        "cloud_draft_cover": False,
        "cloud_draft_sync": False,
        "draft_cover": "draft_cover.jpg",
        "draft_fold_path": project_dir,
        "draft_id": project_id,
        "draft_materials": [
            {"type": 0, "value": draft_materials_meta},
            {"type": 1, "value": []},
            {"type": 2, "value": []},
            {"type": 3, "value": []},
            {"type": 6, "value": []},
            {"type": 7, "value": []},
            {"type": 8, "value": []}
        ],
        "draft_name": project_name,
        "draft_need_rename_folder": False,
        "draft_root_path": CAPCUT_DRAFT_ROOT,
        "tm_duration": total_duration_us,
        "tm_draft_create": now_us,
        "tm_draft_modified": now_us
    }

    with open(os.path.join(project_dir, "draft_info.json"), "w", encoding="utf-8") as f:
        json.dump(draft_info, f, ensure_ascii=False, indent=2)

    with open(os.path.join(project_dir, "draft_meta_info.json"), "w", encoding="utf-8") as f:
        json.dump(draft_meta_info, f, ensure_ascii=False, indent=2)

    # Generate a thumbnail cover from first video clip
    if video_paths and os.path.exists(video_paths[0]):
        cover_path = os.path.join(project_dir, "draft_cover.jpg")
        cmd_thumb = [
            "/opt/homebrew/bin/ffmpeg", "-y",
            "-ss", "00:00:01",
            "-i", video_paths[0],
            "-vframes", "1",
            "-q:v", "2",
            cover_path
        ]
        subprocess.run(cmd_thumb, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("=" * 60)
    print(f"🎉 ĐÃ XUẤT THÀNH CÔNG PROJECT CAPCUT:")
    print(f"📁 Tên Project: {project_name}")
    print(f"📍 Đường dẫn: {project_dir}")
    print(f"🎞️ Số clip: {len(video_materials)} clips")
    print(f"⏱️ Tổng thời lượng: {total_duration_us / 1_000_000:.1f}s")
    print(f"📐 Tỷ lệ Canvas: 9:16 (1080x1920 Vertical)")
    print(f"👉 Bây giờ bạn chỉ cần mở CapCut trên Mac, project sẽ xuất hiện ngay!")
    print("=" * 60)

    return project_dir

if __name__ == "__main__":
    import glob
    # Test on today's recent Christmas video clips in ~/Downloads
    recent_clips = sorted(glob.glob(os.path.expanduser("~/Downloads/*20260928*.mp4")), key=os.path.getmtime)
    if not recent_clips:
        # Fallback to Sep 26 family clips
        recent_clips = sorted(glob.glob(os.path.expanduser("~/Downloads/*20260926*.mp4")), key=os.path.getmtime)

    print(f"Tìm thấy {len(recent_clips)} clips gần đây.")
    if recent_clips:
        # Take 5 latest clips
        selected = recent_clips[-5:]
        bgm = os.path.expanduser("~/.gemini/antigravity/scratch/ai-video-studio/public/assets/audio/jingle_bells_cozy.mp3")
        if not os.path.exists(bgm):
            bgm = None
        create_capcut_project("AI Christmas Tree 2026 Auto", selected, bgm)
