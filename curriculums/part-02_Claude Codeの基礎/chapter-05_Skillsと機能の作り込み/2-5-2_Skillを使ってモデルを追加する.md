# 2-5-2 Skill を使ってモデルを追加する

## 概要

前のセクションで、モデル追加用の `/add-model` Skill を作成しました。このセクションでは、その Skill を実際に使いながら、テック記事プラットフォームに **Tag**、**Comment**、**Series** の3つの機能を段階的に追加します。

ここから指示の出し方が変わります。2-2-2 では「role: enum('admin', 'author'), デフォルト'author'」のようにカラム型まで細かく指定していました。中盤では **ビジネス要件レベル** の指示に移行します。「タグ機能を追加して」のように機能単位で伝え、実装の詳細は Claude Code に委ねます。

3つのモデルを段階的に追加する過程で、セッション命名の実践と、1つのセッションに詰め込みすぎない「セッション分割」の考え方も体験します。

## Tag の追加

### Skill を使って多対多リレーションを追加する

まず、テック記事プラットフォームのディレクトリで Claude Code を起動します。今回はセッションに名前をつけて始めましょう。

```bash
claude -n "tag-feature"
```

2-3-2 で学んだセッション命名です。これから Tag 機能の作業をすることが名前から明確にわかります。後から `claude -r "tag-feature"` で再開できます。

では、前のセクションで作った Skill を使います。

```
> /add-model Tag
```

SKILL.md の指示が Claude Code に渡されます。ここで追加の要件を伝えましょう。

```
> 記事にタグを付けられるようにしてください。
> 1つの記事に複数のタグ、1つのタグに複数の記事を紐づけられる多対多のリレーションです。
> 記事の作成・編集画面でタグを選択でき、記事一覧でタグによる絞り込みができるようにしてください。
```

2-2-2 のときと比べてみてください。カラム型（`string(50)` など）もテーブル名（`article_tag`）も指定していません。「多対多のリレーション」「タグで絞り込み」というビジネス要件だけを伝えています。Claude Code がプロジェクトの既存コードを読み、適切なカラム型・テーブル構造・中間テーブルを判断します。

皆さんの環境では異なるコードが生成されます。以下は一例です。

```php
// database/migrations/xxxx_create_tags_table.php
Schema::create('tags', function (Blueprint $table) {
    $table->id();
    $table->string('name', 50);
    $table->string('slug', 50)->unique();
    $table->timestamps();
});
```

```php
// database/migrations/xxxx_create_article_tag_table.php
Schema::create('article_tag', function (Blueprint $table) {
    $table->id();
    $table->foreignId('article_id')->constrained()->cascadeOnDelete();
    $table->foreignId('tag_id')->constrained()->cascadeOnDelete();
    $table->timestamps();
    $table->unique(['article_id', 'tag_id']);
});
```

```php
// app/Models/Article.php（リレーション追加部分）
public function tags()
{
    return $this->belongsToMany(Tag::class);
}
```

```php
// app/Models/Tag.php
public function articles()
{
    return $this->belongsToMany(Article::class);
}
```

生成されたコードを確認しましょう。多対多リレーションでは中間テーブル（`article_tag`）が作られます。Laravel の命名規則に従い、2つのモデル名をアルファベット順に結合した名前（article_tag）になっているかを見てください。`belongsToMany` メソッドで双方向のリレーションが定義されていれば、基本的な構造は正しいです。

### ブラウザで動作を確認する

マイグレーションと Seeder が実行されたら、ブラウザで確認します。

- 記事の作成画面でタグを選択できるか
- 記事一覧でタグによる絞り込みができるか
- 記事詳細画面にタグが表示されるか

「動いた」ことを自分の目で確認するのは、見極める力の第一歩です。

## Comment・Series の追加

### セッションを分ける

Tag の追加が完了しました。続いて Comment と Series を追加しますが、ここで1つ大事なことをお伝えします。

> ⚠️ よくある問題: Kitchen Sink セッション
>
> 1つのセッションにあれもこれもと詰め込むことを **Kitchen Sink セッション** と呼びます。Tag の追加、Comment の追加、Series の追加、UI の調整、バグ修正……と1つのセッションで全部やろうとすると、コンテキストが膨らみ、Claude Code の応答品質が低下します（2-3-2 で学んだコンテキストウィンドウの制約です）。
>
> 機能単位でセッションを分けましょう。Tag の作業が終わったら、新しいセッションで Comment に取り掛かります。

Tag の作業が終わったセッションを閉じて、新しいセッションを起動します。

```bash
claude -n "comment-feature"
```

### Comment（ネスト対応）を追加する

Comment にはネスト（返信）機能を持たせます。Skill を使いつつ、ビジネス要件を伝えます。

```
> /add-model Comment
```

```
> 記事にコメントを投稿でき、コメントに対して返信（ネスト）ができるようにしてください。
> ネストは1階層までとします。
> コメントは認証済みユーザーのみ投稿可能です。
```

皆さんの環境では異なるコードが生成されます。以下は一例です。

```php
// app/Models/Comment.php
class Comment extends Model
{
    protected $fillable = ['article_id', 'user_id', 'parent_id', 'body'];

    public function article()
    {
        return $this->belongsTo(Article::class);
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function parent()
    {
        return $this->belongsTo(Comment::class, 'parent_id');
    }

    public function replies()
    {
        return $this->hasMany(Comment::class, 'parent_id');
    }
}
```

ネスト構造のポイントは **自己参照リレーション** です。Comment が自分自身への外部キー（`parent_id`）を持ち、`parent()` と `replies()` で親子関係を表現しています。この構造は、カテゴリの親子関係やフォルダのツリー構造など、実務で頻繁に使うパターンです。

ブラウザで確認しましょう。記事の詳細ページにコメントフォームが追加され、コメントへの返信ができることを確認してください。

### Series を追加する

Comment の確認が終わったら、再びセッションを分けて Series に取り掛かります。

```bash
claude -n "series-feature"
```

Series は、複数の記事をまとめて連載として管理する機能です。Zenn の「本」に相当します。

```
> /add-model Series
```

```
> 記事を連載（シリーズ）としてまとめられるようにしてください。
> シリーズは名前と説明を持ちます。
> 1つのシリーズに複数の記事を登録でき、シリーズ内での記事の表示順序を管理できるようにしてください。
> 1つの記事は複数のシリーズに所属できます。
```

皆さんの環境では異なるコードが生成されます。以下は一例です。

```php
// database/migrations/xxxx_create_article_series_table.php
Schema::create('article_series', function (Blueprint $table) {
    $table->id();
    $table->foreignId('article_id')->constrained()->cascadeOnDelete();
    $table->foreignId('series_id')->constrained()->cascadeOnDelete();
    $table->unsignedInteger('order')->default(0);
    $table->timestamps();
    $table->unique(['article_id', 'series_id']);
});
```

Tag の中間テーブルとの違いに注目してください。`article_series` テーブルには `order` カラムがあります。これが順序管理の仕組みです。中間テーブルに追加のカラムを持たせることで、単なる「紐づけ」ではなく「順番付きの紐づけ」を表現しています。

Laravel では中間テーブルの追加カラムにアクセスするために、`withPivot` メソッドを使います。

```php
// app/Models/Series.php（リレーション部分）
public function articles()
{
    return $this->belongsToMany(Article::class, 'article_series')
        ->withPivot('order')
        ->orderByPivot('order');
}
```

ブラウザでシリーズの作成と記事の登録ができることを確認してください。

💡 ここまでの変更をコミットしておきましょう。Tag・Comment・Series の3つの機能が追加されています。コミットメッセージの例: 「Add Tag, Comment (nested), and Series models with pivot tables」。

## 見極めチェック

- [ ] **正しさ**: Tag と Article の多対多リレーションが正しく動作するか。記事にタグを付け、タグで絞り込みができるか。中間テーブル `article_tag` に `article_id` と `tag_id` の一意制約があるか
- [ ] **正しさ**: Comment のネスト構造が正しく動作するか。返信が親コメントの下に表示されるか。`parent_id` による自己参照リレーションが定義されているか
- [ ] **正しさ**: Series と Article の多対多リレーションで順序管理ができるか。中間テーブル `article_series` に `order` カラムがあり、`withPivot('order')` で取得できるか
- [ ] **品質**: 3つのモデルそれぞれで、既存の User・Article モデルとの一貫したコーディングスタイルが保たれているか（命名規則、fillable の定義方法、リレーションの書き方）
- [ ] **安全性**: Comment の投稿が認証済みユーザーに限定されているか。未認証ユーザーがコメントを投稿できないか

> このセクションでは特に **正しさ** に注目してください。3つのモデルはそれぞれ異なるリレーションパターン（多対多、自己参照、順序付き多対多）を使っています。生成されたコードを読み、「なぜこの構造になっているか」を理解することが大切です。分からない部分があれば、Claude Code に「なぜこう書いたか」を質問してみてください。

## 公式ドキュメント

- [Common Workflows](https://code.claude.com/docs/en/common-workflows)（コードベースへの機能追加ワークフロー）
- [Best Practices](https://code.claude.com/docs/en/best-practices)（Kitchen Sink セッションの回避、セッション管理のベストプラクティス）

## まとめ

- 中盤では **ビジネス要件レベル** の指示に移行します。カラム型やテーブル名を指定するのではなく、「タグ機能を追加して」のように機能単位で伝えます
- `/add-model` Skill を使うことで、モデル追加の定型手順を毎回書く必要がなくなりました。Skill は「指示のテンプレート化」です
- **セッション命名**（`claude -n "feature-name"`）で作業内容を明確にし、**機能単位でセッションを分ける** ことでコンテキストの汚染を防ぎます
- 多対多（Tag）、自己参照（Comment）、順序付き多対多（Series）の3つのリレーションパターンを実装しました

次のセクションでは、2-4-2 でバックエンドを実装した公開ワークフローに UI を追加し、ブラウザで状態遷移を操作できるようにします。合わせて、記事関連画面の UI を Blade コンポーネントで整えます。
