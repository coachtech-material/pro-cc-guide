# 2-5-3 公開ワークフロー UI と Blade コンポーネント

## 概要

2-4-2 で認証・認可と状態遷移のバックエンドを実装し、前のセクションで Tag・Comment・Series を追加しました。機能は揃ってきましたが、記事の公開ワークフロー（draft → review → published）はまだ tinker でしか操作できません。UI がないのです。

このセクションでは、公開ワークフローの UI（ステータス表示・遷移ボタン・admin 承認画面）を作成し、ブラウザで状態遷移を操作できるようにします。合わせて、記事一覧・詳細・シリーズの画面を Tailwind CSS で整え、Blade コンポーネントとして再利用可能にします。

> ⚠️ よくあるエラー: Tailwind CSS が反映されない
>
> ```
> Tailwind のクラスを追加したのに、ブラウザでスタイルが変わらない
> ```
>
> **原因**: `sail npm run dev` が起動していない状態で Blade テンプレートを編集しています。Tailwind CSS は Vite の開発サーバーがファイルの変更を検知し、CSS をリアルタイムでビルドする仕組みです。
>
> **対処法**: 別のターミナルタブで `sail npm run dev` を実行してください。Claude Code を使っているターミナルとは別のタブで起動しておくと、開発中ずっと Tailwind が有効になります。
>
> ```bash
> sail npm run dev
> ```

## 公開ワークフロー UI

### 状態遷移ルールに対応するフロントを作成する

2-4-2 を振り返りましょう。記事には3つのステータスがあり、以下の遷移ルールを実装しました。

- **draft → review**: 本文が300字以上の場合のみ遷移可能
- **review → published**: admin ユーザーのみ遷移可能
- **published → draft**: 遷移時に published_at をリセットする

バックエンドのロジックは完成していますが、ユーザーがこれらの操作を行う UI がありません。ここで UI を追加して、公開ワークフローを完成させます。

新しいセッションを起動しましょう。

```bash
claude -n "workflow-ui"
```

以下のプロンプトで、公開ワークフロー UI の作成を指示します。

```
> 記事の公開ワークフロー UI を作成してください。
>
> 1. 記事詳細画面にステータスバッジを表示する（draft: グレー、review: イエロー、published: グリーン）
> 2. 現在のステータスに応じた遷移ボタンを表示する
>    - draft の記事には「レビューに出す」ボタン
>    - review の記事には「公開する」ボタン（admin のみ表示）
>    - published の記事には「下書きに戻す」ボタン
> 3. 遷移できない場合は理由を表示する（例: 本文が300字未満の場合「本文を300字以上にしてからレビューに出してください」）
> 4. admin ユーザー向けの承認画面を作成する（レビュー待ちの記事を一覧表示し、承認・却下できる）
```

これもビジネス要件レベルの指示です。Blade のコンポーネント名やルートの定義は Claude Code に任せています。

皆さんの環境では異なるコードが生成されます。以下は一例です。

**ステータスバッジ:**

```php
<!-- resources/views/components/status-badge.blade.php -->
@props(['status'])

@php
    $colors = [
        'draft' => 'bg-gray-100 text-gray-800',
        'review' => 'bg-yellow-100 text-yellow-800',
        'published' => 'bg-green-100 text-green-800',
    ];
@endphp

<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {{ $colors[$status] ?? 'bg-gray-100 text-gray-800' }}">
    {{ ucfirst($status) }}
</span>
```

**遷移ボタン:**

```php
<!-- resources/views/articles/show.blade.php（遷移ボタン部分） -->
@if($article->status === 'draft')
    @if(mb_strlen($article->body_markdown) >= 300)
        <form action="{{ route('articles.transition', $article) }}" method="POST">
            @csrf
            <input type="hidden" name="status" value="review">
            <button type="submit" class="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded">
                レビューに出す
            </button>
        </form>
    @else
        <p class="text-sm text-gray-500">本文を300字以上にしてからレビューに出してください</p>
    @endif
@endif
```

### ブラウザで状態遷移を操作する

UI が生成されたら、ブラウザで実際に操作してみましょう。これは見極めチェックの前段階として重要な確認です。

1. **author ユーザーでログイン** し、記事を作成します
2. 本文が300字未満の状態で「レビューに出す」ボタンが表示されないこと（または無効化されていること）を確認します
3. 本文を300字以上にして「レビューに出す」ボタンを押し、ステータスが review に変わることを確認します
4. **admin ユーザーでログイン** し直し、承認画面にレビュー待ちの記事が表示されることを確認します
5. 「公開する」ボタンを押し、ステータスが published に変わることを確認します

2-4-2 では tinker で確認した状態遷移ルールが、今度は UI を通じて同じように動作していることを確認しています。バックエンドとフロントエンドが正しく連動していることの検証です。

## Blade コンポーネント化

### 記事関連画面を Tailwind CSS でコンポーネント化する

公開ワークフロー UI が完成したら、記事関連の画面全体を整えましょう。ここまでの Chapter で作ってきた記事一覧、記事詳細、シリーズ一覧などの画面を、Tailwind CSS で見た目を整えつつ Blade コンポーネントで再利用可能にします。

```
> 記事関連の画面を Tailwind CSS で整えてください。
>
> 1. 記事一覧: カード型のレイアウトで、タグ・カテゴリ・ステータスバッジ・著者名を表示する
> 2. 記事詳細: Markdown の本文、タグ一覧、コメント欄、シリーズナビゲーション（前の記事・次の記事）を表示する
> 3. シリーズ一覧: シリーズ名・説明・記事数を表示する
> 4. 共通部分は Blade コンポーネント（x-component）として抽出する
```

Claude Code は記事カードやタグリスト、コメントツリーなどを Blade コンポーネントとして切り出します。たとえば、記事カードは `<x-article-card :article="$article" />` のように呼び出せるコンポーネントになります。

皆さんの環境では異なるコードが生成されます。以下は一例です。

```php
<!-- resources/views/components/article-card.blade.php -->
@props(['article'])

<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
    <div class="flex items-center gap-2 mb-3">
        <x-status-badge :status="$article->status" />
        @if($article->category)
            <span class="text-sm text-gray-500">{{ $article->category->name }}</span>
        @endif
    </div>

    <h2 class="text-xl font-bold mb-2">
        <a href="{{ route('articles.show', $article) }}" class="hover:text-blue-600">
            {{ $article->title }}
        </a>
    </h2>

    <p class="text-gray-600 text-sm mb-4">
        {{ Str::limit(strip_tags($article->body_markdown), 150) }}
    </p>

    <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
            <span class="text-sm text-gray-500">{{ $article->user->name }}</span>
        </div>
        <div class="flex gap-1">
            @foreach($article->tags as $tag)
                <span class="text-xs bg-blue-50 text-blue-600 px-2 py-0.5 rounded">{{ $tag->name }}</span>
            @endforeach
        </div>
    </div>
</div>
```

Blade コンポーネントの利点は、同じ UI パーツを複数の画面で再利用できることです。記事カードは記事一覧ページでも、著者のプロフィールページでも、シリーズ詳細ページでも使えます。HTML を何度もコピペする必要がなくなり、デザインを変更するときも1箇所を修正すれば全画面に反映されます。

ブラウザで各画面の見た目を確認しましょう。記事一覧がカード型になり、ステータスバッジやタグが表示されていれば成功です。

💡 ここまでの変更をコミットしておきましょう。コミットメッセージの例: 「Add publication workflow UI and Blade component styling」。

## 見極めチェック

- [ ] **正しさ**: ステータスバッジが draft（グレー）、review（イエロー）、published（グリーン）で正しく色分けされているか
- [ ] **正しさ**: 遷移ボタンが 2-4-2 の状態遷移ルールに従っているか。本文300字未満で「レビューに出す」が使えないか。author ユーザーに「公開する」ボタンが表示されないか
- [ ] **正しさ**: admin 承認画面にレビュー待ちの記事が一覧表示され、承認操作ができるか
- [ ] **正しさ**: ブラウザで draft → review → published の遷移を実際に操作して、正しく動作するか
- [ ] **品質**: 共通の UI パーツが Blade コンポーネント（`resources/views/components/`）として適切に切り出されているか。同じ HTML が複数箇所にコピペされていないか
- [ ] **品質**: 既存の Blade テンプレートのスタイルと一貫した Tailwind CSS クラスが使われているか
- [ ] **安全性**: 状態遷移のリクエストに CSRF トークン（`@csrf`）が含まれているか。ステータス変更のルートに認証ミドルウェアが適用されているか

> このセクションでは **正しさ** と **品質** の両方に注目してください。正しさの観点では、UI が 2-4-2 で実装したバックエンドの状態遷移ルールと正しく連動しているかを確認します。品質の観点では、Blade コンポーネントとして適切に共通化されているかを確認します。「動く」だけでなく「保守しやすい」コードになっているかを見る練習です。

## 公式ドキュメント

- [Common Workflows](https://code.claude.com/docs/en/common-workflows)（機能実装のワークフロー）
- [Best Practices](https://code.claude.com/docs/en/best-practices)（生成コードの検証パターン）

## まとめ

- 2-4-2 で実装した状態遷移ロジックに対応する UI を追加し、公開ワークフローを完成させました。ブラウザで draft → review → published の遷移を操作できます
- Blade コンポーネント（`<x-component-name>`）を使って、記事カード・ステータスバッジ・タグリストなどの共通パーツを再利用可能にしました
- `sail npm run dev` が起動していないと Tailwind CSS が反映されません。UI の作業中は常に Vite の開発サーバーを起動しておきましょう

次の Chapter では、Claude Code にテストを書かせて実行し、テスト失敗時のデバッグを体験します。このセクションで「ブラウザで動いた」ことを目視で確認しましたが、テストを書くことでこの確認を自動化し、変更のたびに繰り返せるようにします。
