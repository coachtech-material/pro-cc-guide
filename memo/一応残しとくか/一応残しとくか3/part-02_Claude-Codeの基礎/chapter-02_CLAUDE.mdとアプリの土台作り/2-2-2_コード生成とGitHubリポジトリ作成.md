# 2-2-2 コード生成と GitHub リポジトリ作成

## 概要

前のセクションで `CLAUDE.md` を整備し、Claude Code がプロジェクトの文脈を理解できる状態になりました。ここからは、Claude Code の真骨頂——コード生成——を体験します。

「Claude Code が書いたコードを自分で読む」——この習慣は、AI との協働で品質を担保するための基本です。生成されたコードをそのまま受け入れるのではなく、自分が理解し、判断した上で適用する。この「見極める力」の第一歩をここで踏み出します。

このセクションでは、Claude Code に mini Zenn のモデル設計と CRUD を依頼し、生成されたコードを確認した上で、GitHub リポジトリに保存するところまで進めます。解説しながら実際に手を動かしていきます。

## コード生成と確認

### Claude Code にモデル設計を依頼する

mini Zenn の最初の3つのモデル——User、Article、Category——を Claude Code に作らせましょう。Claude Code が `CLAUDE.md` を読んでいるので、Sail 環境での作業であることを理解した上でコードを生成してくれます。

プロンプトの書き方がポイントです。何を作りたいかだけでなく、テーブル設計の詳細を伝えると、より的確なコードが生成されます。Claude Code が起動していない場合は、mini-zenn ディレクトリで起動してください。

```bash
cd mini-zenn
claude
```

以下の指示を送りましょう。

```
mini Zennというテック記事プラットフォームを作ります。
以下の3つのモデル・マイグレーション・リレーションと、ArticleのCRUD（Controller, Blade, Route）、
Seeder（Category 5件、Article 10〜15件、テスト用User 1人）を一括で作成してください。

1. User — roleカラム追加（enum: admin, author。デフォルト: author）
2. Article — user_id, category_id(nullable), title(string), body_markdown(text), status(enum: draft/review/published, デフォルト: draft), published_at(nullable timestamp)
3. Category — name(unique), slug(unique)

リレーション:
- User has many Articles
- Article belongs to User, belongs to Category
- Category has many Articles
```

テーブル構成・カラム型・リレーションを具体的に伝えることで、Claude Code はマイグレーション、モデルクラス、Controller、Blade テンプレート、ルート定義、Seeder を一括で生成します。diff が複数回表示されるので、1つずつ内容を確認して承認していきましょう。

Claude Code はエージェントループ（Chapter 2-1 で紹介しました）で作業を進めます。ターミナル上で Claude Code がどのツールを使っているか——ファイルの読み取り、作成、編集——を観察してみてください。

### マイグレーションとシーディングを実行する

コードが生成されたら、マイグレーションとシーディングを実行してサンプルデータを投入します。

```
! ./vendor/bin/sail artisan migrate --seed
```

エラーなく完了すれば成功です。

> ⚠️ よくあるエラー: データベース接続エラー
>
> ```
> SQLSTATE[HY000] [2002] Connection refused
> ```
>
> **原因**: Sail のコンテナが起動しきっていない、または MySQL コンテナの準備が完了していません。
>
> **対処法**: `./vendor/bin/sail up -d` で Sail が起動していることを確認し、数秒待ってから再実行してください。`./vendor/bin/sail mysql` で MySQL に接続できるか確認するのも有効です。

### ブラウザで動作確認する

ブラウザで `http://localhost/articles` にアクセスし、記事一覧が表示されることを確認してください（URL はルート定義によって異なる場合があります。`./vendor/bin/sail artisan route:list` コマンドでルート一覧を確認できます）。

<!-- TODO: 画像追加 - 記事一覧画面 -->

以下の操作を試してみましょう。

- 記事一覧の表示
- 記事の詳細表示
- 新規記事の作成
- 記事の編集
- 記事の削除

### 生成されたコードを確認する

ここで一度立ち止まって、Claude Code が生成したコードを自分の目で確認しましょう。Claude Code に「確認して」と聞くのではなく、皆さん自身がコードを読みます。

**マイグレーション**を確認します。`database/migrations/` ディレクトリにあるファイルを開き、以下の点を見てください。

- カラム型は意図通りか（例: `body_markdown` が `text` 型になっているか）
- NOT NULL / nullable の設定は正しいか
- 外部キー制約が設定されているか（`->constrained()` や `->foreign()`）
- インデックスが適切に設定されているか（`status` や `slug` にインデックスはあるか）

**Controller** を確認します。`app/Http/Controllers/ArticleController.php` を開き、以下を見てください。

- 各アクションが意図通りの処理をしているか
- Eloquent のリレーション（`with('category')` など）が使われているか
- バリデーションはあるか（この段階ではなくても OK。Chapter 2-6 で追加します）

**Blade テンプレート**を確認します。`resources/views/articles/` の各ファイルを見てください。

- 一覧・詳細・作成・編集の画面が揃っているか
- レイアウトの構造は妥当か

**ルート定義**を確認します。`routes/web.php` を開き、リソースルートが追加されていることを確認してください。Article の CRUD に必要なルート（index, create, store, show, edit, update, destroy）が揃っていることを確認しましょう。

## GitHub リポジトリの作成

### `gh` CLI のインストールと認証

プロジェクトを GitHub に保存するために、GitHub CLI（`gh`）を使います。皆さんは COACHTECH で Git/GitHub を使ってきたので、基本的な操作は馴染みがあるはずです。

`gh` CLI がインストールされていない場合は、インストールしてください。

**macOS（Homebrew）:**

```bash
brew install gh
```

**WSL（Linux）:**

```bash
sudo apt install gh
```

インストールしたら、GitHub アカウントで認証します。

```bash
gh auth login
```

対話形式で認証方法を選択できます。「GitHub.com」→「HTTPS」→「Login with a web browser」の順に選ぶと、ブラウザで認証を完了できます。

### GitHub リポジトリの作成と初回 push

`gh repo create` でリポジトリを作成し、コードを push しましょう。

```bash
git init
git add -A
git commit -m "Initial commit: Laravel Sail project with Article CRUD"
gh repo create mini-zenn --private --source=. --push
```

`gh repo create` のオプションの意味は以下の通りです。

| オプション | 説明 |
|---|---|
| `--private` | プライベートリポジトリとして作成する |
| `--source=.` | 現在のディレクトリをソースとして指定する |
| `--push` | 作成と同時に push する |

💡 `--private` と `--public` はプロジェクトに応じて選んでください。実務では、企業のリポジトリは通常プライベートです。

💡 Claude Code に「GitHubリポジトリを作成してpushして」と指示することもできます。Claude Code は `gh` CLI を使ってリポジトリの作成から push までを自動で実行してくれます。ただし、リポジトリ名やプライベート/パブリックの設定は指示に含めましょう。

## 👀 確認ポイント（コードレビュー）

ここで、生成されたマイグレーションファイルを改めて自分で読む練習をします。`database/migrations/` のファイルを開いて、以下の点を確認してください。

**カラム型と制約:**
- `body_markdown` は `text` 型か（`string` だと長い記事が入りません）
- `status` は `enum` またはそれに相当する型か
- `published_at` は `nullable` か（下書きの段階では公開日がないため）
- `category_id` は `nullable` か（カテゴリ未設定の記事があり得るため）

**外部キー:**
- `articles` テーブルの `user_id` に外部キー制約が設定されているか
- `onDelete` の挙動は設定されているか（ユーザーが削除されたとき記事はどうなるべきか）

**インデックス:**
- `status` カラムにインデックスはあるか（公開記事の検索で使う）
- `categories` テーブルの `slug` に unique インデックスはあるか

意図と異なる箇所が見つかった場合は、Claude Code に理由を聞いてみましょう。

```
マイグレーションで articles テーブルの status カラムにインデックスがないのですが、
公開記事のフィルタリングで使うので追加してもらえますか？
```

「なぜそうなっているのか」を聞き、納得した上で修正を依頼する。このやり取りが、Claude Code との協働における「見極める力」の実践です。

## 公式ドキュメント

- [Interactive mode](https://code.claude.com/docs/en/interactive-mode)
- [Tools reference](https://code.claude.com/docs/en/tools-reference)
- [Commands](https://code.claude.com/docs/en/commands)

## まとめ

- Claude Code にモデル設計を依頼するときは、テーブル構成・カラム型・リレーションを具体的に伝えると的確なコードが生成される
- 生成されたコード（マイグレーション、Controller、Blade、Route）は自分の目で確認する。特にマイグレーションのカラム型・制約・インデックスは重要
- Seeder でサンプルデータを投入し、ブラウザで動作確認する
- `gh repo create` で GitHub リポジトリを作成し、初回コミットを push する
- 意図と異なる箇所を見つけたら、Claude Code に理由を聞き、納得してから修正を依頼する。これが「見極める力」の第一歩

次の Chapter では、Claude Code がどのように動いているか——エージェントループの仕組みとコンテキストの管理方法——を学びます。Claude Code をより効率的に使うための知識です。
