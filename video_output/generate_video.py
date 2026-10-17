"""
SocialConnect — Video Generation Script
========================================
Generates a complete MP4 video explaining the SocialConnect DBMS project.
Uses: Pillow (image generation), gTTS (narration), MoviePy (video assembly)

Output: C:/Users/remme nivas/social_media_project/video_output/SocialConnect_DBMS_Explanation.mp4
"""

import os
import sys
import math
import textwrap
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE = r"C:\Users\remme nivas\social_media_project\video_output"
AUDIO_DIR = os.path.join(BASE, "audio_scenes")
FRAME_DIR = os.path.join(BASE, "frame_scenes")
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(FRAME_DIR, exist_ok=True)

# ─── Imports ──────────────────────────────────────────────────────────────────
from PIL import Image, ImageDraw, ImageFont
import numpy as np

print("✓ Pillow and NumPy ready")

try:
    from gtts import gTTS
    TTS_ENGINE = "gtts"
    print("✓ gTTS ready (online TTS)")
except ImportError:
    TTS_ENGINE = None
    print("✗ gTTS not available")

try:
    import moviepy
    from moviepy import (
        VideoFileClip, AudioFileClip, ImageClip,
        concatenate_videoclips, CompositeVideoClip, TextClip
    )
    MOVIEPY_OK = True
    print("✓ MoviePy ready")
except Exception as e:
    MOVIEPY_OK = False
    print(f"✗ MoviePy import issue: {e}")

# ─── Video settings ───────────────────────────────────────────────────────────
W, H = 1920, 1080
FPS = 30
FONT_PATH = None  # Will try to find a system font

# ─── Colors ───────────────────────────────────────────────────────────────────
BG_DARK       = (10, 14, 35)        # Deep navy
BG_PANEL      = (16, 22, 55)        # Slightly lighter navy
BG_CARD       = (22, 30, 72)        # Card background
ACCENT_CYAN   = (0, 220, 255)       # Bright cyan
ACCENT_VIOLET = (138, 43, 226)      # Violet
ACCENT_PURPLE = (120, 80, 220)      # Purple
ACCENT_PINK   = (255, 60, 140)      # Pink accent
TEXT_WHITE    = (255, 255, 255)
TEXT_LIGHT    = (200, 210, 240)
TEXT_MUTED    = (130, 145, 190)
TEXT_YELLOW   = (255, 220, 60)
TEXT_GREEN    = (80, 220, 130)
TEXT_CODE     = (170, 255, 170)     # Code text green
TEXT_KEYWORD  = (90, 180, 255)      # SQL keyword blue
BORDER_COLOR  = (50, 70, 160)

# ─── Font loading ─────────────────────────────────────────────────────────────
def get_font(size=36, bold=False, mono=False):
    """Try to load a real font, fall back to default."""
    candidates = []
    if mono:
        candidates = [
            "C:/Windows/Fonts/consola.ttf",
            "C:/Windows/Fonts/cour.ttf",
            "C:/Windows/Fonts/lucon.ttf",
        ]
    elif bold:
        candidates = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


# ─── Drawing helpers ──────────────────────────────────────────────────────────
def draw_gradient_bg(draw, w, h, color1=BG_DARK, color2=BG_PANEL):
    """Draw a vertical gradient background."""
    for y in range(h):
        t = y / h
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def draw_text_wrapped(draw, text, x, y, font, color, max_width, line_spacing=8):
    """Draw wrapped text, returns final y."""
    # Estimate characters per line
    try:
        avg_char_w = font.getlength("A")
    except:
        avg_char_w = font.size * 0.6 if hasattr(font, 'size') else 18
    
    chars_per_line = max(10, int(max_width / max(1, avg_char_w)))
    lines = textwrap.wrap(text, width=chars_per_line)
    
    current_y = y
    for line in lines:
        draw.text((x, current_y), line, font=font, fill=color)
        try:
            bbox = font.getbbox(line)
            line_h = bbox[3] - bbox[1]
        except:
            line_h = getattr(font, 'size', 36)
        current_y += line_h + line_spacing
    return current_y


def draw_rounded_rect(draw, x1, y1, x2, y2, radius=16, fill=None, outline=None, width=2):
    """Draw a rounded rectangle."""
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)


def draw_title_bar(draw, w, title, subtitle=None):
    """Draw top brand bar."""
    draw.rectangle([0, 0, w, 72], fill=(8, 12, 30))
    font_title = get_font(28, bold=True)
    font_sub = get_font(18)
    
    # S circle
    draw.ellipse([20, 14, 60, 54], fill=ACCENT_CYAN)
    draw.text((33, 22), "S", font=get_font(26, bold=True), fill=BG_DARK)
    
    draw.text((72, 20), "SocialConnect", font=font_title, fill=TEXT_WHITE)
    if subtitle:
        draw.text((72, 50), subtitle, font=font_sub, fill=TEXT_MUTED)


def draw_section_label(draw, x, y, text, color=ACCENT_CYAN):
    """Draw a small eyebrow label."""
    font = get_font(22, bold=True)
    # Draw small accent line
    draw.rectangle([x, y + 14, x + 36, y + 18], fill=color)
    draw.text((x + 48, y), text, font=font, fill=color)


def draw_code_panel(draw, x, y, w, h, lines, title=None):
    """Draw a code block panel."""
    # Background
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12,
                           fill=(12, 18, 45), outline=ACCENT_CYAN, width=1)
    # Header bar
    if title:
        draw.rounded_rectangle([x, y, x + w, y + 40], radius=12, fill=(20, 28, 70))
        draw.text((x + 16, y + 10), title, font=get_font(18, bold=True), fill=ACCENT_CYAN)
        # Traffic light dots
        for i, c in enumerate([(255, 90, 90), (255, 190, 60), (80, 200, 100)]):
            draw.ellipse([x + w - 70 + i*20, y+12, x + w - 56 + i*20, y+28], fill=c)
        y_start = y + 50
    else:
        y_start = y + 16
    
    mono = get_font(20, mono=True)
    SQL_KEYWORDS = {"SELECT", "FROM", "JOIN", "LEFT", "WHERE", "ON", "GROUP", "BY",
                    "ORDER", "DESC", "ASC", "INSERT", "INTO", "VALUES", "DELETE",
                    "UPDATE", "RETURNING", "COUNT", "DISTINCT", "ON CONFLICT",
                    "DO NOTHING", "AND", "OR", "NOT", "NULL", "ILIKE", "LIKE",
                    "@app.route", "def ", "return", "try:", "except", "finally:"}
    
    current_y = y_start
    for line in lines:
        if current_y > y + h - 30:
            break
        # Simple colorization
        if any(kw in line.upper() for kw in ["SELECT", "FROM", "WHERE", "INSERT",
                                               "DELETE", "JOIN", "GROUP", "ORDER"]):
            color = TEXT_KEYWORD
        elif line.strip().startswith("#") or line.strip().startswith("--"):
            color = TEXT_MUTED
        elif "@app.route" in line or "def " in line:
            color = TEXT_YELLOW
        elif "\"" in line or "'" in line:
            color = (255, 200, 120)
        else:
            color = TEXT_CODE
        
        draw.text((x + 16, current_y), line, font=mono, fill=color)
        try:
            bbox = mono.getbbox(line if line else "A")
            line_h = bbox[3] - bbox[1]
        except:
            line_h = 24
        current_y += max(26, line_h + 4)


def make_base_image():
    """Create a fresh base 1920×1080 image."""
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H)
    return img, draw


# ═══════════════════════════════════════════════════════════════════════════════
#  SCENE IMAGE GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

def scene01_opening():
    """Scene 1 — Title screen."""
    img, draw = make_base_image()
    
    # Animated orbit rings (static representation)
    cx, cy = W // 2, H // 2 - 80
    draw.ellipse([cx-280, cy-280, cx+280, cy+280], outline=(30, 50, 120), width=1)
    draw.ellipse([cx-180, cy-180, cx+180, cy+180], outline=(40, 60, 160), width=1)
    
    # Glowing S logo
    draw.ellipse([cx-70, cy-70, cx+70, cy+70], fill=ACCENT_VIOLET)
    draw.ellipse([cx-65, cy-65, cx+65, cy+65], fill=ACCENT_CYAN)
    draw.text((cx-28, cy-40), "S", font=get_font(72, bold=True), fill=BG_DARK)
    
    # Floating icons
    icon_positions = [(200, 300), (1650, 280), (180, 750), (1700, 700)]
    icons = ["⬡", "⬢", "◈", "◇"]
    for (ix, iy), ico in zip(icon_positions, icons):
        draw.text((ix, iy), ico, font=get_font(48), fill=(50, 80, 180))
    
    # Main title
    title_font = get_font(96, bold=True)
    title = "SOCIALCONNECT"
    try:
        tw = draw.textlength(title, font=title_font)
    except:
        tw = len(title) * 60
    draw.text(((W - tw) // 2, cy + 120), title, font=title_font, fill=TEXT_WHITE)
    
    # Subtitle 1
    sub1_font = get_font(42)
    sub1 = "Social Media Database Management System"
    try:
        sw = draw.textlength(sub1, font=sub1_font)
    except:
        sw = len(sub1) * 24
    draw.text(((W - sw) // 2, cy + 230), sub1, font=sub1_font, fill=ACCENT_CYAN)
    
    # Subtitle 2
    sub2_font = get_font(30)
    sub2 = "An Integrated Web Application Using Flask & PostgreSQL"
    try:
        sw2 = draw.textlength(sub2, font=sub2_font)
    except:
        sw2 = len(sub2) * 18
    draw.text(((W - sw2) // 2, cy + 295), sub2, font=sub2_font, fill=TEXT_MUTED)
    
    # Tech badges
    badge_labels = ["Python Flask", "PostgreSQL", "psycopg2", "JavaScript", "HTML/CSS"]
    badge_colors = [ACCENT_CYAN, (70, 130, 240), ACCENT_VIOLET, (255, 180, 60), ACCENT_PINK]
    badge_x = 310
    badge_y = H - 140
    for label, bc in zip(badge_labels, badge_colors):
        font = get_font(22, bold=True)
        try:
            bw = draw.textlength(label, font=font)
        except:
            bw = len(label) * 14
        pad = 20
        draw.rounded_rectangle([badge_x - pad, badge_y - 8,
                                 badge_x + bw + pad, badge_y + 40],
                               radius=20, fill=(20, 25, 60), outline=bc, width=2)
        draw.text((badge_x, badge_y), label, font=font, fill=bc)
        badge_x += bw + 60
    
    # Bottom bar
    draw_title_bar(draw, W, "SocialConnect", "DBMS Project Presentation")
    
    path = os.path.join(FRAME_DIR, "scene01.png")
    img.save(path)
    print(f"  ✓ scene01.png saved")
    return path


def scene02_problem():
    """Scene 2 — Problem statement."""
    img, draw = make_base_image()
    draw_title_bar(draw, W, "SocialConnect", "Why We Need a Database")
    
    # Left panel — Browser mockup
    draw.rounded_rectangle([60, 100, 860, 980], radius=16, fill=BG_CARD, outline=BORDER_COLOR, width=1)
    draw.rounded_rectangle([60, 100, 860, 160], radius=12, fill=(20, 28, 70))
    draw.text((80, 120), "🌐  SocialConnect   ×", font=get_font(22), fill=TEXT_MUTED)
    
    # Browser content mockup
    draw.rounded_rectangle([80, 180, 840, 280], radius=8, fill=(18, 25, 60))
    draw.text((100, 200), "📝 Create Post", font=get_font(28, bold=True), fill=TEXT_WHITE)
    draw.text((100, 240), "\"Hello World — my first post!\"", font=get_font(22), fill=TEXT_LIGHT)
    
    # Post cards
    for i, (name, post, likes) in enumerate([
        ("Alex Rao", "Sharing ideas with SocialConnect!", 5),
        ("Priya K.", "Great platform for our community!", 12),
        ("Rajan M.", "DBMS in action — real data!", 3),
    ]):
        py = 300 + i * 200
        draw.rounded_rectangle([80, py, 840, py+180], radius=8, fill=(18, 25, 60))
        draw.ellipse([90, py+20, 130, py+60], fill=ACCENT_VIOLET)
        draw.text((100, py+32), name[0], font=get_font(24, bold=True), fill=TEXT_WHITE)
        draw.text((140, py+25), name, font=get_font(22, bold=True), fill=TEXT_WHITE)
        draw.text((140, py+52), post, font=get_font(20), fill=TEXT_LIGHT)
        draw.text((100, py+100), f"♥ {likes} likes   💬 Comment   🗑 Delete", font=get_font(20), fill=ACCENT_CYAN)
    
    # Arrow
    for ay in range(400, 700, 20):
        draw.ellipse([900, ay, 910, ay+8], fill=ACCENT_CYAN)
    draw.polygon([(870, 700), (940, 700), (905, 730)], fill=ACCENT_CYAN)
    
    # Right panel — Database
    draw.rounded_rectangle([960, 100, 1860, 980], radius=16, fill=BG_CARD, outline=BORDER_COLOR, width=1)
    draw.rounded_rectangle([960, 100, 1860, 160], radius=12, fill=(20, 28, 70))
    draw.text((980, 120), "🐘 PostgreSQL — social_media_db", font=get_font(22, bold=True), fill=TEXT_YELLOW)
    
    tables = [
        ("users", ["user_id", "username", "full_name", "email", "bio"]),
        ("posts", ["post_id", "user_id(FK)", "content", "image_url", "created_at"]),
        ("likes", ["like_id", "post_id(FK)", "user_id(FK)"]),
        ("comments", ["comment_id", "post_id(FK)", "user_id(FK)", "comment_text"]),
        ("messages", ["message_id", "sender_id", "recipient_id", "message_text"]),
    ]
    ty = 180
    for tname, cols in tables:
        draw.rounded_rectangle([980, ty, 1840, ty + 130], radius=8,
                               fill=(12, 18, 50), outline=ACCENT_PURPLE, width=1)
        draw.text((1000, ty + 10), f"TABLE: {tname.upper()}", font=get_font(22, bold=True), fill=ACCENT_CYAN)
        col_text = " | ".join(cols)
        draw_text_wrapped(draw, col_text, 1000, ty + 45, get_font(18), TEXT_MUTED, 800)
        ty += 155
    
    # Section labels
    draw_section_label(draw, 60, 80, "USER INTERFACE", ACCENT_CYAN)
    draw_section_label(draw, 960, 80, "DATABASE LAYER", TEXT_YELLOW)
    
    draw.text((860, 500), "HTTP", font=get_font(20, bold=True), fill=TEXT_WHITE)
    draw.text((860, 525), "JSON", font=get_font(20, bold=True), fill=TEXT_YELLOW)
    
    path = os.path.join(FRAME_DIR, "scene02.png")
    img.save(path)
    print(f"  ✓ scene02.png saved")
    return path


def scene03_features():
    """Scene 3 — Features grid."""
    img, draw = make_base_image()
    draw_title_bar(draw, W, "SocialConnect", "Objectives & Features")
    
    draw_section_label(draw, 80, 90, "WHAT SOCIALCONNECT DOES")
    
    title_font = get_font(52, bold=True)
    draw.text((80, 125), "Core Features", font=title_font, fill=TEXT_WHITE)
    
    features = [
        ("📝", "Create Posts", "Users write and publish text posts with optional images"),
        ("📰", "Browse Feed", "Live post feed sorted newest-first from PostgreSQL"),
        ("🔍", "Search Posts", "Keyword search using SQL ILIKE filtering"),
        ("❤️", "Like / Unlike", "Like tracking with duplicate prevention at DB level"),
        ("💬", "Comments", "Add and view comments per post"),
        ("👤", "User Profiles", "View bio, email, and post count for any user"),
        ("✉️", "Direct Messages", "Private chat between users, auto-refreshing every 5s"),
        ("🌓", "Dark/Light Theme", "UI theme toggle stored in browser localStorage"),
    ]
    
    cols = 4
    card_w = 410
    card_h = 200
    pad_x = 60
    pad_y = 210
    gap_x = 60
    gap_y = 36
    
    for i, (icon, label, desc) in enumerate(features):
        col = i % cols
        row = i // cols
        x = pad_x + col * (card_w + gap_x)
        y = pad_y + row * (card_h + gap_y)
        
        # Card
        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=14,
                               fill=BG_CARD, outline=ACCENT_PURPLE, width=1)
        # Icon background circle
        draw.ellipse([x + 20, y + 20, x + 80, y + 80], fill=(30, 20, 80))
        draw.text((x + 30, y + 28), icon, font=get_font(36), fill=TEXT_WHITE)
        
        # Label
        draw.text((x + 95, y + 24), label, font=get_font(26, bold=True), fill=TEXT_WHITE)
        
        # Description
        draw_text_wrapped(draw, desc, x + 20, y + 100, get_font(20), TEXT_MUTED, card_w - 40)
        
        # Bottom accent line
        draw.rectangle([x + 20, y + card_h - 8, x + 80, y + card_h - 4], fill=ACCENT_CYAN)
    
    # Right summary
    draw.rounded_rectangle([1740, 210, 1900, 640], radius=12, fill=BG_CARD, outline=ACCENT_CYAN, width=1)
    draw.text((1755, 225), "BACKED BY", font=get_font(20, bold=True), fill=ACCENT_CYAN)
    for i, t in enumerate(["5 DB Tables", "11 API", "Endpoints", "Full CRUD", "Real SQL"]):
        draw.text((1760, 265 + i * 68), t, font=get_font(26, bold=True), fill=TEXT_WHITE)
    
    path = os.path.join(FRAME_DIR, "scene03.png")
    img.save(path)
    print(f"  ✓ scene03.png saved")
    return path


def scene04_techstack():
    """Scene 4 — Technology stack diagram."""
    img, draw = make_base_image()
    draw_title_bar(draw, W, "SocialConnect", "Technology Stack")
    
    draw_section_label(draw, 80, 90, "THREE-TIER ARCHITECTURE")
    draw.text((80, 125), "How the Layers Work Together", font=get_font(52, bold=True), fill=TEXT_WHITE)
    
    # Three tiers
    tiers = [
        {
            "label": "FRONTEND LAYER",
            "color": ACCENT_CYAN,
            "tech": ["HTML5", "CSS3", "JavaScript (ES6+)"],
            "desc": "Structures the page, styles the UI, handles user interactions without reload",
            "y": 220
        },
        {
            "label": "BACKEND LAYER",
            "color": TEXT_YELLOW,
            "tech": ["Python Flask", "psycopg2", "flask-cors"],
            "desc": "Routes, validates requests, executes SQL, returns JSON responses",
            "y": 510
        },
        {
            "label": "DATABASE LAYER",
            "color": (70, 200, 130),
            "tech": ["PostgreSQL", "social_media_db", "5 Tables"],
            "desc": "Stores all data relationally with constraints, keys, and indexes",
            "y": 800
        },
    ]
    
    connector_labels = [
        ("HTTP Requests + JSON Body", "GET / POST / DELETE", 445),
        ("SQL Queries (parameterized)", "psycopg2 cursor.execute()", 735),
    ]
    
    for tier in tiers:
        y = tier["y"]
        c = tier["color"]
        draw.rounded_rectangle([120, y, 1800, y + 240], radius=16,
                               fill=BG_CARD, outline=c, width=2)
        # Left color bar
        draw.rounded_rectangle([120, y, 175, y + 240], radius=14, fill=c)
        
        # Label
        draw.text((200, y + 20), tier["label"], font=get_font(32, bold=True), fill=c)
        
        # Tech badges
        bx = 200
        for tech in tier["tech"]:
            font = get_font(24, bold=True)
            try:
                tw = draw.textlength(tech, font=font)
            except:
                tw = len(tech) * 14
            draw.rounded_rectangle([bx - 8, y + 72, bx + tw + 16, y + 116],
                                  radius=20, fill=(20, 30, 80), outline=c, width=1)
            draw.text((bx, y + 78), tech, font=font, fill=c)
            bx += tw + 40
        
        # Description
        draw_text_wrapped(draw, tier["desc"], 200, y + 148, get_font(24), TEXT_LIGHT, 1550)
    
    # Connectors with arrows
    for (label1, label2, arrow_y) in connector_labels:
        draw.rectangle([700, arrow_y, 1200, arrow_y + 58], fill=(15, 22, 55))
        draw.rounded_rectangle([695, arrow_y - 2, 1205, arrow_y + 60], radius=8,
                               outline=ACCENT_PURPLE, width=1)
        
        # Arrow down
        ax = 960
        draw.polygon([(ax - 20, arrow_y + 2), (ax + 20, arrow_y + 2), (ax, arrow_y - 18)],
                    fill=ACCENT_CYAN)  # up (response)
        draw.polygon([(ax - 20, arrow_y + 56), (ax + 20, arrow_y + 56), (ax, arrow_y + 74)],
                    fill=TEXT_YELLOW)  # down (request)
        
        draw.text((720, arrow_y + 4), label1, font=get_font(22, bold=True), fill=TEXT_WHITE)
        draw.text((720, arrow_y + 32), label2, font=get_font(20), fill=TEXT_MUTED)
    
    path = os.path.join(FRAME_DIR, "scene04.png")
    img.save(path)
    print(f"  ✓ scene04.png saved")
    return path


def scene05_frontend():
    """Scene 5 — Frontend UI demonstration."""
    img, draw = make_base_image()
    draw_title_bar(draw, W, "SocialConnect", "Frontend — User Interface")
    
    draw_section_label(draw, 80, 90, "RUNNING APPLICATION")
    draw.text((80, 125), "SocialConnect in the Browser", font=get_font(52, bold=True), fill=TEXT_WHITE)
    
    # Main browser frame
    BF = [80, 195, 1180, 1010]
    draw.rounded_rectangle(BF, radius=14, fill=(8, 12, 30), outline=ACCENT_CYAN, width=2)
    
    # Browser chrome
    draw.rounded_rectangle([80, 195, 1180, 255], radius=12, fill=(18, 24, 55))
    # Traffic lights
    for i, c in enumerate([(255,90,90),(255,190,60),(80,200,100)]):
        draw.ellipse([100+i*26, 215, 118+i*26, 233], fill=c)
    # URL bar
    draw.rounded_rectangle([165, 210, 900, 244], radius=6, fill=(25, 32, 70))
    draw.text((178, 214), "🔒 localhost:5000", font=get_font(20), fill=TEXT_MUTED)
    
    # Sidebar mockup
    draw.rounded_rectangle([88, 255, 220, 1003], radius=0, fill=(12, 17, 45))
    side_items = ["⌂ Home", "⌕ Explore", "＋ Create", "♙ Profiles", "▤ Messages"]
    for i, item in enumerate(side_items):
        cy = 290 + i * 70
        if i == 0:
            draw.rounded_rectangle([88, cy-4, 220, cy+40], radius=6, fill=(30, 45, 120))
        draw.text((100, cy), item, font=get_font(20), fill=TEXT_WHITE if i == 0 else TEXT_MUTED)
    
    # Main content
    # Create post form
    draw.rounded_rectangle([230, 260, 1165, 420], radius=10, fill=BG_CARD)
    draw.text((250, 274), "✦ CREATE SOMETHING", font=get_font(20, bold=True), fill=ACCENT_CYAN)
    draw.text((250, 304), "What's on your mind?", font=get_font(28, bold=True), fill=TEXT_WHITE)
    draw.rounded_rectangle([250, 348, 700, 385], radius=6, fill=(18, 25, 65), outline=ACCENT_PURPLE, width=1)
    draw.text((262, 355), "Alex Rao (@alex_r)", font=get_font(20), fill=TEXT_LIGHT)
    draw.rounded_rectangle([720, 348, 1145, 385], radius=6, fill=ACCENT_CYAN)
    draw.text((780, 354), "＋ Publish post", font=get_font(22, bold=True), fill=BG_DARK)
    
    # Search
    draw.rounded_rectangle([230, 430, 1165, 490], radius=10, fill=BG_CARD)
    draw.text((250, 445), "⌕ EXPLORE — Community feed", font=get_font(22, bold=True), fill=TEXT_WHITE)
    draw.rounded_rectangle([800, 448, 1140, 483], radius=6, fill=(18, 25, 65), outline=BORDER_COLOR, width=1)
    draw.text((820, 452), "Search posts...", font=get_font(20), fill=TEXT_MUTED)
    
    # Post cards
    posts_data = [
        ("AR", "Alex Rao", "@alex_r · Oct 12, 12:03", "Hello from SocialConnect! This is my first post on the platform.", 5, ACCENT_VIOLET),
        ("PK", "Priya Kumar", "@priya_k · Oct 12, 11:45", "Great to see the community growing! Love the dark theme.", 12, ACCENT_CYAN),
        ("RM", "Rajan Mehta", "@rajan_m · Oct 12, 11:20", "DBMS concepts in action — real SQL queries powering every feature!", 3, ACCENT_PINK),
    ]
    py_start = 500
    for (initls, name, meta, content, likes, av_color) in posts_data:
        draw.rounded_rectangle([230, py_start, 1165, py_start+155], radius=10, fill=BG_CARD)
        draw.ellipse([245, py_start+12, 290, py_start+57], fill=av_color)
        draw.text((258, py_start+22), initls, font=get_font(22, bold=True), fill=TEXT_WHITE)
        draw.text((302, py_start+12), name, font=get_font(24, bold=True), fill=TEXT_WHITE)
        draw.text((302, py_start+40), meta, font=get_font(18), fill=TEXT_MUTED)
        draw_text_wrapped(draw, content, 245, py_start+68, get_font(20), TEXT_LIGHT, 900)
        # Action buttons
        for bx, (blabel, bcolor) in enumerate([
            (f"♡ Like ({likes})", ACCENT_CYAN),
            ("♥ Unlike", TEXT_MUTED),
            ("▤ Comments", TEXT_MUTED),
            ("Delete", ACCENT_PINK),
        ]):
            btx = 245 + bx * 200
            draw.rounded_rectangle([btx-4, py_start+120, btx+160, py_start+148],
                                  radius=6, outline=bcolor, width=1)
            draw.text((btx+4, py_start+124), blabel, font=get_font(18), fill=bcolor)
        py_start += 168
    
    # Right panel
    draw.rounded_rectangle([1200, 195, 1880, 1010], radius=14, fill=BG_CARD, outline=BORDER_COLOR, width=1)
    
    # Orbit art in right panel
    cx2, cy2 = 1540, 380
    draw.ellipse([cx2-100, cy2-100, cx2+100, cy2+100], outline=(40,60,150), width=1)
    draw.ellipse([cx2-60, cy2-60, cx2+60, cy2+60], outline=(60,90,180), width=1)
    draw.ellipse([cx2-30, cy2-30, cx2+30, cy2+30], fill=ACCENT_CYAN)
    draw.text((cx2-18, cy2-20), "S", font=get_font(34, bold=True), fill=BG_DARK)
    
    draw.text((1220, 430), "WELCOME ABOARD", font=get_font(20, bold=True), fill=ACCENT_CYAN)
    draw.text((1220, 460), "Your community,", font=get_font(28, bold=True), fill=TEXT_WHITE)
    draw.text((1220, 494), "your space.", font=get_font(28, bold=True), fill=TEXT_WHITE)
    
    draw.rounded_rectangle([1220, 540, 1820, 590], radius=8, fill=ACCENT_CYAN)
    draw.text((1430, 552), "Open messages →", font=get_font(24, bold=True), fill=BG_DARK)
    
    # Callout annotations
    annotations = [
        (720, 365, "User selector dropdown"),
        (930, 365, "Publish button → POST /api/posts"),
        (800, 470, "Search → GET /api/posts?search="),
        (700, 515, "Post card — username, time, likes from DB"),
    ]
    for (ax, ay, label) in annotations:
        draw.rounded_rectangle([ax-4, ay+50, ax+len(label)*9+8, ay+78],
                              radius=6, fill=(0, 200, 230, 180), outline=ACCENT_CYAN, width=1)
        draw.text((ax, ay+54), label, font=get_font(18), fill=BG_DARK)
    
    path = os.path.join(FRAME_DIR, "scene05.png")
    img.save(path)
    print(f"  ✓ scene05.png saved")
    return path


def scene06_architecture():
    """Scene 6 — System architecture flow."""
    img, draw = make_base_image()
    draw_title_bar(draw, W, "SocialConnect", "System Architecture")
    
    draw_section_label(draw, 80, 90, "REQUEST-RESPONSE FLOW")
    draw.text((80, 125), "How Data Moves Through the System", font=get_font(48, bold=True), fill=TEXT_WHITE)
    
    # Flow diagram — centered
    boxes = [
        ("USER", "Click button / Fill form", ACCENT_CYAN, 190),
        ("FRONTEND", "HTML · CSS · JavaScript\nfetch('/api/posts', {...})", (70, 140, 240), 340),
        ("HTTP + JSON", "POST /api/posts\n{user_id, content, image_url}", ACCENT_PURPLE, 490),
        ("FLASK BACKEND", "app.py · Routes · Validation\nget_db_connection()", TEXT_YELLOW, 640),
        ("PSYCOPG2", "cur.execute(SQL, params)\nParameterized queries", (100, 200, 100), 790),
        ("POSTGRESQL", "social_media_db\nINSERT INTO posts...", (70, 130, 240), 940),
    ]
    
    # Response boxes on right side
    response_boxes = [
        ("JSON RESPONSE", "{post_id: 42, message: 'created'}", ACCENT_CYAN, 790),
        ("FLASK jsonify()", "return jsonify(result), 201", TEXT_YELLOW, 640),
        ("HTTP 201", "Content-Type: application/json", ACCENT_PURPLE, 490),
        ("JS UPDATES DOM", "New post card appears in feed", (70, 140, 240), 340),
        ("USER SEES RESULT", "Post visible • Toast shown", ACCENT_CYAN, 190),
    ]
    
    box_w = 600
    box_h = 72
    left_x = 80
    right_x = 1240
    center_x = 960
    
    # Draw left (request) boxes
    for (label, detail, color, y) in boxes:
        draw.rounded_rectangle([left_x, y, left_x+box_w, y+box_h], radius=10,
                               fill=BG_CARD, outline=color, width=2)
        draw.text((left_x+16, y+8), label, font=get_font(24, bold=True), fill=color)
        draw.text((left_x+16, y+38), detail, font=get_font(18), fill=TEXT_MUTED)
        
        # Arrow down (except last)
        if y < 940:
            ay = y + box_h + 2
            draw.polygon([(left_x+280, ay), (left_x+320, ay), (left_x+300, ay+24)],
                        fill=TEXT_YELLOW)
    
    # REQUEST label
    draw.text((300, 168), "◄ REQUEST PATH", font=get_font(22, bold=True), fill=TEXT_YELLOW)
    
    # Draw right (response) boxes
    draw.text((1340, 168), "RESPONSE PATH ►", font=get_font(22, bold=True), fill=ACCENT_CYAN)
    
    for (label, detail, color, y) in response_boxes:
        draw.rounded_rectangle([right_x, y, right_x+box_w, y+box_h], radius=10,
                               fill=BG_CARD, outline=color, width=2)
        draw.text((right_x+16, y+8), label, font=get_font(24, bold=True), fill=color)
        draw.text((right_x+16, y+38), detail, font=get_font(18), fill=TEXT_MUTED)
        
        if y > 340:
            ay = y - 26
            draw.polygon([(right_x+280, ay+24), (right_x+320, ay+24), (right_x+300, ay)],
                        fill=ACCENT_CYAN)
    
    # Center connector — PostgreSQL at bottom connecting both
    draw.rounded_rectangle([700, 940, 1220, 1012], radius=10, fill=BG_CARD,
                           outline=(70, 130, 240), width=2)
    draw.text((730, 953), "🐘 PostgreSQL — social_media_db", font=get_font(26, bold=True), fill=(70, 130, 240))
    draw.text((730, 983), "Stores data  ·  Returns query results", font=get_font(20), fill=TEXT_MUTED)
    
    # Horizontal connectors
    draw.polygon([(1100, 975), (left_x+600+10, 975), (left_x+590, 963)], fill=TEXT_YELLOW)
    draw.polygon([(700, 975), (right_x-10, 975), (right_x, 963)], fill=ACCENT_CYAN)
    
    path = os.path.join(FRAME_DIR, "scene06.png")
    img.save(path)
    print(f"  ✓ scene06.png saved")
    return path


def scene07_backend():
    """Scene 7 — Flask backend and API."""
    img, draw = make_base_image()
    draw_title_bar(draw, W, "SocialConnect", "Backend — Flask API")
    
    draw_section_label(draw, 80, 90, "app.py — 11 ENDPOINTS")
    draw.text((80, 125), "Python Flask Routes & SQL", font=get_font(52, bold=True), fill=TEXT_WHITE)
    
    # Left — Route table
    draw.rounded_rectangle([60, 210, 600, 1040], radius=14, fill=BG_CARD, outline=BORDER_COLOR, width=1)
    draw.text((80, 220), "API ENDPOINTS", font=get_font(26, bold=True), fill=ACCENT_CYAN)
    
    routes = [
        ("GET",    "/api/posts",              "Fetch feed (JOIN 3 tables)"),
        ("POST",   "/api/posts",              "Create post (INSERT RETURNING)"),
        ("POST",   "/api/posts/<id>/like",    "Like (ON CONFLICT DO NOTHING)"),
        ("POST",   "/api/posts/<id>/unlike",  "Unlike (DELETE from likes)"),
        ("DELETE", "/api/posts/<id>",         "Delete post"),
        ("GET",    "/api/users",              "All users"),
        ("GET",    "/api/users/<id>",         "Profile + post count"),
        ("GET",    "/api/posts/<id>/comments","Get comments"),
        ("POST",   "/api/posts/<id>/comments","Add comment"),
        ("POST",   "/api/messages",           "Send message"),
        ("GET",    "/api/messages",           "Chat history"),
    ]
    method_colors = {"GET": (80, 200, 130), "POST": ACCENT_CYAN, "DELETE": ACCENT_PINK}
    
    for i, (method, path_r, desc) in enumerate(routes):
        ry = 264 + i * 70
        mc = method_colors.get(method, TEXT_WHITE)
        draw.rounded_rectangle([76, ry, 580, ry+60], radius=6, fill=(15, 22, 55))
        draw.rounded_rectangle([76, ry, 150, ry+60], radius=6, fill=(20, 30, 70), outline=mc, width=1)
        draw.text((82, ry+14), method, font=get_font(18, bold=True), fill=mc)
        draw.text((160, ry+8), path_r, font=get_font(19, mono=True), fill=TEXT_WHITE)
        draw.text((160, ry+34), desc, font=get_font(17), fill=TEXT_MUTED)
    
    # Right — Code panel
    code_lines_1 = [
        "# ── Database Connection ──────────────────",
        "def get_db_connection():",
        "    return psycopg2.connect(",
        "        host=os.getenv('DB_HOST','localhost'),",
        "        database=os.getenv('DB_NAME','social_media_db'),",
        "        password=os.getenv('DB_PASSWORD')  # env var",
        "    )",
        "",
        "# ── GET /api/posts ────────────────────────",
        "@app.route('/api/posts', methods=['GET'])",
        "def get_posts():",
        "    search = request.args.get('search','').strip()",
        "    cur.execute(\"\"\"",
        "        SELECT p.post_id, u.username, u.full_name,",
        "               p.content, p.created_at,",
        "               COUNT(DISTINCT l.like_id) AS likes",
        "        FROM posts p",
        "        JOIN users u ON p.user_id = u.user_id",
        "        LEFT JOIN likes l ON p.post_id = l.post_id",
        "        WHERE p.content ILIKE %s",
        "        GROUP BY p.post_id, ...",
        "        ORDER BY p.created_at DESC;",
        "    \"\"\", (f'%{search}%',))",
        "    return jsonify(posts)",
    ]
    draw_code_panel(draw, 620, 210, 1280, 510, code_lines_1, "app.py — get_posts()")
    
    code_lines_2 = [
        "# ── Like with conflict handling ────────────",
        "@app.route('/api/posts/<int:post_id>/like',",
        "           methods=['POST'])",
        "def like_post(post_id):",
        "    cur.execute(\"\"\"",
        "        INSERT INTO likes (post_id, user_id)",
        "        VALUES (%s, %s)",
        "        ON CONFLICT (post_id, user_id) DO NOTHING;",
        "    \"\"\", (post_id, user_id))",
        "    conn.commit()   # Transaction committed",
        "",
        "# ── Error handling pattern ──────────────────",
        "    try:",
        "        cur.execute(sql, params)",
        "        conn.commit()       # ✓ Success",
        "    except Exception:",
        "        conn.rollback()     # ✗ Rollback",
        "    finally:",
        "        cur.close()",
        "        conn.close()",
    ]
    draw_code_panel(draw, 620, 740, 1280, 310, code_lines_2, "app.py — like_post() + error handling")
    
    path = os.path.join(FRAME_DIR, "scene07.png")
    img.save(path)
    print(f"  ✓ scene07.png saved")
    return path


def scene08_database():
    """Scene 8 — Database schema and ER diagram."""
    img, draw = make_base_image()
    draw_title_bar(draw, W, "SocialConnect", "PostgreSQL Database — social_media_db")
    
    draw_section_label(draw, 80, 90, "DATABASE SCHEMA")
    draw.text((80, 125), "5 Tables, Foreign Keys, Constraints", font=get_font(52, bold=True), fill=TEXT_WHITE)
    
    # Table schemas
    tables_data = [
        ("USERS", [("user_id", "INTEGER", "PK"), ("username", "VARCHAR", ""),
                   ("email", "VARCHAR", ""), ("full_name", "VARCHAR", ""), ("bio", "TEXT", "")],
         ACCENT_CYAN, 210),
        ("POSTS", [("post_id", "INTEGER", "PK"), ("user_id", "INTEGER", "FK→users"),
                   ("content", "TEXT", ""), ("image_url", "TEXT", "NULL"), ("created_at", "TIMESTAMP", "AUTO")],
         TEXT_YELLOW, 210),
        ("LIKES", [("like_id", "INTEGER", "PK"), ("post_id", "INTEGER", "FK→posts"),
                   ("user_id", "INTEGER", "FK→users"), ("—", "UNIQUE", "(post_id,user_id)")],
         ACCENT_PINK, 560),
        ("COMMENTS", [("comment_id", "INTEGER", "PK"), ("post_id", "INTEGER", "FK→posts"),
                      ("user_id", "INTEGER", "FK→users"), ("comment_text", "TEXT", ""),
                      ("created_at", "TIMESTAMP", "AUTO")],
         ACCENT_PURPLE, 760),
        ("MESSAGES", [("message_id", "INTEGER", "PK"), ("sender_id", "INTEGER", "FK→users"),
                      ("recipient_id", "INTEGER", "FK→users"), ("message_text", "TEXT", ""),
                      ("created_at", "TIMESTAMP", "AUTO")],
         (100, 200, 130), 560),
    ]
    
    col_xs = [80, 580, 560+500]
    
    for idx, (tname, cols, color, y) in enumerate(tables_data):
        xoff = (idx % 2) * 880 + 80
        draw.rounded_rectangle([xoff, y, xoff+820, y + 40 + len(cols)*40],
                               radius=12, fill=BG_CARD, outline=color, width=2)
        # Table header
        draw.rounded_rectangle([xoff, y, xoff+820, y+40], radius=10, fill=color)
        draw.text((xoff+16, y+8), f"🗃 {tname}", font=get_font(24, bold=True), fill=BG_DARK)
        
        for ci, (col_name, col_type, col_note) in enumerate(cols):
            cy = y + 50 + ci * 38
            row_bg = (15, 22, 55) if ci % 2 == 0 else (18, 26, 62)
            draw.rectangle([xoff+2, cy-4, xoff+818, cy+32], fill=row_bg)
            draw.text((xoff+16, cy), col_name, font=get_font(20, mono=True), fill=TEXT_WHITE)
            draw.text((xoff+260, cy), col_type, font=get_font(20, mono=True), fill=TEXT_MUTED)
            if col_note:
                nc = ACCENT_CYAN if "PK" in col_note else (255,160,60) if "FK" in col_note else ACCENT_PINK
                draw.rounded_rectangle([xoff+440, cy, xoff+780, cy+26],
                                      radius=6, fill=(25, 35, 85), outline=nc, width=1)
                draw.text((xoff+450, cy+2), col_note, font=get_font(18), fill=nc)
    
    # ER relationship lines (simplified arrows between table positions)
    # users(80,210) → posts(960,210): arrow  
    # users → likes, comments, messages
    rel_lines = [
        ((880, 390), (960, 390)),    # users → posts
        ((500, 800), (500, 600)),    # users → likes (conceptual)
    ]
    for (x1,y1),(x2,y2) in rel_lines:
        draw.line([(x1,y1),(x2,y2)], fill=ACCENT_PURPLE, width=2)
    
    # FK Legend
    draw.rounded_rectangle([80, 1000, 900, 1055], radius=8, fill=BG_CARD, outline=BORDER_COLOR, width=1)
    draw.text((100, 1012), "🔑 PK = Primary Key", font=get_font(22, bold=True), fill=ACCENT_CYAN)
    draw.text((350, 1012), "🔗 FK = Foreign Key", font=get_font(22, bold=True), fill=(255,160,60))
    draw.text((600, 1012), "⚡ UNIQUE = Prevents duplicate likes", font=get_font(22), fill=ACCENT_PINK)
    
    path = os.path.join(FRAME_DIR, "scene08.png")
    img.save(path)
    print(f"  ✓ scene08.png saved")
    return path


def scene09_concepts():
    """Scene 9 — DBMS concepts."""
    img, draw = make_base_image()
    draw_title_bar(draw, W, "SocialConnect", "DBMS Concepts Demonstrated")
    
    draw_section_label(draw, 80, 90, "DATABASE THEORY IN PRACTICE")
    draw.text((80, 125), "Core DBMS Concepts Used in This Project", font=get_font(46, bold=True), fill=TEXT_WHITE)
    
    concepts = [
        ("🔑", "Primary Key", "Uniquely identifies each row", "user_id, post_id, like_id…", ACCENT_CYAN),
        ("🔗", "Foreign Key", "Links tables, enforces integrity", "posts.user_id → users.user_id", (255, 160, 60)),
        ("🔄", "JOIN", "Combines rows from multiple tables", "JOIN users, LEFT JOIN likes", (80, 200, 255)),
        ("📊", "Aggregate / COUNT", "Counts likes per post", "COUNT(DISTINCT l.like_id) AS likes", TEXT_GREEN),
        ("➕", "INSERT RETURNING", "Create record + get new ID", "INSERT INTO posts... RETURNING post_id", ACCENT_CYAN),
        ("⚡", "ON CONFLICT DO NOTHING", "Idempotent upsert logic", "Prevents duplicate likes safely", ACCENT_PINK),
        ("💾", "COMMIT / ROLLBACK", "Transaction safety", "conn.commit() / conn.rollback()", TEXT_YELLOW),
        ("✅", "Full CRUD", "Create Read Update Delete", "Posts, Likes, Comments, Messages", (100, 220, 130)),
    ]
    
    cols = 4
    cw = 430
    ch = 220
    px = 60
    py = 215
    gx = 30
    gy = 24
    
    for i, (icon, label, defn, example, color) in enumerate(concepts):
        col = i % cols
        row = i // cols
        x = px + col * (cw + gx)
        y = py + row * (ch + gy)
        
        # Card background
        draw.rounded_rectangle([x, y, x+cw, y+ch], radius=14,
                               fill=BG_CARD, outline=color, width=1)
        # Top color accent
        draw.rounded_rectangle([x, y, x+cw, y+5], radius=4, fill=color)
        
        # Icon
        draw.text((x+16, y+18), icon, font=get_font(36), fill=color)
        draw.text((x+64, y+22), label, font=get_font(24, bold=True), fill=TEXT_WHITE)
        
        # Definition
        draw_text_wrapped(draw, defn, x+16, y+72, get_font(20), TEXT_LIGHT, cw-32)
        
        # Code example box
        draw.rounded_rectangle([x+12, y+ch-64, x+cw-12, y+ch-8],
                              radius=6, fill=(10, 16, 45))
        draw.text((x+20, y+ch-56), example, font=get_font(17, mono=True), fill=color)
    
    path = os.path.join(FRAME_DIR, "scene09.png")
    img.save(path)
    print(f"  ✓ scene09.png saved")
    return path


def scene10_sql():
    """Scene 10 — SQL demonstration."""
    img, draw = make_base_image()
    draw_title_bar(draw, W, "SocialConnect", "SQL in Action")
    
    draw_section_label(draw, 80, 90, "LIVE SQL QUERIES")
    draw.text((80, 125), "Database Queries Powering the Application", font=get_font(46, bold=True), fill=TEXT_WHITE)
    
    # Query 1 — Simple SELECT
    draw.rounded_rectangle([60, 210, 900, 540], radius=14, fill=BG_CARD, outline=BORDER_COLOR, width=1)
    draw.text((80, 220), "Query 1 — View all posts", font=get_font(26, bold=True), fill=ACCENT_CYAN)
    
    q1_lines = [
        "-- Retrieve all posts from the table",
        "SELECT * FROM posts;",
        "",
        "-- Result:",
    ]
    draw_code_panel(draw, 80, 260, 820, 120, q1_lines)
    
    # Result table for query 1
    headers = ["post_id", "user_id", "content", "created_at"]
    rows = [
        ["1", "1", "Hello from SocialConnect!", "2026-10-12 12:00:00"],
        ["2", "2", "Great platform for DBMS learning", "2026-10-12 11:45:00"],
        ["3", "3", "SQL JOINs in a real app!", "2026-10-12 11:20:00"],
    ]
    
    col_widths = [100, 90, 380, 200]
    tx = 88
    ty = 390
    header_h = 36
    row_h = 38
    
    # Header row
    draw.rectangle([tx, ty, tx+sum(col_widths)+20, ty+header_h], fill=(30, 45, 120))
    hx = tx + 8
    for hdr, cw in zip(headers, col_widths):
        draw.text((hx, ty+8), hdr, font=get_font(18, bold=True), fill=ACCENT_CYAN)
        hx += cw
    
    for ri, row in enumerate(rows):
        ry = ty + header_h + ri * row_h
        bg = (15, 22, 55) if ri % 2 == 0 else (18, 26, 62)
        draw.rectangle([tx, ry, tx+sum(col_widths)+20, ry+row_h], fill=bg)
        rx = tx + 8
        for val, cw in zip(row, col_widths):
            draw.text((rx, ry+8), val, font=get_font(18, mono=True), fill=TEXT_LIGHT)
            rx += cw
    
    # Query 2 — The main JOIN
    draw.rounded_rectangle([60, 550, 1860, 1060], radius=14, fill=BG_CARD, outline=ACCENT_CYAN, width=2)
    draw.text((80, 562), "Query 2 — Full Feed Query (3-table JOIN with Aggregation)", font=get_font(26, bold=True), fill=ACCENT_CYAN)
    
    q2_lines = [
        "SELECT",
        "    p.post_id,",
        "    u.username,         -- From users table via JOIN",
        "    u.full_name,        -- Author's display name",
        "    p.content,          -- Post text",
        "    p.created_at,       -- Timestamp",
        "    COUNT(DISTINCT l.like_id) AS likes  -- Aggregate: count likes",
        "FROM posts p",
        "JOIN users u ON p.user_id = u.user_id   -- INNER JOIN: match post → author",
        "LEFT JOIN likes l ON p.post_id = l.post_id  -- LEFT JOIN: keep posts with 0 likes",
        "WHERE p.content ILIKE '%search_term%'   -- Case-insensitive filter",
        "GROUP BY p.post_id, u.username, u.full_name, p.content, p.image_url, p.created_at",
        "ORDER BY p.created_at DESC;             -- Newest post first",
    ]
    draw_code_panel(draw, 80, 600, 1060, 430, q2_lines)
    
    # Annotation labels
    annotations = [
        (920, 420, "JOIN\nlinks tables"),
        (920, 460, "LEFT JOIN\n0 likes OK"),
        (920, 500, "COUNT\naggregates"),
        (920, 540, "GROUP BY\nper post"),
        (920, 580, "ORDER BY\nnewest first"),
    ]
    
    # Clause explanations on right
    explain_items = [
        ("JOIN", "Combines posts with their author from users table", ACCENT_CYAN),
        ("LEFT JOIN", "Includes posts even when they have zero likes", TEXT_YELLOW),
        ("COUNT DISTINCT", "Counts unique likes — avoids double-counting", TEXT_GREEN),
        ("ILIKE", "Case-insensitive text search — finds 'hello' and 'HELLO'", ACCENT_PINK),
        ("GROUP BY", "Aggregates likes per post, not across all posts", (80, 200, 255)),
        ("ORDER BY DESC", "Newest posts appear at top of the feed", ACCENT_PURPLE),
    ]
    
    ex_y = 610
    for (kw, ex, ec) in explain_items:
        draw.rounded_rectangle([1160, ex_y, 1840, ex_y+56], radius=8, fill=(15, 22, 55), outline=ec, width=1)
        draw.text((1178, ex_y+4), kw, font=get_font(20, bold=True), fill=ec)
        draw.text((1178, ex_y+28), ex, font=get_font(18), fill=TEXT_MUTED)
        ex_y += 72
    
    path = os.path.join(FRAME_DIR, "scene10.png")
    img.save(path)
    print(f"  ✓ scene10.png saved")
    return path


def scene11_workflow():
    """Scene 11 — End-to-end workflow."""
    img, draw = make_base_image()
    draw_title_bar(draw, W, "SocialConnect", "End-to-End Workflow")
    
    draw_section_label(draw, 80, 90, "CREATING A POST — FULL FLOW")
    draw.text((80, 125), "From Browser Click to Database and Back", font=get_font(46, bold=True), fill=TEXT_WHITE)
    
    # Data flow strip at top
    strip_items = [
        ("User Action", "Click 'Publish'", ACCENT_CYAN),
        ("JavaScript", "fetch() POST", (80, 180, 255)),
        ("Flask API", "/api/posts", TEXT_YELLOW),
        ("SQL Query", "INSERT INTO posts", (100, 220, 130)),
        ("PostgreSQL", "Row stored", (70, 130, 240)),
        ("JSON Response", "201 Created", TEXT_YELLOW),
        ("Updated UI", "Post appears", ACCENT_CYAN),
    ]
    
    strip_y = 210
    strip_h = 70
    sw = 240
    sx = 60
    for i, (label, detail, color) in enumerate(strip_items):
        bx = sx + i * (sw + 16)
        draw.rounded_rectangle([bx, strip_y, bx+sw, strip_y+strip_h], radius=10,
                               fill=BG_CARD, outline=color, width=2)
        draw.text((bx+10, strip_y+8), label, font=get_font(20, bold=True), fill=color)
        draw.text((bx+10, strip_y+34), detail, font=get_font(18), fill=TEXT_MUTED)
        if i < len(strip_items)-1:
            ax = bx + sw + 4
            draw.polygon([(ax, strip_y+32), (ax+12, strip_y+24), (ax+12, strip_y+42)], fill=color)
    
    # Step-by-step walkthrough
    steps = [
        (1, "User fills form", "Selects 'Alex Rao', types 'Hello from SocialConnect!', clicks Publish", ACCENT_CYAN),
        (2, "JavaScript sends POST", "fetch('/api/posts', {method:'POST', body: JSON.stringify({user_id:1, content:'...'}) })", (80, 180, 255)),
        (3, "Flask receives request", "data = request.get_json()  →  user_id=1, content='Hello from SocialConnect!'", TEXT_YELLOW),
        (4, "Flask validates", "if not user_id or not content: return 400 Bad Request", (255, 150, 60)),
        (5, "Flask queries PostgreSQL", "INSERT INTO posts (user_id, content, image_url) VALUES (1, '...', NULL) RETURNING post_id;", (100, 220, 130)),
        (6, "PostgreSQL stores row", "post_id = 42 returned  ·  conn.commit()  →  Transaction committed", (70, 130, 240)),
        (7, "Flask returns response", "return jsonify({message:'Post created', post_id:42}), 201", TEXT_YELLOW),
        (8, "JS reloads feed", "await loadPosts()  →  GET /api/posts  →  New post at top of feed", ACCENT_CYAN),
    ]
    
    step_y = 300
    for step_num, title, detail, color in steps:
        draw.ellipse([66, step_y+4, 100, step_y+38], fill=color)
        draw.text((78, step_y+9), str(step_num), font=get_font(22, bold=True), fill=BG_DARK)
        draw.rounded_rectangle([110, step_y, 1860, step_y+68], radius=8, fill=BG_CARD)
        draw.text((126, step_y+6), title, font=get_font(22, bold=True), fill=color)
        draw_text_wrapped(draw, detail, 126, step_y+32, get_font(19, mono=True), TEXT_MUTED, 1700)
        step_y += 88
        if step_num < len(steps):
            draw.line([(83, step_y-12), (83, step_y-4)], fill=(60, 80, 180), width=2)
    
    path = os.path.join(FRAME_DIR, "scene11.png")
    img.save(path)
    print(f"  ✓ scene11.png saved")
    return path


def scene12_api_response():
    """Scene 12 — API response format."""
    img, draw = make_base_image()
    draw_title_bar(draw, W, "SocialConnect", "API — JSON Data Format")
    
    draw_section_label(draw, 80, 90, "REQUEST & RESPONSE")
    draw.text((80, 125), "How Flask and JavaScript Communicate", font=get_font(46, bold=True), fill=TEXT_WHITE)
    
    # Left — JSON response
    draw.rounded_rectangle([60, 210, 860, 1040], radius=14, fill=BG_CARD, outline=ACCENT_CYAN, width=2)
    draw.text((80, 220), "GET /api/posts — Response (JSON)", font=get_font(26, bold=True), fill=ACCENT_CYAN)
    
    json_lines = [
        '[',
        '  {',
        '    "post_id":    1,',
        '    "username":   "alex_r",',
        '    "full_name":  "Alex Rao",',
        '    "content":    "Hello from SocialConnect!",',
        '    "image_url":  null,',
        '    "created_at": "2026-10-12 12:00:00",',
        '    "likes":      5',
        '  },',
        '  {',
        '    "post_id":    2,',
        '    "username":   "priya_k",',
        '    "full_name":  "Priya Kumar",',
        '    "content":    "Great platform for learning!",',
        '    "image_url":  null,',
        '    "created_at": "2026-10-12 11:45:00",',
        '    "likes":      12',
        '  }',
        ']',
    ]
    draw_code_panel(draw, 80, 265, 760, 740, json_lines, "JSON Array Response")
    
    # Arrows
    for ay in range(480, 780, 40):
        draw.polygon([(880, ay), (960, ay+16), (880, ay+32)], fill=ACCENT_CYAN)
    draw.text((882, 618), "JS\nparsed", font=get_font(22, bold=True), fill=ACCENT_CYAN)
    
    # Right — Post card mockup showing JSON → UI
    draw.rounded_rectangle([980, 210, 1860, 1040], radius=14, fill=BG_CARD, outline=ACCENT_PURPLE, width=1)
    draw.text((1000, 220), "Frontend Renders — Post Card", font=get_font(26, bold=True), fill=ACCENT_PURPLE)
    
    # Post card visual
    draw.rounded_rectangle([1000, 275, 1840, 600], radius=12, fill=(15, 22, 55), outline=BORDER_COLOR, width=1)
    
    field_mappings = [
        ("post_id", "→", "Article ID (#1)", 300, ACCENT_CYAN),
        ("username", "→", "@alex_r  (handle shown below name)", 360, (255, 200, 80)),
        ("full_name", "→", "Alex Rao  (bold author name)", 420, TEXT_GREEN),
        ("content", "→", "Hello from SocialConnect!  (post body)", 480, (200, 200, 255)),
        ("image_url", "→", "null → no image rendered", 540, TEXT_MUTED),
        ("created_at", "→", "Oct 12, 12:00  (formatted with JS)", 600, (200, 180, 255)),
        ("likes", "→", "♡ Like (5)  (button label)", 660, ACCENT_PINK),
    ]
    
    for (field, arrow, ui_label, fy, fc) in field_mappings:
        draw.text((1010, fy), field, font=get_font(22, mono=True), fill=fc)
        draw.text((1190, fy), arrow, font=get_font(22, bold=True), fill=TEXT_MUTED)
        draw.text((1230, fy), ui_label, font=get_font(22), fill=TEXT_LIGHT)
    
    # JSON how-it-works
    draw.rounded_rectangle([1000, 720, 1840, 870], radius=10, fill=(12, 18, 48), outline=BORDER_COLOR, width=1)
    draw.text((1020, 734), "How JavaScript uses the JSON:", font=get_font(24, bold=True), fill=ACCENT_CYAN)
    js_lines = [
        "const data = await apiJSON('/api/posts');",
        "data.forEach(post => {",
        "  card.innerHTML = `<h3>${post.full_name}</h3>",
        "    <p>${post.content}</p>",
        "    <span>♡ Like (${post.likes})</span>`;",
        "});",
    ]
    draw_code_panel(draw, 1010, 775, 810, 180, js_lines)
    
    path = os.path.join(FRAME_DIR, "scene12.png")
    img.save(path)
    print(f"  ✓ scene12.png saved")
    return path


def scene13_results():
    """Scene 13 — Testing and results."""
    img, draw = make_base_image()
    draw_title_bar(draw, W, "SocialConnect", "Testing & Results")
    
    draw_section_label(draw, 80, 90, "VERIFIED FUNCTIONALITY")
    draw.text((80, 125), "Project Outcomes and Demonstration", font=get_font(52, bold=True), fill=TEXT_WHITE)
    
    checks = [
        ("Flask application starts cleanly", True),
        ("PostgreSQL connection via psycopg2", True),
        ("GET /api/posts — 3-table JOIN + COUNT", True),
        ("POST /api/posts — INSERT RETURNING", True),
        ("POST /api/posts/<id>/like — ON CONFLICT DO NOTHING", True),
        ("POST /api/posts/<id>/unlike — DELETE from likes", True),
        ("DELETE /api/posts/<id> — removes post", True),
        ("GET/POST /api/posts/<id>/comments", True),
        ("GET/POST /api/messages — direct chat", True),
        ("GET /api/users + /api/users/<id>", True),
        ("Search with ILIKE filtering", True),
        ("Duplicate like prevention (DB constraint)", True),
        ("Transaction COMMIT / ROLLBACK", True),
        ("Parameterized queries (SQL injection safe)", True),
        ("Frontend dynamically updates without reload", True),
        ("Dark/Light theme toggle", True),
    ]
    
    col1 = checks[:8]
    col2 = checks[8:]
    
    for col_idx, col_items in enumerate([col1, col2]):
        xoff = 80 + col_idx * 900
        for i, (feature, passed) in enumerate(col_items):
            fy = 210 + i * 76
            color = TEXT_GREEN if passed else ACCENT_PINK
            icon = "✅" if passed else "❌"
            draw.rounded_rectangle([xoff, fy, xoff+830, fy+62], radius=10,
                                  fill=BG_CARD, outline=(30, 50, 100), width=1)
            draw.text((xoff+16, fy+16), icon, font=get_font(26), fill=color)
            draw.text((xoff+72, fy+14), feature, font=get_font(22), fill=TEXT_WHITE)
    
    # Summary box
    draw.rounded_rectangle([80, 840, 1840, 1060], radius=14, fill=(12, 45, 30), outline=TEXT_GREEN, width=2)
    draw.text((120, 860), "✅  ALL FEATURES VERIFIED", font=get_font(36, bold=True), fill=TEXT_GREEN)
    summary_text = ("SocialConnect demonstrates a complete, working DBMS-driven web application. "
                   "All 11 Flask endpoints operate correctly. PostgreSQL stores and retrieves data "
                   "with complex SQL including JOINs, aggregations, and constraints. "
                   "Full CRUD operations are implemented across 5 relational tables.")
    draw_text_wrapped(draw, summary_text, 120, 914, get_font(24), TEXT_LIGHT, 1680)
    
    path = os.path.join(FRAME_DIR, "scene13.png")
    img.save(path)
    print(f"  ✓ scene13.png saved")
    return path


def scene14_conclusion():
    """Scene 14 — Conclusion."""
    img, draw = make_base_image()
    
    # Gradient background — slightly brighter
    draw_gradient_bg(draw, W, H, (8, 12, 40), (20, 15, 60))
    
    draw_title_bar(draw, W, "SocialConnect", "Conclusion & Future Scope")
    
    # Summary cards at top
    summary_items = [
        ("🌐", "Full-Stack", "HTML · CSS · JS · Flask · PostgreSQL", ACCENT_CYAN),
        ("🐍", "11 API Endpoints", "All HTTP methods · Error handling", TEXT_YELLOW),
        ("🐘", "5 DB Tables", "users, posts, likes, comments, messages", (70, 130, 240)),
        ("🔢", "Complex SQL", "JOIN · COUNT · ILIKE · RETURNING", TEXT_GREEN),
        ("✅", "Full CRUD", "Create, Read, Update, Delete", ACCENT_PINK),
    ]
    
    sw = 340
    sx = 60
    sy = 100
    for i, (icon, label, tech, color) in enumerate(summary_items):
        bx = sx + i * (sw + 30)
        draw.rounded_rectangle([bx, sy, bx+sw, sy+150], radius=14, fill=BG_CARD, outline=color, width=2)
        draw.text((bx+16, sy+14), icon, font=get_font(36), fill=color)
        draw.text((bx+16, sy+58), label, font=get_font(24, bold=True), fill=TEXT_WHITE)
        draw_text_wrapped(draw, tech, bx+16, sy+90, get_font(19), TEXT_MUTED, sw-32)
    
    # Future scope section
    draw.text((80, 280), "Future Enhancement Possibilities", font=get_font(36, bold=True), fill=TEXT_MUTED)
    future = ["User Authentication & Login", "Image File Uploads", "Following / Followers System",
              "Push Notifications", "Pagination & Infinite Scroll", "Full-Text Search Index"]
    for i, f in enumerate(future):
        fx = 80 + (i % 3) * 580
        fy = 340 + (i // 3) * 80
        draw.rounded_rectangle([fx-4, fy-4, fx+520, fy+52], radius=8,
                               fill=(18, 20, 50), outline=(40, 50, 100), width=1)
        draw.text((fx+12, fy+8), f"◦ {f}", font=get_font(24), fill=TEXT_MUTED)
    
    # Note about future scope
    draw.rounded_rectangle([80, 520, 1840, 570], radius=8, fill=(20, 15, 50), outline=BORDER_COLOR, width=1)
    draw.text((100, 532), "Note: Items above are future possibilities — not currently implemented.",
             font=get_font(22), fill=(150, 130, 200))
    
    # Final big title
    cx = W // 2
    big_font = get_font(100, bold=True)
    title = "SOCIALCONNECT"
    try:
        tw = draw.textlength(title, font=big_font)
    except:
        tw = len(title) * 62
    
    # Glow effect (multiple passes)
    for offset in [6, 4, 2]:
        draw.text(((W-tw)//2, 610), title, font=big_font, fill=(20, 40, 100))
    draw.text(((W-tw)//2, 610), title, font=big_font, fill=TEXT_WHITE)
    
    sub1 = "Connecting the Frontend, Backend, and Database"
    sub1_font = get_font(38)
    try:
        s1w = draw.textlength(sub1, font=sub1_font)
    except:
        s1w = len(sub1) * 22
    draw.text(((W-s1w)//2, 730), sub1, font=sub1_font, fill=ACCENT_CYAN)
    
    # Divider
    div_x = (W - 400) // 2
    draw.rectangle([div_x, 792, div_x+400, 796], fill=ACCENT_PURPLE)
    
    # Thank you
    ty_font = get_font(72, bold=True)
    ty_text = "Thank You"
    try:
        tyw = draw.textlength(ty_text, font=ty_font)
    except:
        tyw = len(ty_text) * 44
    draw.text(((W-tyw)//2, 820), ty_text, font=ty_font, fill=ACCENT_CYAN)
    
    # Footer tech badges
    badge_labels = ["Flask", "PostgreSQL", "Python", "JavaScript", "HTML/CSS", "psycopg2"]
    badge_x = (W - 1000) // 2
    badge_y = 940
    for label in badge_labels:
        font = get_font(22)
        try:
            bw = draw.textlength(label, font=font)
        except:
            bw = len(label) * 13
        draw.rounded_rectangle([badge_x-8, badge_y-4, badge_x+bw+16, badge_y+36],
                              radius=14, fill=(20, 25, 60), outline=ACCENT_PURPLE, width=1)
        draw.text((badge_x, badge_y), label, font=font, fill=TEXT_MUTED)
        badge_x += bw + 36
    
    # Bottom SocialConnect brand
    draw.rectangle([0, 1038, W, 1080], fill=(8, 12, 30))
    draw.text((W//2 - 200, 1048), "SOCIALCONNECT · DBMS PROJECT · 2026", font=get_font(22), fill=TEXT_MUTED)
    
    path = os.path.join(FRAME_DIR, "scene14.png")
    img.save(path)
    print(f"  ✓ scene14.png saved")
    return path


# ═══════════════════════════════════════════════════════════════════════════════
#  ER DIAGRAM GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

def generate_er_diagram():
    """Generate a proper ER diagram."""
    img = Image.new("RGB", (1600, 1000), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, 1600, 1000)
    
    # Title
    draw.text((40, 20), "SocialConnect — Entity-Relationship Diagram", font=get_font(36, bold=True), fill=TEXT_WHITE)
    draw.text((40, 66), "Database: social_media_db  ·  5 Tables  ·  4 Foreign Key Relationships", font=get_font(22), fill=TEXT_MUTED)
    
    # Entity positions
    entities = {
        "USERS":    (800, 420, ACCENT_CYAN),
        "POSTS":    (300, 220, TEXT_YELLOW),
        "LIKES":    (300, 680, ACCENT_PINK),
        "COMMENTS": (1300, 220, ACCENT_PURPLE),
        "MESSAGES": (1300, 680, (100, 200, 130)),
    }
    
    entity_cols = {
        "USERS":    ["🔑 user_id (PK)", "username", "email", "full_name", "bio"],
        "POSTS":    ["🔑 post_id (PK)", "🔗 user_id (FK)", "content", "image_url", "created_at"],
        "LIKES":    ["🔑 like_id (PK)", "🔗 post_id (FK)", "🔗 user_id (FK)", "UNIQUE(post_id,user_id)"],
        "COMMENTS": ["🔑 comment_id (PK)", "🔗 post_id (FK)", "🔗 user_id (FK)", "comment_text", "created_at"],
        "MESSAGES": ["🔑 message_id (PK)", "🔗 sender_id (FK)", "🔗 recipient_id (FK)", "message_text", "created_at"],
    }
    
    entity_boxes = {}
    
    for name, (cx, cy, color) in entities.items():
        cols = entity_cols[name]
        ew = 340
        eh = 50 + len(cols) * 34
        x1, y1 = cx - ew//2, cy - eh//2
        x2, y2 = cx + ew//2, cy + eh//2
        entity_boxes[name] = (x1, y1, x2, y2, cx, cy)
        
        draw.rounded_rectangle([x1, y1, x2, y2], radius=12, fill=BG_CARD, outline=color, width=2)
        # Header
        draw.rounded_rectangle([x1, y1, x2, y1+46], radius=10, fill=color)
        draw.text((cx - len(name)*10, y1+10), name, font=get_font(24, bold=True), fill=BG_DARK)
        
        for i, col in enumerate(cols):
            cy2 = y1 + 54 + i * 34
            c = ACCENT_CYAN if "PK" in col else (255,160,60) if "FK" in col else ACCENT_PINK if "UNIQUE" in col else TEXT_LIGHT
            draw.text((x1+14, cy2), col, font=get_font(18, mono=True), fill=c)
    
    # Relationships (lines)
    def connect(name1, name2, label, card="1:N"):
        x1,y1,x2,y2,cx1,cy1 = entity_boxes[name1]
        x1b,y1b,x2b,y2b,cx2,cy2 = entity_boxes[name2]
        draw.line([(cx1,cy1),(cx2,cy2)], fill=(80,100,180), width=2)
        mx, my = (cx1+cx2)//2, (cy1+cy2)//2
        draw.rounded_rectangle([mx-70, my-14, mx+130, my+14], radius=6, fill=(20,28,70))
        draw.text((mx-60, my-10), f"{label} ({card})", font=get_font(16), fill=TEXT_MUTED)
    
    connect("USERS", "POSTS",    "writes",   "1:N")
    connect("USERS", "LIKES",    "gives",    "1:N")
    connect("POSTS", "LIKES",    "receives", "1:N")
    connect("POSTS", "COMMENTS", "has",      "1:N")
    connect("USERS", "COMMENTS", "writes",   "1:N")
    connect("USERS", "MESSAGES", "sends",    "1:N")
    
    # Legend
    draw.rounded_rectangle([40, 920, 800, 975], radius=8, fill=BG_CARD, outline=BORDER_COLOR, width=1)
    draw.text((60, 932), "🔑 PK = Primary Key   🔗 FK = Foreign Key   ⚡ UNIQUE = Constraint   1:N = One-to-Many", 
             font=get_font(20), fill=TEXT_MUTED)
    
    path = os.path.join(BASE, "SocialConnect_ER_Diagram.png")
    img.save(path)
    print(f"  ✓ SocialConnect_ER_Diagram.png saved")
    return path


def generate_architecture_diagram():
    """Generate a standalone architecture diagram."""
    img = Image.new("RGB", (1600, 900), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, 1600, 900)
    
    draw.text((40, 20), "SocialConnect — System Architecture", font=get_font(36, bold=True), fill=TEXT_WHITE)
    
    tiers = [
        ("FRONTEND LAYER", "HTML5 · CSS3 · JavaScript (ES6+)", 
         "Renders UI · Handles interactions · Sends HTTP requests · Parses JSON responses",
         ACCENT_CYAN, 100),
        ("HTTP + JSON LAYER", "HTTP GET / POST / DELETE  +  JSON Body",
         "Stateless request-response protocol · No server sessions · Standard web communication",
         ACCENT_PURPLE, 340),
        ("BACKEND LAYER", "Python Flask · psycopg2 · flask-cors",
         "11 REST API routes · SQL execution · Validation · Error handling · Transaction management",
         TEXT_YELLOW, 580),
        ("DATABASE LAYER", "PostgreSQL — social_media_db",
         "5 Tables: users, posts, likes, comments, messages · FK constraints · UNIQUE constraints",
         (70, 130, 240), 760),
    ]
    
    for (label, tech, desc, color, y) in tiers:
        draw.rounded_rectangle([100, y, 1500, y+170], radius=16, fill=BG_CARD, outline=color, width=2)
        draw.rounded_rectangle([100, y, 160, y+170], radius=14, fill=color)
        draw.text((180, y+20), label, font=get_font(34, bold=True), fill=color)
        draw.text((180, y+72), tech, font=get_font(26, bold=True), fill=TEXT_WHITE)
        draw_text_wrapped(draw, desc, 180, y+112, get_font(22), TEXT_MUTED, 1280)
        
        if y < 760:
            aw = 800 + y // 2
            draw.polygon([(aw-20, y+172), (aw+20, y+172), (aw, y+200)], fill=color)
    
    path = os.path.join(BASE, "SocialConnect_Architecture.png")
    img.save(path)
    print(f"  ✓ SocialConnect_Architecture.png saved")
    return path


# ═══════════════════════════════════════════════════════════════════════════════
#  TTS NARRATION GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

NARRATION_TEXTS = {
    "scene01": (
        "Welcome to SocialConnect — a Social Media Database Management System. "
        "This project is a fully functional web application that demonstrates how a "
        "modern database-driven system works — from a user interface in the browser, "
        "through a Python backend, all the way to a PostgreSQL relational database. "
        "In the next seven minutes, we will walk through every layer of this system — "
        "what it does, how it is built, and which database concepts it demonstrates in practice."
    ),
    "scene02": (
        "Every social media application you use today depends on a database at its core. "
        "When you write a post, that text must be saved somewhere. "
        "When someone likes your post, that action must be recorded. "
        "When you send a private message, it must be stored and delivered accurately. "
        "A database management system is the engine that makes all of this possible. "
        "It stores data in organized tables, enforces relationships between records, "
        "and answers questions instantly using a language called SQL. "
        "SocialConnect was built to demonstrate exactly these principles — not as a "
        "commercial product, but as a complete, working example of how frontend "
        "interfaces, backend logic, and relational database operations work together."
    ),
    "scene03": (
        "Let's look at what SocialConnect actually does. "
        "The application allows users to create posts with text and optional images. "
        "Every post is associated with a registered user stored in the database. "
        "Users can browse a live feed of all posts, sorted by creation time. "
        "They can search posts by keyword using the built-in search feature. "
        "Each post supports likes and unlikes. "
        "The system prevents the same user from liking the same post twice, "
        "enforced at the database level. "
        "Users can read and add comments to any post. "
        "They can view user profiles showing bio, email, and post count. "
        "And SocialConnect includes a full direct messaging system — "
        "users can send private messages to one another, "
        "with conversations auto-refreshing every five seconds. "
        "All of these features are backed by real database operations happening in real time."
    ),
    "scene04": (
        "SocialConnect uses a clearly separated three-tier architecture. "
        "At the top is the frontend — built with HTML, which defines the page structure; "
        "CSS, which controls layout and colors; "
        "and JavaScript, which handles all user interactions without refreshing the page. "
        "In the middle is the backend — a Python application using the Flask framework. "
        "Flask provides routes, or URL endpoints, that receive requests from the browser, "
        "execute business logic, and return structured responses. "
        "At the bottom is the database — PostgreSQL, "
        "a powerful open-source relational database management system "
        "storing all persistent data: users, posts, likes, comments, and messages. "
        "Connecting the backend to the database is psycopg2, "
        "a Python library that lets Flask send SQL queries to PostgreSQL and receive results. "
        "The frontend and backend communicate using HTTP and exchange data in JSON format."
    ),
    "scene05": (
        "Here is SocialConnect running in a browser. "
        "The layout has a left sidebar for navigation, a central content area, and a right panel. "
        "At the top of the main area is the post creation form. "
        "A user selects their identity from a dropdown, types their message, "
        "optionally adds an image URL, and clicks Publish. "
        "This sends a request to the Flask backend, which inserts the post into PostgreSQL. "
        "Below that is the community feed — a list of post cards, each showing the author, "
        "username, timestamp, post content, and like count. "
        "Each post card has Like, Unlike, and Comments buttons. "
        "If the post belongs to the currently selected user, a Delete button also appears. "
        "The search bar lets you filter posts in real time using SQL case-insensitive matching. "
        "The Profiles section lets you view any user's bio, email, and post count. "
        "Clicking Messages opens the private chat interface with auto-refreshing conversations."
    ),
    "scene06": (
        "Let's visualize how these layers work together. "
        "A user interacts with the browser — clicking a button or filling a form. "
        "JavaScript captures that event and uses the Fetch API to send an HTTP request to Flask. "
        "The request may be a GET to retrieve data, or a POST or DELETE to modify data. "
        "Flask receives the request on the corresponding route. "
        "It extracts parameters from the URL or JSON body, validates them, "
        "and constructs a SQL query. "
        "psycopg2 executes that query against the PostgreSQL database called social_media_db. "
        "PostgreSQL processes the query, applies its rules and constraints, "
        "and returns the results. "
        "Flask converts those results into a JSON response and sends it back to the browser. "
        "JavaScript receives the response, parses the JSON, and dynamically updates the page. "
        "The frontend never touches the database directly. "
        "All database communication passes through the Flask backend."
    ),
    "scene07": (
        "Let's look at the Flask backend in detail. "
        "Flask is a Python web framework. "
        "You define a route using the app.route decorator, "
        "which maps a URL path to a Python function. "
        "The backend has eleven endpoints in total. "
        "GET /api/posts returns a JSON array of all posts. "
        "It uses a three-table JOIN — joining posts with users for the author's name, "
        "and with likes to count how many likes each post has received. "
        "The WHERE clause uses ILIKE for case-insensitive search. "
        "POST /api/posts creates a new post using a parameterized SQL INSERT with RETURNING. "
        "The like endpoint uses PostgreSQL's ON CONFLICT DO NOTHING clause — "
        "meaning if the same user tries to like the same post twice, "
        "the database simply ignores the second request. "
        "Every database operation uses parameterized queries, "
        "which completely prevents SQL injection attacks. "
        "Every write operation wraps database calls with commit on success "
        "and rollback on failure."
    ),
    "scene08": (
        "Now let's look at the PostgreSQL database. "
        "The database is named social_media_db and contains five tables. "
        "The users table holds user accounts with user_id as the primary key, "
        "plus username, email, full name, and bio. "
        "The posts table stores every post. "
        "The user_id column is a foreign key that references the users table — "
        "this is how the database knows which user wrote each post. "
        "The likes table records which user liked which post. "
        "Both post_id and user_id are foreign keys, "
        "and together they form a unique constraint — "
        "the database itself prevents the same user from liking the same post twice. "
        "The comments table stores comments linked to both a post and a user. "
        "The messages table stores direct messages with both a sender and recipient, "
        "both referencing the users table via foreign keys. "
        "The entity-relationship diagram shows users at the center, "
        "related to posts, likes, comments, and messages through one-to-many relationships."
    ),
    "scene09": (
        "SocialConnect demonstrates a wide range of core database concepts. "
        "A primary key uniquely identifies each row. "
        "Every table has one: user_id, post_id, like_id, comment_id, and message_id. "
        "A foreign key links a row in one table to a row in another, "
        "enforcing referential integrity. "
        "A JOIN combines rows from multiple tables. "
        "The post feed query joins three tables in a single SQL statement. "
        "The COUNT aggregate function counts how many likes each post has, "
        "grouped using GROUP BY. "
        "INSERT with RETURNING is used after creating a post, comment, or message — "
        "PostgreSQL executes the insertion and immediately returns the new ID. "
        "ON CONFLICT DO NOTHING demonstrates upsert logic — "
        "where an INSERT either succeeds or is gracefully ignored. "
        "Transaction management with commit and rollback ensures database consistency. "
        "Together, these concepts demonstrate the full practical scope "
        "of a relational database in a real application."
    ),
    "scene10": (
        "Let's look at a few key SQL queries in action. "
        "First, a simple SELECT to retrieve all posts from the table: "
        "SELECT star FROM posts. "
        "This returns every row with post_id, user_id, content, image_url, and created_at. "
        "Next, the full query used by the API — joining three tables to build the complete post feed. "
        "We select post_id, username, full_name, content, created_at, "
        "and COUNT DISTINCT like_id as likes. "
        "Posts is joined with users using an INNER JOIN to get the author's name. "
        "Likes is included using a LEFT JOIN — this is important because "
        "posts with zero likes must still appear in the feed. "
        "An INNER JOIN would hide them entirely. "
        "COUNT DISTINCT ensures even if a duplicate like somehow existed, "
        "it would only be counted once. "
        "GROUP BY groups the aggregate per post, and ORDER BY created_at DESC "
        "puts the newest post at the top."
    ),
    "scene11": (
        "Let's trace a complete user action from browser to database and back. "
        "A user opens SocialConnect. "
        "The browser calls GET /api/users to populate the user dropdown, "
        "and GET /api/posts to load the feed. "
        "The user selects their identity, types a message — "
        "Hello from SocialConnect — and clicks Publish. "
        "JavaScript reads the user ID and content, packages them as JSON, "
        "and sends a POST request to /api/posts. "
        "Flask receives the request, extracts user_id and content from the JSON body, "
        "and validates that both are present. "
        "Then it opens a psycopg2 connection to PostgreSQL. "
        "Flask executes the INSERT statement with parameterized values. "
        "PostgreSQL stores the new row, assigns a post_id of 42, "
        "and returns that ID to Flask. "
        "Flask commits the transaction and sends a 201 Created response back to the browser. "
        "JavaScript receives the success response, clears the form, "
        "shows a toast notification, and calls GET /api/posts to reload the feed. "
        "The new post now appears at the top with the correct author name, timestamp, "
        "and zero likes — all retrieved live from the database."
    ),
    "scene12": (
        "Let's look at what the API actually returns. "
        "When the browser calls GET /api/posts, Flask responds with a JSON array. "
        "Each element represents one post and contains these fields: "
        "post_id, the unique numeric identifier; "
        "username, the author's handle; "
        "full_name, the author's display name; "
        "content, the text body of the post; "
        "image_url, either a URL or null if no image was provided; "
        "created_at, the timestamp from PostgreSQL; "
        "and likes, an integer count of how many users liked this post. "
        "This JSON structure is what JavaScript receives, parses, "
        "and uses to build each post card in the browser. "
        "JSON is important because it is a universal format. "
        "Flask generates it using jsonify, "
        "and JavaScript parses it natively without any special conversion."
    ),
    "scene13": (
        "Let's summarize what has been demonstrated. "
        "SocialConnect successfully runs as a Python Flask application "
        "connected to a PostgreSQL database. "
        "The application starts cleanly, connects via psycopg2, "
        "and all eleven API endpoints respond as expected. "
        "The post feed retrieves data using a complex three-table JOIN with aggregation. "
        "Post creation, liking, unliking, deleting, commenting, and messaging "
        "all work correctly through their respective endpoints. "
        "Duplicate like prevention works at the database level "
        "through a unique constraint and ON CONFLICT clause. "
        "The frontend dynamically updates after every action "
        "without requiring a page reload, "
        "demonstrating real-world integration between JavaScript, Flask, and PostgreSQL."
    ),
    "scene14": (
        "SocialConnect demonstrates that a complete, database-driven web application "
        "can be built using open-source tools — "
        "HTML, CSS, JavaScript, Python Flask, psycopg2, and PostgreSQL. "
        "The project covers the full stack from browser to database. "
        "It uses a five-table relational schema with primary keys, "
        "foreign keys, and unique constraints. "
        "It performs complex SQL operations including joins, aggregations, "
        "filtering, and sorting. "
        "It implements all four CRUD operations across multiple tables. "
        "Looking forward, the project could be extended with user authentication, "
        "image uploads, a following system, push notifications, and pagination. "
        "These are possibilities for future development — "
        "not features that are currently implemented. "
        "The current version is a clean, functional demonstration "
        "of relational database principles applied in a real web application. "
        "Thank you for watching this explanation of SocialConnect — "
        "a Social Media Database Management System built with Flask and PostgreSQL."
    ),
}


def generate_narration_gtts(scene_key, text):
    """Generate audio using gTTS."""
    path = os.path.join(AUDIO_DIR, f"{scene_key}.mp3")
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print(f"  ✓ {scene_key}.mp3 already exists, skipping")
        return path
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(path)
        print(f"  ✓ {scene_key}.mp3 generated ({os.path.getsize(path)//1024}KB)")
        return path
    except Exception as e:
        print(f"  ✗ TTS failed for {scene_key}: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
#  SUBTITLE GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

def generate_srt(scene_durations):
    """Generate SRT subtitle file based on scene durations."""
    scenes = list(NARRATION_TEXTS.keys())
    srt_lines = []
    sub_index = 1
    current_time = 0.0
    
    for scene_key in scenes:
        text = NARRATION_TEXTS[scene_key]
        duration = scene_durations.get(scene_key, 30.0)
        
        # Split text into subtitle chunks (roughly 10 words each)
        words = text.split()
        chunk_size = 12
        chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        
        if not chunks:
            current_time += duration
            continue
        
        chunk_duration = duration / len(chunks)
        
        for chunk in chunks:
            start = current_time
            end = current_time + chunk_duration
            
            def fmt_time(t):
                h = int(t // 3600)
                m = int((t % 3600) // 60)
                s = int(t % 60)
                ms = int((t - int(t)) * 1000)
                return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
            
            srt_lines.append(str(sub_index))
            srt_lines.append(f"{fmt_time(start)} --> {fmt_time(end)}")
            srt_lines.append(chunk)
            srt_lines.append("")
            
            sub_index += 1
            current_time = end
    
    srt_path = os.path.join(BASE, "SocialConnect_Subtitles.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))
    print(f"  ✓ SocialConnect_Subtitles.srt generated ({sub_index-1} subtitles)")
    return srt_path


# ═══════════════════════════════════════════════════════════════════════════════
#  VIDEO ASSEMBLY
# ═══════════════════════════════════════════════════════════════════════════════

def get_audio_duration(path):
    """Get audio file duration in seconds."""
    try:
        clip = AudioFileClip(path)
        dur = clip.duration
        clip.close()
        return dur
    except:
        return 30.0


def build_scene_clip(scene_key, image_path, audio_path, min_duration=15.0):
    """Build a single scene video clip from image + audio."""
    if audio_path and os.path.exists(audio_path):
        duration = get_audio_duration(audio_path)
        duration = max(duration + 1.0, min_duration)
    else:
        duration = min_duration
    
    # Create image clip
    img_clip = ImageClip(image_path, duration=duration)
    
    if audio_path and os.path.exists(audio_path):
        audio_clip = AudioFileClip(audio_path)
        audio_clip = audio_clip.with_end(duration)
        img_clip = img_clip.with_audio(audio_clip)
    
    return img_clip, duration


def assemble_video(scene_clips, output_path):
    """Concatenate all clips and write final MP4."""
    print(f"\n🎬 Assembling {len(scene_clips)} scenes into final video...")
    
    final = concatenate_videoclips(scene_clips, method="compose")
    
    print(f"   Total duration: {final.duration:.1f} seconds ({final.duration/60:.1f} minutes)")
    print(f"   Writing to: {output_path}")
    
    final.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        logger="bar",
        preset="fast",
        threads=4
    )
    final.close()
    
    for clip in scene_clips:
        try:
            clip.close()
        except:
            pass
    
    return output_path


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "="*60)
    print("  SocialConnect — Video Generator")
    print("="*60)
    
    # Step 1: Generate all scene images
    print("\n📸 STEP 1: Generating scene images...")
    scene_generators = [
        ("scene01", scene01_opening),
        ("scene02", scene02_problem),
        ("scene03", scene03_features),
        ("scene04", scene04_techstack),
        ("scene05", scene05_frontend),
        ("scene06", scene06_architecture),
        ("scene07", scene07_backend),
        ("scene08", scene08_database),
        ("scene09", scene09_concepts),
        ("scene10", scene10_sql),
        ("scene11", scene11_workflow),
        ("scene12", scene12_api_response),
        ("scene13", scene13_results),
        ("scene14", scene14_conclusion),
    ]
    
    image_paths = {}
    for key, gen_fn in scene_generators:
        try:
            path = gen_fn()
            image_paths[key] = path
        except Exception as e:
            print(f"  ✗ {key} failed: {e}")
            import traceback
            traceback.print_exc()
    
    # Step 2: Generate ER and architecture diagrams
    print("\n📊 STEP 2: Generating diagrams...")
    try:
        generate_er_diagram()
    except Exception as e:
        print(f"  ✗ ER diagram failed: {e}")
    
    try:
        generate_architecture_diagram()
    except Exception as e:
        print(f"  ✗ Architecture diagram failed: {e}")
    
    # Step 3: Generate narration audio
    print("\n🎤 STEP 3: Generating narration audio...")
    audio_paths = {}
    if TTS_ENGINE == "gtts":
        for key, text in NARRATION_TEXTS.items():
            try:
                path = generate_narration_gtts(key, text)
                audio_paths[key] = path
            except Exception as e:
                print(f"  ✗ Audio {key} failed: {e}")
    else:
        print("  ✗ No TTS engine available — video will be silent")
    
    # Step 4: Build subtitle file (using estimated durations first)
    print("\n📝 STEP 4: Generating subtitles...")
    scene_durations = {}
    for key in NARRATION_TEXTS:
        ap = audio_paths.get(key)
        if ap and os.path.exists(ap):
            scene_durations[key] = get_audio_duration(ap)
        else:
            # Estimate: ~150 words per minute
            words = len(NARRATION_TEXTS[key].split())
            scene_durations[key] = (words / 150) * 60
    
    generate_srt(scene_durations)
    
    # Step 5: Assemble video
    print("\n🎬 STEP 5: Assembling video...")
    if not MOVIEPY_OK:
        print("  ✗ MoviePy not available — cannot assemble video")
        print("  ✓ All individual files have been generated successfully")
        print("  → Install MoviePy and rerun to assemble final video")
        return
    
    output_path = os.path.join(BASE, "SocialConnect_DBMS_Explanation.mp4")
    
    clips = []
    for key, _ in scene_generators:
        img_path = image_paths.get(key)
        if not img_path or not os.path.exists(img_path):
            print(f"  ✗ Missing image for {key}, skipping")
            continue
        
        audio_path = audio_paths.get(key)
        min_dur = max(15.0, scene_durations.get(key, 30.0))
        
        try:
            clip, dur = build_scene_clip(key, img_path, audio_path, min_dur)
            clips.append(clip)
            print(f"  ✓ {key}: {dur:.1f}s")
        except Exception as e:
            print(f"  ✗ Clip build failed for {key}: {e}")
    
    if not clips:
        print("  ✗ No clips to assemble!")
        return
    
    try:
        assemble_video(clips, output_path)
        
        # Verify output
        size = os.path.getsize(output_path)
        print(f"\n✅ VIDEO COMPLETE!")
        print(f"   File: {output_path}")
        print(f"   Size: {size / (1024*1024):.1f} MB")
        
    except Exception as e:
        print(f"  ✗ Video assembly failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n📁 Output files:")
    for f in os.listdir(BASE):
        fp = os.path.join(BASE, f)
        if os.path.isfile(fp):
            print(f"   {f} ({os.path.getsize(fp)//1024}KB)")


if __name__ == "__main__":
    main()
