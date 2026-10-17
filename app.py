
import os

import psycopg2
from psycopg2 import errors
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# ================= DATABASE CONNECTION =================

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "social_media_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )

# ================= FRONTEND =================

@app.route("/")
def home():
    return render_template("index.html")


# ================= GET / SEARCH POSTS =================

@app.route("/api/posts", methods=["GET"])
def get_posts():
    search = request.args.get("search", "").strip()

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                p.post_id,
                u.username,
                u.full_name,
                p.content,
                p.image_url,
                p.created_at,
                COUNT(DISTINCT l.like_id) AS likes
            FROM posts p
            JOIN users u ON p.user_id = u.user_id
            LEFT JOIN likes l ON p.post_id = l.post_id
            WHERE p.content ILIKE %s
            GROUP BY
                p.post_id, u.username, u.full_name,
                p.content, p.image_url, p.created_at
            ORDER BY p.created_at DESC;
        """, (f"%{search}%",))

        posts = []
        for row in cur.fetchall():
            posts.append({
                "post_id": row[0],
                "username": row[1],
                "full_name": row[2],
                "content": row[3],
                "image_url": row[4],
                "created_at": str(row[5]),
                "likes": row[6]
            })

        return jsonify(posts)
    finally:
        cur.close()
        conn.close()


# ================= CREATE POST =================

@app.route("/api/posts", methods=["POST"])
def create_post():
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    content = (data.get("content") or "").strip()
    image_url = (data.get("image_url") or "").strip() or None

    if not user_id or not content:
        return jsonify({
            "error": "User ID and content are required"
        }), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO posts (user_id, content, image_url)
            VALUES (%s, %s, %s)
            RETURNING post_id;
        """, (user_id, content, image_url))

        post_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({
            "message": "Post created successfully",
            "post_id": post_id
        }), 201
    except Exception:
        conn.rollback()
        app.logger.exception("Failed to create post")
        return jsonify({"error": "Could not create post"}), 500
    finally:
        cur.close()
        conn.close()


# ================= LIKE POST =================

@app.route("/api/posts/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO likes (post_id, user_id)
            VALUES (%s, %s)
            ON CONFLICT (post_id, user_id) DO NOTHING;
        """, (post_id, user_id))

        conn.commit()
        return jsonify({"message": "Like added or already exists"})
    except Exception:
        conn.rollback()
        app.logger.exception("Failed to like post")
        return jsonify({"error": "Could not like post"}), 500
    finally:
        cur.close()
        conn.close()


# ================= UNLIKE POST =================

@app.route("/api/posts/<int:post_id>/unlike", methods=["POST"])
def unlike_post(post_id):
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            DELETE FROM likes
            WHERE post_id = %s AND user_id = %s;
        """, (post_id, user_id))

        removed = cur.rowcount
        conn.commit()

        return jsonify({
            "message": "Like removed" if removed else "Like not found"
        })
    except Exception:
        conn.rollback()
        app.logger.exception("Failed to unlike post")
        return jsonify({"error": "Could not unlike post"}), 500
    finally:
        cur.close()
        conn.close()


# ================= DELETE POST =================

@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            DELETE FROM posts
            WHERE post_id = %s;
        """, (post_id,))

        deleted = cur.rowcount
        conn.commit()

        if not deleted:
            return jsonify({"error": "Post not found"}), 404

        return jsonify({"message": "Post deleted successfully"})
    except Exception:
        conn.rollback()
        app.logger.exception("Failed to delete post")
        return jsonify({"error": "Could not delete post"}), 500
    finally:
        cur.close()
        conn.close()


# ================= GET USERS =================

@app.route("/api/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT user_id, username, email, full_name, bio
            FROM users
            ORDER BY user_id;
        """)

        users = []
        for row in cur.fetchall():
            users.append({
                "user_id": row[0],
                "username": row[1],
                "email": row[2],
                "full_name": row[3],
                "bio": row[4]
            })

        return jsonify(users)
    finally:
        cur.close()
        conn.close()


# ================= USER PROFILE =================

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user_profile(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                u.user_id,
                u.username,
                u.full_name,
                u.bio,
                COUNT(p.post_id) AS post_count
            FROM users u
            LEFT JOIN posts p ON p.user_id = u.user_id
            WHERE u.user_id = %s
            GROUP BY
                u.user_id, u.username, u.full_name, u.bio;
        """, (user_id,))

        row = cur.fetchone()

        if not row:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "user_id": row[0],
            "username": row[1],
            "full_name": row[2],
            "bio": row[3],
            "post_count": row[4]
        })
    finally:
        cur.close()
        conn.close()


# ================= GET COMMENTS =================

@app.route("/api/posts/<int:post_id>/comments", methods=["GET"])
def get_comments(post_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                c.comment_id,
                c.comment_text,
                c.created_at,
                u.username,
                u.full_name
            FROM comments c
            JOIN users u ON u.user_id = c.user_id
            WHERE c.post_id = %s
            ORDER BY c.created_at ASC;
        """, (post_id,))

        comments = []
        for row in cur.fetchall():
            comments.append({
                "comment_id": row[0],
                "comment_text": row[1],
                "created_at": str(row[2]),
                "username": row[3],
                "full_name": row[4]
            })

        return jsonify(comments)
    finally:
        cur.close()
        conn.close()


# ================= ADD COMMENT =================

@app.route("/api/posts/<int:post_id>/comments", methods=["POST"])
def add_comment(post_id):
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    comment_text = (data.get("comment_text") or "").strip()

    if not user_id or not comment_text:
        return jsonify({
            "error": "User ID and comment are required"
        }), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO comments (post_id, user_id, comment_text)
            VALUES (%s, %s, %s)
            RETURNING comment_id;
        """, (post_id, user_id, comment_text))

        comment_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({
            "message": "Comment added successfully",
            "comment_id": comment_id
        }), 201
    except Exception:
        conn.rollback()
        app.logger.exception("Failed to add comment")
        return jsonify({"error": "Could not add comment"}), 500
    finally:
        cur.close()
        conn.close()


# ================= SEND CHAT MESSAGE =================

@app.route("/api/messages", methods=["POST"])
def send_message():
    data = request.get_json(silent=True) or {}

    sender_id = data.get("sender_id")
    recipient_id = data.get("recipient_id")
    message_text = (data.get("message_text") or "").strip()

    if not sender_id or not recipient_id or not message_text:
        return jsonify({
            "error": "Sender, recipient and message are required"
        }), 400

    if sender_id == recipient_id:
        return jsonify({
            "error": "Choose another user"
        }), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO messages
                (sender_id, recipient_id, message_text)
            VALUES (%s, %s, %s)
            RETURNING message_id, created_at;
        """, (sender_id, recipient_id, message_text))

        row = cur.fetchone()
        conn.commit()

        return jsonify({
            "message": "Message sent",
            "message_id": row[0],
            "created_at": str(row[1])
        }), 201
    except Exception:
        conn.rollback()
        app.logger.exception("Failed to send message")
        return jsonify({"error": "Could not send message"}), 500
    finally:
        cur.close()
        conn.close()


# ================= GET CHAT HISTORY =================

@app.route("/api/messages", methods=["GET"])
def get_messages():
    user1 = request.args.get("user1_id", type=int)
    user2 = request.args.get("user2_id", type=int)

    if not user1 or not user2 or user1 == user2:
        return jsonify({
            "error": "Two different user IDs are required"
        }), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                m.message_id,
                m.sender_id,
                m.recipient_id,
                m.message_text,
                m.created_at,
                u.username
            FROM messages m
            JOIN users u ON u.user_id = m.sender_id
            WHERE
                (m.sender_id = %s AND m.recipient_id = %s)
                OR
                (m.sender_id = %s AND m.recipient_id = %s)
            ORDER BY m.created_at ASC, m.message_id ASC;
        """, (user1, user2, user2, user1))

        messages = []
        for row in cur.fetchall():
            messages.append({
                "message_id": row[0],
                "sender_id": row[1],
                "recipient_id": row[2],
                "message_text": row[3],
                "created_at": str(row[4]),
                "username": row[5]
            })

        return jsonify(messages)
    finally:
        cur.close()
        conn.close()


# ================= RUN APPLICATION =================

if __name__ == "__main__":
    app.run(debug=True)
