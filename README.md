# SQL Injection CTF

SQLインジェクション入門教材。全3問、Docker + Node.js/Express。ソースコードは全部公開(白箱)。
各問のヒント・解答は`apps/NN-*/README.md`にある。設計背景は[INTENT.md](./INTENT.md)、
詳細仕様は[SPECIFICATION.md](./SPECIFICATION.md)。

## 起動

```
docker compose up --build
```

初回はMySQLの初期化に少し時間がかかる。各appは自前でDB接続をリトライするので、
起動順を気にする必要はない。

## 問題一覧

| # | URL | 概要 | 難易度 |
|---|-----|------|--------|
| 01 | http://localhost:3001 | ログインフォームを突破してadminになれ | 基礎 |
| 02 | http://localhost:3002 | 商品検索からDB内のflagを抜き出せ(UNION) | 中級手前 |
| 03 | http://localhost:3003 | 応答は真偽値のみ。blindでflagを抜き出せ | 中級 |

## 進め方

1. まず各アプリを実際に触って正規の使い方を確認する。
2. `apps/NN-*/server.js`のソースを読み、クエリがどう組み立てられているか確認する。
3. 詰まったら該当READMEのヒントを1段階ずつ開く。

## 停止・後片付け

```
docker compose down -v
```

`-v`をつけるとDBのボリュームも削除され、次回`up`で全問題が初期状態から再構築される。
