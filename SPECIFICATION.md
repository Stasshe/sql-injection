# SPECIFICATION

CTF初学者向けSQLインジェクション教材。Docker + Python/Flask + PyMySQL、依存管理は`uv`、
ソース公開(白箱)、全5問。設計背景は[[INTENT]]参照。1問1技術、独立Flask+独立MySQL。

## 全体構成

```
sql-injection/
├── docker-compose.yml
└── apps/
    ├── 01-auth-bypass/     (port 3001) 認証バイパス(tautology)
    ├── 02-union-search/    (port 3002) UNION-based抽出
    ├── 03-error-based/     (port 3003) Error-based抽出
    ├── 04-boolean-blind/   (port 3004) Boolean-blind
    └── 05-time-blind/      (port 3005) Time-blind
```

各app構成:
```
apps/NN-name/
├── Dockerfile          ghcr.io/astral-sh/uv:python3.12-bookworm-slim, uv sync --locked
├── pyproject.toml       flask, pymysql
├── uv.lock
├── server.py            flag文字列は絶対に埋め込まない
├── public/               vanilla HTML/CSS/fetch
├── db/
│   ├── 01-schema.sql     schema+seed(flagは含まない)
│   └── 02-flag.sh        環境変数FLAGを読んでflagsテーブルにINSERT
└── README.md             問題文+段階ヒント+<details>解答(flag実値は書かない)
```

flag実値はリポジトリ内のどこにも書かない。ルートの`.env`(gitignore済み)に
`FLAG_01`〜`FLAG_05`として置き、`docker-compose.yml`が各`db-*`に`FLAG`環境変数として渡す。
このためリポジトリのコード(上記全ファイル)は丸ごと公開してよい。詳細は[[INTENT]]参照。

## 01-auth-bypass

- `users(id, username, password, is_admin)` + `flags(id, flag)`(1行のみ)。
- ログインクエリ(脆弱):
  ```python
  f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
  ```
- 攻略: `username=admin' -- ` または `' OR '1'='1' -- ` でWHERE句を無効化しログイン成立。
- 成功後`is_admin`が真なら`SELECT flag FROM flags LIMIT 1`(injectionではなく通常クエリ)でflag取得
  し画面表示。

## 02-union-search

- `products(id,name,description,price)` + `flags(id,flag)`。**テーブル/カラム名・カラム数(4)とも
  問題文に明記**(この問題の主眼はUNION機構の理解であり、スキーマ探索ではない。ORDER BYでの
  カラム数探索は「もっと自力で探したい場合」の任意ルートとしてのみREADMEに残す)。
- `GET /search?q=` → 脆弱クエリ:
  ```python
  f"SELECT id, name, description, price FROM products WHERE name LIKE '%{q}%'"
  ```
- エラーをそのまま`{error: str(e)}`で返す(verbose)。
- 攻略: `ORDER BY`でSELECT対象カラム数(4)を特定 → `UNION SELECT id,flag,NULL,NULL FROM flags`で抽出。

## 03-error-based

- `products(id,name,description,price)` + `flags(id,flag)`。
- `GET /product?id=` → 脆弱クエリ(numeric context、クォートなし):
  ```python
  f"SELECT name, description, price FROM products WHERE id = {id_}"
  ```
- エラーはそのまま返す(この問題の核が「エラーメッセージにデータを埋め込ませる」ため必須)。
- クエリ自体はバリデーションなしでそのまま実行するが、**表示は`id_.isdigit()`が真の時だけ**
  行う。これによりUNION SELECTで行を混ぜても表示には反映されず(素の数字以外は`result: null`)、
  抽出手段がerror-based一本に絞られる(実際にUNIONで解けてしまうことが判明したため追加)。
- 攻略: `extractvalue()`によるXPATH構文エラーを利用しflagをエラーメッセージに出力させる。
  ```
  id=1 AND extractvalue(1, concat(0x7e, (SELECT flag FROM flags)))
  ```
  `extractvalue`は結果を約32文字(マーカー含む)で切り詰めるため、`SUBSTRING(flag,1,31)`と
  `SUBSTRING(flag,32,31)`のように2回に分けて抽出する必要がある(実機検証済み)。

## 04-boolean-blind

- `users(id, username, is_admin)` + `flags(id, flag)`。
- `GET /api/user?id=` → 脆弱クエリ(numeric context、クォートなし):
  ```python
  f"SELECT username FROM users WHERE id = {id_}"
  ```
- レスポンスは`{found: true}` / `{found: false}`のみ。データは一切echoしない。
- 攻略: `id=1 AND (SELECT SUBSTRING(flag,1,1) FROM flags)='F'`のような二値応答を1文字ずつ繰り返し
  flagを復元。

## 05-time-blind

- `subscribers(id, email)`(1行のみ)+ `flags(id, flag)`。行数を1に絞っているのは、
  `SLEEP()`を含む条件はMySQLが行ごとに評価するため複数行あると遅延が行数倍に積み重なり
  (実機確認済み、`LIMIT`を足しても解消しない)、学習時に混乱するため。
- `POST /api/subscribe` (body: `email`) → 脆弱クエリ(string context):
  ```python
  f"SELECT id FROM subscribers WHERE email = '{email}'"
  ```
- レスポンスは真偽に関わらず常に同一(`{status:"ok"}`)。差が出るのは応答時間のみ。
- 攻略: まず`email=x' OR SLEEP(3)-- `で遅延を確認しinjection成立を検証、その後
  `email=x' OR IF((SELECT SUBSTRING(flag,1,1) FROM flags)='F', SLEEP(3), 0)-- `を
  1文字ずつ試し応答時間でtrue/falseを判定してflagを復元。

## Docker

- `docker-compose.yml`は5組の`app-*`/`db-*`サービス。mysqlはhost port非公開、appコンテナからのみ
  到達可能(問題ごとに独立network)。
- 各`db-*`: `image: mysql:8`、`volumes: apps/NN-name/db:/docker-entrypoint-initdb.d:ro`
  (ディレクトリごとマウント、`01-schema.sql`→`02-flag.sh`の順で実行)、
  `environment.FLAG: ${FLAG_NN}`(`.env`から)、healthcheck (`mysqladmin ping`)。
- 各`app-*`: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`ベース、`uv sync --locked`で依存解決、
  `depends_on: db-*: condition: service_healthy` + server.py内で接続リトライ(DB起動待ちレース対策)。
- host公開ポートはapp側のみ(3001〜3005)。

## 起動・確認

```
cp .env.example .env   # 初回のみ。FLAG_01〜FLAG_05を必要なら書き換える
docker compose up --build
curl -s localhost:3001/
curl -s "localhost:3002/search?q=a"
curl -s "localhost:3003/product?id=1"
curl -s "localhost:3004/api/user?id=1"
curl -s -X POST -d "email=a@b.com" localhost:3005/api/subscribe
```

各問正規動作(injection抜き)が壊れていないこと。全問で実際にpayloadを送りflagが取得できること。
