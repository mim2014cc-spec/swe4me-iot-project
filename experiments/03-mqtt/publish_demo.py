import json
import time

import paho.mqtt.client as mqtt

# กำหนด topic ที่ใช้ส่งข้อความ
TOPIC = "demo/team01/test"
BROKER = "broker.hivemq.com"
PORT = 1883

# สร้าง client สำหรับส่งข้อความ
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT, 60)

# ส่งข้อมูล 5 ครั้ง เพื่อให้เห็นว่าข้อความจะถูกส่งไปยัง broker
for i in range(5):
    payload = {
        "device_id": "demo-device",
        "value": i,
        "status": "ok"
    }
    message = json.dumps(payload)  # แปลงข้อมูลเป็นข้อความ JSON
    client.publish(TOPIC, message)
    print(f"ส่งข้อความแล้ว: {message}")
    time.sleep(2)

client.disconnect()
