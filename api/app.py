from flask import Flask, jsonify, request, render_template
from db import get_connection

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    # Po prostu renderujemy pusty szablon GUI. 
    # Całą resztę roboty z pobieraniem danych zrobi JavaScript.
    return render_template("index.html")

# @app.route("/", methods=["GET"])
# def home():
#     return render_template("index.html", measurement=None)

@app.route("/dashboard", methods=["GET"])
def dashboard():
    # Podstrona z automatycznie odświeżanym wykresem i historią
    return render_template("dashboard.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/measurements/last", methods=["GET"])
def get_last_measurement():
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Wyciągamy dokładnie 1 najnowszy rekord (LIMIT 1)
        query = """
            SELECT ts_ms, device_name, description, value, unit, msgIdx 
            FROM measurements 
            ORDER BY id DESC 
            LIMIT 1;
        """
        cur.execute(query)
        row = cur.fetchone() # fetchone() zamiast fetchall(), bo chcemy tylko jeden rząd
        
        cur.close()
        conn.close()

        if row:
            data = {
                "ts_ms": row[0],
                "device_name": row[1],
                "description": row[2],
                "value": row[3],
                "unit": row[4],
                "msgIdx": row[5]
            }
        else:
            data = {"ts_ms": "-", "device_name": "Brak danych", "value": "-", "unit": ""}

        # Zamiast jsonify(), przekazujemy dane do szablonu HTML
        return render_template("index.html", measurement=data)

    except Exception as e:
        return f"Błąd bazy danych: {str(e)}", 500

@app.route("/measurements", methods=["GET"])
def get_measurements():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ts_ms, device_name, description, value, unit, msgIdx
        FROM measurements
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

@app.route("/measurements/latest", methods=["GET"])
def get_latestMeasurements():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ts_ms, device_name, description, value, unit, msgIdx
        FROM measurements
        ORDER BY id DESC
        LIMIT 1
    """)
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is not None:
        return jsonify({
            "ts_ms": row[0],
            "device_name": row[1],
            "description": row[2],
            "value": row[3],
            "unit": row[4],
            "msgIdx": row[5]
        })
    else:
        return jsonify({"error": "No measurements found"}), 404
    
@app.route("/measurements/history", methods=["GET"])
def get_measurementsHistory():
    device_id = request.args.get("device_name", default = "35589507-be86-4a21-a68c-c5fcc1d3a436") 
    description = request.args.get("description")
    limit = request.args.get("limit", default=20, type=int)

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT ts_ms, device_name, description, value, unit, msgIdx
        FROM measurements
        WHERE 1=1
    """

    params = []

    if device_id:
        query += " AND device_name = %s"
        params.append(device_id)
    
    if description:
        query += " AND description = %s"
        params.append(description)
    
    query += " ORDER BY id DESC LIMIT %s"
    params.append(limit)

    cur.execute(query, params)
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
            "msgIdx": row[5]
        })
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
