import os
import time

import pymysql
from flask import Flask, request, send_from_directory

PORT = int(os.environ.get("PORT", 3000))
DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "rootpassword")
DB_NAME = os.environ.get("DB_NAME", "ctf01")

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


# 脆弱: usernameとpasswordをパラメータ化せず、SQL文字列にそのまま連結している。
@app.post("/login")
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username is None or password is None:
        return "ユーザー名とパスワードは必須です", 400

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    try:
        with db.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
    except pymysql.err.MySQLError as e:
        return f"SQLエラー: {e}", 500

    if not rows:
        return "ログイン失敗。<a href='/'>戻る</a>", 401

    # 本来はusernameで一意に1件だけヒットする想定。injectionで複数件/別人の行が
    # 返ってきても、先頭行をそのまま信用してしまっている。
    user = rows[0]
    if user["is_admin"]:
        # flagはユーザー入力を経由しない通常クエリで取得する(ここ自体は安全)。
        with db.cursor() as cur:
            cur.execute("SELECT flag FROM flags LIMIT 1")
            flag = cur.fetchone()["flag"]
        return f"""
        <h1>管理者ダッシュボード</h1>
        <p>ようこそ、{user['username']} さん。</p>
        <p>{flag}</p>
        """

    return f"<h1>ようこそ、{user['username']} さん</h1><p>管理者権限はありません。</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
