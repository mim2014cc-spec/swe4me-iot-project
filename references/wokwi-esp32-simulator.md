# Wokwi ESP32 Simulator Guide

โปรเจคนี้อ้างอิงจากเทมเพลตของ Uri Shaked: https://wokwi.com/projects/322577683855704658

นักศึกษาสามารถทำสำเนาโปรเจคด้านล่างนี้แล้วปรับค่าให้เหมาะกับกลุ่มของตนเอง:
https://wokwi.com/projects/475687629828433921

> หมายเหตุ: เอกสารนี้เน้นเรื่องการใช้งาน Wokwi เป็นหลัก สำหรับภาพรวมทั้งระบบ โปรดดูที่ [instruction.md](instruction.md)

---

## 1. Wokwi คืออะไร

Wokwi คือแพลตฟอร์มจำลองอุปกรณ์อิเล็กทรอนิกส์บนเว็บที่ช่วยให้ผู้ใช้สามารถสร้างวงจรและรันโค้ดบนไมโครคอนโทรลเลอร์ได้ทันที โดยไม่ต้องใช้ hardware จริง

สำหรับโปรเจคนี้ Wokwi ใช้เพื่อจำลอง:

- ESP32 DevKit
- DHT22 Sensor
- LED เป็นตัวแทนพัดลม
- การเชื่อมต่อ Wi-Fi และ MQTT

Wokwi เหมาะสำหรับการเรียนรู้ IoT เพราะช่วยให้เห็นการทำงานของวงจรและซอฟต์แวร์พร้อมกันได้อย่างรวดเร็ว

---

## 2. ทำไมต้องใช้ Wokwi

Wokwi มีประโยชน์สำหรับการเรียนรู้เรื่อง IoT ดังนี้:

- ไม่ต้องมี hardware จริงติดตั้งบนเครื่อง
- สามารถรันและทดสอบโค้ดได้ทันทีบนเว็บ
- เห็นการทำงานของเซนเซอร์และ actuator แบบ real-time
- เหมาะสำหรับการเรียนรู้และทดลองแบบง่าย ๆ ก่อนใช้งานจริง
- ช่วยลดค่าใช้จ่ายและเวลาในการตั้งค่าอุปกรณ์

---

## 3. ส่วนประกอบของโปรเจคบน Wokwi

ในสภาพแวดล้อมจำลองนี้ประกอบด้วย:

- ESP32: ตัวประมวลผลหลัก
- DHT22: เซนเซอร์วัดอุณหภูมิและความชื้น
- LED: ใช้แทนพัดลมหรือสถานะการทำงาน
- Resistor 220Ω: ป้องกันกระแสเกินสำหรับ LED
- Serial Monitor: ใช้ดูผลลัพธ์และ error จากเครื่อง

---

## 4. การตั้งค่าไฟล์ Wokwi

โปรเจคนี้มี 2 ส่วนสำคัญที่ต้องทำงานร่วมกัน:

1. `main.py` สำหรับโค้ด ESP32
2. `diagram.json` สำหรับการวางวงจรและการเชื่อมต่อบน Wokwi

### 4.1 หน้า Wokwi ที่ใช้

นักเรียนสามารถ:

- เปิด Wokwi ในเบราว์เซอร์
- สร้าง project ใหม่
- เพิ่ม ESP32, DHT22, LED และ resistor
- กำหนด pin wiring ตาม diagram
- อัปโหลดไฟล์ `main.py`
- กด Start Simulation เพื่อทดสอบการทำงาน

---

## 5. Source code ของ ESP32 (main.py)

```py
# main.py

import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

# ==========================================
# Wi-Fi settings for Wokwi
# ==========================================
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# ==========================================
# MQTT Broker settings
# ==========================================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

# เปลี่ยนชื่อทีมให้ไม่ซ้ำกับกลุ่มอื่น
TEAM_ID = "team01"
DEVICE_ID = "esp32-" + TEAM_ID

MQTT_CLIENT_ID = "wokwi-" + DEVICE_ID

# ต้องแก้ team01 ให้ตรงกับ TEAM_ID ของกลุ่ม
TELEMETRY_TOPIC = b"mechatronics/2026/sectionA/team01/telemetry"
CONTROL_TOPIC = b"mechatronics/2026/sectionA/team01/control/fan"
STATUS_TOPIC = b"mechatronics/2026/sectionA/team01/status"

# ==========================================
# Hardware pins
# ==========================================
DHT_PIN = 15
LED_PIN = 2

sensor = dht.DHT22(Pin(DHT_PIN))
fan_led = Pin(LED_PIN, Pin.OUT)

fan_led.off()


def connect_wifi():
    """Connect ESP32 to Wokwi virtual Wi-Fi."""
    print("Connecting to WiFi", end="")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        while not wlan.isconnected():
            print(".", end="")
            time.sleep(0.1)

    print(" Connected!")
    print("IP address:", wlan.ifconfig()[0])


def mqtt_callback(topic, message):
    """Handle MQTT control messages from Python server."""
    print("Received MQTT message")
    print("Topic:", topic)
    print("Message:", message)

    if topic == CONTROL_TOPIC:
        if message == b"ON":
            fan_led.on()
            print("Fan simulation: ON")

        elif message == b"OFF":
            fan_led.off()
            print("Fan simulation: OFF")


def connect_mqtt():
    """Connect to HiveMQ broker and subscribe to control topic."""
    print("Connecting to MQTT broker...", end=" ")

    client = MQTTClient(
        client_id=MQTT_CLIENT_ID,
        server=MQTT_BROKER,
        port=MQTT_PORT,
        keepalive=60
    )

    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(CONTROL_TOPIC)

    status_message = ujson.dumps({
        "device_id": DEVICE_ID,
        "status": "online"
    })

    client.publish(STATUS_TOPIC, status_message)

    print("Connected!")
    print("Subscribed to:", CONTROL_TOPIC)

    return client


def publish_telemetry(client):
    """Read DHT22 and publish JSON telemetry."""
    sensor.measure()

    temperature = sensor.temperature()
    humidity = sensor.humidity()

    payload = {
        "device_id": DEVICE_ID,
        "temperature": temperature,
        "humidity": humidity
    }

    message = ujson.dumps(payload)

    client.publish(TELEMETRY_TOPIC, message)

    print("Published to:", TELEMETRY_TOPIC)
    print("Data:", message)


connect_wifi()
mqtt_client = connect_mqtt()

last_publish_time = time.ticks_ms()
PUBLISH_INTERVAL_MS = 5000

while True:
    try:
        # รับคำสั่ง ON/OFF จาก Python server
        mqtt_client.check_msg()

        # ส่งข้อมูลทุก 5 วินาที
        if time.ticks_diff(time.ticks_ms(), last_publish_time) >= PUBLISH_INTERVAL_MS:
            publish_telemetry(mqtt_client)
            last_publish_time = time.ticks_ms()

        time.sleep_ms(100)

    except Exception as error:
        print("Connection error:", error)
        print("Reconnecting in 2 seconds...")
        time.sleep(2)

        try:
            mqtt_client.disconnect()
        except:
            pass

        connect_wifi()
        mqtt_client = connect_mqtt()
```

### อธิบายโค้ดหลัก

- `connect_wifi()`: ต่อ ESP32 เข้าสู่เครือข่าย Wi‑Fi ของ Wokwi
- `connect_mqtt()`: เชื่อมต่อกับ MQTT Broker และสมัครสมาชิกรับคำสั่งควบคุม
- `mqtt_callback()`: รอรับคำสั่ง เช่น ON / OFF จาก server
- `publish_telemetry()`: อ่านค่าจาก DHT22 แล้วส่งข้อมูล JSON ไปยัง MQTT Topic
- `while True`: ทำงานวนลูปตลอดเวลาเพื่ออ่านข้อความและส่งข้อมูลทุก 5 วินาที

---

## 6. การเชื่อมต่อวงจรใน Wokwi

### 6.1 รายละเอียดการต่อพิน

| อุปกรณ์ | ขา | ต่อกับ ESP32 |
|---|---|---|
| DHT22 | VCC | 3V3 |
| DHT22 | GND | GND |
| DHT22 | SDA | GPIO 15 |
| LED | Anode ผ่าน resistor 220Ω | GPIO 2 |
| LED | Cathode | GND |

### 6.2 ความหมายของการต่อพิน

- `GPIO 15` ใช้สำหรับ DHT22
- `GPIO 2` ใช้สำหรับ LED ที่ทำหน้าที่เป็นพัดลมจำลอง
- `3V3` / `GND` ใช้จ่ายไฟให้กับเซนเซอร์และ LED

---

## 7. Source code ของวงจรใน Wokwi (`diagram.json`)

```json
// diagram.json

{
  "version": 1,
  "author": "IoT Mechatronics Course",
  "editor": "wokwi",
  "parts": [
    {
      "type": "board-esp32-devkit-c-v4",
      "id": "esp32",
      "top": 86.4,
      "left": 148.84,
      "attrs": {}
    },
    {
      "type": "wokwi-dht22",
      "id": "dht1",
      "top": 125.1,
      "left": 42.6,
      "attrs": {}
    },
    {
      "type": "wokwi-resistor",
      "id": "r1",
      "top": 205,
      "left": 239.15,
      "rotate": 270,
      "attrs": {
        "value": "220"
      }
    },
    {
      "type": "wokwi-led",
      "id": "led1",
      "top": 121.2,
      "left": 282.6,
      "attrs": {
        "color": "red",
        "flip": "1"
      }
    }
  ],
  "connections": [
    [ "esp32:TX", "$serialMonitor:RX", "", [] ],
    [ "esp32:RX", "$serialMonitor:TX", "", [] ],

    [ "esp32:3V3", "dht1:VCC", "red", [ "h-124.65", "v134.4" ] ],
    [ "esp32:GND.1", "dht1:GND", "black", [ "h-38.25", "v19.2", "h-76.8" ] ],
    [ "esp32:15", "dht1:SDA", "green", [ "h28.8", "v48", "h-230.5" ] ],

    [ "esp32:2", "r1:1", "green", [] ],
    [ "r1:2", "led1:A", "green", [] ],
    [ "esp32:GND.1", "led1:C", "black", [ "h-38.25", "v96", "h192", "v-172.8" ] ]
  ],
  "dependencies": {},
  "serialMonitor": {
    "display": "always",
    "collapse": false,
    "newline": "lf"
  }
}
```

### อธิบายวงจร

- ESP32: เป็นไมโครคอนโทรลเลอร์หลัก
- DHT22: เซนเซอร์วัดอุณหภูมิและความชื้น
- LED: ใช้แทนพัดลมหรือการแสดงสถานะ
- Resistor 220 Ω: ป้องกันกระแสเกินใน LED

การเชื่อมต่อที่สำคัญ:

- `GPIO 15` เชื่อมไปยัง `DHT22 SDA`
- `GPIO 2` เชื่อมไปยัง LED ผ่านตัวต้านทาน
- `3V3` และ `GND` ให้พลังงานแก่เซนเซอร์และ LED

---

## 8. สิ่งที่นักศึกษาได้เรียนรู้จากการทำ Wokwi

- เข้าใจการทำงานของ ESP32 ในสภาพแวดล้อมจำลอง
- เรียนรู้การต่อวงจรเบื้องต้นสำหรับเซนเซอร์และ actuator
- เข้าใจการอ่านค่า DHT22 และแปลงเป็นข้อมูลตัวเลข
- เรียนรู้วิธีส่งข้อมูล MQTT จากอุปกรณ์ไปยัง broker
- เข้าใจการรับคำสั่งควบคุมกลับมายังอุปกรณ์
- ฝึกการตรวจสอบผลลัพธ์ด้วย Serial Monitor

---

## 9. ข้อแนะนำสำหรับนักศึกษา

- เปลี่ยน `TEAM_ID` ให้เป็นชื่อกลุ่มหรือเลขกลุ่มของตนเอง
- ใช้ Topic ที่ไม่ซ้ำกันกับกลุ่มอื่นเพื่อหลีกเลี่ยงข้อมูลรบกวน
- ตรวจสอบ Serial Monitor ทุกครั้งก่อนทำการทดสอบต่อเนื่อง
- ทดสอบการ reconnect เมื่อ Wi‑Fi หรือ MQTT หลุด
- ทดลองปรับค่าเกณฑ์อุณหภูมิ เช่น จาก 30°C เป็น 28°C หรือ 35°C

---

## 10. สรุป

เอกสารนี้เน้นไปที่การใช้งาน Wokwi เป็นหลัก เพื่อให้ผู้เรียนได้ฝึกสร้างโปรเจค IoT จำลองบน ESP32 อย่างมีประสิทธิภาพ ก่อนจะต่อยอดไปสู่การเชื่อมต่อกับ Python Server, MQTT Broker, SQLite และ Dashboard ตามที่ระบุใน [instruction.md](instruction.md)

Wokwi จึงเป็นจุดเริ่มต้นที่ดีสำหรับการเรียนรู้ IoT เพราะช่วยให้เห็นการทำงานของอุปกรณ์จริงแบบไม่ต้องมี hardware จริงติดตั้งในเครื่อง
