# 01 - Login Bypass

`http://localhost:3001` の管理画面にログインし、adminとしてflagを取得せよ。
ソースコード(`server.js`, `db/init.sql`)は全部読んでよい。

## ヒント

<details><summary>ヒント1</summary>

`server.js`の`/login`エンドポイントを見ろ。SQLクエリはどう組み立てられている?

</details>

<details><summary>ヒント2</summary>

ユーザー入力(`username`, `password`)がクォート内にそのまま埋め込まれている。
SQL文字列の中で`'`(シングルクォート)を使うとどうなるか。

</details>

<details><summary>ヒント3</summary>

`--`はMySQLのコメント開始(直後にスペース必須)。WHERE句の一部をコメントアウトできれば
password条件自体を消せる。

</details>

<details><summary>解答</summary>

usernameフィールドに以下を入れてログイン(passwordは何でもよい):

```
admin' -- 
```

これによりクエリは
```sql
SELECT * FROM users WHERE username = 'admin' -- ' AND password = '...'
```
となり、`--`以降がコメントアウトされpassword比較自体が消える。`admin`ユーザーとして
そのままログイン成立、`is_admin`が真なのでdashboardにflagが表示される。

`' OR '1'='1' -- ` でも(先頭行=adminがヒットするため)同様に通る。

**現実のミス**: パスワードを平文でDBに保存し、かつSQLを文字列結合で組み立てている。
どちらか片方だけでも問題だが、両方揃うとSQLi一発で全ユーザーの認証情報が完全に無効化される。

</details>
