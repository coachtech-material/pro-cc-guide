# 3-6-0 Chapter 6 の地図

> Part 3 の最終 Chapter です。これまで Claude Code と協働してバグ修正・機能開発・リファクタリングを遂行してきましたが、実務ではここからが本番です。書いたコードをチームに共有し、レビューを受け、本番環境に届けるまでが仕事です。この Chapter では、AI 生成コードをチームに届けるときの責任と仕組みを学びます。

## セクション一覧

### 3-6-1 AI 時代のチーム開発 ｜ 📖 読んで学ぶ

- 「AI が書いた」は言い訳にならない説明責任の原則と「説明できるか」テスト
- AI 生成コード増加によるレビュー負荷と PR 説明（Summary / Approach / Testing / Impact）での対策
- 帰属表示設定（`attribution.commit` / `attribution.pr`）のチーム方針の選び方
- CLAUDE.md・rules・skills・settings.json をチームの成果物として共有する考え方

### 3-6-2 CourseHub の変更をチームに届ける ｜ 📖🏃 読んで手を動かす

- PR 作成時の自己レビュー（規約準拠・テスト十分性・セキュリティ確認）
- `.github/workflows/claude.yml` での GitHub Actions 自動レビュー設定と GitHub Secrets での API キー管理
- `.claude/settings.json`（Project スコープ）と `.claude/settings.local.json`（Local スコープ）の分離
- 繰り返し使うワークフローの Skill 化によるチーム標準化

## 📖 この Chapter の進め方

3-6-1 で AI 生成コードをチームに共有する際の考え方を学び、3-6-2 で CourseHub の変更を実際にチームに届ける実践を行います。Part 2 で学んだ Git 操作（[2-3-7](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-7_GitとWorktree.md)）と GitHub Actions（[2-3-8](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-8_GitHub%20Actions.md)）の知識を実務コンテキストで総動員します。
