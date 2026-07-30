import os
import time

import pymysql
from flask import Flask, jsonify, request, send_from_directory

PORT = int(os.environ.get("PORT", 3000))
DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "rootpassword")
DB_NAME = os.environ.get("DB_NAME", "ctf04")

app = Flask(__name__, static_folder="public", static_url_path="")


# Retry because the app container may start before MySQL is ready.
def connect_with_retry(retries=20, delay_sec=2):
    for attempt in range(1, retries + 1):
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
            print("[db] connected", flush=True)
            return conn
        except pymysql.err.OperationalError as e:
            print(f"[db] not ready (attempt {attempt}/{retries}): {e}", flush=True)
            time.sleep(delay_sec)
    raise RuntimeError("could not connect to database")


db = connect_with_retry()


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# Vulnerable: the case-sensitive filter misses lowercase SQL keywords.
BLOCKED = ["UNION"]


@app.get("/search")
def search():
    q = request.args.get("q", "")

    for word in BLOCKED:
        if word in q:
            return jsonify({"error": "forbidden pattern detected"}), 400

    query = f"SELECT id, name, description, price FROM products WHERE name LIKE '%{q}%'"

    try:
        with db.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
    except pymysql.err.MySQLError as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"results": rows})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
