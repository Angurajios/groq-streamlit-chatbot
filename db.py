import sqlite3

DB_NAME = "chat.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            title TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    conn.close()



def create_conversation(conv_id, username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO conversations (id, username) VALUES (?, ?)",
        (conv_id, username),
    )
    conn.commit()
    conn.close()



def get_conversations(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title FROM conversations WHERE username = ? ORDER BY created_at",
        (username,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_messages(conv_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id",
        (conv_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [{"role": role, "content": content} for role, content in rows]


def update_title(conv_id, title):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE conversations SET title = ? WHERE id = ?",
        (title, conv_id),
    )
    conn.commit()
    conn.close()


def add_message(conv_id, role, content):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
        (conv_id, role, content),
    )
    conn.commit()
    conn.close()


def delete_conversation(conv_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
    cur.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
    conn.commit()
    conn.close()