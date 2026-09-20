import sqlite3
from datetime import datetime

DB_NAME = "iot_data.db"


def get_connection():
    """Create a SQLite database connection."""
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create table if it does not exist."""
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            fan_status TEXT NOT NULL,
            received_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_sensor_reading(device_id, temperature, humidity, fan_status):
    """Save an incoming sensor reading."""
    connection = get_connection()

    connection.execute("""
        INSERT INTO sensor_readings (
            device_id,
            temperature,
            humidity,
            fan_status,
            received_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        device_id,
        temperature,
        humidity,
        fan_status,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_latest_reading():
    """Get the newest sensor reading."""
    connection = get_connection()

    row = connection.execute("""
        SELECT *
        FROM sensor_readings
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()

    connection.close()
    return row


def get_recent_readings(limit=20):
    """Get recent readings for dashboard table."""
    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM sensor_readings
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()

    connection.close()
    return rows