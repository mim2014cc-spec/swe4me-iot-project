import paho.mqtt.client as mqtt

# กำหนด topic ที่ต้องการฟังข้อความ
TOPIC = "demo/team01/test"
BROKER = "broker.hivemq.com"
PORT = 1883


def on_connect(client, userdata, flags, reason_code, properties):
    # เมื่อเชื่อมต่อกับ broker สำเร็จ ให้สมัครสมาชิกเพื่อฟัง topic นี้
    print("เชื่อมต่อกับ MQTT broker สำเร็จ")
    client.subscribe(TOPIC)
    print(f"กำลังติดตาม topic: {TOPIC}")


def on_message(client, userdata, message):
    # เมื่อมีข้อความเข้ามา ให้แสดงข้อความที่ได้รับ
    print(f"ได้รับข้อความจาก {message.topic}: {message.payload.decode('utf-8')}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_forever()
