# SocialConnect — Scene-by-Scene Storyboard

**Project:** SocialConnect — Social Media Database Management System  
**Video Format:** MP4, 1920×1080, 30 FPS  
**Target Duration:** ~7 minutes 30 seconds  

---

## Scene 1 — Professional Opening
**Duration:** 0:00 – 0:18 (18 seconds)

### Narration
> "Welcome to SocialConnect — a Social Media Database Management System. This project is a fully functional web application that demonstrates how a modern database-driven system works — from a user interface in the browser, through a Python backend, all the way to a PostgreSQL relational database. In the next seven minutes, we will walk through every layer of this system."

### Visuals
- Deep navy/violet gradient background (1920×1080)
- Animated "S" logo with orbit rings — pulsing glow
- Large title: **SOCIALCONNECT** (white, bold, centered)
- Subtitle: *Social Media Database Management System*
- Sub-subtitle: *An Integrated Web Application Using Flask & PostgreSQL*
- Floating icons: database cylinder, browser window, Python logo, code brackets
- Animated particles/dots moving toward center

### On-Screen Text
- `SOCIALCONNECT`
- `Social Media Database Management System`
- `Flask | PostgreSQL | Python | JavaScript`

### Transition
Fade title down, reveal content area sliding in from right

---

## Scene 2 — Problem Statement
**Duration:** 0:18 – 0:50 (32 seconds)

### Narration
> "Every social media application you use today depends on a database at its core. When you write a post, that text must be saved somewhere. When someone likes your post, that action must be recorded. When you send a private message, it must be stored and delivered accurately. A DBMS is the engine that makes all of this possible..."

### Visuals
- Split screen: left = stylized browser mockup (user clicking); right = database table rows appearing
- Animated arrow connecting both sides
- Text callouts: "Post saved in DB", "Like recorded", "Message stored"
- Data flow particles moving from browser → database icon

### On-Screen Text
- `Why does social media need a database?`
- Callouts: `users table`, `posts table`, `likes table`, `messages table`

### Required Screenshot/Diagram
- Generic browser + database icon diagram (generated)

### Transition
Slide left → wipe to next scene

---

## Scene 3 — Objectives and Features
**Duration:** 0:50 – 1:30 (40 seconds)

### Narration
> "The application allows users to create posts, browse a live feed, search by keyword, like and unlike posts, add comments, view user profiles, and send direct messages. All features backed by real database operations."

### Visuals
- Feature cards grid (2×4) with icons and short labels:
  - 📝 Create Posts
  - 📰 Browse Feed
  - 🔍 Search Posts
  - ❤️ Like / Unlike
  - 💬 Comments
  - 👤 User Profiles
  - ✉️ Direct Messaging
  - 🌓 Dark/Light Theme
- Cards appear one by one with slight stagger animation
- Background: dark navy with subtle grid pattern

### On-Screen Text
Feature labels on each card

### Transition
Cards shrink → new background slides in

---

## Scene 4 — Technology Stack
**Duration:** 1:30 – 2:05 (35 seconds)

### Narration
> "At the top is the frontend — HTML, CSS, and JavaScript. In the middle is Flask, the Python backend. At the bottom is PostgreSQL. psycopg2 connects Python to the database. Communication uses HTTP and JSON."

### Visuals
- Vertical stack diagram with 3 tiers:
  - **FRONTEND** box: HTML5 | CSS3 | JavaScript
  - Arrow labeled: HTTP + JSON
  - **BACKEND** box: Python Flask + psycopg2
  - Arrow labeled: SQL Queries
  - **DATABASE** box: PostgreSQL — social_media_db
- Each tier lights up as narrated
- Background: dark blue with subtle hex grid

### On-Screen Text
```
FRONTEND LAYER     HTML · CSS · JavaScript
        ↕  HTTP + JSON
BACKEND LAYER      Python Flask · psycopg2
        ↕  SQL Queries
DATABASE LAYER     PostgreSQL · social_media_db
```

### Transition
Stack diagram zooms out → next scene fades in

---

## Scene 5 — Frontend Demonstration
**Duration:** 2:05 – 2:55 (50 seconds)

### Narration
> "Here is SocialConnect running in a browser. The layout has a sidebar for navigation, a main content area, and a right panel. The post creation form lets a user select identity, type a message, and publish. The feed shows post cards with author info, content, and like counts. Search filters posts in real time via ILIKE..."

### Visuals
- Screenshots of the running SocialConnect UI:
  - Full page screenshot (dark theme)
  - Zoom into post creation form
  - Zoom into post feed / post card
  - Zoom into search bar
  - Screenshot of Profiles section
  - Screenshot of Messages/chat UI
- Animated highlight boxes (cyan border) showing each UI element as narrated
- Browser chrome frame around each screenshot

### On-Screen Text
- Labels on UI elements: "User Selector", "Post Content", "Publish Button", "Like Button", "Search Bar"

### Required Screenshot
- Actual SocialConnect UI screenshots (captured or simulated from HTML)

### Transition
UI screenshot slides right → architecture diagram appears

---

## Scene 6 — System Architecture
**Duration:** 2:55 – 3:32 (37 seconds)

### Narration
> "A user interacts with the browser. JavaScript sends an HTTP request to Flask. Flask validates and queries PostgreSQL via psycopg2. PostgreSQL returns results. Flask converts them to JSON. JavaScript updates the page. The frontend never touches the database directly."

### Visuals
- Animated flow diagram (top to bottom):
  ```
  [USER] 
     ↓ (click/action)
  [BROWSER — JS fetch()]
     ↓ HTTP POST/GET/DELETE + JSON
  [FLASK BACKEND — app.py]
     ↓ psycopg2 SQL query
  [POSTGRESQL — social_media_db]
     ↑ Query Result (rows)
  [FLASK — jsonify()]
     ↑ JSON Response
  [BROWSER — updates DOM]
     ↑ User sees result
  ```
- Arrows animate with moving dots (request = blue, response = cyan)
- Each box highlights when narrated

### On-Screen Text
Each box label in diagram

### Transition
Diagram fades → code panel slides in

---

## Scene 7 — Backend and Flask API
**Duration:** 3:32 – 4:25 (53 seconds)

### Narration
> "Flask defines a route using the app.route decorator. The backend has eleven endpoints covering all features. GET /api/posts uses a three-table JOIN. POST /api/posts runs an INSERT with RETURNING. The like endpoint uses ON CONFLICT DO NOTHING. All SQL uses parameterized queries for security. Transactions use commit and rollback."

### Visuals
- Dark code panel (VS Code-style dark theme)
- Code excerpts highlighted one at a time:
  1. `get_db_connection()` function
  2. `@app.route("/api/posts", methods=["GET"])` with SELECT JOIN query
  3. `@app.route("/api/posts", methods=["POST"])` with INSERT RETURNING
  4. `ON CONFLICT (post_id, user_id) DO NOTHING` highlighted
  5. `conn.commit()` / `conn.rollback()` pattern
- API endpoint table visible on left:

```
GET    /api/posts
POST   /api/posts
POST   /api/posts/<id>/like
POST   /api/posts/<id>/unlike
DELETE /api/posts/<id>
GET    /api/users
GET    /api/users/<id>
GET    /api/posts/<id>/comments
POST   /api/posts/<id>/comments
POST   /api/messages
GET    /api/messages
```

### On-Screen Text
Route decorators and key SQL lines highlighted in cyan

### Required Code Excerpt
Actual lines from app.py (lines 32–74 for get_posts, lines 79–115 for create_post)

### Transition
Code panel slides left → database schema view

---

## Scene 8 — PostgreSQL Database and Schema
**Duration:** 4:25 – 5:15 (50 seconds)

### Narration
> "The database is named social_media_db and contains five tables: users, posts, likes, comments, and messages. users has user_id as primary key. posts references users via user_id as a foreign key. likes prevents duplicates via a unique constraint. An ER diagram shows these relationships."

### Visuals
- ER Diagram (generated image) showing:
  - 5 entities: users, posts, likes, comments, messages
  - Relationships with cardinality labels
  - PK/FK indicators on columns
- Table schema cards appearing for each table:
  ```
  USERS:    user_id (PK), username, email, full_name, bio
  POSTS:    post_id (PK), user_id (FK), content, image_url, created_at
  LIKES:    like_id (PK), post_id (FK), user_id (FK), UNIQUE(post_id, user_id)
  COMMENTS: comment_id (PK), post_id (FK), user_id (FK), comment_text, created_at
  MESSAGES: message_id (PK), sender_id (FK), recipient_id (FK), message_text, created_at
  ```
- Highlighted foreign key lines connecting tables

### On-Screen Text
Table names, column names, PK/FK badges

### Required Assets
- SocialConnect_ER_Diagram.png (generated)

### Transition
ER Diagram stays, zoom out → DBMS concepts overlay

---

## Scene 9 — DBMS Concepts
**Duration:** 5:15 – 6:00 (45 seconds)

### Narration
> "Primary keys uniquely identify rows. Foreign keys enforce referential integrity. JOINs combine tables. COUNT is an aggregate. INSERT with RETURNING retrieves the new ID. ON CONFLICT DO NOTHING is upsert logic. Commit and rollback manage transactions."

### Visuals
- Concept cards appearing in sequence:
  - 🔑 PRIMARY KEY — "Uniquely identifies each row"
  - 🔗 FOREIGN KEY — "Links tables, enforces integrity"
  - 🔄 JOIN — "Combines data from multiple tables"
  - 📊 COUNT / GROUP BY — "Aggregation"
  - ➕ INSERT RETURNING — "Create and immediately read ID"
  - ⚡ ON CONFLICT DO NOTHING — "Idempotent upsert"
  - 💾 COMMIT / ROLLBACK — "Transaction safety"
  - ✅ CRUD — "Create, Read, Update, Delete"
- Each card shows: concept name + short definition + relevant code snippet

### On-Screen Text
Concept cards with icons, labels, and one-line definitions

### Transition
Cards fade → SQL query panel

---

## Scene 10 — SQL Demonstration
**Duration:** 6:00 – 6:38 (38 seconds)

### Narration
> "SELECT * FROM posts shows raw table rows. The full join query combines posts, users, and likes with COUNT DISTINCT for the like count, GROUP BY to aggregate per post, and ORDER BY created_at DESC for newest first. LEFT JOIN ensures posts with zero likes still appear."

### Visuals
- Terminal/psql-style query panel (dark background, monospace font)
- Query 1 typed and executed:
  ```sql
  SELECT * FROM posts;
  ```
  → Shows simulated result rows
- Query 2 (the full JOIN):
  ```sql
  SELECT p.post_id, u.username, u.full_name, 
         p.content, p.created_at,
         COUNT(DISTINCT l.like_id) AS likes
  FROM posts p
  JOIN users u ON p.user_id = u.user_id
  LEFT JOIN likes l ON p.post_id = l.post_id
  GROUP BY p.post_id, u.username, u.full_name,
           p.content, p.image_url, p.created_at
  ORDER BY p.created_at DESC;
  ```
  → Shows result table with all columns highlighted
- Arrows annotating key clauses: JOIN, LEFT JOIN, COUNT, GROUP BY, ORDER BY

### On-Screen Text
SQL syntax highlighted (keywords in blue/cyan, table names in yellow, columns in white)

### Transition
Query result table morphs → application screenshot

---

## Scene 11 — End-to-End Workflow
**Duration:** 6:38 – 7:15 (37 seconds)

### Narration
> "A complete workflow: user opens app, loads users and posts from API, types a post and clicks Publish. JavaScript sends POST /api/posts with JSON. Flask validates, opens psycopg2 connection, executes INSERT RETURNING, commits, returns 201 Created. JavaScript clears form, shows toast, reloads feed. New post appears. User clicks Like — likes table gets a row. ON CONFLICT prevents duplicates."

### Visuals
- Animated data-flow strip at bottom of screen:
  ```
  [User Action] → [JavaScript] → [Flask API] → [SQL Query] → [PostgreSQL] → [JSON Response] → [Updated UI]
  ```
  Dots travel across the strip animating as each step is narrated
- Alongside: step-by-step numbered callouts appearing
- Screenshot panels showing: form → toast → feed refresh → new post at top

### On-Screen Text
Data flow strip labels, step numbers (1–7)

### Transition
Flow animation collapses → API response panel

---

## Scene 12 — API Response Format
**Duration:** 7:15 – 7:45 (30 seconds)

### Narration
> "The GET /api/posts response is a JSON array. Each element has: post_id, username, full_name, content, image_url (or null), created_at timestamp, and likes count. JavaScript parses this JSON and builds a post card for each element."

### Visuals
- Left panel: JSON code block (syntax highlighted)
  ```json
  [
    {
      "post_id": 1,
      "username": "alex_r",
      "full_name": "Alex Rao",
      "content": "Hello from SocialConnect!",
      "image_url": null,
      "created_at": "2026-10-12 12:00:00",
      "likes": 3
    }
  ]
  ```
- Right panel: Rendered post card showing how JSON fields map to UI elements
- Animated arrows connecting JSON fields to their UI counterparts

### On-Screen Text
Field names in JSON highlighted; corresponding UI element labels

### Transition
JSON panel fades → testing summary

---

## Scene 13 — Testing and Results
**Duration:** 7:45 – 8:10 (25 seconds)

### Narration
> "SocialConnect runs successfully, connects to PostgreSQL, and all eleven endpoints respond correctly. Post creation, liking, unliking, deleting, commenting, messaging, and searching all work. Duplicate like prevention works at the database level. The frontend dynamically updates after every action."

### Visuals
- Checklist/table of features with green ✅ checkmarks appearing:
  - ✅ Flask app starts
  - ✅ DB connection via psycopg2
  - ✅ GET /api/posts (with JOIN + COUNT)
  - ✅ POST /api/posts (create)
  - ✅ Like / Unlike
  - ✅ Delete post
  - ✅ Comments
  - ✅ Direct messages
  - ✅ User profiles
  - ✅ Search (ILIKE)
  - ✅ Duplicate like prevention

### On-Screen Text
Results checklist

### Transition
Checklist brightens → final scene

---

## Scene 14 — Conclusion and Future Scope
**Duration:** 8:10 – 8:45 (35 seconds)

### Narration
> "SocialConnect demonstrates a complete, database-driven web application built with open-source tools. Full-stack integration, Flask API development, PostgreSQL connectivity, relational data management, SQL operations, and CRUD — all working together. Future enhancements could include authentication, image uploads, a following system, notifications, and pagination. These are future possibilities. The current implementation is a clean, functional demonstration of DBMS concepts. Thank you for watching."

### Visuals
- Summary cards:
  - 🌐 Full-Stack Integration
  - 🐍 Flask API — 11 Endpoints
  - 🐘 PostgreSQL — 5 Tables
  - 🔢 Complex SQL — JOIN, COUNT, ILIKE
  - ✅ All CRUD Operations
- Future scope items (dimmed/greyed, labeled "Future"):
  - Authentication, Image Uploads, Following, Notifications, Pagination
- Final screen: 
  - **SOCIALCONNECT** title
  - *Connecting the Frontend, Backend, and Database*
  - **Thank You**
  - Logos: Python | Flask | PostgreSQL | HTML/CSS/JS

### On-Screen Text
```
SOCIALCONNECT
Connecting the Frontend, Backend, and Database

Thank You
```

### Transition
Fade to black

---

## Storyboard Summary

| # | Scene | Start | Duration | Key Visual |
|---|-------|-------|----------|------------|
| 1 | Opening | 0:00 | 18s | Title animation + floating icons |
| 2 | Problem Statement | 0:18 | 32s | Browser ↔ Database split |
| 3 | Objectives & Features | 0:50 | 40s | Feature cards grid |
| 4 | Technology Stack | 1:30 | 35s | Three-tier stack diagram |
| 5 | Frontend Demo | 2:05 | 50s | UI screenshots with highlights |
| 6 | System Architecture | 2:55 | 37s | Animated flow diagram |
| 7 | Flask Backend | 3:32 | 53s | Code panel with routes |
| 8 | PostgreSQL Schema | 4:25 | 50s | ER diagram + table schemas |
| 9 | DBMS Concepts | 5:15 | 45s | Concept cards |
| 10 | SQL Demo | 6:00 | 38s | Query panel + results |
| 11 | End-to-End Workflow | 6:38 | 37s | Data flow animation |
| 12 | API Response | 7:15 | 30s | JSON ↔ UI mapping |
| 13 | Testing & Results | 7:45 | 25s | Checklist |
| 14 | Conclusion | 8:10 | 35s | Summary + Thank You |
| **Total** | | | **~8:45** | |
