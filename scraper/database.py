import sqlite3
from datetime import datetime

DB_NAME = "news_data.db"

def create_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            source TEXT,
            label TEXT,
            timestamp TEXT,
            UNIQUE(title, source) ON CONFLICT IGNORE
        )
    """)
    conn.commit()
    conn.close()

def insert_news(news_list):
    conn = create_connection()
    c = conn.cursor()
    for news in news_list:
        c.execute("""
            INSERT OR IGNORE INTO news (title, content, source, label, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            news.get("title", ""),
            news.get("content", "") or news.get("summary", ""),  # support 'content' or 'summary'
            news.get("source", "") or news.get("link", ""),
            news.get("label", ""),
            datetime.now().isoformat()
        ))
    conn.commit()
    conn.close()

def fetch_all_news():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT title, content, source, label, timestamp FROM news ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows
