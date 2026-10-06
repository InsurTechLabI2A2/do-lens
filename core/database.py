
import sqlite3
from pathlib import Path
DB_PATH = Path("data/do_lens.db")
def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS apolices (
        id TEXT PRIMARY KEY,
        seguradora TEXT,
        json_data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    return DB_PATH
