import os
import sqlite3

# กำหนดให้ไฟล์ฐานข้อมูลถูกสร้างในโฟลเดอร์ของการทดลองนี้เท่านั้น
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "demo.db")

# เปิดการเชื่อมต่อฐานข้อมูล
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# ลบตารางเก่า (ถ้ามี) เพื่อให้การทดลองเริ่มจากสภาพที่สะอาด
cursor.execute("DROP TABLE IF EXISTS sensor_logs")

# สร้างตารางเพื่อเก็บข้อมูลเซ็นเซอร์
cursor.execute("""
    CREATE TABLE sensor_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        temperature REAL,
        humidity REAL
    )
""")

# ข้อมูลตัวอย่างที่เราจะบันทึก
sample_data = [
    ("demo-device", 25.0, 60.0),
    ("demo-device", 27.5, 58.0),
    ("demo-device", 30.2, 55.0),
]

# เพิ่มข้อมูลหลายแถวลงในตาราง
cursor.executemany(
    "INSERT INTO sensor_logs (device_id, temperature, humidity) VALUES (?, ?, ?)",
    sample_data
)

connection.commit()

# อ่านข้อมูลที่บันทึกไว้ทั้งหมด
rows = cursor.execute("SELECT * FROM sensor_logs").fetchall()
print("ข้อมูลเซ็นเซอร์ที่บันทึกไว้:")
for row in rows:
    print(row)

connection.close()
print(f"ฐานข้อมูลถูกสร้างที่: {DB_NAME}")
