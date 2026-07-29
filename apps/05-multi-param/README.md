# 05 - Multi-parameter Injection

`http://localhost:3005` の商品検索から、DB内のflagを抜き出せ。
`server.py`のソースコードは読んでよい。

このDBのテーブル構成:
- `products(id, name, description, price)` — 検索対象
- `flags(id, flag)` — 無関係の別テーブル。目標はこの`flag`を検索結果に混ぜ込むこと

`/search`は`field`(検索対象カラム: `name`/`description`/`price`)と`q`(検索語)の
2パラメータを受け取る。`field=name`や`field=description`だけを使っている限り`q`は
クォートエスケープ済みで安全に見える。両方のパラメータを正しく組み合わせないと
このアプリは崩れない。

## ヒント

<details><summary>ヒント1</summary>

`server.py`の`/search`を見ろ。`field`の値によって`query`の組み立て方が完全に
分岐している。それぞれの分岐で`q`はどう扱われている?

</details>

<details><summary>ヒント2</summary>

`field=name`や`field=description`の分岐は`q.replace("'", "''")`でクォートを
エスケープしているので、この経路からの脱出は難しい。だが`field=price`の分岐だけ
別処理になっている。`price`はDECIMAL(数値)カラムだから安全という思い込みで、
クォート処理を一切していない。

</details>

<details><summary>ヒント3</summary>

`field=price`のクエリは`WHERE price = {q}`とクォートなしでそのまま埋め込まれる。
03/06で見た「numeric contextはクォート不要」パターンと同じ抜け道。`field`を
`price`に固定した上で、`q`にUNION SELECTを流し込め。

</details>

<details><summary>解答</summary>

送るリクエスト:
```
GET /search?field=price&q=0 UNION SELECT id,flag,NULL FROM flags-- -
```

サーバー側で組み立てられる実際のSQLはこうなる:
```sql
SELECT id, name, description FROM products
WHERE price = 0 UNION SELECT id,flag,NULL FROM flags-- -
```

分解すると:
- `field=price` — サーバーを「クォート不要のnumeric context」分岐に誘導する。これが
  なければ`q`はエスケープされ、注入は成立しない
- `q=0 UNION SELECT id,flag,NULL FROM flags-- -` — `price = 0`は偽(該当なし)、
  そこに`UNION SELECT`で`flags`テーブルの行を、`products`と同じ3カラムの形
  (id, name, description)に変形して混ぜ込む。`id,flag`は型が合うので、残り1カラムは
  `NULL`で埋める

`field`だけ、`q`だけではこの脆弱性は成立しない。`field=price`が数値専用の
未エスケープ経路を開き、`q`側がその経路にpayloadを流し込む — 2パラメータの
組み合わせで初めて崩れるWHERE句であることを見抜くのがこの問題の核心。

sqlmapを使う場合:
```
sqlmap -u "http://localhost:3005/search?field=price&q=1" -p q --dump
```

</details>
