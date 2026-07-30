# 02 - OR Injection

`http://localhost:3002`の商品詳細から、非公開の商品に隠されたflagを表示せよ。
`server.py`は読んでよい。

この問題のテーマは、クォートで囲まれていない数値条件へ`OR`を追加すること。
商品IDに`1`を入れると1件だけ表示される。SQLの`OR`を使えば、すべての商品を
一度に表示できる。

## ヒント

<details><summary>ヒント1</summary>

`server.py`では商品IDを次のSQLへ直接入れている。

```sql
SELECT name, description, price FROM products WHERE id = 入力値
```

</details>

<details><summary>ヒント2</summary>

`OR 1=1`は「または、常に正しい」という条件になる。商品IDの後ろにつなげてみよう。

</details>

<details><summary>解答</summary>

商品IDへ次を入力する。

```
0 OR 1=1
```

実行されるSQL:

```sql
SELECT name, description, price FROM products WHERE id = 0 OR 1=1
```

`1=1`は必ず正しいため、すべての商品が表示される。`Internal Backup`の説明欄にflagがある。

</details>
