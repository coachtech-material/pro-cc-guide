# 3-4-2 CourseHub に機能を追加する

## 🎯 このセクションで学ぶこと

- 既存機能の拡張（小テスト再受験）を、既存コードの理解に基づいて遂行できる
- 新規機能の構築（コースレビュー）を、Plan Mode で設計してから段階的に実装・検証できる
- 既存の設計パターンとコーディング規約との整合性を見極められる

2つの機能を開発します。1つ目の小テスト再受験機能で「既存機能の拡張」のアプローチを実践し、2つ目のコースレビュー機能で「新規機能の構築」のアプローチを実践します。

> 📝 このセクションで使う機能: セッション管理（[2-2-2 コンテキストとセッション管理](../../part-02_Claude%20Codeの基礎/chapter-02_基本を理解する/2-2-2_コンテキストとセッション管理.md) で学習）、Plan Mode（[2-3-1 Plan Mode](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-1_Plan%20Mode.md) で学習）、Hooks（[2-3-3 Hooks](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-3_Hooks.md) で学習）、`/simplify`（[2-3-2 Skills](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-2_Skills.md) で学習）、`/test` Skill（[3-1-3 プロジェクトの規約・設定を確認する](../chapter-01_実践の準備/3-1-3_プロジェクトの規約・設定を確認する.md) で更新）

---

## 導入: 「動くコード」と「馴染むコード」の違い

バグ修正では「壊れたものを直す」ことがゴールでした。正解が明確で、修正後に正しく動けば完了です。

機能開発はそうはいきません。「動く」だけでは不十分です。新しいコードが既存のコードベースに **馴染んでいるか** が問われます。

たとえば、CourseHub の Controller を見てみましょう。`EnrollmentController` は薄く設計されていて、ビジネスロジックは `EnrollmentService` に切り出されています。一方、`CourseController@store` は 200 行超の Fat Controller です。同じプロジェクト内でもパターンが統一されていない状態です。

こういう状況で新しい機能を追加するとき、「どのパターンに合わせるべきか」を判断する必要があります。Claude Code は指示がなければ独自の判断でコードを書きます。既存パターンを読み取り、どのパターンに従うべきかを指示に含めることで、プロジェクト全体の一貫性を保てます。

### 🧠 先輩エンジニアはこう考える

> 新しいメンバーが書いたコードが PR で上がってきたとき、最初に見るのは「動くかどうか」じゃなくて「うちのプロジェクトの書き方に合ってるか」なんだよね。動くのは前提で、既存コードとスタイルが揃っているか、規約に沿っているかが重要。
>
> Claude Code に機能を作ってもらうときも同じ。「作って」だけだと動くコードは出てくるけど、プロジェクトの流儀と違うパターンで書かれることがある。だから「○○Controller のパターンに従って」「Form Request を使って」と具体的に指示する。この一手間が、PR レビューでの手戻りを大幅に減らしてくれる。

---

## 🏃 実践①: 小テスト再受験機能（既存機能の拡張）

CourseHub の小テスト（Quiz）には、受験して結果を見る機能があります。しかし、現在の実装には以下の問題があります。

- 合格済みでも再受験ボタンが表示される
- 受験回数に制限がない
- 過去の受験履歴を確認できない

これらを改善する「小テスト再受験機能」を開発します。

**要件**:
- 合格済み（スコアが合格点以上）の場合は再受験できない
- 不合格の場合は再受験できる（回数制限なし）
- 結果画面に過去の受験履歴（日時とスコア）を表示する
- 結果画面の再受験ボタンは不合格の場合のみ表示する

**使用する Part 2 の機能**: セッション管理（`--continue`）、`/test`

> 📌 CourseHub のプロジェクトディレクトリで Claude Code を起動していることを確認してください。前の Chapter でバグ修正のブランチにいる場合は、main に戻してから新しいブランチを作成します。

### Step 1: 作業ブランチを作成し、セッションに名前を付ける

まず、作業ブランチを作成します。

```
> main ブランチに切り替えて、feature/quiz-retake ブランチを作成してください
```

次に、セッションに名前を付けます。機能開発は複数回に分けて作業することが多いため、後で再開しやすいように名前を付けておきます。

```
/rename quiz-retake
```

> 💡 [2-2-2 コンテキストとセッション管理](../../part-02_Claude%20Codeの基礎/chapter-02_基本を理解する/2-2-2_コンテキストとセッション管理.md) で学んだように、セッションに名前を付けておけば `claude --resume quiz-retake` で再開できます。機能開発のように作業時間が長くなるタスクでは、セッション名を付ける習慣をつけましょう。

### Step 2: 既存の Quiz/Submission フローを読む

3-4-1 で学んだように、拡張のアプローチでは **まず既存コードを読む** ことから始めます。

```
> 小テストの再受験機能を追加したいです。まず、既存の小テスト関連のコードを
> 確認してください。以下のファイルを読んで、現在の処理フローを説明してください。
> - QuizController（show, submit, result）
> - SubmissionPolicy
> - quizzes/show.blade.php
> - quizzes/result.blade.php
> - Submission モデル
> 修正はまだしないでください。
```

Claude Code が読み取った内容を確認しましょう。主なポイントは以下のとおりです。

- `QuizController@show`: クイズの問題一覧を表示する。`CoursePolicy@view` で認可チェック
- `QuizController@submit`: 回答を受け取り、正答数からスコアを計算して Submission を作成する
- `QuizController@result`: 最新の Submission を取得して結果画面を表示する
- `SubmissionPolicy@submit`: student ロールかつ active な Enrollment がある場合のみ送信可能
- `result.blade.php`: スコアの合否表示、解答詳細、再受験ボタン（常に表示）

> 💡 **「修正はまだしないでください」と明示する理由**: [3-3-1 バグ修正の方法論](../chapter-03_バグを修正する/3-3-1_バグ修正の方法論.md) でも学んだように、調査と実装を分離することで、コードを理解してから変更に入れます。機能開発でも同様です。

<!-- TODO: 画像追加 - Claude Code が既存コードの処理フローを説明する画面 -->

### Step 3: 変更箇所を特定し、実装を依頼する

既存フローを理解したら、要件に基づいて変更箇所を特定し、実装を依頼します。

```
> 以下の要件で小テスト再受験機能を実装してください。
>
> 要件:
> - 合格済み（score >= passing_score）の Submission がある場合は再受験不可
> - 不合格の場合は再受験可能（回数制限なし）
> - 結果画面に過去の受験履歴（日時・スコア）を一覧表示
> - 再受験ボタンは不合格の場合のみ表示
>
> 制約:
> - 新規モデルは作成しない。既存の Quiz, Submission モデルを活用する
> - SubmissionPolicy に合格チェックのロジックを追加する
> - QuizController@result で全履歴を取得して View に渡す
> - 既存の QuizController の処理フローを壊さないようにする
> - rules/coding.md のコーディング規約に従う
```

Claude Code が生成するコードはあなたの環境では異なりますが、主な変更箇所は以下のようになるはずです。

**SubmissionPolicy**: 合格済みチェックの追加

```
> SubmissionPolicy に submit メソッドを修正して、
> 合格済みの Submission が存在する場合は false を返すようにしてください
```

<details>
<summary>生成されたコードの例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なるコードが生成されます。以下は参考例です。

```php
// app/Policies/SubmissionPolicy.php
public function submit(User $user, Quiz $quiz, Course $course): bool
{
    if ($user->role !== 'student') {
        return false;
    }

    $hasActiveEnrollment = Enrollment::where('user_id', $user->id)
        ->where('course_id', $course->id)
        ->where('status', 'active')
        ->exists();

    if (!$hasActiveEnrollment) {
        return false;
    }

    // 合格済みの場合は再受験不可
    $hasPassed = Submission::where('user_id', $user->id)
        ->where('quiz_id', $quiz->id)
        ->where('score', '>=', $quiz->passing_score)
        ->exists();

    return !$hasPassed;
}
```

ポイントを確認しましょう。

- 既存の student ロールチェックと active enrollment チェックはそのまま維持されています
- 新たに合格済みの Submission チェックが追加されています
- `$quiz->passing_score` を使って動的に判定しているため、Quiz ごとに異なる合格点に対応できます

</details>

**QuizController@result**: 受験履歴の取得

```
> QuizController@result を修正して、最新の Submission だけでなく
> 全ての Submission 履歴も取得して View に渡してください
```

<details>
<summary>生成されたコードの例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なるコードが生成されます。

```php
// app/Http/Controllers/QuizController.php
public function result(Course $course, Quiz $quiz)
{
    $this->authorize('view', $course);

    $quiz->load('questions.options');

    $submission = Submission::where('user_id', auth()->id())
        ->where('quiz_id', $quiz->id)
        ->latest()
        ->firstOrFail();

    // 受験履歴を全件取得
    $submissions = Submission::where('user_id', auth()->id())
        ->where('quiz_id', $quiz->id)
        ->orderBy('submitted_at', 'desc')
        ->get();

    // 合格済みかどうか
    $hasPassed = $submissions->contains(fn ($s) => $s->score >= $quiz->passing_score);

    return view('quizzes.result', compact('course', 'quiz', 'submission', 'submissions', 'hasPassed'));
}
```

ポイントを確認しましょう。

- `$submission`（最新の結果表示用）と `$submissions`（履歴一覧用）を分けて取得しています
- `$hasPassed` をコレクションの `contains` で判定し、再受験ボタンの表示制御に使います
- 既存の `$submission` の取得ロジックはそのまま維持されています

</details>

**result.blade.php**: 再受験ボタンの条件付き表示と受験履歴の追加

<details>
<summary>生成されたコードの例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なるコードが生成されます。

```html
{{-- result.blade.php（変更箇所のみ抜粋） --}}

{{-- 再受験ボタン: 不合格の場合のみ表示 --}}
<div class="mt-8 flex flex-wrap gap-3">
    @unless($hasPassed)
        <a href="{{ route('courses.quizzes.show', [$course, $quiz]) }}" class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg px-4 py-2.5 shadow-sm transition-all duration-150">再受験する</a>
    @endunless
    <a href="{{ route('courses.show', $course) }}" class="bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 font-medium rounded-lg px-4 py-2.5 transition-all duration-150">コースに戻る</a>
</div>

{{-- 受験履歴 --}}
@if($submissions->count() > 1)
    <div class="mt-8 border-t pt-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">受験履歴</h2>
        <div class="space-y-2">
            @foreach($submissions as $pastSubmission)
                <div class="flex justify-between items-center p-3 rounded-lg bg-gray-50">
                    <span class="text-sm text-gray-600">{{ $pastSubmission->submitted_at->format('Y/m/d H:i') }}</span>
                    <span class="text-sm font-medium {{ $pastSubmission->score >= $quiz->passing_score ? 'text-green-600' : 'text-red-600' }}">
                        {{ $pastSubmission->score }}%
                        {{ $pastSubmission->score >= $quiz->passing_score ? '(合格)' : '(不合格)' }}
                    </span>
                </div>
            @endforeach
        </div>
    </div>
@endif
```

ポイントを確認しましょう。

- `@unless($hasPassed)` で再受験ボタンの表示を制御しています。合格済みなら非表示です
- 受験履歴は `$submissions->count() > 1` で2回以上受験した場合のみ表示されます
- 既存の Blade テンプレートのスタイリングパターン（Tailwind CSS のクラス、色の使い方）に合わせています

</details>

**QuizController@show**: 合格済みチェックの追加

合格済みの場合に小テスト画面へのアクセスを防ぐため、`show` メソッドにもチェックを追加します。

<details>
<summary>生成されたコードの例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なるコードが生成されます。

```php
// app/Http/Controllers/QuizController.php
public function show(Course $course, Quiz $quiz)
{
    $this->authorize('view', $course);

    // 合格済みの場合は結果画面にリダイレクト
    $hasPassed = Submission::where('user_id', auth()->id())
        ->where('quiz_id', $quiz->id)
        ->where('score', '>=', $quiz->passing_score)
        ->exists();

    if ($hasPassed) {
        return redirect()->route('courses.quizzes.result', [$course, $quiz])
            ->with('info', 'この小テストは合格済みです。');
    }

    $quiz->load('questions.options');

    return view('quizzes.show', compact('course', 'quiz'));
}
```

</details>

### Step 4: テストを書いて検証する

変更が完了したら、テストで検証します。[3-3-2 CourseHub のバグを修正する](../chapter-03_バグを修正する/3-3-2_CourseHubのバグを修正する.md) で学んだように、テストケースは **自分で設計** してから Claude Code に実装を依頼します。

テストで確認すべきケースを整理しましょう。

| テストケース | 期待結果 |
|---|---|
| 未受験の student が小テストを受験する | 受験できる（Submission が作成される） |
| 不合格の student が再受験する | 受験できる（新しい Submission が作成される） |
| 合格済みの student が再受験しようとする | 受験できない（結果画面にリダイレクト） |
| 合格済みの student が submit エンドポイントに直接 POST する | 403 Forbidden（Policy で拒否） |
| 結果画面に受験履歴が表示される | 全 Submission が新しい順に表示される |
| 合格済みの結果画面に再受験ボタンが表示されない | ボタンが非表示 |
| 不合格の結果画面に再受験ボタンが表示される | ボタンが表示される |

```
> 以下のテストケースで小テスト再受験機能のテストを作成してください。
> 既存のテストスタイル（tests/Feature/ 配下）に従ってください。
>
> [上記のテストケース一覧を貼り付ける]
```

テストが作成されたら、`/test` で実行します。

```
/test
```

> ⚠️ **よくあるエラー**: テストでデータベースの状態を作る際、`Submission::factory()` が未定義の場合があります。その場合は Claude Code に Factory の作成を依頼してください。既存の Factory（`CourseFactory`, `QuizFactory` 等）のパターンに従うよう指示しましょう。

テストが全て通ることを確認したら、コミットします。

```
> 小テスト再受験機能の変更をコミットしてください。
> rules/git.md の命名規則に従ってください
```

### Step 5: セッションを終了し、後で再開する

ここで一度セッションを終了しましょう。実務では、1つの機能を1回の作業で完了させるとは限りません。ミーティングや他のタスクで中断し、後で再開することはよくあります。

Ctrl+C でセッションを終了します。

次回、作業を再開するときは以下のコマンドを使います。

```bash
claude --resume quiz-retake
```

セッション名を付けておいたので、すぐに前回の続きから始められます。Claude Code は前回のコンテキスト（読んだファイル、行った変更、テスト結果）を全て記憶しています。

> 💡 `--continue` は「最後のセッション」を再開するコマンドです。複数の機能を並行して開発しているときは、`--resume セッション名` で特定のセッションを指定する方が確実です。

### 🔍 見極めチェック: 小テスト再受験機能

> 🧠 先輩エンジニアの思考: 「既存機能の拡張で最も重要なのは、既存の動作を壊していないこと。そして新しいコードが既存パターンに馴染んでいること。動くだけでは不十分だ。」

この Chapter の見極めの重点は **品質（既存設計との整合性）** です。

- [ ] **正しさ**: 合格済みの場合に再受験が防止されるか。不合格の場合に再受験できるか。受験履歴が正しく表示されるか
- [ ] **品質**: SubmissionPolicy の変更が既存の認可パターン（student チェック + enrollment チェック）を維持しているか。Controller の変更が既存メソッドの構造を壊していないか。Blade テンプレートのスタイリングが既存パターンと統一されているか
- [ ] **安全性**: 合格済みチェックが Policy（サーバーサイド）で行われているか。URL 直打ちで合格済み小テストの show ページにアクセスした場合も適切に処理されるか

> 🔑 この実践では特に「品質」に注目してください。Claude Code が生成したコードが、既存の `QuizController` や `SubmissionPolicy` のパターンを壊していないか、不要な複雑さを持ち込んでいないかを確認しましょう。

---

## 🏃 実践②: コースレビュー機能（新規機能の構築）

次は、新規機能を構築します。CourseHub にはまだコースの評価・感想を共有する仕組みがありません。受講完了した学生がコースにレビュー（星評価 + コメント）を投稿できる機能を追加します。

**要件**:
- コース詳細画面にレビュー一覧と投稿フォームを表示する
- レビューは受講完了（Enrollment の status が completed）した student のみ投稿可能
- 1つのコースに対して1人1件のみ投稿可能
- レビューには星評価（1〜5）とコメント（任意）を含む
- コーチと admin はレビューを閲覧できるが投稿はできない

**使用する Part 2 の機能**: Plan Mode、Hooks、`/simplify`、`/test`

### Step 1: 類似機能のコードを読む

新規機能の構築では、3-4-1 で学んだように **類似機能のパターンを把握する** ことから始めます。コースレビューは「受講生がコースに対して操作する」機能なので、同じパターンの「受講登録（Enrollment）」の実装を参考にします。

```
> コースレビュー機能を新規開発します。まず参考にする既存パターンを確認させてください。
> 以下のファイルを読んで、実装パターンを説明してください。
> - EnrollmentController
> - EnrollmentService
> - StoreLessonRequest（Form Request のパターン）
> - SubmissionPolicy（Policy のパターン）
> 修正はまだしないでください。
```

Claude Code の説明から、以下のパターンが把握できるはずです。

- **Controller**: 薄い Controller + Service クラスへの委譲（EnrollmentController のパターン）
- **Form Request**: `authorize()` で認可、`rules()` でバリデーション、`messages()` で日本語メッセージ（StoreLessonRequest のパターン）
- **Policy**: ロールチェック + ビジネスルールチェック（SubmissionPolicy のパターン）
- **エラーハンドリング**: try-catch + flash メッセージでリダイレクト

### Step 2: Plan Mode で設計する

既存パターンを把握したら、Plan Mode で設計を検討します。Shift+Tab で権限モードを切り替えてください。Normal Mode からは1回目で Auto-Accept Mode、2回目で Plan Mode に切り替わります（プロンプトバーに `⏸ plan mode on` と表示されます）。

```
> コースレビュー機能を設計してください。
>
> 要件:
> - コース詳細画面にレビュー一覧と投稿フォームを表示
> - 受講完了（Enrollment status=completed）した student のみ投稿可能
> - 1コースにつき1人1件
> - 星評価（1〜5）+ コメント（任意）
> - コーチと admin は閲覧のみ
>
> 制約:
> - 既存の EnrollmentController + EnrollmentService のパターンに従う
> - バリデーションは Form Request（StoreLessonRequest のパターン）
> - 認可は Policy（SubmissionPolicy のパターン）
> - rules/coding.md のコーディング規約に従う
>
> Review モデルの設計、Controller の構成、ルーティング、
> View の変更箇所を含む実装計画を作成してください。
```

<!-- TODO: 画像追加 - Claude Code が Plan Mode でレビュー機能の設計を提案する画面 -->

Claude Code が設計を提案します。設計内容を確認し、以下の観点で判断してください。

**確認すべき設計判断**:

| 観点 | 確認ポイント |
|---|---|
| モデル設計 | Review テーブルのカラムは要件を満たしているか。user_id + course_id にユニーク制約があるか |
| Controller の構成 | ReviewController は薄く保たれているか。レビュー投稿ロジックが Service に切り出されるべき複雑さか、Controller で完結する程度か |
| ルーティング | 既存のルート構造と整合しているか。RESTful な設計になっているか |
| Policy | 受講完了チェックと1人1件チェックが含まれているか |
| View の変更 | 既存の `courses/show.blade.php` への追加が最小限か |

> 💡 Claude Code が Service クラスの作成を提案する場合がありますが、レビュー投稿は「Review モデルの作成」だけで完結するシンプルな処理です。README の設計方針では「複数モデルにまたがる処理は Service クラスに集約する」とあります。この基準に照らして、Service が本当に必要かを判断してください。不要であれば「Service は不要です。Controller に直接書いてください」と指示しましょう。

設計を修正したい場合は、Ctrl+G でテキストエディタに開いて直接注釈を加えられます。

設計に納得したら、Plan Mode を承認します。

### Step 3: Hooks を設定する（Laravel Pint 自動フォーマット）

> 📌 この Hooks は `jq`（JSON 操作ツール）と Sail の起動を前提とします。`jq --version` でインストールを確認してください。macOS では `brew install jq`、Ubuntu では `sudo apt install jq` でインストールできます。Sail が停止している場合は `./vendor/bin/sail up -d` で起動してください（Sail が停止中は、ファイル編集のたびに Hook がエラーになります）。

実装に入る前に、Hooks を設定します。Hooks は [2-3-3 Hooks](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-3_Hooks.md) で学んだ機能で、Claude Code がファイルを編集するたびに自動で処理を実行できます。

ここでは、Claude Code がファイルを書き込み・編集するたびに Laravel Pint（コードフォーマッター）を自動実行するよう設定します。これにより、生成されるコードが自動的にプロジェクトのコーディングスタイルに整形されます。

```
> CourseHub の .claude/settings.json に Hooks を追加してください。
> PostToolUse イベントで Write と Edit ツールにマッチさせ、
> 編集された PHP ファイルに対して ./vendor/bin/sail exec laravel.test
> ./vendor/bin/pint を実行するフックを設定してください。
```

<details>
<summary>生成された設定の例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なる内容が生成されます。

```json
{
  "permissions": {
    "allow": [
      "Bash(./vendor/bin/sail artisan *)",
      "Bash(composer *)",
      "Bash(npm *)",
      "Bash(./vendor/bin/sail *)",
      "Bash(git *)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(cat /dev/stdin | jq -r '.tool_input.file_path // .tool_input.path // empty') && if [ -n \"$FILE\" ] && echo \"$FILE\" | grep -q '\\.php$'; then cd \"$CLAUDE_PROJECT_DIR\" && ./vendor/bin/sail exec -T laravel.test ./vendor/bin/pint \"$FILE\" 2>/dev/null; fi",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

ポイントを確認しましょう。

- `"matcher": "Write|Edit"` でファイルの書き込み・編集ツールにマッチします
- Hooks はツール実行の情報を **stdin の JSON** で受け取ります。`jq` で `tool_input.file_path` を抽出しています
- PHP ファイルの場合のみ Pint を実行します（`.php` 拡張子チェック）
- Sail 経由で実行しているため、Docker コンテナ内の Pint が使われます
- `timeout: 30` で最大 30 秒まで待ちます

</details>

> ⚠️ **よくあるエラー**: Hooks の設定で `./vendor/bin/pint` を直接実行するとエラーになります。CourseHub は Sail 環境で動作しているため、`sail exec` 経由で実行する必要があります。Sail を起動していない場合は `./vendor/bin/sail up -d` で起動してください。

Hooks が正しく設定されているか、`/hooks` コマンドで確認できます。

```
/hooks
```

PostToolUse に Write|Edit のフックが表示されていれば OK です。

> 💡 Hooks は `.claude/settings.json` に保存されるため、チームで共有できます。プロジェクトの `.claude/settings.json` に Hooks を追加しておけば、チーム全員が同じ自動フォーマットの恩恵を受けられます。これについては Chapter 3-6「チームに共有する」で詳しく扱います。

### Step 4: 段階的に実装する

Plan Mode を承認したら、Shift+Tab で Normal Mode に切り替え、段階的に実装します。3-4-1 で学んだように、一度に全てを作らず、ステップごとに確認しながら進めます。

**Step 4-1: マイグレーションとモデルの作成**

```
> 計画の Step 1 を実装してください。
> Review モデルとマイグレーションを作成してください。
> user_id + course_id にユニーク制約を設定してください。
```

マイグレーションが作成されたら実行して確認します。

```
> マイグレーションを実行してください
```

<details>
<summary>生成されたコードの例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なるコードが生成されます。

```php
// database/migrations/xxxx_xx_xx_create_reviews_table.php
public function up(): void
{
    Schema::create('reviews', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->constrained()->cascadeOnDelete();
        $table->foreignId('course_id')->constrained()->cascadeOnDelete();
        $table->unsignedTinyInteger('rating'); // 1-5
        $table->text('comment')->nullable();
        $table->timestamps();

        $table->unique(['user_id', 'course_id']);
    });
}
```

```php
// app/Models/Review.php
class Review extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'course_id',
        'rating',
        'comment',
    ];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function course(): BelongsTo
    {
        return $this->belongsTo(Course::class);
    }
}
```

ポイントを確認しましょう。

- `user_id + course_id` のユニーク制約により、1ユーザー1コースにつき1件のレビューがデータベースレベルで保証されます
- `rating` は `unsignedTinyInteger`（0〜255）で十分です。1〜5 のバリデーションは Form Request で行います
- `comment` は `nullable` で任意入力に対応しています
- リレーション定義が明示的に記述されています（rules/coding.md の規約どおり）

</details>

> 💡 Hooks を設定したので、Claude Code がモデルファイルを作成した直後に Laravel Pint が自動実行されます。コードスタイルが自動で整形されているか確認してみてください。

**Step 4-2: Policy と Form Request の作成**

```
> ReviewPolicy と StoreReviewRequest を作成してください。
> - ReviewPolicy: 受講完了した student のみ投稿可能、1コース1件の制約
> - StoreReviewRequest: StoreLessonRequest のパターンに従って作成
```

<details>
<summary>生成されたコードの例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なるコードが生成されます。

```php
// app/Policies/ReviewPolicy.php
class ReviewPolicy
{
    public function create(User $user, Course $course): bool
    {
        if ($user->role !== 'student') {
            return false;
        }

        // 受講完了していること
        $hasCompleted = Enrollment::where('user_id', $user->id)
            ->where('course_id', $course->id)
            ->where('status', 'completed')
            ->exists();

        if (!$hasCompleted) {
            return false;
        }

        // まだレビューを書いていないこと
        return !Review::where('user_id', $user->id)
            ->where('course_id', $course->id)
            ->exists();
    }
}
```

```php
// app/Http/Requests/StoreReviewRequest.php
class StoreReviewRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // Policy で認可チェック済み
    }

    public function rules(): array
    {
        return [
            'rating' => ['required', 'integer', 'min:1', 'max:5'],
            'comment' => ['nullable', 'string', 'max:1000'],
        ];
    }

    public function messages(): array
    {
        return [
            'rating.required' => '評価を選択してください。',
            'rating.integer' => '評価は数値で指定してください。',
            'rating.min' => '評価は1以上で指定してください。',
            'rating.max' => '評価は5以下で指定してください。',
            'comment.max' => 'コメントは1000文字以内で入力してください。',
        ];
    }
}
```

ポイントを確認しましょう。

- `ReviewPolicy@create` は `SubmissionPolicy@submit` と同じパターン（ロールチェック → ビジネスルールチェック）に従っています
- `StoreReviewRequest` は `StoreLessonRequest` のパターン（`authorize()`, `rules()`, `messages()`）に従い、日本語のエラーメッセージも定義されています
- `authorize()` が `true` を返していますが、これは Controller 側で `$this->authorize('create', ...)` を呼ぶため、Form Request での二重チェックを避ける設計です

</details>

**Step 4-3: Controller とルーティングの作成**

```
> ReviewController を作成してください。
> EnrollmentController のパターン（薄い Controller）に従い、
> store メソッドで Policy の認可チェック → Form Request のバリデーション
> → Review 作成 → リダイレクトの流れにしてください。
> ルーティングも追加してください。
```

<details>
<summary>生成されたコードの例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なるコードが生成されます。

```php
// app/Http/Controllers/ReviewController.php
class ReviewController extends Controller
{
    public function store(StoreReviewRequest $request, Course $course)
    {
        $this->authorize('create', [Review::class, $course]);

        try {
            Review::create([
                'user_id' => auth()->id(),
                'course_id' => $course->id,
                'rating' => $request->validated()['rating'],
                'comment' => $request->validated()['comment'],
            ]);

            return redirect()->route('courses.show', $course)
                ->with('success', 'レビューを投稿しました。');
        } catch (\Exception $e) {
            return redirect()->route('courses.show', $course)
                ->with('error', 'レビューの投稿に失敗しました。');
        }
    }
}
```

ポイントを確認しましょう。

- Controller は薄く保たれています。バリデーションは `StoreReviewRequest`、認可は `ReviewPolicy` に委譲
- エラーハンドリングは `EnrollmentController` と同じパターン（try-catch + flash メッセージ）
- `$request->validated()` でバリデーション済みの値のみを使用しています

</details>

**Step 4-4: View の追加**

```
> コース詳細画面（courses/show.blade.php）にレビュー一覧と投稿フォームを追加してください。
> 既存の Blade テンプレートのスタイリングパターンに合わせてください。
> 受講完了した student にのみ投稿フォームを表示してください。
```

View が追加されたら、ブラウザで確認しましょう。`http://localhost/courses/{course}` にアクセスして、レビューセクションが表示されるか確認します。

<!-- TODO: 画像追加 - コース詳細画面にレビューセクションが追加された状態 -->

> 💡 View の確認はブラウザで行うのが最も確実です。Blade テンプレートの表示崩れやレイアウトの問題は、コードだけでは気づきにくいものです。

**Step 4-5: Course モデルにリレーションを追加**

Review モデルを作成したので、Course モデルにも `reviews()` リレーションを追加する必要があります。Claude Code が自動で追加している場合もありますが、確認してください。

```
> Course モデルに reviews() リレーションが追加されているか確認してください。
> なければ追加してください。
```

### Step 5: `/simplify` で品質チェックする

実装が完了したら、`/simplify` で品質チェックを行います。`/simplify` は変更されたコードの再利用性、品質、効率性をチェックし、問題があれば修正を提案するコマンドです。

```
/simplify
```

Claude Code が変更したファイルを分析し、改善点があれば報告します。たとえば以下のような指摘が出る可能性があります。

- Controller のメソッドが肥大化していないか
- 重複したクエリがないか
- 不要な変数がないか

指摘内容を確認し、妥当であれば修正を適用してください。

### Step 6: テストを書いて検証する

コースレビュー機能のテストケースを設計します。

| テストケース | 期待結果 |
|---|---|
| 受講完了した student がレビューを投稿する | 成功（Review が作成される） |
| 受講中（active）の student がレビューを投稿しようとする | 403 Forbidden |
| coach がレビューを投稿しようとする | 403 Forbidden |
| 同じ student が同じコースに2件目を投稿しようとする | 403 Forbidden |
| 評価（rating）が 0 または 6 で投稿する | バリデーションエラー |
| コメントなしで投稿する | 成功（comment は任意） |
| コース詳細画面にレビュー一覧が表示される | レビューが表示される |

```
> 以下のテストケースでコースレビュー機能のテストを作成してください。
> 既存のテストスタイルに従ってください。
>
> [上記のテストケース一覧を貼り付ける]
```

```
/test
```

全てのテストが通ることを確認したら、コミットします。

```
> コースレビュー機能の変更をコミットしてください。
> rules/git.md の命名規則に従ってください
```

### 🔍 見極めチェック: コースレビュー機能

> 🧠 先輩エンジニアの思考: 「新規機能は自由度が高いからこそ、既存パターンとの整合性が崩れやすい。特に Policy の設計と Form Request の使い方は、プロジェクト全体の一貫性に直結する。Claude Code が提案した設計を鵜呑みにせず、既存コードと見比べながら判断しよう。」

- [ ] **正しさ**: 受講完了した student のみ投稿できるか。1コース1件の制約が機能しているか。星評価のバリデーションが正しいか。テストが全て通るか
- [ ] **品質**: ReviewPolicy が SubmissionPolicy と同じパターンに従っているか。StoreReviewRequest が StoreLessonRequest と同じパターンに従っているか。ReviewController が EnrollmentController のような薄い Controller になっているか。不要に Service クラスが作られていないか。Blade テンプレートのスタイリングが既存のパターンと統一されているか
- [ ] **安全性**: 認可チェックが Policy で実装されているか（Controller に直書きされていないか）。バリデーションが Form Request で実装されているか。CSRF トークンがフォームに含まれているか

> 🔑 この実践では特に「品質」に注目してください。新規構築では設計の自由度が高いぶん、Claude Code が既存パターンから逸脱したコードを生成しやすくなります。「動くかどうか」だけでなく「既存コードに馴染んでいるか」を確認しましょう。

---

## ふりかえり: 拡張 vs 新規構築

2つの機能開発を振り返り、アプローチの違いを整理しましょう。

| 観点 | 小テスト再受験（拡張） | コースレビュー（新規構築） |
|---|---|---|
| 事前のコードリーディング | 拡張対象（Quiz/Submission フロー）を詳細に読んだ | 類似機能（Enrollment パターン）を参考として読んだ |
| 設計フェーズ | 変更箇所の特定が中心（Plan Mode 不使用） | Plan Mode で全体設計を検討 |
| Claude Code への指示 | 「既存の○○を修正して」（変更範囲を指定） | 「○○のパターンに従って作成して」（参考パターンを指定） |
| テストの重点 | 既存機能が壊れていないか + 新機能の動作 | 新機能の動作 + 認可・バリデーション |
| 見極めの焦点 | 既存コードとの整合性 | 設計パターンの一貫性 |

どちらのパターンでも共通していたのは以下のポイントです。

- **着手前に既存コードを読む**: 何も読まずに「作って」と依頼しない
- **要件を明確にしてから実装する**: Claude Code に仕様の判断を委ねない
- **段階的に実装・検証する**: 一度に全てを作らない
- **既存パターンを指示に含める**: 「○○のパターンに従って」と具体的に伝える

---

### ✅ 完成チェックリスト

- [ ] 小テスト再受験: 合格済みの場合に再受験が防止される
- [ ] 小テスト再受験: 不合格の場合に再受験できる
- [ ] 小テスト再受験: 結果画面に受験履歴が表示される
- [ ] 小テスト再受験: テストが全て通る
- [ ] コースレビュー: 受講完了した student がレビューを投稿できる
- [ ] コースレビュー: 1コース1件の制約が機能している
- [ ] コースレビュー: Policy・Form Request・Controller が既存パターンに従っている
- [ ] コースレビュー: `/simplify` で品質チェック済み
- [ ] コースレビュー: テストが全て通る
- [ ] Hooks（Laravel Pint）が正しく動作している
- [ ] 2つの機能がそれぞれ個別にコミットされている

---

## ✨ まとめ

- 既存機能の拡張では、**拡張対象のコードを詳細に読み**、既存の処理フローを壊さない制約の中で変更を加える。Claude Code への指示には「既存の○○を修正して」と変更範囲を明示する
- 新規機能の構築では、**類似機能のパターンを参考にし**、Plan Mode で設計を固めてから段階的に実装する。Claude Code への指示には「○○のパターンに従って」と参考パターンを明示する
- セッション管理（`/rename` と `--resume`）を活用することで、中断・再開を繰り返す機能開発でもコンテキストを維持できる
- Hooks で自動フォーマットを設定すると、Claude Code が生成するコードが自動的にプロジェクトのスタイルに整形される
- 見極めの3観点（正しさ・品質・安全性）のうち、機能開発では **品質（既存設計との整合性）** が特に重要。「動くかどうか」だけでなく「既存コードに馴染んでいるか」を確認する
- テストケースは自分で設計してから Claude Code に実装を依頼する。特に認可とバリデーションのテストは網羅的に書く

---

次の Chapter では、CourseHub の既存コードを改善（リファクタリング）します。機能開発は「新しい価値を加える」タスクでしたが、リファクタリングは「既存のコードを内部的に改善する」タスクです。動作を変えずにコードの品質を上げるために、テストで動作不変を保証する方法を学びます。
