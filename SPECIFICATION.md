# SPECIFICATION

CTF初学者向けSQLインジェクション教材。Docker + Node.js/Express、白箱(ソース公開)、全3問。
設計背景は[[INTENT]]参照。

## 全体構成

```
sql-injection/
├── docker-compose.yml
└── apps/
    ├── 01-login-bypass/    (port 3001)
    ├── 02-product-search/  (port 3002)
    └── 03-blind-numeric/   (port 3003)
```

各app = 独立Express + 独立MySQL。mysqlはhost port非公開、appコンテナからのみ到達。
各app構成:
```
apps/NN-name/
├── Dockerfile        node:20-alpine, npm ci --omit=dev, CMD node server.js
├── package.json      express, mysql2 (+01のみbcryptjs)
├── server.js
├── public/           vanilla HTML/CSS/fetch、ビルドステップなし
├── db/init.sql       mysql起動時に自動実行、schema+seed+flag
└── README.md         問題概要+段階ヒント+<details>解答
```

## 01-login-bypass

- `users(id, username, password, is_admin)`。passwordは平文保存(レガシー社内ツールの体で意図的に採用)。
- ログインクエリ(脆弱):
  ```js
  `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`
  ```
  両フィールドとも生入力、SQL文字列結合。
- 攻略: `username`に`admin' -- ` を入れるとpassword比較がコメントアウトされWHERE成立、
  もしくは`' OR '1'='1' -- `でも任意行にマッチしログイン成立。
- 成功条件: マッチした行の`is_admin`が真ならadmin扱い → `/dashboard`でflag表示。
- flag: DB内に持たず、admin判定後のダッシュボードHTML内に直書き。

## 02-product-search

- `products(id, name, description, price, category)` + 無関係`secrets(id, flag)`。
- `GET /search?q=` → 脆弱クエリ:
  ```js
  `SELECT id,name,description,price FROM products WHERE name LIKE '%${q}%'`
  ```
- エラーはそのまま`{error: err.message}`でクライアントへ返す(verboseエラー設定)。
- 攻略手順: `ORDER BY`でカラム数特定 → `UNION SELECT`成立確認 →
  `information_schema.tables`/`columns`で`secrets`テーブルとカラム名を発見(UIに一切出てこない)→
  `UNION SELECT id,flag,NULL,NULL FROM secrets`で抽出。
- flag: `secrets.flag`カラムに格納。

## 03-blind-numeric

- `users(id, username, is_admin)` + `secrets(id, flag)`。
- `GET /api/user?id=` → 脆弱クエリ(numeric context、クォートなし):
  ```js
  `SELECT username FROM users WHERE id = ${id}`
  ```
- レスポンスは`{found: true}` / `{found: false}`のみ。データは一切echoしない(真の意味でblind)。
- idはバリデーションなしでそのまま埋め込み → boolean-blind / UNION-blind両方成立。
- 攻略: `id=1 AND (SELECT SUBSTRING(flag,1,1) FROM secrets)='F'`のような二値応答で1文字ずつ抽出、
  または`id=-1 UNION SELECT 1 FROM secrets WHERE flag LIKE 'FLAG%'`系で存在確認を繰り返す。
  sqlmap `--technique=B` でも解ける難易度。
- flag: `secrets.flag`カラムに格納。

## Docker

- `docker-compose.yml`直下に3組の`app-*`/`db-*`サービス定義。
- 各`db-*`: `image: mysql:8`、`volumes: apps/NN-name/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro`、
  healthcheck (`mysqladmin ping`)。
- 各`app-*`: `depends_on: db-*: condition: service_healthy` + server.js内でも接続リトライ
  (`connectWithRetry`、DB起動待ちレース対策)。
- host公開ポートはapp側のみ(3001/3002/3003)。dbは内部networkのみ。

## 起動・確認

```
docker compose up --build
curl -s localhost:3001/         # 01 ログインフォーム
curl -s localhost:3002/search?q=a
curl -s localhost:3003/api/user?id=1
```

各問正規動作(injection抜き)も壊れていないこと。flagは各問攻略で取得できること。
