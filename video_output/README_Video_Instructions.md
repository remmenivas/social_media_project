# SocialConnect DBMS Explanation Video — Instructions & Documentation

This folder contains the complete AI-narrated educational video presentation and associated assets for the **SocialConnect — Social Media Database Management System** project.

---

## 1. Deliverables Included

| File | Description |
| :--- | :--- |
| **`SocialConnect_DBMS_Explanation.mp4`** | **The complete master MP4 presentation video** (1080p, 30 FPS, full narration & slides). |
| **`SocialConnect_Narration_Script.txt`** | Full verbatim narration script across all 14 educational scenes (~7-8 min duration). |
| **`SocialConnect_Storyboard.md`** | Scene-by-scene storyboard with visuals, on-screen text, durations, and transitions. |
| **`SocialConnect_Subtitles.srt`** | Synchronized English subtitles with millisecond timestamps for the entire video. |
| **`SocialConnect_ER_Diagram.png`** | High-resolution Entity-Relationship diagram covering all 5 verified database tables. |
| **`SocialConnect_Architecture.png`** | System architecture diagram showing Frontend ↔ Flask API ↔ psycopg2 ↔ PostgreSQL. |
| **`SocialConnect_Project_Inspection.md`** | Comprehensive inspection report of all routes, schema, frontend controls, and SQL queries. |
| **`generate_video.py`** | Fully reproducible Python script to re-render slides, narration audio, and assemble the video. |

---

## 2. Project Architecture & DBMS Highlights

SocialConnect is built upon a clean 3-tier architecture:
1. **Frontend:** Single-page responsive web application built with semantic HTML5, CSS3 (dark/light theme support), and modern JavaScript (Fetch API, DOM manipulation).
2. **Backend API:** Python Flask server (`app.py`) providing 11 REST endpoints with full JSON input/output validation, parameterized query execution, and database transaction control (`commit()` and `rollback()`).
3. **Database Layer:** PostgreSQL (`social_media_db`) accessed directly via `psycopg2`.
   - **5 Relational Tables:** `users`, `posts`, `likes`, `comments`, `messages`.
   - **Keys & Integrity:** Primary Keys (`SERIAL/INTEGER`), Foreign Keys linking posts/likes/comments/messages to users, and `UNIQUE(post_id, user_id)` constraint preventing duplicate likes.
   - **Advanced SQL:** Multi-table `JOIN` with `LEFT JOIN` on likes, `COUNT(DISTINCT l.like_id)`, `GROUP BY`, case-insensitive search with `ILIKE`, and `INSERT ... RETURNING`.

---

## 3. How to Regenerate or Modify the Video

If you ever wish to re-generate the presentation video or adjust any scene:

1. **Ensure Prerequisites are Installed:**
   ```powershell
   pip install moviepy gtts pillow numpy imageio_ffmpeg
   ```

2. **Run the Video Generator:**
   ```powershell
   cd "C:\Users\remme nivas\social_media_project\video_output"
   $env:PYTHONIOENCODING="utf-8"
   python generate_video.py
   ```

The script will:
- Re-render all 14 visual slides into `frame_scenes/`
- Generate audio voice-overs using gTTS into `audio_scenes/`
- Export diagrams and subtitles
- Concatenate everything into `SocialConnect_DBMS_Explanation.mp4`
