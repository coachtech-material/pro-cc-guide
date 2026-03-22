# 2-2-1 CLAUDE.md と `/init` でプロジェクトを準備する

## 概要

前の Chapter では、Claude Code の基本操作を体験し、バイブコーディングの光と影を知りました。ここからは、テック記事プラットフォームを Claude Code と一緒にゼロから構築していきます。

このセクションでは、まず Part 2 を通して作るアプリの全体像を把握し、Laravel Sail でプロジェクトを作成します。そして、Claude Code がプロジェクトの文脈を理解するための仕組みである **CLAUDE.md** を整備します。CLAUDE.md を適切に書くことで、Claude Code の出力品質は大きく変わります。解説しながら手を動かしていきますので、ターミナルを開いて一緒に進めましょう。

## テック記事プラットフォームの全体像

Part 2 では、皆さんが日常的に使っている Zenn や Qiita のようなテック記事プラットフォームを構築します。Chapter を進めるごとに機能が増えていき、最終的には以下の機能を備えたアプリが完成します。

- 検索・フィルタ・ソート・ページネーション付き記事一覧
- Markdown 記事の作成・プレビュー
- 公開ワークフロー（下書き → レビュー → 公開）
- ロール別アクセス制御（管理者 / 著者）
- タグ・コメント・シリーズ（Zenn の「本」に相当）
- いいね・トレンドランキング
- ブックマーク・コレクション
- 著者プロフィール・ダッシュボード
- フォロー・フィード

モデル構成は 10 モデル + 中間テーブル 2 つです。

```
User（role: admin / author）
├── Profile（自己紹介、SNSリンク）+ 著者ダッシュボード（統計）
├── Article（title, body_markdown, status: draft/review/published）
│   ├── ArticleTag（多対多の中間テーブル）
│   ├── Comment（ネスト対応）
│   ├── Like + トレンドランキング
│   ├── Bookmark + コレクション管理
│   └── Series（シリーズ名・説明）+ article_series 中間テーブル（順序管理）
└── Follow（ユーザー間フォロー）+ フォローフィード

Category（記事カテゴリ）
Tag（技術タグ）
```

このセクションでは全体像を把握するだけで十分です。各機能は Chapter を進めながら段階的に実装していきます。

💡 テック記事プラットフォームはモデルケースです。別のアプリを作りたい場合はそれで構いません。大切なのは各 Chapter で Claude Code の機能を使い、生成コードを自分で確認することです。

## プロジェクト作成

Laravel 10 + Sail でプロジェクトを作成します。COACHTECH の環境構築と同じ手順なので、簡潔に進めます。

まず、プロジェクトを作成します。`laravel.build` ではなく `composer create-project` でバージョンを明示してください。`laravel.build` は最新版がインストールされるため、この教材では使用しません。

```bash
docker run --rm -v $(pwd):/app -w /app composer create-project laravel/laravel:^10.0 tech-article-platform
cd tech-article-platform
```

Sail を導入します。

```bash
docker run --rm -v $(pwd):/app -w /app composer require laravel/sail --dev
docker run --rm -v $(pwd):/app -w /app php artisan sail:install --with=mysql
```

`.env` の DB 接続設定を確認してください。Sail 環境では `DB_HOST=mysql` になっている必要があります。

Sail を起動し、アプリケーションキーを生成します。

```bash
./vendor/bin/sail up -d
./vendor/bin/sail artisan key:generate
```

Tailwind CSS と Alpine.js をセットアップします。

```bash
./vendor/bin/sail npm install
./vendor/bin/sail npm install -D tailwindcss@3 postcss autoprefixer alpinejs
./vendor/bin/sail npx tailwindcss init -p
```

`tailwind.config.js` と `resources/css/app.css`、`resources/js/app.js` を Tailwind CSS + Alpine.js に対応させてください。COACHTECH の教材で設定した内容と同じです。

開発中は Vite の開発サーバーを常時起動しておきます。

```bash
./vendor/bin/sail npm run dev
```

💡 `sail npm run dev` を実行しないと、Tailwind CSS のスタイルがビルドされず UI が反映されません。開発中は別のターミナルタブで常に実行しておきましょう。

ブラウザで `http://localhost` を開き、Laravel のウェルカムページが表示されれば成功です。

⚠️ よくあるエラー: ポート競合

```
Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use
```

**原因**: 別のプロセスがポート 80 を使用しています。

**対処法**: `.env` の `APP_PORT` を変更するか、競合しているプロセスを停止してください。`APP_PORT=8080` に変更した場合、ブラウザでは `http://localhost:8080` でアクセスします。

⚠️ `.env` ファイルの取り扱い注意

`.env` にはデータベースのパスワードやアプリケーションキーなどの機密情報が含まれます。Claude Code に `.env` の内容を直接渡さないでください。Claude Code は会話の内容を Anthropic のサーバーに送信するため、機密情報が外部に送られるリスクがあります。`.env` の設定を確認・変更する作業は、自分でエディタを開いて行いましょう。

## CLAUDE.md の整備

### なぜ CLAUDE.md が必要なのか

前の Chapter で、Claude Code に一言指示するだけで動くアプリが生まれることを体験しました。しかし、Claude Code は皆さんのプロジェクトについて何も知りません。技術スタックも、ディレクトリ構成も、コマンド体系も知らない状態で作業を始めます。

たとえば、Laravel Sail を使っているプロジェクトで「マイグレーションを実行して」と指示したとします。Claude Code は `php artisan migrate` を実行しようとするかもしれません。しかし Sail 環境では、コマンドは Docker コンテナ内で実行する必要があるため、正しくは `./vendor/bin/sail artisan migrate` です。`php artisan migrate` はホストマシンで直接実行されるので、DB 接続に失敗します。

CLAUDE.md がない状態は、優秀なエンジニアがプロジェクトの README も読まずにコードを書き始めるようなものです。基本的なことで間違え、何度も手戻りが発生します。

### CLAUDE.md とは

CLAUDE.md はプロジェクトのルートに配置するマークダウンファイルです。Claude Code はセッション開始時にこのファイルを読み込み、プロジェクトの文脈として利用します。いわば、Claude Code への**プロジェクト専用の指示書**です。

CLAUDE.md には以下のような情報を書きます。

- プロジェクトの技術スタック
- コマンド体系（ビルド、テスト、デプロイ）
- コーディング規約やディレクトリ構成
- プロジェクト固有の注意事項

配置場所によってスコープが異なります。

| 配置場所 | スコープ | 共有範囲 |
|---|---|---|
| `./CLAUDE.md` または `./.claude/CLAUDE.md` | プロジェクト全体 | チームメンバー（Git 管理） |
| `~/.claude/CLAUDE.md` | ユーザー全体 | 自分のみ（全プロジェクト共通） |

プロジェクトレベルの CLAUDE.md は、プロジェクトルート直下（`./CLAUDE.md`）に置く方法と、`.claude/` ディレクトリ内（`./.claude/CLAUDE.md`）に置く方法があります。どちらもプロジェクト全体に適用されます。この教材ではプロジェクトルート直下に配置します。

💡 CLAUDE.md はサブディレクトリにも配置できます。たとえば `frontend/CLAUDE.md` に書いたルールは、Claude Code が `frontend/` 配下のファイルを扱うときに読み込まれます。大規模プロジェクトでフロントエンドとバックエンドでルールを分けたい場合に便利です。

### `/init` で CLAUDE.md を自動生成する

CLAUDE.md をゼロから手書きする必要はありません。Claude Code の `/init` コマンドを使えば、プロジェクトの構成を分析して CLAUDE.md のたたき台を自動生成してくれます。

Claude Code をプロジェクトディレクトリで起動しましょう。

```bash
cd tech-article-platform
claude
```

起動したら、以下を入力します。

```
> /init
```

Claude Code がプロジェクト内のファイル（`composer.json`、`package.json`、ディレクトリ構成など）を読み取り、技術スタックやビルドコマンドを推測して CLAUDE.md を生成します。diff が表示されるので、内容を確認して承認してください。

生成された CLAUDE.md を見てみましょう。おそらく、Laravel プロジェクトであること、PHP のバージョン、主要な依存パッケージなどが記載されているはずです。しかし、いくつか不足している情報があります。

### 手動で追記する

`/init` で生成された CLAUDE.md は出発点です。プロジェクト固有の情報を手動で追記します。特に重要なのは **Sail のコマンド体系** です。

以下のような内容を CLAUDE.md に追記してください。Claude Code に依頼しても、自分でエディタを開いて編集しても構いません。

```
> CLAUDE.mdに以下の内容を追記してください。
>
> ## コマンド体系
> このプロジェクトはLaravel Sailを使用しています。すべてのコマンドはSail経由で実行してください。
> - artisanコマンド: ./vendor/bin/sail artisan [command]
> - composerコマンド: ./vendor/bin/sail composer [command]
> - npmコマンド: ./vendor/bin/sail npm [command]
> - テスト実行: ./vendor/bin/sail artisan test
> - php artisan を直接実行しないでください（Docker外で実行され、DB接続に失敗します）
>
> ## 技術スタック
> - Laravel 10 / PHP
> - MySQL（Sail経由）
> - Blade + Tailwind CSS v3 + Alpine.js
> - Vite（アセットビルド）
```

この追記によって、Claude Code は以降のセッションで `php artisan` ではなく `./vendor/bin/sail artisan` を使うようになります。たった数行の記述ですが、これがないと Sail 環境で毎回エラーが発生し、その都度修正を依頼する手間が生じます。

CLAUDE.md に書いた内容は、セッションを終了しても保持されます。次回 `claude` を起動したとき、Claude Code は自動的に CLAUDE.md を読み込みます。一度整備すれば、そのプロジェクトで作業する限りずっと有効です。

💡 `.claude/rules/` ディレクトリを使うと、CLAUDE.md のルールをファイルごとに分割できます。たとえば `.claude/rules/testing.md` にテスト規約を書くと、CLAUDE.md が長くなりすぎることを防げます。ルールファイルは CLAUDE.md と同じ優先度で読み込まれます。今はファイルが増えるほどではないので、CLAUDE.md に直接書く形で進めます。

### CLAUDE.md を書くコツ

効果的な CLAUDE.md を書くためのポイントをいくつか紹介します。

- **簡潔に書く**: 1ファイルあたり 200 行以内を目安にします。長すぎると Claude Code のコンテキスト（記憶容量のようなもの。2-3 で詳しく学びます）を圧迫し、指示への従い方が不安定になります
- **具体的に書く**: 「コードをきれいに書いて」ではなく「インデントは4スペースを使う」のように、検証可能な形で書きます
- **矛盾させない**: 複数の CLAUDE.md ファイルで矛盾する指示があると、Claude Code の動作が不安定になります

## 見極めチェックの導入

次のセクションから、Claude Code にコードを生成させる作業が本格的に始まります。ここで、この教材全体を通して使う**見極めチェック**の仕組みを紹介します。

1-2-1 で学んだように、AI が生成したコードに対する責任は皆さん自身にあります。Claude Code がどんなに優秀でも、生成されたコードをそのまま受け入れるのではなく、自分で確認する習慣が必要です。

この教材では、コードを生成するセクションの末尾に **見極めチェック** というチェックリストを配置します。チェック項目は以下の3つの観点で構成されています。

- **正しさ**: 要件通りに動くか
- **品質**: 保守性・パフォーマンス・既存設計との一貫性は適切か
- **安全性**: 脆弱性がないか。認可・入力検証・機密情報の漏洩がないか

確認の手段は場面によって変わります。ブラウザで動作を確認する、コードを読んで設計を判断する、テストを実行するなど、セクションごとに適切な方法が異なります。各セクションの見極めチェックで具体的な確認方法を案内するので、最初は「こういう観点で見るのか」と知るところから始めましょう。次のセクションで、最初の見極めチェックを実践します。

💡 作業を中断して翌日に再開するときは、`claude -c` で直前のセッションを継続できます。ターミナルを閉じても会話の文脈は保持されるので、翌日にプロジェクトディレクトリで `claude -c` を実行すれば続きから作業できます。セッション管理の詳細は 2-3 で学びます。

## 公式ドキュメント

- [Memory](https://code.claude.com/docs/en/memory)（CLAUDE.md の仕組み、配置場所、読み込み順序）
- [Common Workflows](https://code.claude.com/docs/en/common-workflows)（`/init` による初期化など一般的なワークフロー）

## まとめ

- Part 2 では、Zenn や Qiita のようなテック記事プラットフォームを 10 モデル構成で段階的に構築します
- **CLAUDE.md** はプロジェクトの文脈を Claude Code に伝えるファイルです。セッション開始時に自動で読み込まれ、出力品質を大きく左右します
- `/init` で CLAUDE.md のたたき台を自動生成し、Sail コマンド体系や技術スタックを手動で追記します
- 特に **Sail のコマンド体系**（`./vendor/bin/sail artisan`）を書かないと、Claude Code が Docker 外でコマンドを実行してエラーになります
- コード生成のたびに**見極めチェック**（正しさ・品質・安全性）で生成コードを検証します。次のセクションから実践が始まります

次のセクションでは、Claude Code にテック記事プラットフォームの土台となるモデルと CRUD を生成させ、最初の見極めチェックを実践します。
