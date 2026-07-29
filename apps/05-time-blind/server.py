import os
import time

import pymysql
from flask import Flask, jsonify, request, send_from_directory

PORT = int(os.environ.get("PORT", 3000))
DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "rootpassword")
DB_NAME = os.environ.get("DB_NAME", "ctf05")

app = Flask(__name__, static_folder="public", static_url_path="")


# MySQLコンテナの起動完了より先にappが立ち上がるレースを避けるため、
# 接続できるまでリトライする。
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


# 脆弱: emailをバインドパラメータではなく文字列連結している。レスポンスは
# 真偽に関わらず常に同一で、booleanの手がかりすら与えない。応答時間の差だけが
# injectionを検知・悪用する唯一の手段になる(time-based blind)。
@app.post("/api/subscribe")
def subscribe():
    email = request.form.get("email", "")

    query = f"SELECT id FROM subscribers WHERE email = '{email}'"

    try:
        with db.cursor() as cur:
            cur.execute(query)
            cur.fetchall()
    except pymysql.err.MySQLError:
        pass

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
