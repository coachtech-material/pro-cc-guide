# 2-2-2 コード生成と GitHub リポジトリ作成

## 概要

前のセクションで、Laravel Sail のプロジェクトを作成し、CLAUDE.md を整備しました。このセクションでは、いよいよ Claude Code にテック記事プラットフォームの土台となるコードを生成させます。

ここでのポイントは2つあります。1つ目は、Claude Code への**指示の出し方**です。序盤ではテーブル設計やカラム型を具体的に伝えることで、Claude Code が的確なコードを生成できるようにします。2つ目は、生成されたコードを**自分の目で確認する**ことです。前のセクションで導入した見極めチェックの最初の実践になります。

## コード生成と確認

### 具体的な指示で的確なコードを引き出す

Claude Code はテーブル設計やリレーションを具体的に伝えるほど、意図に沿ったコードを生成します。「記事管理機能を作って」のような曖昧な指示でも何かは生成されますが、カラム型やリレーションの判断が Claude 任せになり、意図と異なる結果になりやすくなります。

この教材の序盤では、実装の粒度で指示を出します。Claude Code の動きを把握しながら、生成されるコードと指示の関係を理解するためです。Chapter が進むにつれて、指示は徐々に抽象的になり、ビジネス要件レベルの一言で大きな機能を任せられるようになっていきます。

### モデル・CRUD を一括生成する

Claude Code がインタラクティブモードで起動していない場合は、プロジェクトディレクトリで起動してください。

```bash
cd tech-article-platform
claude
```

以下のプロンプトを入力します。3つのモデルのテーブル設計を具体的に伝えています。

```
> 以下の3つのモデルとマイグレーション、リレーション、Controller、Blade テンプレート、Route、Seederを作成してください。
>
> 1. User（name, email, password）
>    - Laravel標準のusersテーブルをそのまま使用
>
> 2. Category
>    - name: string(50)
>    - slug: string(50), unique
>
> 3. Article
>    - user_id: foreignId（usersへの外部キー）
>    - category_id: foreignId（categoriesへの外部キー、nullable）
>    - title: string(255)
>    - body_markdown: text
>    - status: enum('draft', 'review', 'published'), デフォルト'draft'
>    - published_at: timestamp, nullable
>
> 記事一覧ページには以下の機能をつけてください:
> - キーワード検索（タイトルと本文を対象）
> - カテゴリでの絞り込み
> - ステータスでの絞り込み
> - 公開日の新しい順・古い順のソート
> - ページネーション（1ページ15件）
>
> 記事一覧でMarkdownの本文を抜粋表示してください。
> Seederでは、カテゴリ5件、ユーザー3件、記事30件のダミーデータを作成してください。
```

Claude Code が動き始めます。マイグレーション、モデル、コントローラ、Blade テンプレート、ルート定義、シーダーと、複数のファイルにわたるコードが次々に生成されます。diff が表示されたら、内容を確認して承認してください。

皆さんの環境では異なるコードが生成されます。以下は一例です。

マイグレーションでは、指示したカラム型が反映されているかを確認します。

```php
// database/migrations/xxxx_create_articles_table.php
Schema::create('articles', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->cascadeOnDelete();
    $table->foreignId('category_id')->nullable()->constrained()->nullOnDelete();
    $table->string('title', 255);
    $table->text('body_markdown');
    $table->enum('status', ['draft', 'review', 'published'])->default('draft');
    $table->timestamp('published_at')->nullable();
    $table->timestamps();
});
```

モデルでは、リレーションが正しく定義されているかを確認します。

```php
// app/Models/Article.php
class Article extends Model
{
    protected $fillable = [
        'user_id', 'category_id', 'title', 'body_markdown', 'status', 'published_at',
    ];

    protected $casts = [
        'published_at' => 'datetime',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function category()
    {
        return $this->belongsTo(Category::class);
    }
}
```

コントローラでは、検索・フィルタ・ソート・ページネーションのクエリ構築を確認します。

```php
// app/Http/Controllers/ArticleController.php
public function index(Request $request)
{
    $query = Article::with(['user', 'category']);

    if ($request->filled('keyword')) {
        $keyword = $request->keyword;
        $query->where(function ($q) use ($keyword) {
            $q->where('title', 'like', "%{$keyword}%")
              ->orWhere('body_markdown', 'like', "%{$keyword}%");
        });
    }

    if ($request->filled('category')) {
        $query->where('category_id', $request->category);
    }

    if ($request->filled('status')) {
        $query->where('status', $request->status);
    }

    $sortOrder = $request->input('sort', 'desc');
    $query->orderBy('published_at', $sortOrder);

    $articles = $query->paginate(15);

    return view('articles.index', compact('articles'));
}
```

すべての diff を承認したら、マイグレーションとシーダーを実行します。Claude Code に依頼しましょう。

```
> マイグレーションとシーダーを実行してください
```

Claude Code が以下のようなコマンドを実行しようとするはずです。

```bash
./vendor/bin/sail artisan migrate
./vendor/bin/sail artisan db:seed
```

CLAUDE.md に Sail コマンド体系を書いておいたので、`php artisan` ではなく `./vendor/bin/sail artisan` が使われています。前のセクションで CLAUDE.md を整備した効果がここで確認できます。

### ブラウザで動作確認

ブラウザで記事一覧ページにアクセスしてみましょう。URL はルート定義によって異なりますが、`http://localhost/articles` のようなパスになっているはずです。ルート定義がわからない場合は、Claude Code に聞いてみてください。

```
> 記事一覧ページのURLを教えてください
```

ブラウザで以下の操作を試して、機能が動作することを確認します。

- 記事一覧が表示され、ダミーデータの記事が並んでいるか
- 記事の新規作成ができるか（タイトル・本文・カテゴリを入力して保存）
- 作成した記事の編集・削除ができるか
- キーワード検索で記事が絞り込まれるか
- カテゴリで絞り込みができるか
- ソート順を切り替えると表示順が変わるか
- ページネーションで次のページに遷移できるか

動作に問題がある場合は、Claude Code にエラー内容を伝えて修正を依頼してください。

```
> 記事一覧ページで〇〇のエラーが出ています。修正してください
```

### 生成コードを自分の目で確認する

ブラウザで動作することを確認したら、次はコードの中身を見てみましょう。

2-1-3 でバイブコーディングの危険性を学びました。「動いているから大丈夫」ではなく、生成されたコードが意図通りかを自分で判断することが大切です。

確認すべきポイントを具体的に挙げます。

**マイグレーション**:
- `category_id` は `nullable` になっているか（記事はカテゴリなしでも作成できるべき）
- `body_markdown` は `text` 型か（`string` だと文字数制限で長い記事が保存できない）
- 外部キー制約は適切か（User 削除時に記事はどうなるか、Category 削除時に記事はどうなるか）

**モデル**:
- `$fillable` に必要なカラムが含まれているか
- `$casts` で型変換が適切に設定されているか（`published_at` は datetime か）
- リレーション（`belongsTo`, `hasMany`）が正しい方向で定義されているか

**コントローラ**:
- 検索クエリで `like` 検索が `where` のグルーピングで囲まれているか（囲まれていないと、他の条件と組み合わせたときに意図しない結果になる）
- ページネーションの件数は指示通り 15 件か
- `with(['user', 'category'])` でリレーションを Eager Loading しているか（していないと N+1 問題が発生する）

これらは、皆さんが COACHTECH で学んだ Laravel の知識で判断できる内容です。マイグレーションのカラム型、Eloquent のリレーション、クエリビルダの使い方。AI が生成したコードであっても、確認に使う知識は同じです。

もし意図と異なる箇所があれば、Claude Code に理由を聞いたり、修正を依頼したりしてください。

```
> articles テーブルの外部キー制約について確認したいです。user_id に cascadeOnDelete が設定されていますが、ユーザーを削除したときに記事も全削除される設計で問題ないですか？
```

Claude Code は設計の意図を説明してくれます。その説明に納得できるか、自分の判断で決めてください。「Claude がそう言うから」ではなく「自分で考えて納得した」と言えることが大切です。

## GitHub リポジトリの作成

生成したコードを GitHub に保存しましょう。ここでは `gh` CLI（GitHub CLI）を使います。

`gh` CLI は、GitHub の操作をターミナルから行えるコマンドラインツールです。皆さんが COACHTECH で学んだ `git` コマンド（`git add`、`git commit`、`git push`）はバージョン管理のツールですが、`gh` は GitHub というサービスとやり取りするためのツールで、別物です。

| ツール | 役割 | 例 |
|---|---|---|
| `git` | バージョン管理（ローカル・リモート問わず） | `git add`, `git commit`, `git push` |
| `gh` | GitHub サービスとの連携 | `gh repo create`, `gh pr create` |

`gh` を使うと、リポジトリの作成や PR の作成をブラウザを開かずにターミナルから直接行えます。Claude Code と組み合わせると、コード生成からリポジトリ作成・プッシュまでターミナルだけで完結するため、開発のテンポが良くなります。

### `gh` CLI のセットアップ

`gh` CLI がインストールされていない場合は、以下でインストールします。

```bash
# macOS
brew install gh

# Windows（WSL）
sudo apt install gh
```

GitHub にログインします。

```bash
gh auth login
```

ブラウザが開くので、GitHub アカウントで認証してください。

### リポジトリ作成とプッシュ

Git リポジトリを初期化し、GitHub にプッシュします。

```bash
cd tech-article-platform
git init
git add -A
git commit -m "Initial commit: Laravel 10 + Sail project with Article, Category, User models"
```

GitHub にリポジトリを作成してプッシュします。

```bash
gh repo create tech-article-platform --private --source=. --push
```

このコマンドは以下を一括で行います。

- GitHub に `tech-article-platform` というプライベートリポジトリを作成
- ローカルリポジトリのリモートに設定
- `main` ブランチをプッシュ

⚠️ よくあるエラー: `gh repo create` の認証エラー

```
error: insufficient permissions
```

**原因**: `gh auth login` で認証した際に、リポジトリ作成の権限が付与されていない場合があります。

**対処法**: `gh auth login` をもう一度実行し、認証フローでリポジトリの読み書き権限を許可してください。

プッシュが成功したら、ブラウザで GitHub のリポジトリページを開いて確認しましょう。

```bash
gh repo view --web
```

ファイル一覧にマイグレーション、モデル、コントローラ、Blade テンプレートなどが含まれていれば成功です。

💡 以降の Chapter では、機能を追加するたびに作業の区切りでコミットする習慣をつけていきます。Git の体系的な操作は 2-7 で学びますが、それまでは各セクションの終わりに「コミットしておきましょう」と案内します。

## 見極めチェック

- [ ] **正しさ**: マイグレーションのカラム型・制約が指示通りか（`category_id` は nullable、`body_markdown` は text、`published_at` は nullable timestamp）
- [ ] **正しさ**: リレーションが正しい方向で定義されているか（Article `belongsTo` User / Category、User `hasMany` Article）
- [ ] **正しさ**: 記事一覧ページがブラウザで動作するか（一覧表示、キーワード検索、カテゴリ絞り込み、ステータス絞り込み、ソート、ページネーション）
- [ ] **正しさ**: シーダーが実行され、ダミーデータが表示されているか
- [ ] **品質**: コントローラの検索クエリで `where` のグルーピングが適切か（`keyword` 検索が他の条件に影響しない構造か）
- [ ] **品質**: リレーションの Eager Loading（`with()`）が使われているか（N+1 問題の防止）
- [ ] **安全性**: `.env` ファイルが `.gitignore` に含まれているか（GitHub にプッシュされていないか）
- [ ] **安全性**: シーダーのダミーデータに本物の個人情報が含まれていないか（Faker を使用しているか）

> このセクションでは特に「正しさ」に注目してください。生成されたマイグレーションのカラム型や制約を自分で読み、指示した内容と一致しているかを確認します。たとえば `body_markdown` が `string(255)` になっていたら、長い記事が保存できません。`text` 型であることを自分の目で確認する。これが「見極める力」の第一歩です。

## 公式ドキュメント

- [Interactive Mode](https://code.claude.com/docs/en/interactive-mode)
- [Tools Reference](https://code.claude.com/docs/en/tools-reference)（Claude Code が使用するツールの一覧）
- [Commands](https://code.claude.com/docs/en/commands)（スラッシュコマンドの一覧）

## まとめ

- Claude Code への指示は、序盤ではテーブル設計やカラム型を**具体的に伝える**ことで的確なコードを引き出せます
- 1つのプロンプトで、マイグレーション・モデル・コントローラ・ビュー・ルート・シーダーを**一括生成**できます
- CLAUDE.md に Sail コマンド体系を書いておいたことで、Claude Code が `./vendor/bin/sail artisan` を正しく使いました
- 生成コードは「動くか」だけでなく、マイグレーションのカラム型やリレーション定義を**自分の Laravel 知識で確認**します
- `gh repo create` で GitHub リポジトリを作成し、初回コミットをプッシュしました

次の Chapter では、Claude Code の裏側で何が起きているか（エージェントループ）を理解し、長時間の作業を効率的に進めるためのコンテキスト管理を学びます。
