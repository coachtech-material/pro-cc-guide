# 2-2-1 CLAUDE.md と `/init` でプロジェクトを準備する

## 概要

前の Chapter で Claude Code の基本操作を体験しました。ここからは、Pro生の皆さんがテック記事プラットフォーム「mini Zenn」の構築に入ります。

Claude Code は優秀なアシスタントですが、皆さんのプロジェクトのことは何も知りません。使っているフレームワーク、コマンド体系、ディレクトリ構成——こうした「プロジェクトの文脈」を伝えなければ、Claude Code は的外れなコードを生成してしまいます。実務でも同じです。新しいプロジェクトに参加したとき、最初にやるのはプロジェクトの構成や開発ルールを把握することですよね。Claude Code にとっての「プロジェクトの把握」が、`CLAUDE.md` です。

このセクションでは、Laravel Sail でプロジェクトを作成し、`CLAUDE.md` を整備して Claude Code がプロジェクトを理解できる状態を作ります。解説しながら実際に手を動かしていきます。

## プロジェクト作成

### Laravel Sail でプロジェクトを作成する

mini Zenn のプロジェクトを Laravel Sail で作成します。Laravel Sail は Docker ベースの開発環境で、皆さんが COACHTECH で使い慣れた Docker Compose をラップしたものです。

では、プロジェクトを作成しましょう。

```bash
curl -s "https://laravel.build/mini-zenn" | bash
```

ダウンロードが完了したら、プロジェクトディレクトリに移動して Sail を起動します。

```bash
cd mini-zenn
./vendor/bin/sail up -d
```

`-d` はバックグラウンド起動のオプションです。起動が完了したら、ブラウザで `http://localhost` にアクセスして Laravel のウェルカムページが表示されることを確認しましょう。

<!-- TODO: 画像追加 - Laravel ウェルカムページ -->

> ⚠️ よくあるエラー: ポートの競合
>
> ```
> Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use
> ```
>
> **原因**: 他のプロジェクトやサービスがポート 80 を使用しています。
>
> **対処法**: 他の Docker コンテナを停止するか、`.env` の `APP_PORT` を変更してください（例: `APP_PORT=8080`）。

### `.env` の取り扱い注意

⚠️ `.env` ファイルにはデータベースのパスワードやアプリケーションキーなどの機密情報が含まれています。Claude Code に `.env` の内容を渡さないよう注意してください。

Claude Code は `@` でファイルを添付したり、プロンプトにファイルパスを含めると内容を読み取ります。`.env` を指示に含めたり、「`.env` を確認して」のような指示は避けましょう。

`.env` が `.gitignore` に含まれていれば、Git 操作で誤ってコミットされることはありませんが、Claude Code との対話の中で内容が送信されるリスクは別の問題です。`.env` の情報が必要な場合は、値そのものではなく「環境変数名」だけを伝えるようにしてください。

```
# NG: .env の内容を渡してしまう
@.env この設定を確認して

# OK: 環境変数名だけを伝える
DB_CONNECTIONにmysqlを使っています。Sailのデフォルト設定です
```

ここで `.env` が `.gitignore` に含まれていることを確認しておきましょう。Bash モードで確認できます。

```
! grep '\.env' .gitignore
```

`.env` が `.gitignore` に記載されていれば OK です。Laravel のデフォルトで含まれていますが、念のため確認する習慣をつけておきましょう。実務では `.env` がコミットに含まれていた事故が後を絶ちません。

## CLAUDE.md の整備

### CLAUDE.md の役割と仕組み

`CLAUDE.md` は、Claude Code にプロジェクトの文脈を伝えるためのファイルです。Claude Code はセッション開始時に `CLAUDE.md` を自動的に読み込み、その内容をすべての応答の前提とします。

`CLAUDE.md` に書く内容は、たとえば以下のようなものです。

- **技術スタック**: 使用フレームワーク、バージョン、主要ライブラリ
- **コマンド体系**: ビルド、テスト、マイグレーションなどの実行コマンド
- **ディレクトリ構成**: プロジェクト固有の構成ルール
- **コーディング規約**: 命名規則、フォーマット、設計方針

実務で新しいプロジェクトに参加するとき、README やプロジェクトの Wiki を読んで開発ルールを把握するのと同じです。`CLAUDE.md` は「Claude Code 向けの README」だと思ってください。

### 配置場所と読み込み順序

`CLAUDE.md` はプロジェクト内の複数の場所に配置でき、それぞれスコープ（適用範囲）が異なります。

| 配置場所 | スコープ | 用途 |
|---|---|---|
| `./CLAUDE.md` または `./.claude/CLAUDE.md` | プロジェクト全体 | チームで共有する開発ルール。Git にコミットする |
| `~/.claude/CLAUDE.md` | ユーザー全体 | 個人の好みや共通設定。すべてのプロジェクトに適用される |

プロジェクトの `CLAUDE.md` に書くのは、チームメンバー全員が従うべきルールです。「インデントはスペース4つ」「テストは `sail test` で実行する」といった内容です。ユーザーレベルの `CLAUDE.md` には、「日本語で応答して」のような個人的な好みを書きます。

読み込み順序は、ユーザーレベル → プロジェクトレベルの順です。プロジェクトレベルの方が優先度が高いため、プロジェクト固有のルールがユーザーの設定を上書きします。

さらに、サブディレクトリに配置した `CLAUDE.md` は、Claude Code がそのディレクトリ内のファイルを読んだときにオンデマンドで読み込まれます。たとえば `tests/CLAUDE.md` に「テストではファクトリーを使う」と書いておけば、テスト関連の作業時にだけそのルールが適用されます。

### `/init` で CLAUDE.md を自動生成する

`CLAUDE.md` をゼロから書くのは大変です。Claude Code の `/init` コマンドを使えば、プロジェクトのコードベースを分析して `CLAUDE.md` のたたき台を自動生成してくれます。

では、mini-zenn ディレクトリで Claude Code を起動して `/init` を実行しましょう。

```bash
claude
```

```
/init
```

Claude Code がプロジェクトの構成を読み取り、ビルドコマンド、テスト手順、プロジェクトの規約などを含む `CLAUDE.md` を生成します。diff が表示されたら内容を確認して承認してください。すでに `CLAUDE.md` が存在する場合は、上書きではなく改善提案をしてくれます。

<!-- TODO: 画像追加 - /init 実行後の CLAUDE.md 生成画面 -->

### 手動で追記する

自動生成された内容はあくまでたたき台です。プロジェクト固有のルールや、Claude Code に特に守ってほしいことは手動で追記しましょう。

`/init` で生成された `CLAUDE.md` に、技術スタック・Sail コマンド体系・ディレクトリ構成を追記します。Claude Code に以下のように指示してみましょう。

```
CLAUDE.mdに以下の情報を追記してください。

## 技術スタック
- PHP 8.x / Laravel 10
- Laravel Sail（Docker ベース開発環境）
- MySQL 8.0
- Blade + Tailwind CSS
- PHPUnit

## コマンド
- サーバー起動: `./vendor/bin/sail up -d`
- Artisan: `./vendor/bin/sail artisan <command>`
- テスト: `./vendor/bin/sail test`
- マイグレーション: `./vendor/bin/sail artisan migrate`
- Composer: `./vendor/bin/sail composer <command>`

## ディレクトリ構成
Laravel のデフォルト構成に従う。主要ディレクトリ:
- `app/Models/` — Eloquent モデル
- `app/Http/Controllers/` — コントローラー
- `resources/views/` — Blade テンプレート
- `routes/web.php` — Web ルーティング
- `database/migrations/` — マイグレーション
- `database/seeders/` — シーダー
- `tests/Feature/` — Feature テスト
```

diff が表示されたら、追記された内容を確認して承認してください。

特に **Sail コマンド体系**は重要です。Laravel Sail を使うプロジェクトでは、`php artisan` の代わりに `sail artisan` を使います。これを `CLAUDE.md` に明記しておかないと、Claude Code は `php artisan` でコマンドを実行しようとして失敗します。

💡 `CLAUDE.md` は長くなりすぎないよう注意してください。目安は 200 行以内です。Claude Code はセッション開始時に `CLAUDE.md` を全文読み込むため、内容が多すぎるとコンテキストを圧迫し、重要な指示が無視される原因になります。必要十分な情報を簡潔に書くことを心がけましょう。

### `.claude/rules/` でルールをファイル分割する

💡 プロジェクトが成長してルールが増えてきたら、`CLAUDE.md` に全部書くのではなく、`.claude/rules/` ディレクトリにファイル分割できます。

```
.claude/
└── rules/
    ├── coding-style.md    # コーディング規約
    ├── testing.md         # テスト方針
    └── frontend/
        └── blade.md       # Blade テンプレートのルール
```

`.claude/rules/` に置いたファイルは、`CLAUDE.md` と同じようにセッション開始時に読み込まれます。さらに、YAML フロントマターの `paths` フィールドを使えば、特定のファイルタイプにだけルールを適用することもできます。

```markdown
---
paths:
  - "resources/views/**/*.blade.php"
---

Blade テンプレートでは Tailwind CSS のユーティリティクラスを使用する。
コンポーネントは `resources/views/components/` に配置する。
```

この例では、Blade ファイルに関連する作業をしているときだけ、このルールが読み込まれます。

mini Zenn ではまだルールが少ないので、`CLAUDE.md` 1ファイルで十分です。プロジェクトが育ってきたら、ルールの分割を検討してみてください。

## 公式ドキュメント

- [Memory](https://code.claude.com/docs/en/memory)
- [Common workflows](https://code.claude.com/docs/en/common-workflows)

## まとめ

- Laravel Sail でプロジェクトを作成し、`sail up -d` で起動する
- `CLAUDE.md` は Claude Code にプロジェクトの文脈を伝えるファイル。セッション開始時に自動で読み込まれる
- `/init` でたたき台を自動生成し、技術スタック・コマンド体系・ディレクトリ構成を手動で追記する
- `.env` は Claude Code に渡さない。環境変数名だけ伝える
- ルールが増えたら `.claude/rules/` でファイル分割できる
- `CLAUDE.md` は 200 行以内を目安に、必要十分な情報を簡潔に書く

次のセクションでは、この `CLAUDE.md` を備えた mini Zenn プロジェクトで、Claude Code にモデル設計とコード生成を依頼します。
