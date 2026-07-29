# INTENT

CTF初学者向けSQLi教材。座学でなく手を動かして技術を身につけさせるのが目的。

## なぜこの5問構成か

SQLiの代表的攻略技術を1問1技術で網羅する構成にした。入門〜中級序盤。

1. 認証バイパス(tautology/コメントアウト) — 最初の一歩。WHERE句が壊れる感覚を掴む
2. UNION-based抽出 — 別テーブルの値を結果に混ぜ込む。カラム数合わせが山場
3. Error-based抽出 — エラーメッセージ自体にデータを埋め込ませる
4. Boolean-blind — 画面に出るのはtrue/falseのみ。真偽の組み立てで1文字ずつ割り出す
5. Time-blind — 真偽すら見えない。応答時間の差だけが手がかり

技術の網羅性を優先し、実務でありがちな設定・背景付けはしていない。各問は独立した
Flask + MySQLで、問題間の依存はゼロ。

## 配布範囲(公開/非公開)

flagの実値は`.env`にのみ置き、`db/*.sql`(schema)には一切書かない。DBへの注入は
`db/02-flag.sh`が起動時に環境変数`FLAG`を読んでINSERTする(`.env`の値は
`docker-compose.yml`経由で各`db-*`サービスに渡る)。これにより:

- 公開してよい: `server.py`, `public/`, `README.md`, `db/*.sql`, `db/*.sh`, `docker-compose.yml`,
  `.env.example`。schemaに実値が入らないので、リポジトリのコードは丸ごと公開できる。
- 非公開(運営専用): `.env`のみ。ここに実際のflag文字列(`FLAG_01`〜`FLAG_05`)が入る。
  `.gitignore`済み、コミットされない。

CTFとして人に配る場合は`.env`を渡さず、参加者が自分でDockerを起動する場合は
`.env.example`をコピーして参加者自身が任意のダミー値を入れる(運営がホストする場合は
運営だけが本物の`.env`を持つ)。
