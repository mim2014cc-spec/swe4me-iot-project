import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "mechatronics/2026/sectionA/TEAM_Jitti/telemetry"

def on_connect(client, userdata, flags, rc, properties=None):
    print("เชื่อมต่อ MQTT Broker สำเร็จ!")
    print(f"กำลังรอรับข้อมูลจาก Topic: {TOPIC}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print("\n--- ได้รับข้อมูลเซนเซอร์จาก Wokwi! ---")
    print(f"Topic: {msg.topic}")
    print(f"Data: {msg.payload.decode('utf-8')}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print("กำลังเชื่อมต่อไปยัง Broker...")
client.connect(BROKER, PORT, 60)
client.loop_forever()
