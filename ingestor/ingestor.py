import json
import paho.mqtt.client as mqtt
import db 
import secrets as sec

MQTT_HOST = sec.MQTT_HOST
MQTT_PORT = sec.MQTT_PORT
MQTT_TOPIC = sec.MQTT_TOPIC

def save_measurement(topic, data):
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO measurements
        (ts_ms, device_name, description, value, unit, msgIdx, uuid, topic)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["ts_ms"],
        data["device_name"],
        data["description"],
        data["value"],
        data["unit"],
        data["msgIdx"],
        data.get("uuid"),
        topic
    ))
    
    conn.commit()
    cur.close()
    conn.close()

def is_valid(data):
    required = ["ts_ms", "device_name", "description", "value", "unit", "msgIdx"]
    return all(field in data for field in required)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        if not is_valid(data):
            print("Invalid payload:", data)
            return
    
        save_measurement(msg.topic, data)
        print("Saved message from topic:", msg.topic)
        
    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()
