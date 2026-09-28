import json
import threading
from flask import Flask, render_template, jsonify, request
import paho.mqtt.client as mqtt
from database import init_db, insert_record, get_latest_record, get_history_records

app = Flask(__name__)

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
TOPIC_TELEMETRY = "mechatronics/2026/sectionA/TEAM_Jitti/telemetry"
TOPIC_CONTROL = "mechatronics/2026/sectionA/TEAM_Jitti/control"

latest_data = {
    "ph": 7.40,
    "temperature": 29.5,
    "turbidity": 2.1,
    "water_level": "NORMAL",
    "pump_fill": "OFF",
    "pump_dose": "OFF",
    "timestamp": "-"
}

def on_connect(client, userdata, flags, rc, properties=None):
    print("MQTT Connected! Subscribed to:", TOPIC_TELEMETRY)
    client.subscribe(TOPIC_TELEMETRY)

def on_message(client, userdata, msg):
    global latest_data
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        latest_data = payload
        insert_record(
            float(payload.get("ph", 7.4)),
            float(payload.get("temperature", 28.5)),
            float(payload.get("turbidity", 2.0)),
            payload.get("water_level", "NORMAL"),
            payload.get("pump_fill", "OFF"),
            payload.get("pump_dose", "OFF")
        )
        print(f"Recorded to DB: pH={payload.get('ph')} | Level={payload.get('water_level')} | Pump={payload.get('pump_fill')}")
    except Exception as e:
        print("Error parsing MQTT payload:", e)

def start_mqtt():
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except:
        client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

threading.Thread(target=start_mqtt, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data", methods=["GET"])
def get_data():
    record = get_latest_record()
    if record:
        return jsonify(record)
    return jsonify(latest_data)

@app.route("/api/history", methods=["GET"])
def get_history():
    records = get_history_records(limit=10)
    return jsonify(records)

@app.route("/api/pump", methods=["POST"])
def control_pump():
    data = request.get_json()
    action = data.get("action", "OFF")
    
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except:
        client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(TOPIC_CONTROL, json.dumps({"pump_fill": action}))
    client.disconnect()
    
    return jsonify({"status": "command_sent", "action": action})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)