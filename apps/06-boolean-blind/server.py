import os
import time

import pymysql
from flask import Flask, jsonify, request, send_from_directory

PORT = int(os.environ.get("PORT", 3000))
DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "rootpassword")
DB_NAME = os.environ.get("DB_NAME", "ctf06")

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


# 脆弱: idは常に数値だと思い込み、クォートもint()等のバリデーションも
# 一切していない。レスポンスは行がヒットしたかどうかしか返さない(データは
# 一切echoしない)ため、blindでの攻略が必要になる。
@app.get("/api/user")
def api_user():
    id_ = request.args.get("id")
    if id_ is None:
        return jsonify({"error": "id is required"}), 400

    query = f"SELECT username FROM users WHERE id = {id_}"

    try:
        with db.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
    except pymysql.err.MySQLError:
        # 03とは違い、ここではクエリの詳細を一切漏らさず汎用エラーのみ返す。
        # 完全にblindな攻略を意図している。
        return jsonify({"found": False}), 400

    return jsonify({"found": len(rows) > 0})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
