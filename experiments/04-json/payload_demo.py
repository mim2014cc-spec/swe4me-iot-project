import json

# ข้อมูลตัวอย่างที่อุปกรณ์จะส่งออกมา
sample_data = {
    "device_id": "team01",
    "temperature": 31.2,
    "humidity": 55.5,
    "status": "ok"
}

# แปลง dictionary ให้เป็นข้อความ JSON
json_text = json.dumps(sample_data)
print("ข้อความ JSON:")
print(json_text)

# แปลงข้อความ JSON กลับเป็น dictionary เพื่ออ่านค่า
parsed_data = json.loads(json_text)
print("\nค่าที่อ่านได้:")
print(f"อุปกรณ์: {parsed_data['device_id']}")
print(f"อุณหภูมิ: {parsed_data['temperature']} C")
print(f"ความชื้น: {parsed_data['humidity']} %")
