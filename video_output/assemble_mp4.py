import os
import sys
import subprocess
import imageio_ffmpeg

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\remme nivas\social_media_project\video_output"
FRAME_DIR = os.path.join(BASE, "frame_scenes")
AUDIO_DIR = os.path.join(BASE, "audio_scenes")
OUTPUT_MP4 = os.path.join(BASE, "SocialConnect_DBMS_Explanation.mp4")

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
print(f"Using FFmpeg: {ffmpeg}")

scenes = [f"scene{i:02d}" for i in range(1, 15)]
scene_mp4s = []

print("Step 1: Rendering 14 scene clips...")
for idx, s in enumerate(scenes, 1):
    img = os.path.join(FRAME_DIR, f"{s}.png")
    mp3 = os.path.join(AUDIO_DIR, f"{s}.mp3")
    out = os.path.join(BASE, f"part_{s}.mp4")
    
    cmd = [
        ffmpeg, "-y",
        "-loop", "1", "-i", img,
        "-i", mp3,
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        out
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0 and os.path.exists(out):
        print(f"  ✓ [{idx}/14] {s}.mp4 rendered ({os.path.getsize(out)//1024} KB)")
        scene_mp4s.append(out)
    else:
        print(f"  ✗ Failed to render {s}")

print("\nStep 2: Concatenating all scenes into final master video...")
concat_list = os.path.join(BASE, "concat_list.txt")
with open(concat_list, "w", encoding="utf-8") as f:
    for clip in scene_mp4s:
        # Format for ffmpeg concat demuxer (forward slashes or escaped backslashes)
        clip_fixed = clip.replace("\\", "/")
        f.write(f"file '{clip_fixed}'\n")

concat_cmd = [
    ffmpeg, "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_list,
    "-c", "copy",
    OUTPUT_MP4
]

res = subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if res.returncode == 0 and os.path.exists(OUTPUT_MP4):
    size_mb = os.path.getsize(OUTPUT_MP4) / (1024 * 1024)
    print(f"\n Master Video Assembled Successfully!")
    print(f" Output File: {OUTPUT_MP4}")
    print(f" File Size: {size_mb:.2f} MB")
    
    # Clean up part files
    for clip in scene_mp4s:
        try:
            os.remove(clip)
        except:
            pass
    try:
        os.remove(concat_list)
        os.remove(os.path.join(BASE, "s01.mp4"))
        os.remove(os.path.join(BASE, "test_out.mp4"))
        os.remove(os.path.join(BASE, "test_img.png"))
        os.remove(os.path.join(BASE, "test.mp3"))
        tmp_snd = os.path.join(BASE, "SocialConnect_DBMS_ExplanationTEMP_MPY_wvf_snd.mp4")
        if os.path.exists(tmp_snd):
            os.remove(tmp_snd)
    except:
        pass
    print("✓ Temporary files cleaned up.")
else:
    print("✗ Concat failed.")
