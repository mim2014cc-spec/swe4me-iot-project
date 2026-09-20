# เอกสารประกอบการสอน

IoT Mechatronics: ESP32, MQTT, Python Server, Database และ Web Dashboard

Smart Greenhouse Monitoring and Fan Control Simulation

---

## 1. ภาพรวมโครงงาน

ในกิจกรรมนี้ นักเรียนจะพัฒนาระบบ IoT จำลองสำหรับตรวจวัดอุณหภูมิและความชื้น พร้อมระบบควบคุมพัดลมอัตโนมัติ โดยใช้อุปกรณ์จำลองบน Wokwi และเชื่อมต่อระบบผ่าน MQTT

อุปกรณ์ ESP32 จะอ่านค่าจาก DHT22 ส่งข้อมูลไปยัง MQTT Broker จากนั้น Python server จะรับข้อมูล บันทึกลงฐานข้อมูล และตัดสินใจสั่งเปิดหรือปิดพัดลมจำลองผ่าน LED

```text
+-----------------------------+
| Wokwi Simulation            |
| ESP32 + DHT22 + LED         |
+-----------------------------+
              |
              | MQTT Publish: telemetry
              v
+-----------------------------+
| HiveMQ Public MQTT Broker   |
| broker.hivemq.com           |
+-----------------------------+
              |
              | MQTT Subscribe
              v
+-----------------------------+
| Python Application Server   |
| Flask + Paho MQTT           |
+-----------------------------+
       |                 |
       | Save data       | Publish ON/OFF command
       v                 v
+-------------+    +----------------------+
| SQLite DB   |    | ESP32 LED / Fan      |
+-------------+    +----------------------+
       |
       v
+-----------------------------+
| Flask Web Dashboard         |
| Share through ngrok         |
+-----------------------------+
```

---

## 2. ผลลัพธ์การเรียนรู้

เมื่อจบกิจกรรม นักเรียนสามารถ:

- อธิบายแนวคิดของ Internet of Things (IoT) ได้
- อธิบายบทบาทของ MQTT Broker, Publisher และ Subscriber ได้
- สร้างวงจรจำลอง ESP32, DHT22 และ LED บน Wokwi ได้
- เขียนโปรแกรม MicroPython เพื่อเชื่อมต่อ Wi-Fi และส่งข้อมูล MQTT ได้
- ส่งข้อมูลเซนเซอร์ในรูปแบบ JSON ได้
- เขียน Python server เพื่อรับ MQTT message ได้
- บันทึกข้อมูลลง SQLite database ได้
- สร้าง Web Dashboard เพื่อแสดงข้อมูลจากเซนเซอร์ได้
- อธิบายแนวคิด Three-Tier Architecture จากระบบที่พัฒนาได้
- สร้างระบบควบคุมแบบวงรอบปิด (Closed-loop Control) เบื้องต้นได้

---

## 3. แนวคิดสำคัญ

### 3.1 MQTT คืออะไร

MQTT เป็นรูปแบบการสื่อสารที่เหมาะกับงาน IoT โดยใช้งานแบบ Publish/Subscribe

- **Publisher:** อุปกรณ์ที่ส่งข้อความ เช่น ESP32
- **Subscriber:** โปรแกรมที่รับข้อความ เช่น Python server
- **Broker:** ตัวกลางรับและกระจายข้อความ เช่น HiveMQ
- **Topic:** ชื่อช่องทางของข้อความ MQTT

ตัวอย่างการไหลของข้อมูล:

```text
ESP32 Publish → Topic: mechatronics/2026/team01/telemetry
Python Server Subscribe → Topic: mechatronics/2026/team01/telemetry
```

### 3.2 Three-Tier Architecture

ระบบนี้แบ่งออกเป็น 3 ชั้นดังนี้

| Tier | หน้าที่ | เทคโนโลยีที่ใช้ |
|---|---|---|
| Presentation Tier | แสดงผลข้อมูลให้ผู้ใช้ผ่านหน้าเว็บ | HTML, CSS, Flask Template |
| Application Tier | รับข้อมูล MQTT, ตรวจสอบข้อมูล, ตัดสินใจควบคุมอุปกรณ์ | Python, Flask, Paho MQTT |
| Data Tier | จัดเก็บประวัติข้อมูลเซนเซอร์ | SQLite |

> หมายเหตุ: ESP32 และ MQTT Broker เป็นส่วนของอุปกรณ์และการสื่อสาร IoT ที่ป้อนข้อมูลเข้าสู่ Application Tier

---

## 4. เครื่องมือที่ใช้

| เครื่องมือ | หน้าที่ |
|---|---|
| Wokwi | จำลองวงจรและ ESP32 ผ่านเว็บ |
| ESP32 | อุปกรณ์ IoT จำลอง |
| MicroPython | ภาษาโปรแกรมบน ESP32 |
| DHT22 | เซนเซอร์วัดอุณหภูมิและความชื้น |
| LED | จำลองพัดลมหรือระบบระบายอากาศ |
| HiveMQ Public Broker | MQTT Broker สำหรับรับส่งข้อความ |
| Python | พัฒนา application server |
| Flask | สร้าง web application และ dashboard |
| Paho MQTT | ให้ Python เชื่อมต่อ MQTT Broker |
| SQLite | ฐานข้อมูลสำหรับเก็บข้อมูลเซนเซอร์ |
| ngrok | แชร์ Flask dashboard จากเครื่องไปยังอินเทอร์เน็ต |

---

## 5. รูปแบบการจัดการเรียนรู้

กิจกรรมแบ่งเป็น 2 ช่วงหลัก

| ช่วง | รูปแบบ | เป้าหมาย |
|---|---|---|
| ช่วงที่ 1 | ผู้สอนสาธิตและนักเรียนทำตาม | ทุกคนตั้งค่าโปรเจกต์พื้นฐานและเห็นข้อมูลวิ่งครบระบบ |
| ช่วงที่ 2 | นักเรียนทำใบงานเป็นกลุ่ม | พัฒนาระบบให้สมบูรณ์ตามเงื่อนไขที่กำหนด |

---

# ส่วนที่ 1: สาธิตและทำตามร่วมกัน

## 6. ขั้นนำเข้าสู่บทเรียน

### 6.1 คำถามนำ

ผู้สอนตั้งคำถามเพื่อเชื่อมโยงกับงานเมคคาทรอนิกส์

- หากเซนเซอร์อยู่ในโรงเรือน แต่อยากดูข้อมูลจากห้องควบคุม ต้องทำอย่างไร?
- หากอุณหภูมิสูงเกินกำหนด ระบบควรตอบสนองอย่างไร?
- ถ้ามีอุปกรณ์หลายตัวส่งข้อมูลเข้ามาพร้อมกัน จะจัดการข้อมูลอย่างไร?
- เหตุใดระบบ IoT จึงนิยมใช้ MQTT แทนการส่งข้อมูลโดยตรงระหว่างอุปกรณ์กับ server?

### 6.2 อธิบายภาพรวมระบบ

ผู้สอนอธิบายเส้นทางข้อมูลดังนี้

```text
1. DHT22 วัดอุณหภูมิและความชื้น
2. ESP32 อ่านค่าจาก DHT22
3. ESP32 ส่ง JSON ผ่าน MQTT ไปยัง Broker
4. Python server รับข้อมูลจาก Broker
5. Python server บันทึกข้อมูลลง SQLite
6. Dashboard แสดงข้อมูลล่าสุด
7. หากอุณหภูมิสูง Python server ส่งคำสั่ง ON กลับไปยัง ESP32
8. ESP32 เปิด LED เพื่อจำลองพัดลม
```

---

## 7. การสาธิตที่ 1: สร้างวงจร ESP32 บน Wokwi

### 7.1 อุปกรณ์จำลอง

- ESP32 DevKit V1
- DHT22
- LED
- Resistor 220Ω

### 7.2 การเชื่อมต่อวงจร

| อุปกรณ์ | ขาอุปกรณ์ | ขา ESP32 |
|---|---|---|
| DHT22 | VCC | 3V3 |
| DHT22 | GND | GND |
| DHT22 | SDA | GPIO 15 |
| LED | Anode ผ่านตัวต้านทาน 220Ω | GPIO 2 |
| LED | Cathode | GND |

### 7.3 ผลลัพธ์ที่คาดหวัง

- นักเรียนมี Wokwi project ของตนเอง
- DHT22 เชื่อมต่อกับ GPIO 15
- LED เชื่อมต่อกับ GPIO 2
- สามารถเริ่ม Simulation ได้

---

## 8. การสาธิตที่ 2: เชื่อมต่อ Wi-Fi และ MQTT ด้วย MicroPython

Wokwi รองรับการจำลอง Wi-Fi สำหรับ ESP32 โดยใช้ชื่อเครือข่าย `Wokwi-GUEST` และรหัสผ่านว่าง รวมถึงมีตัวอย่าง MQTT Weather Logger สำหรับ MicroPython ESP32 ให้ศึกษาได้  
อ้างอิง: [Wokwi ESP32 WiFi Documentation](https://docs.wokwi.com/guides/esp32-wifi) และ [MicroPython MQTT Weather Logger](https://wokwi.com/projects/322577683855704658)

### 8.1 กำหนด MQTT Topic

ทุกกลุ่มต้องใช้ topic ที่ไม่ซ้ำกัน เพราะใช้ public broker ร่วมกับผู้อื่น

```text
mechatronics/2026/sectionA/team01/telemetry
mechatronics/2026/sectionA/team01/control/fan
mechatronics/2026/sectionA/team01/status
```

> ให้เปลี่ยน `team01` เป็นหมายเลขกลุ่มของตนเอง

### 8.2 โค้ด `main.py` สำหรับ ESP32

```python
import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

# Wi-Fi settings for Wokwi
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# MQTT settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

# Change TEAM_ID for each group
TEAM_ID = "team01"
DEVICE_ID = "esp32-" + TEAM_ID

MQTT_CLIENT_ID = "wokwi-" + DEVICE_ID
TELEMETRY_TOPIC = b"mechatronics/2026/sectionA/team01/telemetry"
CONTROL_TOPIC = b"mechatronics/2026/sectionA/team01/control/fan"
STATUS_TOPIC = b"mechatronics/2026/sectionA/team01/status"

# Hardware pins
DHT_PIN = 15
LED_PIN = 2

sensor = dht.DHT22(Pin(DHT_PIN))
fan_led = Pin(LED_PIN, Pin.OUT)

def connect_wifi():
    print("Connecting to WiFi", end="")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.1)

    print(" Connected!")
    print("IP address:", wlan.ifconfig()[0])

def mqtt_callback(topic, message):
    print("Received:", topic, message)

    if topic == CONTROL_TOPIC:
        if message == b"ON":
            fan_led.on()
            print("Fan: ON")

        elif message == b"OFF":
            fan_led.off()
            print("Fan: OFF")

def connect_mqtt():
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
    return client

def publish_telemetry(client):
    sensor.measure()

    payload = {
        "device_id": DEVICE_ID,
        "temperature": sensor.temperature(),
        "humidity": sensor.humidity()
    }

    message = ujson.dumps(payload)

    client.publish(TELEMETRY_TOPIC, message)

    print("Published:", message)

connect_wifi()
mqtt_client = connect_mqtt()

last_publish_time = time.ticks_ms()

while True:
    try:
        # Check MQTT control messages
        mqtt_client.check_msg()

        # Publish sensor data every 5 seconds
        if time.ticks_diff(time.ticks_ms(), last_publish_time) >= 5000:
            publish_telemetry(mqtt_client)
            last_publish_time = time.ticks_ms()

        time.sleep_ms(100)

    except Exception as error:
        print("Error:", error)
        time.sleep(2)

        try:
            mqtt_client.disconnect()
        except:
            pass

        mqtt_client = connect_mqtt()
```

### 8.3 รูปแบบข้อมูล JSON

ESP32 จะส่งข้อมูลลักษณะนี้ทุก 5 วินาที

```json
{
  "device_id": "esp32-team01",
  "temperature": 27,
  "humidity": 65
}
```

---

## 9. การสาธิตที่ 3: ตรวจสอบ MQTT Message

ให้นักเรียนเปิด HiveMQ WebSocket Client เพื่อดูข้อความจาก ESP32

1. เปิด [HiveMQ WebSocket Client](https://www.hivemq.com/demos/websocket-client/)
2. กดปุ่ม `Connect`
3. เพิ่ม Topic Subscription
4. กรอก topic ของกลุ่ม เช่น:

```text
mechatronics/2026/sectionA/team01/telemetry
```

5. เริ่ม Wokwi Simulation
6. คลิก DHT22 และปรับค่าอุณหภูมิหรือความชื้น
7. ตรวจสอบว่า JSON message แสดงใน MQTT client

> HiveMQ Public Broker เป็น broker แบบสาธารณะและใช้ร่วมกัน เหมาะสำหรับการทดสอบระยะสั้น ไม่ควรส่งข้อมูลส่วนบุคคล รหัสผ่าน หรือข้อมูลสำคัญ  
> อ้างอิง: [HiveMQ Public Broker](https://www.hivemq.com/mqtt/public-mqtt-broker/)

---

## 10. การสาธิตที่ 4: Python Server รับข้อมูล MQTT และบันทึกฐานข้อมูล

### 10.1 ติดตั้งไลบรารี

```bash
pip install flask paho-mqtt
```

### 10.2 โครงสร้างโปรเจกต์

```text
iot-mechatronics-project/
├── app.py
├── database.py
├── iot_data.db
└── templates/
    └── index.html
```

### 10.3 หน้าที่ของแต่ละไฟล์

| ไฟล์ | หน้าที่ |
|---|---|
| `app.py` | Flask server, MQTT subscriber และ logic ควบคุม |
| `database.py` | สร้างฐานข้อมูลและบันทึก/อ่านข้อมูล |
| `iot_data.db` | SQLite database |
| `templates/index.html` | หน้า dashboard |

### 10.4 หลักการทำงานของ Python Server

```text
Receive MQTT message
        |
        v
Validate JSON data
        |
        v
Save sensor data to SQLite
        |
        v
Check temperature threshold
        |
        +-- Temperature >= 30°C --> Publish "ON"
        |
        +-- Temperature < 30°C  --> Publish "OFF"
```

---

## 11. การสาธิตที่ 5: Dashboard และ ngrok

ผู้สอนสาธิตการเปิด Flask server

```bash
python app.py
```

จากนั้นเปิด ngrok เพื่อเผยแพร่ dashboard ที่ทำงานในเครื่องผ่าน HTTP tunnel

```bash
ngrok http 5000
```

ngrok จะสร้าง public URL สำหรับเปิดหน้า dashboard จากอุปกรณ์อื่นได้  
อ้างอิง: [ngrok HTTP Endpoints Documentation](https://ngrok.com/docs/universal-gateway/http)

> ngrok ใช้แชร์หน้าเว็บ Flask dashboard เท่านั้น ไม่ได้ใช้เป็นเส้นทางรับส่ง MQTT ระหว่าง ESP32 กับ HiveMQ Broker

---

# ส่วนที่ 2: ใบงานฝึกปฏิบัติ

## 12. ใบงาน: Smart Greenhouse IoT Monitoring and Control

### 12.1 วัตถุประสงค์

พัฒนาระบบ IoT จำลองที่สามารถ:

- อ่านอุณหภูมิและความชื้นจาก DHT22 บน Wokwi
- ส่งข้อมูลผ่าน MQTT ไปยัง `broker.hivemq.com`
- รับข้อมูลด้วย Python server
- บันทึกข้อมูลลง SQLite
- แสดงผลบน Web Dashboard
- ควบคุม LED จำลองพัดลมตามค่าอุณหภูมิ

### 12.2 การทำงานเป็นกลุ่ม

**จำนวนสมาชิก:** 2–3 คนต่อกลุ่ม

| บทบาท | หน้าที่ |
|---|---|
| IoT Developer | สร้าง Wokwi circuit และเขียน MicroPython บน ESP32 |
| Backend Developer | พัฒนา Python, MQTT subscriber และ SQLite database |
| Web/Tester | พัฒนา dashboard, ทดสอบระบบ และจัดทำรายงาน |

> สมาชิกทุกคนต้องสามารถอธิบายภาพรวมระบบและทดลองรันระบบได้

---

## 13. งานที่ต้องทำ

### งานที่ 1: สร้าง Wokwi ESP32 Simulation

- [ ] สร้าง Wokwi project ด้วย ESP32
- [ ] เพิ่ม DHT22
- [ ] เพิ่ม LED และ resistor
- [ ] เชื่อมต่อ DHT22 ที่ GPIO 15
- [ ] เชื่อมต่อ LED ที่ GPIO 2
- [ ] ทดสอบอ่านค่า DHT22 ผ่าน Serial Monitor
- [ ] ทดสอบเปิดและปิด LED

### งานที่ 2: ส่งข้อมูล MQTT

- [ ] กำหนด MQTT topic เฉพาะกลุ่ม
- [ ] เชื่อมต่อ ESP32 กับ Wi-Fi `Wokwi-GUEST`
- [ ] เชื่อมต่อ ESP32 กับ `broker.hivemq.com`
- [ ] Publish ข้อมูล telemetry ทุก 5 วินาที
- [ ] ส่งข้อมูลในรูปแบบ JSON
- [ ] ทดสอบดูข้อความผ่าน HiveMQ WebSocket Client

### งานที่ 3: สร้าง Python MQTT Server

- [ ] ติดตั้ง Flask และ Paho MQTT
- [ ] สร้าง MQTT client บน Python
- [ ] Subscribe telemetry topic ของกลุ่ม
- [ ] ตรวจสอบว่า JSON มี `device_id`, `temperature` และ `humidity`
- [ ] แสดงข้อมูลที่ได้รับใน terminal

### งานที่ 4: สร้างฐานข้อมูล SQLite

สร้างตารางชื่อ `sensor_readings` โดยมีข้อมูลอย่างน้อยดังนี้

| Field | ชนิดข้อมูล | คำอธิบาย |
|---|---|---|
| `id` | INTEGER | Primary key |
| `device_id` | TEXT | รหัสอุปกรณ์ |
| `temperature` | REAL | อุณหภูมิ |
| `humidity` | REAL | ความชื้น |
| `received_at` | TEXT | เวลาที่ server ได้รับข้อมูล |

- [ ] สร้างตารางสำเร็จ
- [ ] บันทึกข้อมูลจาก MQTT ลง SQLite ได้
- [ ] ตรวจสอบว่ามีข้อมูลสะสมอย่างน้อย 10 รายการ

### งานที่ 5: สร้าง Dashboard

Dashboard ต้องแสดงอย่างน้อย:

- [ ] ชื่อกลุ่มและชื่อโครงงาน
- [ ] ค่าล่าสุดของอุณหภูมิ
- [ ] ค่าล่าสุดของความชื้น
- [ ] เวลาที่ server ได้รับข้อมูลล่าสุด
- [ ] ตารางประวัติข้อมูลอย่างน้อย 10 รายการ
- [ ] สถานะพัดลม: `ON` หรือ `OFF`

### งานที่ 6: สร้างระบบควบคุมอัตโนมัติ

กำหนดเงื่อนไขดังนี้

| เงื่อนไข | คำสั่ง MQTT | ผลลัพธ์ใน Wokwi |
|---|---|---|
| อุณหภูมิ $\geq 30°C$ | `ON` | LED ติด แทนพัดลมทำงาน |
| อุณหภูมิ $< 30°C$ | `OFF` | LED ดับ แทนพัดลมหยุดทำงาน |

- [ ] Python server publish คำสั่งไปที่ control topic ได้
- [ ] ESP32 subscribe control topic ได้
- [ ] LED เปลี่ยนสถานะตามคำสั่งจาก server ได้
- [ ] ทดสอบโดยปรับอุณหภูมิ DHT22 บน Wokwi

### งานที่ 7: แชร์ Dashboard ผ่าน ngrok

- [ ] Flask dashboard ทำงานบน port 5000
- [ ] เปิด ngrok ด้วยคำสั่ง `ngrok http 5000`
- [ ] เปิด dashboard ผ่าน public URL ได้
- [ ] ให้ผู้สอนหรือเพื่อนในชั้นทดลองเปิด dashboard ได้

---

## 14. เงื่อนไขขั้นต่ำของระบบสมบูรณ์

ระบบของแต่ละกลุ่มจะถือว่าเสร็จสมบูรณ์เมื่อสามารถสาธิตขั้นตอนต่อไปนี้ได้ครบ

1. เริ่ม Wokwi simulation
2. ESP32 เชื่อมต่อ Wi-Fi และ MQTT Broker ได้
3. ESP32 ส่งข้อมูล JSON ไปยัง telemetry topic ได้
4. Python server รับข้อมูลได้
5. Python server บันทึกข้อมูลลง SQLite ได้
6. Dashboard แสดงข้อมูลล่าสุดและข้อมูลย้อนหลังได้
7. เมื่อปรับอุณหภูมิให้สูงกว่า 30°C LED ต้องติด
8. เมื่อปรับอุณหภูมิให้ต่ำกว่า 30°C LED ต้องดับ
9. Dashboard ต้องเปิดดูผ่าน ngrok URL ได้

---

## 15. เกณฑ์ประเมิน

| รายการประเมิน | คะแนน |
|---|---:|
| วงจร Wokwi และการอ่านค่า DHT22 ถูกต้อง | 15 |
| ESP32 เชื่อมต่อ Wi-Fi และส่ง MQTT JSON ได้ | 20 |
| Python server รับข้อมูลและตรวจสอบ JSON ได้ | 15 |
| บันทึกข้อมูลลง SQLite database ได้ | 15 |
| Dashboard แสดงข้อมูลล่าสุดและข้อมูลย้อนหลังได้ | 15 |
| ระบบควบคุม LED ผ่าน MQTT ทำงานได้ | 10 |
| การอธิบาย Three-Tier Architecture และการนำเสนอ | 10 |
| **รวม** | **100** |

---

## 16. คำถามสรุปหลังปฏิบัติ

ให้นักเรียนตอบคำถามต่อไปนี้ในรายงานหรือการนำเสนอ

1. ESP32 ทำหน้าที่เป็น Publisher, Subscriber หรือทั้งสองอย่าง เพราะเหตุใด?
2. HiveMQ Broker มีหน้าที่อะไรในระบบนี้?
3. หาก Python server ปิดอยู่ ข้อมูลจาก ESP32 จะเกิดอะไรขึ้น?
4. เหตุใดจึงต้องใช้ topic ที่แตกต่างกันสำหรับแต่ละกลุ่ม?
5. ส่วนใดของระบบคือ Presentation Tier, Application Tier และ Data Tier?
6. ngrok มีหน้าที่อะไร และเหตุใดจึงไม่ใช้ ngrok สำหรับ MQTT?
7. ถ้าต้องการเพิ่มเซนเซอร์วัดระดับน้ำ ควรแก้ไขส่วนใดของระบบบ้าง?
8. หากต้องนำระบบไปใช้งานจริง ควรปรับปรุงด้านความปลอดภัยอย่างไร?

---

## 17. แนวทางต่อยอด

สำหรับกลุ่มที่ทำงานพื้นฐานเสร็จแล้ว สามารถเลือกพัฒนาต่อได้

- เพิ่ม potentiometer เพื่อจำลองระดับน้ำหรือความชื้นในดิน
- เพิ่ม relay หรือ servo ใน Wokwi เพื่อจำลองอุปกรณ์ actuator
- เพิ่มปุ่ม Manual Override สำหรับเปิด/ปิดพัดลมเอง
- เพิ่มกราฟอุณหภูมิและความชื้นบน dashboard
- เพิ่มระบบแจ้งเตือนเมื่ออุณหภูมิสูงเกินกำหนด
- เพิ่มหลายอุปกรณ์ โดยใช้ `device_id` แตกต่างกัน
- เปลี่ยนจาก SQLite เป็น PostgreSQL หรือ MySQL
- เพิ่มระบบ login สำหรับ dashboard
- ใช้ private MQTT broker แทน public broker

---

## 18. ข้อควรระวัง

- HiveMQ Public Broker เป็นพื้นที่สาธารณะ ห้ามส่งรหัสผ่าน ข้อมูลส่วนบุคคล หรือข้อมูลสำคัญ
- ห้ามใช้ topic ทั่วไป เช่น `sensor/data` เพราะอาจชนกับผู้ใช้อื่น
- ทุกกลุ่มต้องตั้ง topic ให้แตกต่างกัน
- ห้ามเผยแพร่ ngrok URL ที่เข้าถึงข้อมูลสำคัญ
- ในการใช้งานจริง ไม่ควรเปิด Flask ด้วย `debug=True`
- ควรตรวจสอบชนิดข้อมูล JSON ก่อนบันทึกลงฐานข้อมูลเสมอ

---

## 19. สรุป

โครงงานนี้แสดงให้เห็นระบบ IoT แบบครบวงจร ตั้งแต่การจำลองเซนเซอร์และ actuator บน Wokwi การส่งข้อมูลด้วย MQTT การประมวลผลด้วย Python การจัดเก็บข้อมูลในฐานข้อมูล และการนำเสนอผลผ่าน Web Dashboard

```text
Sensor → ESP32 → MQTT Broker → Python Server → Database → Dashboard
                                         |
                                         v
                              Control Command → ESP32 → LED/Fan
```

ระบบนี้เป็นตัวอย่างของการประยุกต์ใช้ IoT, Mechatronics, Web Application และฐานข้อมูลร่วมกันในโครงงานเดียว