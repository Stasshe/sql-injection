# SQL Injection CTF

SQLインジェクション未経験者向けの教材。全6問、Docker + Python/Flask。ソースコードは全部公開(白箱)。
各問のヒント・解答は`apps/NN-*/README.md`にある。設計背景は[INTENT.md](./INTENT.md)、
詳細仕様は[SPECIFICATION.md](./SPECIFICATION.md)。

**配布時の注意**: flagの実値は`.env`にのみ置く(gitignore済み)。それ以外(`server.py`,
`db/*.sql`, `db/*.sh`など)はリポジトリごと公開してよい。詳細は[INTENT.md](./INTENT.md)。

## 起動

```
cp .env.example .env   # 初回のみ。中身のFLAG_01〜FLAG_06は自由に書き換えてよい
docker compose up --build
```

初回はMySQLの初期化に少し時間がかかる。各appは自前でDB接続をリトライするので、
起動順を気にする必要はない。

## 問題一覧

| # | URL | 技術 | 難易度 |
|---|-----|------|--------|
| 01 | http://localhost:3001 | 認証バイパス(tautology) | 入門 |
| 02 | http://localhost:3002 | UNION-based抽出 | 基礎 |
| 03 | http://localhost:3003 | ORで全件表示 | 入門 |
| 04 | http://localhost:3004 | 大文字小文字によるフィルタ回避 | 入門 |
| 05 | http://localhost:3005 | 価格検索へのOR注入 | 入門 |
| 06 | http://localhost:3006 | Boolean-blindで1桁判定 | 入門 |

## 進め方

1. まず各アプリを実際に触って正規の使い方を確認する。
2. `apps/NN-*/server.py`のソースを読み、クエリがどう組み立てられているか確認する。
3. 詰まったら該当READMEのヒントを1段階ずつ開く。各問は前の問題で使った考え方を
   ほぼそのまま再利用できる。

## 停止・後片付け

```
docker compose down -v
```

`-v`をつけるとDBのボリュームも削除され、次回`up`で全問題が初期状態から再構築される。
