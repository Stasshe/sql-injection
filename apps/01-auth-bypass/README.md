# 01 - Auth Bypass

`http://localhost:3001` の管理画面にログインし、adminとしてflagを取得せよ。
`server.js`のソースコードは読んでよい。

## ヒント

<details><summary>ヒント1</summary>

`server.py`の`/login`エンドポイントを見ろ。SQLクエリはどう組み立てられている?

</details>

<details><summary>ヒント2</summary>

ユーザー入力(`username`, `password`)がクォート内にそのまま埋め込まれている。
SQL文字列の中で`'`(シングルクォート)を使うとどうなるか。

</details>

<details><summary>ヒント3</summary>

`--`はMySQLのコメント開始。**ただし直後に半角スペース(または改行等)が必須**。
`admin' --`(スペース無し)のように詰めて打つとSQL構文エラーになる。忘れやすい罠なので注意。
スペースを付けたくないなら`#`を使う手もある(`#`は直後の文字を問わず行末までコメントになる)。

</details>

<details><summary>解答</summary>

usernameフィールドに以下を入れてログイン(passwordは何でもよい)。**末尾のスペースを忘れると
SQL構文エラーになるので注意**:

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
スペースを付け忘れやすい場合は`admin'#`のように`#`を使ってもよい(スペース不要)。

</details>
