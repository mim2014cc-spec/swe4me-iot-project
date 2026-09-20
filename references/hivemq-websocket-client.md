# HiveMQ WebSocket Client 
คือเครื่องมือบนเว็บสำหรับทดสอบการเชื่อมต่อและรับ–ส่งข้อความ MQTT กับ MQTT Broker โดยไม่ต้องติดตั้งโปรแกรมเพิ่ม เหมาะสำหรับตรวจสอบว่า ESP32/Wokwi ของเราส่งข้อมูลไปถึง Broker หรือไม่ และทดลองส่งคำสั่งกลับไปควบคุมอุปกรณ์จำลอง เช่น LED หรือพัดลมได้ [hivemq](https://www.hivemq.com/demos/websocket-client/)

## วิธีใช้แบบย่อ

1. เปิด [HiveMQ WebSocket Client](https://www.hivemq.com/demos/websocket-client/)

2. กรอกข้อมูลการเชื่อมต่อ

| ช่อง | ค่าแนะนำ |
|---|---|
| Host | `broker.hivemq.com` |
| Port | `8000` |
| Client ID | ชื่อที่ไม่ซ้ำกับ ESP32 เช่น `monitor-team01-karn` |

> ห้ามใช้ Client ID ซ้ำกับ Wokwi/ESP32 เพราะ MQTT Broker จะอนุญาตให้มีการเชื่อมต่อด้วย Client ID เดียวได้เพียงหนึ่งการเชื่อมต่อในเวลาเดียวกัน หากซ้ำกัน ฝั่งหนึ่งอาจถูกตัดการเชื่อมต่อ [ibm](https://www.ibm.com/docs/en/ibm-mq/9.4.x?topic=concepts-client-identifier)

3. กด **Connect**

4. ในส่วน **Subscriptions** เพิ่ม Topic ที่ต้องการตรวจสอบ เช่น

```text
mechatronics/2026/sectionA/team01/telemetry
```

หรือใช้ Wildcard เพื่อดูทุกข้อความของกลุ่ม:

```text
mechatronics/2026/sectionA/team01/#
```

5. เมื่อ Wokwi/ESP32 ส่งข้อมูลทุก 5 วินาที จะเห็นข้อความ JSON เช่น

```json
{
  "device_id": "esp32-team01",
  "temperature": 25,
  "humidity": 60
}
```

## ทดลองส่งคำสั่งกลับ

ในส่วน **Publish** ให้กำหนด Topic:

```text
mechatronics/2026/sectionA/team01/control/fan
```

จากนั้นส่งข้อความ:

```text
ON
```

หรือ

```text
OFF
```

Wokwi ESP32 ที่ Subscribe Topic นี้อยู่จะได้รับข้อความและสั่งเปิด/ปิด LED ซึ่งใช้แทนการทำงานของพัดลมจำลองได้

## หมายเหตุ

- ESP32 ใน Wokwi ใช้ MQTT ปกติผ่านพอร์ต `1883`
- Browser ใช้ WebSocket ผ่านพอร์ต `8000`
- ทั้งสองแบบเชื่อมต่อกับ `broker.hivemq.com` เดียวกัน จึงสื่อสารผ่าน Topic เดียวกันได้ [hivemq](https://www.hivemq.com/demos/websocket-client/)
- `broker.hivemq.com` เป็น Public Broker สำหรับทดลองใช้งาน ไม่ควรส่งข้อมูลส่วนตัว รหัสผ่าน หรือข้อมูลสำคัญผ่านระบบนี้ [hivemq](https://www.hivemq.com/mqtt/public-mqtt-broker/)