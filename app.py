from flask import Flask, request, jsonify, send_file
import sqlite3
import csv
import os

app = Flask(__name__)

DB = "battery.db"


# -----------------------------
# Initialize Database
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS battery(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device TEXT,
        battery INTEGER,
        charging INTEGER,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# -----------------------------
# Home
# -----------------------------
@app.route("/")
def home():
    return "Battery Sync Server Running"


# -----------------------------
# Upload Battery Data
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload():
    try:
        data = request.get_json()

        print("Received:", data)

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO battery(device, battery, charging, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            data["device"],
            data["battery"],
            int(data["charging"]),
            data["timestamp"]
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success"
        }), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -----------------------------
# View All Data
# -----------------------------
@app.route("/data")
def data():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    rows = cur.execute("""
        SELECT *
        FROM battery
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return jsonify(rows)


# -----------------------------
# Download CSV
# -----------------------------
@app.route("/download")
def download():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    rows = cur.execute("""
        SELECT device,
               battery,
               charging,
               timestamp
        FROM battery
        ORDER BY timestamp
    """).fetchall()

    conn.close()

    filename = "battery_data.csv"

    with open(filename, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Device",
            "Battery",
            "Charging",
            "Timestamp"
        ])

        writer.writerows(rows)

    return send_file(
        filename,
        as_attachment=True,
        download_name="battery_data.csv"
    )


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)