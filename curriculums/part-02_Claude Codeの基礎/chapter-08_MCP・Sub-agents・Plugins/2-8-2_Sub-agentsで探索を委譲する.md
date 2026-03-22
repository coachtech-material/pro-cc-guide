# 2-8-2 Sub-agents で探索を委譲する

## 概要

テック記事プラットフォームは8つのモデルを持つアプリケーションに成長しました。コードベースが大きくなると、Claude Code に「既存のコードに合わせて新機能を追加して」と指示したとき、既存コードの調査だけでかなりのコンテキストを消費します。2-3-2 で学んだコンテキストウィンドウには限りがあるため、調査に使った分だけ実装に使える余裕が減ります。

Sub-agents を使えば、この問題を解決できます。コードベースの探索を別の Claude（Sub-agent）に委譲し、その結果だけをメインのセッションに持ち帰る。メインの会話は実装に集中できます。

このセクションでは、Sub-agents の概念を理解した上で、残りの2つのモデル（Profile と Follow）をまとめて追加します。終盤の「まとめて指示し、大量の生成コードを検証する」体験です。

## Sub-agents とは

### 隔離されたコンテキストで動く専門ワーカー

Sub-agent は、メインの Claude Code セッションとは **別のコンテキストウィンドウ** で動く専門のワーカーです。

メインセッションから「このコードベースのリレーション構造を調べて」と依頼すると、Sub-agent が独立したコンテキストで調査を行い、結果の要約だけをメインに返します。調査の過程で読んだ大量のコードはメインのコンテキストを消費しません。

これが Sub-agents のメリットです。**メインのコンテキストを汚さずに探索・検証できる**。

### 組み込みの Sub-agents

Claude Code には、よく使う目的に合わせた Sub-agent があらかじめ用意されています。

| Sub-agent | モデル | 用途 |
|---|---|---|
| **Explore** | Haiku（高速） | ファイル検索、コード探索。読み取り専用 |
| **Plan** | 継承 | Plan Mode でのコードベース調査。読み取り専用 |
| **general-purpose** | 継承 | 複雑な調査、複数ステップの操作、コード変更 |

この他にも **Bash**（ターミナルコマンドの実行）、**Claude Code Guide**（Claude Code 自体の使い方への質問応答）などの組み込み Sub-agent があります。

**Explore** は最も頻繁に使われます。高速なモデル（Haiku）で動作し、コードベースの構造調査やファイル検索を素早くこなします。Claude Code が「このコードベースを調べてから実装しよう」と判断したとき、自動的に Explore Sub-agent を起動することがあります。

**Plan** は 2-4-2 で使った Plan Mode の裏側で動いています。Plan Mode に入ると、Plan Sub-agent がコードベースを調査して文脈を集め、その情報をもとにメインの Claude Code が計画を提示する仕組みです。

**general-purpose** はメインセッションとほぼ同じ能力を持ち、ファイルの編集も可能です。コード変更を伴う複雑なタスクを委譲する場合に使われます。

💡 Sub-agents は他の Sub-agent を起動できません（ネストは不可）。メインセッションだけが Sub-agent を起動できます。

### Sub-agents の動作を見る

Sub-agent が起動すると、ターミナルに「Agent spawned」のような表示が出ます。Sub-agent がどのファイルを読み、何を調べているかはツール実行ログで確認できます。

Sub-agent が作業を終えると、調査結果の要約がメインセッションに返されます。メインの Claude Code はその要約を読んで、次のアクション（実装、追加調査、質問への回答など）を決めます。

## Profile と Follow を追加する

### まとめて要件を伝える

いよいよ残りの2つのモデルを追加して、テック記事プラットフォームを完成させます。これまでの Chapter で学んだ「終盤の指示」を実践します。2つの機能をまとめて伝え、Claude Code に実装を委ねましょう。

```bash
claude -n "profile-follow"
```

```
> 以下の2つの機能をまとめて追加してください。
>
> 1. Profile（著者プロフィール）
>    - User と1対1のリレーション
>    - 自己紹介文、GitHub URL、Twitter URL を持つ
>    - 著者ダッシュボードを作成する（総記事数、総いいね数、投稿ストリーク）
>
> 2. Follow（ユーザー間フォロー）
>    - User 間の多対多リレーション（フォローする側 / される側）
>    - フォローフィード（フォロー中ユーザーの記事を時系列で表示）
>    - フォロー / フォロー解除のボタン
>
> 既存のモデルやルーティングの規約に合わせて実装してください。マイグレーション、モデル、コントローラー、ビュー、シーダーをすべて含めてください。
```

2-2-2 の頃は「role: enum('admin', 'author'), デフォルト'author'」のようにカラム型まで指示していました。今はビジネス要件（「自己紹介文、GitHub URL、Twitter URL を持つ」）を伝えるだけです。カラム型やテーブル構造は Claude Code が既存コードに合わせて判断します。

### Sub-agents の活用を観察する

この規模の指示を出すと、Claude Code は既存のコードベースを調査してから実装に入ります。ツール実行ログを観察してみてください。

Explore Sub-agent が起動し、以下のような調査を行う場面が見られるはずです。

- 既存のモデルファイル（User, Article など）のリレーション定義の確認
- ルーティングの命名規則や URL 構造の調査
- Blade テンプレートのレイアウト構造の確認
- 既存のシーダーのパターン調査

Claude Code が自動的に Sub-agent を使うかどうかは、タスクの複雑さやコンテキストの状況によります。明示的に Sub-agent を使わせたい場合は、以下のように指示できます。

```
> まず Explore Sub-agent で既存のモデルとルーティングの構造を調査してから、実装に入ってください
```

### 生成コードを確認する

皆さんの環境では異なるコードが生成されます。以下は一例です。

Profile モデルは User との1対1リレーションを持ちます。

```php
// app/Models/Profile.php
class Profile extends Model
{
    protected $fillable = ['user_id', 'bio', 'github_url', 'twitter_url'];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

```php
// app/Models/User.php（リレーション追加部分）
public function profile()
{
    return $this->hasOne(Profile::class);
}
```

Follow モデルは User 間の自己参照多対多リレーションです。2-5-2 で Comment の自己参照リレーション（親子関係）を見ましたが、Follow は「ユーザー A がユーザー B をフォローする」という対称ではない関係を表現します。

```php
// app/Models/User.php（フォロー関連のリレーション追加部分）
public function followers()
{
    return $this->belongsToMany(User::class, 'follows', 'followed_id', 'follower_id');
}

public function following()
{
    return $this->belongsToMany(User::class, 'follows', 'follower_id', 'followed_id');
}
```

`follows` テーブルは `follower_id` と `followed_id` の2つの外部キーを持ちます。同じ `users` テーブルを2方向から参照するため、`belongsToMany` の第3・第4引数で外部キーを明示的に指定しています。

著者ダッシュボードは、Profile ページにユーザーの統計情報を表示します。

```php
// app/Http/Controllers/ProfileController.php（ダッシュボード部分）
public function show(User $user)
{
    $stats = [
        'articles_count' => $user->articles()->published()->count(),
        'total_likes' => $user->articles()->withCount('likes')->get()->sum('likes_count'),
        'streak' => $this->calculateStreak($user),
    ];

    return view('profiles.show', compact('user', 'stats'));
}
```

投稿ストリーク（連続投稿日数）の計算ロジックは、Claude Code が独自に実装します。日付の連続性を判定するロジックが正しいか、見極めチェックで確認しましょう。

### ブラウザで動作確認する

`sail artisan migrate` と `sail artisan db:seed` でデータベースを更新し、ブラウザで確認します。

- **著者プロフィールページ**: ユーザー名をクリックすると、自己紹介文、SNS リンク、統計情報（総記事数・総いいね数・投稿ストリーク）が表示されるか
- **フォロー機能**: フォロー / フォロー解除ボタンが動作するか。フォロー数・フォロワー数が正しく更新されるか
- **フォローフィード**: フォロー中のユーザーの記事が時系列で表示されるか

2-8-1 で設定した MCP を活用して、データベースの状態も確認してみましょう。

```
> follows テーブルのデータを確認して、フォロー関係が正しく保存されているか見せてください
```

MCP 経由で実データを確認できるのは、前のセクションで設定した成果です。

### カスタム Sub-agent と `/agents` コマンド

組み込みの Sub-agent 以外に、自分で Sub-agent を定義することもできます。2-5-1 で Skills を `.claude/skills/` に作成したように、Sub-agent は `.claude/agents/` に Markdown ファイルとして定義します。

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. Check for:
1. Consistent coding style with the existing codebase
2. Proper error handling
3. Security vulnerabilities
```

YAML フロントマターで名前・説明・利用可能なツール・モデルを指定し、本文にシステムプロンプトを書きます。

定義した Sub-agent は、`/agents` コマンドで一覧を確認できます。

```
> /agents
```

組み込みの Sub-agent とカスタム Sub-agent の一覧が表示されます。

💡 Sub-agent には **persistent memory** という機能があります。フロントマターに `memory: project` と指定すると、Sub-agent が作業の記録を `.claude/agent-memory/<name>/MEMORY.md` に保存し、次回の起動時に引き継ぎます。繰り返し同じ調査をさせる場合に、前回の知見を活かせます。

💡 **Agent Teams** という実験的機能も存在します。Sub-agents はメインセッションに結果を返す一方向の関係ですが、Agent Teams は複数の Claude Code セッションが互いにメッセージをやり取りしながら協調作業する仕組みです。現時点では実験的機能のため、興味がある方は公式ドキュメントを参照してください。

💡 ここまでの変更をコミットしておきましょう。Profile と Follow の2つのモデルが追加され、テック記事プラットフォームは全10モデルになりました。コミットメッセージの例: 「Add Profile with author dashboard and Follow with feed」。

## 見極めチェック

- [ ] **正しさ**: Profile と User の1対1リレーションが正しく動作するか。1人のユーザーに複数の Profile が作られないか
- [ ] **正しさ**: Follow のリレーションで、`followers()`（フォロワー一覧）と `following()`（フォロー中一覧）が逆になっていないか。実際にフォロー操作をして、期待通りの方向で関係が保存されるか
- [ ] **正しさ**: 著者ダッシュボードの統計値が正しいか。記事数は公開済み（published）のみをカウントしているか。いいね数は全記事の合計か。投稿ストリークの計算ロジックは日付の連続性を正しく判定しているか
- [ ] **正しさ**: フォローフィードに、フォロー中ユーザーの公開済み記事のみが時系列で表示されるか。自分の記事は含まれないか
- [ ] **品質**: 既存の8モデルとの一貫したコーディングスタイルが保たれているか（命名規則、fillable の定義、リレーションの書き方、ルーティングの URL 構造）
- [ ] **安全性**: フォロー / フォロー解除が認証済みユーザーに限定されているか。他人のプロフィールを編集できないか

> このセクションでは特に **正しさ** に注目してください。Sub-agents が探索した結果に基づいて生成されたコードが、本当に正しいかを自分で検証します。特に Follow のリレーション方向（`follower_id` と `followed_id` の対応）は、名前が似ているため間違いやすいポイントです。実際にフォロー操作をしてデータベースの値を確認し、期待通りの方向で保存されているかを確かめてください。

## 公式ドキュメント

- [Sub-agents](https://code.claude.com/docs/en/sub-agents)（Sub-agent の概念、組み込み Sub-agent、カスタム Sub-agent の定義）
- [Agent Teams](https://code.claude.com/docs/en/agent-teams)（複数セッションの協調作業、実験的機能）

## まとめ

- Sub-agents は **隔離されたコンテキスト** で動く専門ワーカーです。メインの会話を汚さずに探索や検証を委譲できます
- 組み込みの Sub-agents には Explore（高速な読み取り専用調査）、Plan（Plan Mode でのコードベース調査）、general-purpose（複雑なタスク）があります
- カスタム Sub-agent は `.claude/agents/` に Markdown ファイルとして定義します。名前・説明・ツール・モデルをフロントマターで指定します
- テック記事プラットフォームは **全10モデル** になりました。User, Profile, Article, Comment, Like, Bookmark, Series, Follow, Category, Tag。ここまでの道のりを振り返ると、Claude Code と協働してかなりの規模のアプリケーションを構築してきたことがわかります

次のセクションでは、これまで作ってきた Skills や Hooks を Plugins としてパッケージ化し、チームメンバーに配布する方法を学びます。個人の工夫をチームの資産にしましょう。
