# IoT Smart Greenhouse Dashboard

โปรเจคนี้เป็นระบบจำลอง IoT สำหรับติดตามอุณหภูมิและความชื้นของโรงเรือน พร้อมระบบควบคุมพัดลมแบบอัตโนมัติ โดยใช้ ESP32 ใน Wokwi, MQTT Broker, Python Flask Server, SQLite และหน้า Dashboard

## ภาพรวม

```text
ESP32 + DHT22 + LED (Wokwi)
        |
        | publish telemetry JSON
        v
HiveMQ Broker
        |
        | subscribe
        v
Python Flask app
        |
        +--> validate payload
        +--> save to SQLite
        +--> send ON/OFF fan command
        +--> show dashboard
        v
Browser / ngrok public URL
```

## จุดประสงค์

- เรียนรู้การทำงานของระบบ IoT แบบเส้นทางข้อมูลจริง
- เชื่อมต่อ ESP32 กับ MQTT ผ่าน Wokwi
- รับข้อมูลเซ็นเซอร์ด้วย Python
- บันทึกข้อมูลลง SQLite
- แสดงผลบนหน้าเว็บแบบ dashboard
- ควบคุมพัดลมจำลองตามค่าอุณหภูมิ

## เทคโนโลยีที่ใช้

- Wokwi
- ESP32 + DHT22
- MicroPython
- MQTT
- Python
- Flask
- SQLite
- ngrok

## โครงสร้างโปรเจค

```text
swe4me-iot-project/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── experiments/
│   ├── README.md
│   ├── 01-flask/
│   ├── 02-sqlite/
│   ├── 03-mqtt/
│   ├── 04-json/
│   └── 05-ngrok/
├── references/
│   ├── wokwi-esp32-simulator.md
│   └── hivemq-websocket-client.md
├── iot_data.db
└── .venv/
```

## Quick Start

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

แล้วเปิด:

```text
http://localhost:5000/
```

และเพื่อแชร์ dashboard ให้คนภายนอกเห็น:

```bash
ngrok http 5000
```

## การทำงานหลัก

- ESP32 ส่ง JSON เข้า MQTT topic ของกลุ่ม
- Flask server subscribe topic นั้น
- server validate payload และบันทึกลง SQLite
- ถ้าอุณหภูมิ >= 30.0°C server ส่งคำสั่ง ON
- ถ้าอุณหภูมิ < 30.0°C server ส่งคำสั่ง OFF
- Dashboard แสดงค่าล่าสุดและประวัติข้อมูลย้อนหลัง

ตัวอย่าง payload:

```json
{
  "device_id": "esp32-team01",
  "temperature": 27.5,
  "humidity": 65.0
}
```

## การทดลองสำหรับนักเรียน

ดูรายละเอียดเพิ่มเติมใน [experiments/README.md](experiments/README.md)

ลำดับแนะนำ:

1. [experiments/01-flask](experiments/01-flask)
2. [experiments/02-sqlite](experiments/02-sqlite)
3. [experiments/03-mqtt](experiments/03-mqtt)
4. [experiments/04-json](experiments/04-json)
5. [experiments/05-ngrok](experiments/05-ngrok)

## เอกสารอ้างอิงรายละเอียด

- [references/wokwi-esp32-simulator.md](references/wokwi-esp32-simulator.md)
- [references/hivemq-websocket-client.md](references/hivemq-websocket-client.md)

รายละเอียดเชิงลึกเรื่องการตั้งค่า Wokwi, MQTT WebSocket Client และโค้ด ESP32 จะอยู่ที่ไฟล์เหล่านี้ เพื่อให้ README หลักกระชับและไม่ซ้ำซ้อน

## หมายเหตุสำคัญ

- topic ต้องไม่ซ้ำกันระหว่างกลุ่ม
- ใช้ public MQTT broker สำหรับทดลองเท่านั้น
- อย่าเปิด Flask หลายตัวบนพอร์ตเดียวกัน
- ใช้ ngrok เพื่อแชร์ dashboard เท่านั้น ไม่ใช่ MQTT broker

- ห้ามใช้ topic ร่วมกันกับกลุ่มอื่นโดยไม่จำเป็น
- HiveMQ Public Broker เป็นสาธารณะ จึงไม่ควรส่งข้อมูลสำคัญหรือข้อมูลส่วนบุคคล
- อย่าเปิดหลาย Flask app บน port เดียวกันพร้อมกัน
- อย่าเปิด debug mode ใน production จริง
- ตรวจสอบ JSON payload เสมอก่อน save ลงฐานข้อมูล

## สรุป

โปรเจคนี้แสดงให้เห็นแนวคิด IoT แบบเต็มวงจร โดยเริ่มจากการวัดข้อมูลของเซ็นเซอร์บน ESP32, ส่งข้อมูลผ่าน MQTT, ทำประมวลผลบน Python, จัดเก็บลง SQLite, และแสดงผลบน Dashboard ผ่าน Flask และ ngrok

นี่เป็นตัวอย่างที่เหมาะสำหรับการเรียนรู้ด้าน IoT, Embedded Systems, Backend, และ Data Presentation ในเวลาเดียวกัน

---

## Quick Start สำหรับนักเรียน

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

แล้วเปิด:

```text
http://localhost:5000/
```

พร้อมด้วย:

```bash
ngrok http 5000
```

สำหรับการทดสอบการแชร์ dashboard จากเครื่องของคุณ
