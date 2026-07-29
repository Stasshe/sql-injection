# 02 - UNION-based Search

`http://localhost:3002` の商品検索から、DB内のflagを抜き出せ。
`server.py`のソースコードは読んでよい。

このDBのテーブル構成:
- `products(id, name, description, price)` — 検索対象、4カラム
- `flags(id, flag)` — 無関係の別テーブル。目標はこの`flag`を検索結果に混ぜ込むこと

## ヒント

<details><summary>ヒント1</summary>

`server.py`の`/search`エンドポイントを見ろ。`?q=`の値はどう組み込まれている?

</details>

<details><summary>ヒント2</summary>

`q`は`LIKE '%...%'`の中にそのまま埋め込まれる。試しに`q`に`'`(シングルクォート)を1つだけ
送ってみろ。SQL構文エラーが返るはずだ → クォートを自分で閉じて、続きに好きなSQLを足せる
状態になっている。

</details>

<details><summary>ヒント3</summary>

`products`は4カラムなので、混ぜ込む`UNION SELECT`も4つの値を返す必要がある。型が違う
カラムには`NULL`を入れれば型エラーを回避できる(例: `UNION SELECT 1,'a','b',1`で試して
エラーが出ないか確認する)。

</details>

<details><summary>解答</summary>

送るpayload(`q`パラメータ):
```
zzz' UNION SELECT id,flag,NULL,NULL FROM flags-- -
```

これによりサーバー側で組み立てられる実際のSQLはこうなる:
```sql
SELECT id, name, description, price FROM products
WHERE name LIKE '%zzz' UNION SELECT id,flag,NULL,NULL FROM flags-- -%'
```

分解すると:
- `zzz` — 本来の検索語。適当な値でよく、存在しない商品名なので本来の検索結果は0件になる
- `' `— LIKE句のクォートを閉じる
- `UNION SELECT id,flag,NULL,NULL FROM flags` — `flags`テーブルの行を、`products`と同じ
  4カラムの形(id, name, description, price)に変形して結果に追加する。`id,flag`は型が
  合うのでそのまま、残り2カラムは`NULL`で埋める
- `-- -` — `--`はMySQLのコメント開始(直後に半角スペース必須)。これで末尾に残る`%'`を
  無効化している

結果、検索結果に`flags`テーブルの行が紛れ込み、`name`カラムの位置にflagが表示される。

### もっと自力で探したい場合

カラム数(4)を教えられずに解く場合は`ORDER BY`で探る:
```
q=zzz' ORDER BY 4-- -   -> 通る
q=zzz' ORDER BY 5-- -   -> エラー(5カラム目は存在しない)
```
エラーになる手前の数字がSELECT対象のカラム数。

</details>
