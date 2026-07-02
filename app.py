from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB = "battery.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS battery(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device TEXT,
        battery INTEGER,
        charging INTEGER,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():
    return "Battery Sync Server Running"


@app.route("/upload", methods=["POST"])
def upload():

    data = request.json

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO battery(device,battery,charging,time)
        VALUES(?,?,?,?)
        """,
        (
            data["device"],
            data["battery"],
            int(data["charging"]),
            data["time"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"status":"ok"})


@app.route("/data")
def data():

    conn=sqlite3.connect(DB)
    cur=conn.cursor()

    rows=cur.execute("SELECT * FROM battery").fetchall()

    conn.close()

    return jsonify(rows)


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)