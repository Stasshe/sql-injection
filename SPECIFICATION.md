# SPECIFICATION

SQLインジェクション未経験者向け教材。Docker + Python/Flask + PyMySQL、依存管理は`uv`、
ソース公開(白箱)、全6問。1問につき新しい判断は1つだけにし、短い手入力で攻略できる。
設計背景は[[INTENT]]参照。

## 全体構成

```
sql-injection/
├── docker-compose.yml
└── apps/
    ├── 01-auth-bypass/  (port 3001) 文字列条件の認証バイパス
    ├── 02-union-search/ (port 3002) UNIONによる別テーブルの表示
    ├── 03-or-listing/   (port 3003) 数値条件のORによる全件表示
    ├── 04-case-bypass/  (port 3004) 大文字小文字によるフィルタ回避
    ├── 05-price-filter/ (port 3005) 検索対象を選んだOR注入
    └── 06-boolean-code/ (port 3006) Boolean-blindによる1桁判定
```

各appは`Dockerfile`、`pyproject.toml`、`uv.lock`、`server.py`、`public/`、`db/`、
問題READMEを持つ。flag実値はコードへ置かない。ルートの`.env`に`FLAG_01`〜`FLAG_06`
として置き、各DBの`02-flag.sh`が初期化時に保存する。

## 01-auth-bypass

- `users(id,username,password,is_admin)`と`flags(id,flag)`。
- `username`と`password`をクォート内へ直接連結する。
- `admin' -- `でpassword条件をコメントアウトする。
- adminとしてログインできた場合、通常クエリでflagを表示する。

## 02-union-search

- `products(id,name,description,price)`と`flags(id,flag)`。
- `q`を`LIKE '%{q}%'`へ直接連結する。
- テーブル名、カラム名、4カラムであることを問題文に明記する。
- `zzz' UNION SELECT id,flag,NULL,NULL FROM flags-- -`でflagを商品名として表示する。

## 03-or-listing

- `products(id,name,description,price)`。ID 999の商品を`02-flag.sh`で追加し、説明欄へflagを置く。
- `id`を数値条件へ直接連結し、該当する全行を表示する。
- `0 OR 1=1`ですべての商品を表示する。
- 専用SQL関数、エラーからの抽出、文字列分割は要求しない。

## 04-case-bypass

- 02と同じテーブルと脆弱な検索クエリを使う。
- 入力に大文字の`UNION`が含まれる場合だけ拒否する。空白、`SELECT`、コメントは拒否しない。
- 02のpayloadにある`UNION`を小文字の`union`へ変えるだけでflagを表示できる。

## 05-price-filter

- `products(id,name,description,price)`。ID 999の商品を`02-flag.sh`で追加し、説明欄へflagを置く。
- `field`は`name`、`description`、`price`のホワイトリスト。
- 文字列検索ではシングルクォートをエスケープする。価格検索だけ`q`を数値条件へ直接連結する。
- 画面と問題文で価格検索が怪しいと明記する。
- `field=price`と`q=0 OR 1=1`の組み合わせですべての商品を表示する。

## 06-boolean-code

- `users(id,username,is_admin)`と`flags(id,flag,code)`。
- DB初期化時に0〜9のcodeを1つランダム生成する。
- `/api/user?id=`は`id`を数値条件へ直接連結し、`found`だけを返す。
- `1 AND (SELECT code FROM flags)=0`の末尾を変え、最大10回でcodeを特定する。
- `/claim?code=`はプレースホルダー付きクエリでcodeを検証し、正しければflagを返す。
- flag本文の1文字ずつの抽出や二分探索は要求しない。

## Docker

- 6組のapp・MySQLサービスを問題別networkで分離する。DBのhost portは公開しない。
- DB初期化は`01-schema.sql`、`02-flag.sh`の順。
- appはDB healthcheck完了後に起動し、接続リトライも行う。
- appだけをhostの3001〜3006へ公開する。

## 確認条件

- `docker compose up --build`で6問が起動する。
- ブラウザで各画面の通常操作と攻略payloadを確認する。
- 03と05は`Internal Backup`の説明欄、04は商品名欄、06はcode送信後にflagが表示される。
