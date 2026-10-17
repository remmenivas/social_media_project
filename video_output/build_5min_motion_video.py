"""
SocialConnect — 5-Minute Motion Graphics Video Generator
=========================================================
Generates a 5.3-minute Full HD (1920x1080) video with animated video clips,
real UI simulations, dynamic data-flow particles, SQL execution animations,
and synchronized AI English voice-over.
"""

import os
import sys
import math
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\remme nivas\social_media_project\video_output"
OUTPUT_MP4 = os.path.join(BASE, "SocialConnect_DBMS_Explanation.mp4")
DESKTOP_1 = r"C:\Users\remme nivas\OneDrive\Desktop\SocialConnect_DBMS_Explanation.mp4"
DESKTOP_2 = r"C:\Users\remme nivas\Desktop\SocialConnect_DBMS_Explanation.mp4"

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 1920, 1080
FPS = 24

# Colors
BG_DARK       = (10, 14, 32)
BG_PANEL      = (16, 22, 52)
BG_CARD       = (22, 30, 68)
ACCENT_CYAN   = (0, 220, 255)
ACCENT_BLUE   = (60, 130, 250)
ACCENT_VIOLET = (140, 50, 240)
ACCENT_PINK   = (255, 60, 140)
ACCENT_YELLOW = (255, 210, 50)
ACCENT_GREEN  = (70, 230, 130)
TEXT_WHITE    = (255, 255, 255)
TEXT_LIGHT    = (210, 220, 245)
TEXT_MUTED    = (130, 145, 185)
TEXT_CODE     = (170, 255, 170)

def get_font(size=28, bold=False, mono=False):
    candidates = []
    if mono:
        candidates = ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"]
    elif bold:
        candidates = ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/calibrib.ttf"]
    else:
        candidates = ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/calibri.ttf"]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except:
                pass
    return ImageFont.load_default()

def draw_top_bar(draw, subtitle="DBMS College Presentation"):
    draw.rectangle([0, 0, W, 68], fill=(8, 12, 28))
    draw.ellipse([24, 14, 60, 50], fill=ACCENT_CYAN)
    draw.text((34, 18), "S", font=get_font(26, bold=True), fill=BG_DARK)
    draw.text((72, 18), "SocialConnect", font=get_font(26, bold=True), fill=TEXT_WHITE)
    draw.text((260, 22), "•   " + subtitle, font=get_font(20), fill=TEXT_MUTED)
    draw.rectangle([0, 66, W, 68], fill=ACCENT_CYAN)

def get_audio_duration(path):
    cmd = [FFMPEG, "-i", path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    for line in res.stderr.split('\n'):
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
    return 25.0

def make_pipe(out_video_path):
    return subprocess.Popen([
        FFMPEG, '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo',
        '-s', f'{W}x{H}', '-pix_fmt', 'rgb24', '-r', str(FPS),
        '-i', '-', '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
        out_video_path
    ], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ─── ANIMATED SCENE RENDERERS ──────────────────────────────────────────────────

def render_clip01(num_frames, out_path):
    """Scene 1: Rotating Orbit Rings, Neon Pulse Title & Floating Particles"""
    pipe = make_pipe(out_path)
    base = Image.new('RGB', (W, H), BG_DARK)
    d_base = ImageDraw.Draw(base)
    for y in range(H):
        t = y / H
        d_base.line([(0, y), (W, y)], fill=(int(8+10*t), int(12+8*t), int(28+20*t)))
    
    cx, cy = W // 2, H // 2 - 40
    for f in range(num_frames):
        img = base.copy()
        draw = ImageDraw.Draw(img)
        draw_top_bar(draw, "Welcome & Overview")
        
        # Rotating orbits
        ang = f * 0.04
        r1, r2 = 260, 180
        draw.ellipse([cx - r1, cy - r1, cx + r1, cy + r1], outline=(30, 50, 120), width=2)
        draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=(50, 80, 170), width=2)
        
        # Orbiting satellites
        ox1 = cx + int(r1 * math.cos(ang))
        oy1 = cy + int(r1 * math.sin(ang))
        ox2 = cx + int(r2 * math.cos(-ang*1.5))
        oy2 = cy + int(r2 * math.sin(-ang*1.5))
        draw.ellipse([ox1-8, oy1-8, ox1+8, oy1+8], fill=ACCENT_CYAN)
        draw.ellipse([ox2-6, oy2-6, ox2+6, oy2+6], fill=ACCENT_VIOLET)
        
        # Central glowing badge
        pulse = 4 * math.sin(f * 0.1)
        br = int(60 + pulse)
        draw.ellipse([cx - br, cy - br, cx + br, cy + br], fill=ACCENT_VIOLET)
        draw.ellipse([cx - br + 5, cy - br + 5, cx + br - 5, cy + br - 5], fill=ACCENT_CYAN)
        draw.text((cx - 24, cy - 35), "S", font=get_font(64, bold=True), fill=BG_DARK)
        
        # Animated title
        title_font = get_font(84, bold=True)
        title = "SOCIALCONNECT"
        draw.text((cx - 360, cy + 110), title, font=title_font, fill=TEXT_WHITE)
        
        sub1 = "Social Media Database Management System"
        draw.text((cx - 380, cy + 215), sub1, font=get_font(38), fill=ACCENT_CYAN)
        
        sub2 = "Python Flask  •  PostgreSQL  •  psycopg2  •  Modern JavaScript"
        draw.text((cx - 365, cy + 275), sub2, font=get_font(26), fill=TEXT_MUTED)
        
        # Badges
        badges = ["Full 3-Tier Stack", "5 DB Tables", "11 API Endpoints", "Full CRUD Operations"]
        bx = 280
        for i, b in enumerate(badges):
            b_alpha = min(1.0, max(0.0, (f - i*10) / 20))
            if b_alpha > 0:
                draw.rounded_rectangle([bx, H - 120, bx + 300, H - 65], radius=14, fill=BG_CARD, outline=ACCENT_CYAN, width=2)
                draw.text((bx + 30, H - 105), b, font=get_font(22, bold=True), fill=TEXT_WHITE)
            bx += 345
        
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    pipe.wait()

def render_clip02(num_frames, out_path):
    """Scene 2: Split Screen — UI vs Database with Dynamic Flowing Packets"""
    pipe = make_pipe(out_path)
    base = Image.new('RGB', (W, H), BG_DARK)
    d = ImageDraw.Draw(base)
    draw_top_bar(d, "Problem Statement & Database Need")
    
    # Left Card — UI Mockup
    d.rounded_rectangle([60, 110, 880, 990], radius=16, fill=BG_PANEL, outline=(40, 60, 140), width=2)
    d.rounded_rectangle([60, 110, 880, 170], radius=16, fill=(22, 30, 75))
    d.text((90, 126), "🌐 User Interaction (Frontend Browser)", font=get_font(26, bold=True), fill=ACCENT_CYAN)
    
    # Right Card — PostgreSQL Tables
    d.rounded_rectangle([1040, 110, 1860, 990], radius=16, fill=BG_PANEL, outline=(40, 60, 140), width=2)
    d.rounded_rectangle([1040, 110, 1860, 170], radius=16, fill=(22, 30, 75))
    d.text((1070, 126), "🐘 Relational Storage (PostgreSQL DBMS)", font=get_font(26, bold=True), fill=ACCENT_YELLOW)
    
    # Static content inside left
    ui_items = [
        ("User clicks 'Publish Post'", "Content + Author ID sent as JSON"),
        ("User clicks 'Like Post'", "Checks and records interaction safely"),
        ("User sends Direct Message", "Private message delivered to recipient"),
        ("Live Feed Exploration", "Requests sorted posts with like counts")
    ]
    for idx, (head, sub) in enumerate(ui_items):
        uy = 210 + idx * 190
        d.rounded_rectangle([90, uy, 850, uy+150], radius=12, fill=BG_CARD)
        d.text((120, uy+20), f"⚡ {head}", font=get_font(24, bold=True), fill=TEXT_WHITE)
        d.text((120, uy+65), sub, font=get_font(20), fill=TEXT_LIGHT)
    
    # Static content inside right
    tables = [
        ("TABLE: posts", "post_id (PK), user_id (FK), content, created_at"),
        ("TABLE: likes", "like_id (PK), post_id (FK), user_id (FK) [UNIQUE]"),
        ("TABLE: messages", "message_id (PK), sender_id (FK), recipient_id (FK)"),
        ("TABLE: users", "user_id (PK), username, email, full_name, bio")
    ]
    for idx, (tname, cols) in enumerate(tables):
        ty = 210 + idx * 190
        d.rounded_rectangle([1070, ty, 1830, ty+150], radius=12, fill=BG_CARD, outline=(70, 100, 200), width=1)
        d.text((1100, ty+20), f"🗄️ {tname}", font=get_font(24, bold=True), fill=ACCENT_CYAN)
        d.text((1100, ty+65), cols, font=get_font(20, mono=True), fill=TEXT_LIGHT)
    
    for f in range(num_frames):
        img = base.copy()
        draw = ImageDraw.Draw(img)
        
        # Animated packets flowing between left and right
        p_progress = (f % 40) / 40.0
        for row in range(4):
            py = 285 + row * 190
            px = int(880 + (1040 - 880) * p_progress)
            draw.line([(880, py), (1040, py)], fill=(40, 60, 120), width=2)
            draw.ellipse([px-8, py-8, px+8, py+8], fill=ACCENT_CYAN if row%2==0 else ACCENT_YELLOW)
        
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    pipe.wait()

def render_clip03(num_frames, out_path):
    """Scene 3: 8 Core Feature Cards with Staggered Entrance & Glowing Border"""
    pipe = make_pipe(out_path)
    base = Image.new('RGB', (W, H), BG_DARK)
    d = ImageDraw.Draw(base)
    draw_top_bar(d, "Objectives & Verified Features")
    d.text((80, 95), "Verified SocialConnect Functionality", font=get_font(44, bold=True), fill=TEXT_WHITE)
    d.text((80, 150), "Every feature below is implemented in app.py and backed by PostgreSQL", font=get_font(22), fill=TEXT_MUTED)
    
    features = [
        ("📝", "Create Posts", "Publish text with optional image URL; returns post_id via RETURNING"),
        ("📰", "Live Post Feed", "Newest-first chronological feed joined with authors and like counts"),
        ("🔍", "Keyword Search", "Live query filtering using SQL case-insensitive ILIKE matching"),
        ("❤️", "Like / Unlike", "Idempotent likes; unique constraint prevents duplicate user likes"),
        ("💬", "Comments", "Threaded comment discussions attached to each individual post"),
        ("👤", "User Profiles", "Displays user bio, email, and live aggregated post counts"),
        ("✉️", "Direct Messages", "Private messaging interface with auto-refresh every 5 seconds"),
        ("🌓", "Theme Switcher", "Dark and light mode UI toggle persisted in browser localStorage")
    ]
    
    for f in range(num_frames):
        img = base.copy()
        draw = ImageDraw.Draw(img)
        
        for i, (icon, title, desc) in enumerate(features):
            col = i % 4
            row = i // 4
            x = 80 + col * 440
            y = 205 + row * 380
            
            # Animation offset
            delay = i * 6
            t = min(1.0, max(0.0, (f - delay) / 12))
            cur_y = int(y + (1.0 - t) * 40)
            
            if t > 0:
                glow = ACCENT_CYAN if (f // 20) % 8 == i else (40, 60, 140)
                draw.rounded_rectangle([x, cur_y, x+410, cur_y+340], radius=16, fill=BG_CARD, outline=glow, width=2)
                draw.ellipse([x+24, cur_y+24, x+84, cur_y+84], fill=(30, 45, 95))
                draw.text((x+36, cur_y+32), icon, font=get_font(36), fill=TEXT_WHITE)
                draw.text((x+105, cur_y+38), title, font=get_font(26, bold=True), fill=TEXT_WHITE)
                
                # Wrap desc
                words = desc.split()
                line1 = " ".join(words[:6])
                line2 = " ".join(words[6:12])
                line3 = " ".join(words[12:])
                draw.text((x+24, cur_y+115), line1, font=get_font(20), fill=TEXT_LIGHT)
                draw.text((x+24, cur_y+150), line2, font=get_font(20), fill=TEXT_LIGHT)
                draw.text((x+24, cur_y+185), line3, font=get_font(20), fill=TEXT_LIGHT)
                
                # Verified badge
                draw.rounded_rectangle([x+24, cur_y+265, x+200, cur_y+305], radius=10, fill=(15, 45, 30))
                draw.text((x+40, cur_y+273), "✓ Verified in Code", font=get_font(18, bold=True), fill=ACCENT_GREEN)
        
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    pipe.wait()

def render_clip04(num_frames, out_path):
    """Scene 4: Three-Tier Tech Stack with Animated Energy Pulses"""
    pipe = make_pipe(out_path)
    base = Image.new('RGB', (W, H), BG_DARK)
    d = ImageDraw.Draw(base)
    draw_top_bar(d, "Technology Stack & Architecture")
    d.text((80, 95), "Three-Tier Architectural Stack", font=get_font(44, bold=True), fill=TEXT_WHITE)
    
    tiers = [
        ("FRONTEND TIER", "HTML5  •  CSS3  •  JavaScript (ES6+)",
         "Browser UI, DOM rendering, fetch() API, responsive dark/light styling", ACCENT_CYAN, 190),
        ("BACKEND TIER", "Python Flask  •  psycopg2  •  flask-cors",
         "11 REST routes, JSON validation, parameterized SQL execution, transactions", ACCENT_YELLOW, 480),
        ("DATABASE TIER", "PostgreSQL (social_media_db)",
         "Relational tables, primary & foreign keys, UNIQUE constraint, ACID compliance", ACCENT_GREEN, 770)
    ]
    
    for label, tech, desc, col, y in tiers:
        d.rounded_rectangle([100, y, 1820, y+230], radius=16, fill=BG_PANEL, outline=col, width=2)
        d.rounded_rectangle([100, y, 140, y+230], radius=14, fill=col)
        d.text((170, y+24), label, font=get_font(30, bold=True), fill=col)
        d.text((170, y+75), tech, font=get_font(32, bold=True), fill=TEXT_WHITE)
        d.text((170, y+135), desc, font=get_font(22), fill=TEXT_LIGHT)
    
    for f in range(num_frames):
        img = base.copy()
        draw = ImageDraw.Draw(img)
        
        # Pulses traveling between Tier 1 <-> Tier 2 and Tier 2 <-> Tier 3
        p1 = (f % 30) / 30.0
        p2 = ((f + 15) % 30) / 30.0
        
        # Link 1: 420 to 480
        y1 = int(420 + 60 * p1)
        draw.text((900, 435), "▲ HTTP GET/POST (JSON) ▼", font=get_font(22, bold=True), fill=ACCENT_CYAN)
        draw.ellipse([860, y1-6, 876, y1+6], fill=ACCENT_CYAN)
        draw.ellipse([1250, y1-6, 1266, y1+6], fill=ACCENT_YELLOW)
        
        # Link 2: 710 to 770
        y2 = int(710 + 60 * p2)
        draw.text((880, 725), "▲ SQL Queries / Rows (psycopg2) ▼", font=get_font(22, bold=True), fill=ACCENT_GREEN)
        draw.ellipse([840, y2-6, 856, y2+6], fill=ACCENT_YELLOW)
        draw.ellipse([1280, y2-6, 1296, y2+6], fill=ACCENT_GREEN)
        
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    pipe.wait()

def render_clip05(num_frames, out_path):
    """Scene 5: LIVE UI DEMO SIMULATION (Cursor moves, types post, clicks publish, shows toast & new post)"""
    pipe = make_pipe(out_path)
    
    for f in range(num_frames):
        img = Image.new('RGB', (W, H), BG_DARK)
        draw = ImageDraw.Draw(img)
        draw_top_bar(draw, "Live Frontend Demonstration")
        
        # Browser chrome
        draw.rounded_rectangle([80, 90, 1840, 1020], radius=16, fill=(12, 16, 38), outline=ACCENT_CYAN, width=2)
        draw.rounded_rectangle([80, 90, 1840, 145], radius=14, fill=(22, 28, 65))
        # Traffic lights
        for i, col in enumerate([(255, 90, 90), (255, 190, 60), (80, 210, 100)]):
            draw.ellipse([105+i*28, 110, 123+i*28, 128], fill=col)
        # URL bar
        draw.rounded_rectangle([200, 104, 1100, 134], radius=6, fill=(16, 22, 50))
        draw.text((220, 108), "🔒 http://localhost:5000  —  SocialConnect", font=get_font(20), fill=TEXT_LIGHT)
        
        # Sidebar
        draw.rectangle([82, 145, 260, 1018], fill=(16, 22, 52))
        navs = ["⌂  Home", "⌕  Explore", "＋ Create Post", "♙  Profiles", "▤  Messages"]
        for idx, n in enumerate(navs):
            ny = 180 + idx * 55
            if idx == 0:
                draw.rounded_rectangle([90, ny-6, 250, ny+36], radius=8, fill=(35, 55, 130))
            draw.text((105, ny), n, font=get_font(20, bold=True), fill=TEXT_WHITE if idx==0 else TEXT_MUTED)
        
        # Main area
        # Create Post Box
        draw.rounded_rectangle([285, 165, 1400, 395], radius=12, fill=BG_PANEL, outline=(40, 60, 130), width=1)
        draw.text((310, 180), "CREATE POST", font=get_font(18, bold=True), fill=ACCENT_CYAN)
        draw.text((310, 205), "What's on your mind?", font=get_font(24, bold=True), fill=TEXT_WHITE)
        
        # User dropdown
        draw.rounded_rectangle([310, 245, 680, 285], radius=6, fill=BG_CARD, outline=ACCENT_CYAN if f > 60 else (40, 60, 120), width=1)
        user_name = "Alex Rao (@alex_r)" if f > 40 else "Choose a user..."
        draw.text((325, 252), user_name, font=get_font(18), fill=TEXT_WHITE if f > 40 else TEXT_MUTED)
        
        # Textarea
        draw.rounded_rectangle([310, 298, 1370, 345], radius=6, fill=BG_CARD)
        full_text = "Exploring PostgreSQL & Flask on SocialConnect! 🚀"
        typed_len = int(min(len(full_text), max(0, (f - 90) * 0.45)))
        typed_text = full_text[:typed_len]
        draw.text((325, 310), typed_text + ("|" if (f // 8) % 2 == 0 and f > 90 and typed_len < len(full_text) else ""), font=get_font(20), fill=TEXT_LIGHT)
        
        # Publish button
        btn_pressed = 220 < f < 250
        btn_col = (0, 180, 210) if btn_pressed else ACCENT_CYAN
        draw.rounded_rectangle([1220, 352, 1370, 388], radius=8, fill=btn_col)
        draw.text((1240, 358), "＋ Publish", font=get_font(20, bold=True), fill=BG_DARK)
        
        # Toast notification sliding down
        if f > 240:
            toast_t = min(1.0, (f - 240) / 15)
            toast_y = int(145 + toast_t * 25)
            draw.rounded_rectangle([750, toast_y, 1150, toast_y+42], radius=10, fill=ACCENT_GREEN)
            draw.text((775, toast_y+8), "✓ Your post has been published!", font=get_font(20, bold=True), fill=BG_DARK)
        
        # Feed cards below
        # Newly published post drops in after f > 250
        posts = []
        if f > 250:
            posts.append(("AR", "Alex Rao", "@alex_r • Just now", full_text, 0, ACCENT_CYAN))
        posts.append(("PK", "Priya Kumar", "@priya_k • 10m ago", "Loving the dark theme and direct messaging speed!", 4, ACCENT_VIOLET))
        posts.append(("RM", "Rajan Mehta", "@rajan_m • 1h ago", "DBMS concepts demonstrated with real SQL queries.", 7, ACCENT_PINK))
        
        card_y = 415
        for ini, name, meta, body, lk, col in posts:
            draw.rounded_rectangle([285, card_y, 1400, card_y+130], radius=12, fill=BG_PANEL)
            draw.ellipse([305, card_y+15, 345, card_y+55], fill=col)
            draw.text((315, card_y+22), ini, font=get_font(20, bold=True), fill=TEXT_WHITE)
            draw.text((360, card_y+15), name, font=get_font(22, bold=True), fill=TEXT_WHITE)
            draw.text((360, card_y+40), meta, font=get_font(16), fill=TEXT_MUTED)
            draw.text((305, card_y+65), body, font=get_font(20), fill=TEXT_LIGHT)
            draw.text((305, card_y+98), f"♡ Like ({lk})    💬 Comments    🗑 Delete", font=get_font(18), fill=ACCENT_CYAN)
            card_y += 145
            if card_y > 980:
                break
        
        # Right sidebar info
        draw.rounded_rectangle([1430, 165, 1815, 600], radius=12, fill=BG_PANEL)
        draw.text((1455, 190), "COMMUNITY", font=get_font(18, bold=True), fill=ACCENT_CYAN)
        draw.text((1455, 225), "Connected Members", font=get_font(22, bold=True), fill=TEXT_WHITE)
        draw.text((1455, 275), "• Alex Rao (@alex_r)\n• Priya Kumar (@priya_k)\n• Rajan Mehta (@rajan_m)", font=get_font(20), fill=TEXT_LIGHT)
        
        # Simulated mouse cursor moving across screen
        if f < 60:
            mx, my = int(500 + f * 2), int(350 - f * 1.5)
        elif f < 100:
            mx, my = int(620 - (f-60)*4), int(260 + (f-60)*1)
        elif f < 220:
            mx, my = int(460 + (f-100)*7), int(300 + (f-100)*0.5)
        else:
            mx, my = 1290, 370
        
        # Draw cursor
        draw.polygon([(mx, my), (mx+18, my+18), (mx+8, my+18), (mx+12, my+28), (mx+6, my+30), (mx+2, my+20), (mx, my)], fill=(255, 255, 255), outline=(0, 0, 0))
        
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    pipe.wait()

def render_clip06(num_frames, out_path):
    """Scene 6: Animated Bidirectional Architecture Flow"""
    pipe = make_pipe(out_path)
    base = Image.new('RGB', (W, H), BG_DARK)
    d = ImageDraw.Draw(base)
    draw_top_bar(d, "System Architecture & Request-Response Flow")
    d.text((80, 95), "End-to-End System Architecture", font=get_font(44, bold=True), fill=TEXT_WHITE)
    
    stages = [
        ("USER INTERFACE", "Browser / JavaScript Fetch", ACCENT_CYAN, 180),
        ("HTTP PROTOCOL", "POST /api/posts (JSON Body)", ACCENT_VIOLET, 340),
        ("FLASK BACKEND", "app.py API Route Handler", ACCENT_YELLOW, 500),
        ("PSYCOPG2 DRIVER", "Parameterized SQL Execution", ACCENT_PINK, 660),
        ("POSTGRESQL DBMS", "social_media_db Engine", ACCENT_GREEN, 820)
    ]
    for lbl, desc, col, y in stages:
        # Request box on left
        d.rounded_rectangle([150, y, 900, y+110], radius=14, fill=BG_PANEL, outline=col, width=2)
        d.text((180, y+20), lbl, font=get_font(26, bold=True), fill=col)
        d.text((180, y+60), desc, font=get_font(20), fill=TEXT_LIGHT)
        
        # Response box on right
        d.rounded_rectangle([1020, y, 1770, y+110], radius=14, fill=BG_PANEL, outline=col, width=2)
        d.text((1050, y+20), f"RETURN: {lbl}", font=get_font(26, bold=True), fill=col)
    
    d.text((1050, 880), "Query Results & Status Codes", font=get_font(20), fill=TEXT_LIGHT)
    d.text((1050, 720), "Result Rows via cursor.fetchall()", font=get_font(20), fill=TEXT_LIGHT)
    d.text((1050, 560), "jsonify(posts), HTTP 200/201", font=get_font(20), fill=TEXT_LIGHT)
    d.text((1050, 400), "HTTP JSON Response Stream", font=get_font(20), fill=TEXT_LIGHT)
    d.text((1050, 240), "DOM Updated without Page Reload", font=get_font(20), fill=TEXT_LIGHT)
    
    for f in range(num_frames):
        img = base.copy()
        draw = ImageDraw.Draw(img)
        
        # Moving request dots down (blue/yellow)
        p_down = (f % 45) / 45.0
        y_down = int(240 + (820 - 240) * p_down)
        draw.ellipse([515, y_down-10, 535, y_down+10], fill=ACCENT_CYAN)
        draw.text((450, 955), "▼ REQUEST FLOW (Downwards) ▼", font=get_font(22, bold=True), fill=ACCENT_CYAN)
        
        # Moving response dots up (green/cyan)
        p_up = 1.0 - ((f % 45) / 45.0)
        y_up = int(240 + (820 - 240) * p_up)
        draw.ellipse([1385, y_up-10, 1405, y_up+10], fill=ACCENT_GREEN)
        draw.text((1300, 955), "▲ RESPONSE FLOW (Upwards) ▲", font=get_font(22, bold=True), fill=ACCENT_GREEN)
        
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    pipe.wait()

def render_clip07(num_frames, out_path):
    """Scene 7: Code Editor with Animated Highlight Scanning Box"""
    pipe = make_pipe(out_path)
    base = Image.new('RGB', (W, H), BG_DARK)
    d = ImageDraw.Draw(base)
    draw_top_bar(d, "Backend Implementation — Python Flask")
    d.text((80, 95), "Flask API & Parameterized SQL Implementation", font=get_font(44, bold=True), fill=TEXT_WHITE)
    
    # Editor window
    d.rounded_rectangle([80, 160, 1840, 1020], radius=16, fill=(12, 16, 36), outline=(40, 60, 140), width=2)
    d.rounded_rectangle([80, 160, 1840, 210], radius=14, fill=(20, 26, 60))
    d.text((110, 175), "📄 app.py  —  Visual Studio Code", font=get_font(22, bold=True), fill=TEXT_WHITE)
    
    code_lines = [
        "@app.route('/api/posts', methods=['GET'])",
        "def get_posts():",
        "    search = request.args.get('search', '').strip()",
        "    conn = get_db_connection()",
        "    cur = conn.cursor()",
        "    cur.execute('''",
        "        SELECT p.post_id, u.username, u.full_name, p.content, p.created_at,",
        "               COUNT(DISTINCT l.like_id) AS likes",
        "        FROM posts p",
        "        JOIN users u ON p.user_id = u.user_id",
        "        LEFT JOIN likes l ON p.post_id = l.post_id",
        "        WHERE p.content ILIKE %s",
        "        GROUP BY p.post_id, u.username, u.full_name, p.content, p.created_at",
        "        ORDER BY p.created_at DESC;",
        "    ''', (f'%{search}%',))",
        "    posts = cur.fetchall()",
        "    return jsonify(posts)",
        "",
        "# Idempotent Like Handling with Conflict Resolution",
        "cur.execute('INSERT INTO likes (post_id, user_id) VALUES (%s, %s)'",
        "            ' ON CONFLICT (post_id, user_id) DO NOTHING;', (post_id, user_id))",
        "conn.commit()  # Safe transaction commit",
    ]
    
    for idx, l in enumerate(code_lines):
        col = ACCENT_YELLOW if l.startswith("@") or l.startswith("def") else ACCENT_CYAN if "SELECT" in l or "INSERT" in l or "ON CONFLICT" in l else TEXT_CODE if "commit" in l or "fetchall" in l else TEXT_LIGHT
        d.text((120, 230 + idx * 36), l, font=get_font(21, mono=True), fill=col)
    
    for f in range(num_frames):
        img = base.copy()
        draw = ImageDraw.Draw(img)
        
        # Animated scanning highlight rectangle
        scan_y = int(225 + ((f * 1.8) % 720))
        draw.rounded_rectangle([100, scan_y, 1820, scan_y+42], radius=6, fill=None, outline=ACCENT_CYAN, width=2)
        
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    pipe.wait()

def render_clip08(num_frames, out_path):
    """Scene 8: PostgreSQL Schema & ER Diagram with Pulsing Foreign Keys"""
    pipe = make_pipe(out_path)
    base = Image.new('RGB', (W, H), BG_DARK)
    d = ImageDraw.Draw(base)
    draw_top_bar(d, "Database Schema & Entity-Relationship Model")
    d.text((80, 95), "PostgreSQL Database: social_media_db", font=get_font(44, bold=True), fill=TEXT_WHITE)
    
    tables = [
        ("USERS (Primary Entity)", [("user_id", "INTEGER PK"), ("username", "VARCHAR UNIQUE"), ("email", "VARCHAR"), ("full_name", "VARCHAR"), ("bio", "TEXT")], 80, 180, ACCENT_CYAN),
        ("POSTS (User Authored)", [("post_id", "INTEGER PK"), ("user_id", "INTEGER FK -> users"), ("content", "TEXT"), ("image_url", "TEXT NULL"), ("created_at", "TIMESTAMP")], 680, 180, ACCENT_YELLOW),
        ("LIKES (Interaction M:N)", [("like_id", "INTEGER PK"), ("post_id", "INTEGER FK -> posts"), ("user_id", "INTEGER FK -> users"), ("CONSTRAINT", "UNIQUE(post_id, user_id)")], 1280, 180, ACCENT_PINK),
        ("COMMENTS (Discussions)", [("comment_id", "INTEGER PK"), ("post_id", "INTEGER FK -> posts"), ("user_id", "INTEGER FK -> users"), ("comment_text", "TEXT"), ("created_at", "TIMESTAMP")], 380, 620, ACCENT_VIOLET),
        ("MESSAGES (Direct Chat)", [("message_id", "INTEGER PK"), ("sender_id", "INTEGER FK -> users"), ("recipient_id", "INTEGER FK -> users"), ("message_text", "TEXT"), ("created_at", "TIMESTAMP")], 1080, 620, ACCENT_GREEN),
    ]
    
    for tname, cols, tx, ty, tcol in tables:
        d.rounded_rectangle([tx, ty, tx+550, ty+380], radius=16, fill=BG_PANEL, outline=tcol, width=2)
        d.rounded_rectangle([tx, ty, tx+550, ty+55], radius=14, fill=tcol)
        d.text((tx+20, ty+14), tname, font=get_font(22, bold=True), fill=BG_DARK)
        for cidx, (cname, ctype) in enumerate(cols):
            cy = ty + 75 + cidx * 55
            d.text((tx+20, cy), cname, font=get_font(20, bold=True), fill=TEXT_WHITE)
            d.text((tx+220, cy), ctype, font=get_font(18, mono=True), fill=ACCENT_CYAN if "PK" in ctype else ACCENT_YELLOW if "FK" in ctype else TEXT_MUTED)
    
    for f in range(num_frames):
        img = base.copy()
        draw = ImageDraw.Draw(img)
        
        # Pulsing connector lines between tables
        pulse_col = ACCENT_CYAN if (f // 10) % 2 == 0 else ACCENT_YELLOW
        draw.line([(630, 320), (680, 320)], fill=pulse_col, width=3)
        draw.line([(1230, 320), (1280, 320)], fill=pulse_col, width=3)
        draw.line([(350, 560), (450, 620)], fill=pulse_col, width=3)
        draw.line([(1400, 560), (1300, 620)], fill=pulse_col, width=3)
        
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    pipe.wait()

def render_clip09(num_frames, out_path):
    """Scene 9: Core DBMS Concepts Interactive Visual"""
    pipe = make_pipe(out_path)
    base = Image.new('RGB', (W, H), BG_DARK)
    d = ImageDraw.Draw(base)
    draw_top_bar(d, "DBMS Academic Concepts in Practice")
    d.text((80, 95), "Key DBMS Principles Demonstrated", font=get_font(44, bold=True), fill=TEXT_WHITE)
    
    concepts = [
        ("🔑", "Primary Key Uniqueness", "Guarantees row identity across users, posts, likes, comments, and messages tables."),
        ("🔗", "Foreign Key Integrity", "Enforces relational links between authors, posts, comments, and direct chats."),
        ("🔄", "Multi-Table JOINs", "Combines posts with authors (INNER JOIN) and like counts (LEFT JOIN) seamlessly."),
        ("📊", "Aggregation & GROUP BY", "Calculates like counters via COUNT(DISTINCT l.like_id) grouped per post."),
        ("➕", "INSERT with RETURNING", "Retrieves newly generated serial primary key IDs immediately in one roundtrip."),
        ("⚡", "Idempotent ON CONFLICT", "Eliminates duplicate likes at the database engine level via UNIQUE constraints."),
        ("💾", "Transaction Management", "Wraps state modifications in explicit conn.commit() and rollback() error blocks."),
        ("✅", "Full CRUD Operations", "Supports Create, Read, Update, and Delete across multiple relational entities.")
    ]
    
    for idx, (icon, title, desc) in enumerate(concepts):
        col = idx % 4
        row = idx // 4
        x = 80 + col * 440
        y = 190 + row * 400
        d.rounded_rectangle([x, y, x+410, y+360], radius=16, fill=BG_PANEL, outline=(40, 60, 140), width=2)
        d.text((x+24, y+24), icon, font=get_font(38), fill=TEXT_WHITE)
        d.text((x+80, y+30), title, font=get_font(24, bold=True), fill=TEXT_WHITE)
        
        words = desc.split()
        d.text((x+24, y+100), " ".join(words[:6]), font=get_font(20), fill=TEXT_LIGHT)
        d.text((x+24, y+135), " ".join(words[6:12]), font=get_font(20), fill=TEXT_LIGHT)
        d.text((x+24, y+170), " ".join(words[12:]), font=get_font(20), fill=TEXT_LIGHT)
        
        d.rounded_rectangle([x+24, y+280, x+380, y+330], radius=10, fill=(18, 40, 70))
        d.text((x+40, y+292), "Active in SocialConnect", font=get_font(18, bold=True), fill=ACCENT_CYAN)
    
    for f in range(num_frames):
        img = base.copy()
        draw = ImageDraw.Draw(img)
        # Highlight concept cards sequentially
        hi = (f // 25) % 8
        col = hi % 4
        row = hi // 4
        x = 80 + col * 440
        y = 190 + row * 400
        draw.rounded_rectangle([x, y, x+410, y+360], radius=16, outline=ACCENT_CYAN, width=3)
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    pipe.wait()

def render_clip10(num_frames, out_path):
    """Scene 10: Live SQL Terminal Execution Video Clip"""
    pipe = make_pipe(out_path)
    
    for f in range(num_frames):
        img = Image.new('RGB', (W, H), BG_DARK)
        draw = ImageDraw.Draw(img)
        draw_top_bar(draw, "Practical SQL Query Demonstration")
        draw.text((80, 95), "Executing Complex Queries in PostgreSQL", font=get_font(44, bold=True), fill=TEXT_WHITE)
        
        # Terminal box
        draw.rounded_rectangle([80, 160, 1840, 1020], radius=16, fill=(10, 14, 25), outline=(40, 60, 140), width=2)
        draw.rounded_rectangle([80, 160, 1840, 215], radius=14, fill=(18, 24, 45))
        draw.text((110, 178), "terminal: psql -U postgres -d social_media_db", font=get_font(22, bold=True), fill=ACCENT_CYAN)
        
        query = (
            "SELECT p.post_id, u.username, p.content, COUNT(DISTINCT l.like_id) AS likes\n"
            "FROM posts p\n"
            "JOIN users u ON p.user_id = u.user_id\n"
            "LEFT JOIN likes l ON p.post_id = l.post_id\n"
            "GROUP BY p.post_id, u.username, p.content\n"
            "ORDER BY p.created_at DESC LIMIT 3;"
        )
        
        draw.text((110, 240), "social_media_db=> ", font=get_font(22, mono=True, bold=True), fill=ACCENT_YELLOW)
        draw.text((360, 240), query, font=get_font(22, mono=True), fill=TEXT_WHITE)
        
        # Execution flash and results appearing after f > 120
        if f > 120:
            draw.text((110, 480), "Execution time: 4.18 ms  |  Rows returned: 3", font=get_font(20, bold=True), fill=ACCENT_GREEN)
            draw.rectangle([110, 520, 1800, 522], fill=ACCENT_CYAN)
            
            headers = ["post_id", "username", "content", "likes"]
            hx = [130, 280, 520, 1650]
            for hidx, hname in enumerate(headers):
                draw.text((hx[hidx], 535), hname, font=get_font(20, mono=True, bold=True), fill=ACCENT_CYAN)
            draw.rectangle([110, 575, 1800, 577], fill=ACCENT_CYAN)
            
            rows = [
                ("1", "alex_r", "Exploring PostgreSQL & Flask on SocialConnect! 🚀", "5"),
                ("2", "priya_k", "Loving the dark theme and direct messaging speed!", "12"),
                ("3", "rajan_m", "DBMS concepts demonstrated with real SQL queries.", "3")
            ]
            for ridx, r in enumerate(rows):
                ry = 595 + ridx * 55
                draw.text((hx[0], ry), r[0], font=get_font(20, mono=True), fill=TEXT_WHITE)
                draw.text((hx[1], ry), r[1], font=get_font(20, mono=True), fill=ACCENT_YELLOW)
                draw.text((hx[2], ry), r[2], font=get_font(20, mono=True), fill=TEXT_LIGHT)
                draw.text((hx[3], ry), r[3], font=get_font(20, mono=True), fill=ACCENT_GREEN)
                draw.line([(110, ry+45), (1800, ry+45)], fill=(30, 40, 75))
            
            draw.text((110, 790), "(3 rows selected)", font=get_font(20, mono=True), fill=TEXT_MUTED)
        
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    pipe.wait()

def render_clip11(num_frames, out_path):
    """Scene 11: End-to-End Execution Flow Pipeline with Moving Progress Node"""
    pipe = make_pipe(out_path)
    base = Image.new('RGB', (W, H), BG_DARK)
    d = ImageDraw.Draw(base)
    draw_top_bar(d, "End-to-End Request Lifecycle")
    d.text((80, 95), "Complete User Action Data Flow", font=get_font(44, bold=True), fill=TEXT_WHITE)
    
    steps = [
        ("1. User Action", "Click 'Publish Post' button in browser UI"),
        ("2. JavaScript Fetch", "Serializes inputs into JSON payload; sends POST"),
        ("3. Flask Routing", "Validates presence of user_id and content"),
        ("4. psycopg2 Query", "Executes parameterized INSERT ... RETURNING"),
        ("5. PostgreSQL Storage", "Commits new row; generates post_id"),
        ("6. API Response", "Returns HTTP 201 with new post ID in JSON"),
        ("7. Dynamic DOM Update", "Prepends new post card onto feed instantly")
    ]
    for idx, (title, desc) in enumerate(steps):
        sy = 190 + idx * 115
        d.rounded_rectangle([150, sy, 1770, sy+95], radius=14, fill=BG_PANEL, outline=(40, 60, 140), width=2)
        d.text((190, sy+18), title, font=get_font(26, bold=True), fill=ACCENT_CYAN)
        d.text((190, sy+56), desc, font=get_font(20), fill=TEXT_LIGHT)
    
    for f in range(num_frames):
        img = base.copy()
        draw = ImageDraw.Draw(img)
        
        # Traveling glowing progress orb across the 7 stages
        p = (f % 60) / 60.0
        cur_y = int(235 + (880 - 235) * p)
        draw.ellipse([110, cur_y-14, 138, cur_y+14], fill=ACCENT_CYAN)
        draw.line([(124, 235), (124, 880)], fill=(40, 60, 120), width=3)
        
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    pipe.wait()

def render_clip12(num_frames, out_path):
    """Scene 12: Professional Outro with Glowing Particles & Celebration"""
    pipe = make_pipe(out_path)
    base = Image.new('RGB', (W, H), BG_DARK)
    d = ImageDraw.Draw(base)
    draw_top_bar(d, "Conclusion & Project Wrap-Up")
    
    cx, cy = W // 2, H // 2
    for f in range(num_frames):
        img = base.copy()
        draw = ImageDraw.Draw(img)
        
        # Floating celebration particles
        for i in range(25):
            px = int((i * 80 + f * 5) % W)
            py = int((H - ((f * 3 + i * 40) % H)))
            draw.ellipse([px-4, py-4, px+4, py+4], fill=ACCENT_CYAN if i%2==0 else ACCENT_VIOLET)
        
        # Title
        draw.text((cx - 380, cy - 140), "SOCIALCONNECT", font=get_font(88, bold=True), fill=TEXT_WHITE)
        draw.text((cx - 400, cy - 30), "Connecting Frontend, Backend, and Relational Database", font=get_font(34), fill=ACCENT_CYAN)
        
        # Thank You box
        draw.rounded_rectangle([cx - 240, cy + 50, cx + 240, cy + 140], radius=16, fill=(20, 30, 75), outline=ACCENT_CYAN, width=2)
        draw.text((cx - 140, cy + 68), "Thank You!", font=get_font(52, bold=True), fill=TEXT_WHITE)
        
        draw.text((cx - 280, cy + 180), "A Complete College DBMS viva & Evaluation Presentation", font=get_font(22), fill=TEXT_MUTED)
        
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    pipe.wait()

# ─── MAIN ORCHESTRATION ────────────────────────────────────────────────────────

def main():
    print("\n" + "="*60)
    print("  SocialConnect — 5-Minute Motion Video Builder")
    print("="*60)
    
    renderers = [
        ("clip01", render_clip01),
        ("clip02", render_clip02),
        ("clip03", render_clip03),
        ("clip04", render_clip04),
        ("clip05", render_clip05),
        ("clip06", render_clip06),
        ("clip07", render_clip07),
        ("clip08", render_clip08),
        ("clip09", render_clip09),
        ("clip10", render_clip10),
        ("clip11", render_clip11),
        ("clip12", render_clip12),
    ]
    
    scene_mp4s = []
    total_time = 0
    
    print("\nStep 1: Rendering 12 animated motion video clips with synchronized audio...")
    for idx, (cname, rfn) in enumerate(renderers, 1):
        audio_file = os.path.join(BASE, f"{cname}.mp3")
        dur = get_audio_duration(audio_file)
        total_time += dur
        num_frames = int(dur * FPS)
        
        raw_video = os.path.join(BASE, f"raw_{cname}.mp4")
        synced_scene = os.path.join(BASE, f"synced_{cname}.mp4")
        
        print(f"\n  [{idx}/12] Rendering {cname} ({dur:.1f}s, {num_frames} frames)...")
        rfn(num_frames, raw_video)
        
        # Mux with audio
        mux_cmd = [
            FFMPEG, "-y",
            "-i", raw_video,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            synced_scene
        ]
        subprocess.run(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(raw_video):
            os.remove(raw_video)
        scene_mp4s.append(synced_scene)
        print(f"  ✓ {cname} finished ({os.path.getsize(synced_scene)//1024} KB)")

    print(f"\nTotal video duration: {total_time:.1f}s ({total_time/60:.2f} minutes)")
    
    print("\nStep 2: Concatenating all scenes into final master video...")
    concat_list = os.path.join(BASE, "motion_concat_list.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for sc in scene_mp4s:
            f.write(f"file '{sc.replace(chr(92), '/')}'\n")
    
    concat_cmd = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        OUTPUT_MP4
    ]
    subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(OUTPUT_MP4):
        size_mb = os.path.getsize(OUTPUT_MP4) / (1024 * 1024)
        print(f"\n Master Video Assembled!")
        print(f" File: {OUTPUT_MP4}")
        print(f" Size: {size_mb:.2f} MB")
        
        # Copy to desktops
        print("\nStep 3: Copying to Desktop...")
        import shutil
        for dest in [DESKTOP_1, DESKTOP_2]:
            try:
                shutil.copy2(OUTPUT_MP4, dest)
                print(f"  ✓ Copied to {dest}")
            except Exception as e:
                print(f"  ✗ Failed copy to {dest}: {e}")
                
        # Clean up temporary synced clips
        for sc in scene_mp4s:
            try:
                os.remove(sc)
            except:
                pass
        try:
            os.remove(concat_list)
        except:
            pass
        print("✓ Cleanup complete!")

if __name__ == "__main__":
    main()
