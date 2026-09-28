import sqlite3
import datetime

DB_NAME = "pool.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pool_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ph REAL,
            temperature REAL,
            turbidity REAL,
            water_level TEXT,
            pump_fill TEXT,
            pump_dose TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_record(ph, temperature, turbidity, water_level, pump_fill, pump_dose):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO pool_records (timestamp, ph, temperature, turbidity, water_level, pump_fill, pump_dose)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (now, ph, temperature, turbidity, water_level, pump_fill, pump_dose))
    conn.commit()
    conn.close()

def get_latest_record():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, ph, temperature, turbidity, water_level, pump_fill, pump_dose FROM pool_records ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "timestamp": row[1],
            "ph": row[2],
            "temperature": row[3],
            "turbidity": row[4],
            "water_level": row[5],
            "pump_fill": row[6],
            "pump_dose": row[7]
        }
    return None

def get_history_records(limit=10):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, ph, temperature, turbidity, water_level, pump_fill, pump_dose FROM pool_records ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "timestamp": row[1],
            "ph": row[2],
            "temperature": row[3],
            "turbidity": row[4],
            "water_level": row[5],
            "pump_fill": row[6],
            "pump_dose": row[7]
        })
    return result