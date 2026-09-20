import json
import threading

from flask import Flask, render_template
import paho.mqtt.client as mqtt

from database import (
    init_db,
    save_sensor_reading,
    get_latest_reading,
    get_recent_readings
)

app = Flask(__name__, template_folder="templates")

# ==========================================
# MQTT Settings
# ==========================================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

# ต้องแก้ team01 ให้ตรงกับไฟล์ main.py ใน Wokwi
TELEMETRY_TOPIC = "mechatronics/2026/sectionA/team01/telemetry"
CONTROL_TOPIC = "mechatronics/2026/sectionA/team01/control/fan"

MQTT_CLIENT_ID = "python-flask-server-team01"

# กำหนดเกณฑ์เปิดพัดลม
TEMPERATURE_THRESHOLD = 30.0


def validate_sensor_data(data):
    """
    Validate incoming JSON data.
    Required:
    - device_id
    - temperature
    - humidity
    """

    if not isinstance(data, dict):
        return False, "Payload must be a JSON object"

    required_fields = ["device_id", "temperature", "humidity"]

    for field in required_fields:
        if field not in data:
            return False, "Missing field: {}".format(field)

    if not isinstance(data["device_id"], str):
        return False, "device_id must be text"

    try:
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
    except (TypeError, ValueError):
        return False, "temperature and humidity must be numbers"

    if temperature < -50 or temperature > 100:
        return False, "temperature out of accepted range"

    if humidity < 0 or humidity > 100:
        return False, "humidity must be between 0 and 100"

    return True, {
        "device_id": data["device_id"],
        "temperature": temperature,
        "humidity": humidity
    }


def get_fan_command(temperature):
    """Return ON/OFF according to temperature threshold."""
    if temperature >= TEMPERATURE_THRESHOLD:
        return "ON"

    return "OFF"


def on_connect(client, userdata, flags, reason_code, properties):
    """Run when Python connects to MQTT broker."""
    if reason_code == 0:
        print("Connected to MQTT broker")
        client.subscribe(TELEMETRY_TOPIC)
        print("Subscribed to:", TELEMETRY_TOPIC)
    else:
        print("MQTT connection failed. Reason code:", reason_code)


def on_message(client, userdata, message):
    """Run when telemetry message arrives."""
    print("\nMQTT message received")
    print("Topic:", message.topic)

    try:
        payload_text = message.payload.decode("utf-8")
        payload = json.loads(payload_text)

        valid, result = validate_sensor_data(payload)

        if not valid:
            print("Rejected message:", result)
            return

        device_id = result["device_id"]
        temperature = result["temperature"]
        humidity = result["humidity"]

        fan_command = get_fan_command(temperature)

        save_sensor_reading(
            device_id=device_id,
            temperature=temperature,
            humidity=humidity,
            fan_status=fan_command
        )

        client.publish(CONTROL_TOPIC, fan_command)

        print("Saved sensor reading")
        print("Device:", device_id)
        print("Temperature:", temperature)
        print("Humidity:", humidity)
        print("Fan command:", fan_command)

    except UnicodeDecodeError:
        print("Rejected message: payload is not UTF-8 text")

    except json.JSONDecodeError:
        print("Rejected message: invalid JSON")

    except Exception as error:
        print("Unexpected error:", error)


def start_mqtt_client():
    """Start MQTT client in a background thread."""
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id=MQTT_CLIENT_ID
    )

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_forever()


@app.route("/")
def dashboard():
    """Render dashboard page."""
    latest_reading = get_latest_reading()
    recent_readings = get_recent_readings(limit=20)

    return render_template(
        "index.html",
        latest=latest_reading,
        readings=recent_readings,
        threshold=TEMPERATURE_THRESHOLD
    )


@app.route("/health")
def health_check():
    """Simple endpoint for checking Flask server."""
    return {
        "status": "ok",
        "service": "iot-mechatronics-dashboard"
    }


if __name__ == "__main__":
    init_db()

    mqtt_thread = threading.Thread(
        target=start_mqtt_client,
        daemon=True
    )

    mqtt_thread.start()

    # debug=False prevents Flask from starting MQTT twice
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )