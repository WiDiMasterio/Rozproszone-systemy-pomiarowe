from flask import Flask, jsonify
from db import get_connection

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/measurements", methods=["GET"])
def get_measurements():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ts_ms, device_name, description, value, unit, unit, msgIdx
        FROM measurementsw
        ORDER BY id DESC
        LIMIT 20
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = []

    for row in rows:
        result.append({
            "ts_ms": row[0],
            "device_name": row[1],
            "description": row[2],
            "value": row[3],
            "unit": row[4],
            "msgIdx": row[5],
    })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
