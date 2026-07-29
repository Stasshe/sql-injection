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


ALLOWED_FIELDS = {"name", "description", "price"}


# 脆弱: fieldとqの2パラメータが揃って初めて注入が成立する。文字列カラム
# (name/description)向けの分岐はクォートをエスケープしており単体では安全。
# だがfield=priceを選ぶと数値カラム用の分岐に入り、そちらはクォート不要な
# numeric contextとしてqをそのまま埋め込む — fieldとqを組み合わせないと
# 崩れないWHERE句になっている。
@app.get("/search")
def search():
    field = request.args.get("field", "name")
    q = request.args.get("q", "")

    if field not in ALLOWED_FIELDS:
        return jsonify({"error": "invalid field"}), 400

    if field == "price":
        query = f"SELECT id, name, description FROM products WHERE price = {q}"
    else:
        q_escaped = q.replace("'", "''")
        query = f"SELECT id, name, description FROM products WHERE {field} LIKE '%{q_escaped}%'"

    try:
        with db.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
    except pymysql.err.MySQLError as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"results": rows})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
