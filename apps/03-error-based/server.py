import os
import time

import pymysql
from flask import Flask, jsonify, request, send_from_directory

PORT = int(os.environ.get("PORT", 3000))
DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "rootpassword")
DB_NAME = os.environ.get("DB_NAME", "ctf03")

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


# 脆弱: idはnumeric contextなのでクォートなしでそのまま連結している。
# エラーをそのまま返す(この問題ではこれが攻略の要 - extractvalue等が
# 起こすXPATH構文エラーにデータを埋め込ませて読み取る)。
@app.get("/product")
def product():
    id_ = request.args.get("id")
    if id_ is None:
        return jsonify({"error": "id is required"}), 400

    query = f"SELECT name, description, price FROM products WHERE id = {id_}"

    try:
        with db.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
    except pymysql.err.MySQLError as e:
        return jsonify({"error": str(e)}), 500

    # idが素の数字のときだけ実際の行を表示する。injection文字列は数字だけには
    # ならないので、UNIONで偽の行を混ぜても表示には反映されない
    # (クエリ自体はバリデーションなしで実行されるのでerror-based技術は変わらず刺さる)。
    if not id_.isdigit():
        return jsonify({"result": None})

    return jsonify({"result": row})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
