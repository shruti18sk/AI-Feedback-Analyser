import sqlite3
import json
from datetime import datetime

conn=sqlite3.connect('feedback.db')
cursor=conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedbacktable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        review_text TEXT NOT NULL,
        sentiment TEXT NOT NULL,
        score INTEGER NOT NULL,
        theme TEXT NOT NULL,
        confidence INTEGER NOT NULL,
        status TEXT NOT NULL,
        insight TEXT NOT NULL,
        keywords TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
""")

conn.commit()
conn.close()

def save_analysis(review_text, analysis):
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedbacktable
        (review_text, sentiment, score, theme, confidence, status, insight, keywords, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        review_text,
        analysis["sentiment"],
        analysis["score"],
        analysis["theme"],
        analysis["confidence"],
        analysis["status"],
        analysis["insight"],
        json.dumps(analysis["keywords"]),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

def get_recent_analyses(limit=5):
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM feedbacktable
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    records = cursor.fetchall()

    conn.close()

    return records
