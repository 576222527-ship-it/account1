import sqlite3
from contextlib import closing
from datetime import datetime

DB_FILE = 'account.db'

def init_db() -> None:
    """建表（若不存在）"""
    with closing(sqlite3.connect(DB_FILE)) as conn, closing(conn.cursor()) as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS record(
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                amount  REAL    NOT NULL,
                note    TEXT    NOT NULL,
                date    TEXT    NOT NULL
            )
        ''')
        conn.commit()

def add_record(amount: float, note: str) -> None:
    init_db()
    with closing(sqlite3.connect(DB_FILE)) as conn, closing(conn.cursor()) as cur:
        cur.execute('INSERT INTO record(amount, note, date) VALUES (?,?,?)',
                    (amount, note, datetime.now().isoformat(timespec='minutes')))
        conn.commit()

def list_records() -> list[dict]:
    init_db()
    with closing(sqlite3.connect(DB_FILE)) as conn, closing(conn.cursor()) as cur:
        cur.execute('SELECT id, amount, note, date FROM record ORDER BY id DESC')
        rows = cur.fetchall()
    return [{'id': r[0], 'amount': r[1], 'note': r[2], 'date': r[3]} for r in rows]

def month_stats(month: str) -> dict:          # month = '2025-11'
    init_db()
    with closing(sqlite3.connect(DB_FILE)) as conn, closing(conn.cursor()) as cur:
        cur.execute("SELECT SUM(amount) FROM record WHERE date LIKE ?", (month + '%',))
        total = cur.fetchone()[0] or 0.0
        cur.execute("SELECT amount, note, date FROM record WHERE date LIKE ? ORDER BY id DESC", (month + '%',))
        detail = [{'amount': r[0], 'note': r[1], 'date': r[2]} for r in cur.fetchall()]
    return {'total': total, 'detail': detail}

def delete_record(rid: int) -> bool:
    init_db()
    with closing(sqlite3.connect(DB_FILE)) as conn, closing(conn.cursor()) as cur:
        cur.execute('DELETE FROM record WHERE id=?', (rid,))
        conn.commit()
        return cur.rowcount > 0