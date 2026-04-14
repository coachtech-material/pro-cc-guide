# 3-5-2 CourseHub のコードを改善する

## 🎯 このセクションで学ぶこと

- Fat Controller の責務分離を、Plan Mode で段階的に進め、各ステップでテストを実行して動作不変を保証できる
- Claude Code の過剰な改善提案（Service 層の導入等）を、プロジェクトの規約と照らして判断できる
- N+1 クエリの問題を特定し、Eager Loading で解消できる

2つの問題を改善します。1つ目の Fat Controller で「コード構造の改善」のアプローチを実践し、2つ目の N+1 クエリで「パフォーマンスの改善」のアプローチを実践します。

> 📝 このセクションで使う機能: Plan Mode（[2-3-1 Plan Mode](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-1_Plan%20Mode.md) で学習）、`/test` Skill（[3-1-3 プロジェクトの規約・設定を確認する](../chapter-01_実践の準備/3-1-3_プロジェクトの規約・設定を確認する.md) で更新）、`/cost`、`/context`

---

## 導入: 「動くけど触りたくないコード」に向き合う

Chapter 3-4 で機能を開発したとき、`CoachCourseController@store` が 200 行近い Fat Controller であることに触れました。また、コース一覧や生徒一覧の画面では、データベースへの問い合わせが非効率に行われている可能性があります。

どちらも「動いている」コードです。機能は正しく動作しています。しかし、このままでは次にこのコードを変更するとき（機能追加やバグ修正のとき）に余計な時間がかかります。Fat Controller は 200 行の中から該当箇所を探す必要があり、N+1 クエリはデータが増えるほど画面の表示が遅くなります。

この Chapter では、[3-5-1 リファクタリングの方法論](3-5-1_リファクタリングの方法論.md) で学んだリファクタリングのフロー（対象特定→テスト確認→改善→テスト再実行）を CourseHub で実践します。

### 🧠 先輩エンジニアはこう考える

> リファクタリングのきっかけとして一番多いのは、機能開発やバグ修正で関連コードを読んでいるときに問題点に気づくパターンだ。ただし、[3-3-1 バグ修正の方法論](../chapter-03_バグを修正する/3-3-1_バグ修正の方法論.md) で学んだ通り、バグ修正やリファクタリングを同じコミットに混ぜるのは NG。気づいた問題はメモしておいて、タスクを分けて着手する。
>
> 今回は Chapter 3-4 の機能開発が終わったタイミングでリファクタリングに取り組む。これも実務では自然な流れ。機能を追加する過程でコードの問題点が見えてくるから、それを別のタスクとして整理する。

---

## 🏃 実践①: Fat Controller の責務分離（コード構造の改善）

> 📌 [3-1-2 セットアップと動作確認](../chapter-01_実践の準備/3-1-2_セットアップと動作確認.md) で説明したとおり、各 Chapter のハンズオンは **必ず `main` ブランチから新しい作業ブランチを切って** 進めてください。前 Chapter の機能開発ブランチに残ったままだと、Claude Code が追加機能込みのコードを前提に動いてしまいます。`/clear` で会話履歴を消してもファイルの状態は残るため、Git でブランチを切り替えて素の状態に戻すことが必要です。

### Step 0: 作業ブランチを作成する

`main` ブランチから作業ブランチを切ります。

```
> main ブランチに切り替えて最新化したあと、refactor/fat-controller ブランチを作成してください
```

### Step 1: 改善対象を確認する

CourseHub の `CoachCourseController@store` は、コースの新規作成を処理するメソッドです。まず、このメソッドの現状を Claude Code で確認しましょう。

```
> CoachCourseController の store メソッドを読んで、何をしているか責務ごとに整理してください。
```

Claude Code が分析すると、このメソッドが **1つのメソッド内に複数の責務を詰め込んでいる** ことがわかります。

<details>
<summary>分析結果の例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なる分析結果が表示されます。

Claude Code はおおむね以下のような責務を特定するはずです。

1. バリデーション（約 30 行）
2. スラッグ生成（重複チェック付きループ、約 15 行）
3. 画像アップロード処理（約 20 行）
4. Course レコード作成（約 15 行）
5. タグの同期（新規タグ作成 + pivot 更新、約 25 行）
6. 初期 Chapter の自動作成（約 10 行）
7. ステータスに応じた published_at の設定（約 10 行）
8. リダイレクト処理（約 10 行）
9. try-catch による全体のエラーハンドリング（約 10 行）

合計で約 200 行近いメソッドです。これは明確な Fat Controller（[3-5-1 リファクタリングの方法論](3-5-1_リファクタリングの方法論.md) で学んだコードスメル）です。

</details>

次に、このコードの問題点をプロジェクトの規約と照らし合わせます。`rules/coding.md` を思い出してください。

> Controller ではバリデーションに Form Request を使用する

しかし、`CoachCourseController@store` はバリデーションを `$request->validate()` でインラインに実装しています。これは **規約違反** です。README のコーディング規約にも「Form Request を使用する」と記載されています。

> 💡 [3-1-3 プロジェクトの規約・設定を確認する](../chapter-01_実践の準備/3-1-3_プロジェクトの規約・設定を確認する.md) で規約と実態のズレを確認しましたね。`CoachCourseController` はそのズレの1つでした。ここでそれを実際に修正します。

### Step 1: テストを確認する

リファクタリングの鉄則に従い、まず既存のテストを確認します。

```
/test
```

テストが通ることを確認してください。`tests/Feature/CourseTest.php` にコース作成のテスト（`test_coach_can_create_course`）が含まれています。

ただし、このテストは基本的な作成フローしかカバーしていません。画像アップロード、スラッグ生成の重複処理、新規タグ作成などはテストされていません。

[3-5-1 リファクタリングの方法論](3-5-1_リファクタリングの方法論.md) で学んだ通り、**テストがない機能のリファクタリングは危険** です。リファクタリング前に、カバーされていない処理のテストを追加しましょう。

```
> CoachCourseController@store のテストを確認しました。
> 以下の処理がテストされていないので、リファクタリング前にテストを追加してください。
> 既存のテストスタイルに従ってください。
>
> - 画像付きのコース作成
> - status が published の場合に published_at が設定されること
> - タグの同期（既存タグの紐付け）
> - 初期 Chapter が自動作成されること
```

```
/test
```

追加したテストが全て通ることを確認します。これが「リファクタリング前のベースライン」になります。このテストが通り続ける限り、リファクタリングが動作を変えていないことを証明できます。

### Step 2: Plan Mode でリファクタリング計画を立てる

Shift+Tab で Plan Mode に切り替え、リファクタリングの計画を立てます。

```
> CoachCourseController@store を段階的にリファクタリングしたいです。
> 以下の方針で計画を立ててください。
>
> - バリデーションを Form Request に抽出する（rules/coding.md の規約に従う）
> - 残りの処理を private メソッドに分割する
> - 1ステップ1つの責務の抽出で、各ステップ後にテストを実行する
> - 既存の LessonController の Form Request パターンを参考にする
```

Claude Code がリファクタリング計画を提示します。計画の内容を確認しましょう。

<details>
<summary>計画の例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なる計画が提示されます。

おおむね以下のようなステップが提示されるはずです。

**ステップ 1**: バリデーションを `StoreCourseRequest` に抽出する
- `app/Http/Requests/StoreCourseRequest.php` を作成
- バリデーションルールを移動
- `store` メソッドの引数を `Request` から `StoreCourseRequest` に変更

**ステップ 2**: スラッグ生成を `generateUniqueSlug()` private メソッドに抽出する

**ステップ 3**: 画像アップロードを `uploadImage()` private メソッドに抽出する

**ステップ 4**: タグ同期を `syncTags()` private メソッドに抽出する

**ステップ 5**: 初期 Chapter 作成と published_at 設定を `initializeCourse()` private メソッドに抽出する

</details>

> ⚠️ **Claude Code が Service クラスへの切り出しを提案した場合**: Claude Code は「より良い設計」として Service クラスの導入を提案することがあります。CourseHub の README には「ビジネスロジックが複雑な場合は Service クラスに切り出す」とありますが、今回の課題は「1つのメソッドが長すぎる」ことです。Form Request への抽出と private メソッドへの分割で十分に解決できます。
>
> [3-2-2 知らない技術への向き合い方](../chapter-02_既存コードを理解する/3-2-2_知らない技術への向き合い方.md) で学んだ対処フローを思い出してください。Service クラスは既に `EnrollmentService` として CourseHub に存在するパターンです。Claude Code が Service クラスを提案した場合は、以下のように判断します。
>
> - **理解**: Service クラスが何をするものか確認する（`EnrollmentService` を参考に）
> - **評価**: 今の問題（Fat Controller）の解決に Service クラスが必要か判断する
> - **判断**: Form Request + private メソッド分割で十分なら、Service クラスの導入は見送る
>
> 「動くコードが書ける」ことと「このプロジェクトに適切な設計判断ができる」ことは別です。Claude Code の提案を鵜呑みにせず、プロジェクトの現状に合った判断をすることが、[3-5-1 リファクタリングの方法論](3-5-1_リファクタリングの方法論.md) で学んだ「改善提案を評価する3つの基準」の実践です。

計画に納得できたら、Shift+Tab で Plan Mode を解除し、1ステップずつ実行します。

### Step 3: 段階的にリファクタリングする

**ステップ 1: バリデーションを Form Request に抽出する**

```
> リファクタリング計画のステップ 1 を実行してください。
> CoachCourseController@store のバリデーションを StoreCourseRequest に抽出してください。
> StoreLessonRequest のパターンに従ってください。
```

<details>
<summary>生成されたコードの例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なるコードが生成されます。

```php
// app/Http/Requests/StoreCourseRequest.php
class StoreCourseRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'category_id' => ['required', 'exists:categories,id'],
            'description' => ['required', 'string', 'min:10'],
            'difficulty' => ['required', 'in:beginner,intermediate,advanced'],
            'status' => ['required', 'in:draft,published'],
            'image' => ['nullable', 'image', 'mimes:jpeg,png,jpg,gif', 'max:2048'],
            'tags' => ['nullable', 'array'],
            'tags.*' => ['exists:tags,id'],
            'new_tags' => ['nullable', 'string'],
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => 'コースタイトルは必須です。',
            'category_id.required' => 'カテゴリを選択してください。',
            'description.required' => 'コース概要は必須です。',
            'description.min' => 'コース概要は10文字以上で入力してください。',
            'difficulty.required' => '難易度を選択してください。',
            'status.required' => 'ステータスを選択してください。',
            'image.max' => '画像は2MB以下でアップロードしてください。',
        ];
    }
}
```

ポイントを確認しましょう。

- `StoreLessonRequest` と同じ構造（`authorize()`, `rules()`, `messages()`）に従っています
- バリデーションルールは元のインラインバリデーションと同一です。**ルールが変わっていないこと** がリファクタリングの要件です
- 日本語のエラーメッセージが定義されています

</details>

テストを実行して、動作が変わっていないことを確認します。

```
/test
```

> 🔑 **リファクタリングの核心**: テストが全て通れば、バリデーションロジックの「移動」は成功です。ルールそのものは変わっていない（動作不変）のに、コードの配置が改善されました。これがリファクタリングです。

**ステップ 2〜4: private メソッドへの分割**

同様に、残りの責務を1つずつ private メソッドに抽出します。

```
> ステップ 2 を実行してください。
> スラッグ生成の処理を generateUniqueSlug() private メソッドに抽出してください。
```

```
/test
```

```
> ステップ 3 を実行してください。
> 画像アップロード処理を uploadImage() private メソッドに抽出してください。
```

```
/test
```

```
> ステップ 4 を実行してください。
> タグ同期処理を syncTags() private メソッドに抽出してください。
```

```
/test
```

各ステップの後にテストを実行し、全てのテストが通ることを確認してください。テストが失敗した場合は、直前のステップで動作を変えてしまっている箇所があるはずです。Claude Code に失敗したテストの内容を伝え、原因を調査してもらいましょう。

> ⚠️ **よくあるエラー**: バリデーションルールの微妙な変更
>
> ```
> Failed asserting that session has errors.
> ```
>
> **原因**: Form Request に移す際にバリデーションルールを変更してしまった（例: `required` を追加・削除した、`max` の値を変えた等）
>
> **対処法**: 元の `$request->validate()` のルールと `StoreCourseRequest@rules()` のルールを比較し、完全に一致していることを確認してください。

### Step 4: リファクタリング結果を確認する

全てのステップが完了したら、リファクタリング後の `store` メソッドを確認します。

```
> CoachCourseController の store メソッドを表示してください。
```

<details>
<summary>リファクタリング後のコード例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なるコードが生成されます。

```php
// app/Http/Controllers/CoachCourseController.php
public function store(StoreCourseRequest $request)
{
    try {
        $slug = $this->generateUniqueSlug($request->title);
        $imagePath = $this->uploadImage($request);

        $course = Course::create([
            'user_id' => auth()->id(),
            'category_id' => $request->category_id,
            'title' => $request->title,
            'slug' => $slug,
            'description' => $request->description,
            'difficulty' => $request->difficulty,
            'status' => $request->status,
            'image_path' => $imagePath,
        ]);

        $this->syncTags($course, $request);

        $course->chapters()->create([
            'title' => 'はじめに',
            'order' => 1,
        ]);

        if ($course->status === 'published') {
            $course->update(['published_at' => now()]);
        }

        return redirect()->route('coach.courses.index')
            ->with('success', 'コースを作成しました。');
    } catch (\Exception $e) {
        \Log::error('コース作成エラー: ' . $e->getMessage());
        return back()->withInput()->with('error', 'コースの作成に失敗しました。');
    }
}
```

200 行近くあったメソッドが約 30 行になりました。各責務が独立した private メソッドに分離され、`store` メソッドは処理の流れだけを記述しています。

</details>

### Step 5: コストを確認する

リファクタリングの作業が一段落したので、ここまでのセッションのコスト（トークン使用量）を確認してみましょう。

```
/cost
```

<!-- TODO: 画像追加 - /cost の出力例 -->

`/cost` は現在のセッションの API 使用状況を表示します。リファクタリングは Plan Mode での計画立案と段階的な実行を繰り返すため、トークン消費が多くなりがちです。コストを意識しながら作業を進める習慣をつけましょう。

> 💡 **Max プランの場合**: `/cost` の代わりに `/stats` を使います。`/stats` はセッションのトークン使用量やメッセージ数などの統計を表示するコマンドです。Max プランは API 課金ではなくサブスクリプションなので、`/cost` の金額は直接的な料金には関係しません。それでも、トークン使用量を把握することでコンテキストの管理に役立ちます。

### Step 6: コミットする

テストが全て通り、リファクタリングの結果に問題がなければコミットします。

```
> Fat Controller のリファクタリングをコミットしてください。
> rules/git.md の命名規則に従ってください。
```

### 🔍 見極めチェック: Fat Controller の責務分離

> 🧠 先輩エンジニアの思考: 「リファクタリングの見極めは『動作が変わっていないこと』が最優先。テストが全て通ったからといって安心するのではなく、バリデーションルールが完全に一致しているか、エラーハンドリングの挙動が変わっていないかも確認する。特にバリデーションは、ルールの微妙な変更がユーザーの入力体験に影響するから注意が必要だ。」

- [ ] **正しさ**: リファクタリング前と全く同じ動作をしているか。テストが全て通っているか。バリデーションルールが元と完全に一致しているか。スラッグ生成・画像アップロード・タグ同期の挙動が変わっていないか
- [ ] **品質**: `StoreCourseRequest` が `StoreLessonRequest` と同じパターンに従っているか。private メソッドの責務が適切に分割されているか（1メソッド1責務）。`rules/coding.md` の「Form Request を使用する」規約に準拠しているか。過剰な抽象化（不要な Service クラス等）が導入されていないか
- [ ] **安全性**: バリデーションルールが緩くなっていないか（例: `required` が外れていないか）。画像アップロードのファイルサイズ制限が維持されているか

> 🔑 この実践では特に「正しさ」に注目してください。リファクタリングの最も重要な検証ポイントは「動作が変わっていない」ことです。テストが通っていることに加え、バリデーションルールやエラーハンドリングの細部まで確認しましょう。

---

## 🏃 実践②: N+1 クエリの解消（パフォーマンスの改善）

次に、パフォーマンスの問題を改善します。CourseHub のコース一覧画面で N+1 クエリが発生しています。

> 📌 実践①のブランチ（`refactor/fat-controller`）にいる場合は、`main` に戻ってから新しい作業ブランチを切ります。

### Step 0: 作業ブランチを作成する

`main` ブランチから作業ブランチを切ります。

```
> main ブランチに切り替えて最新化したあと、refactor/n-plus-one ブランチを作成してください
```

### N+1 クエリとは

N+1 クエリとは、一覧データを取得するときに「1回のクエリで一覧を取得 + N回のクエリで各項目の関連データを取得」してしまう問題です。

たとえば、コース一覧でコースが 12 件あり、各コースのコーチ名を表示する場合を考えます。

```
1回: SELECT * FROM courses WHERE status = 'published' ...   ← コース一覧を取得
1回: SELECT * FROM users WHERE id = 1                        ← コース1のコーチを取得
1回: SELECT * FROM users WHERE id = 2                        ← コース2のコーチを取得
...（コースの数だけ繰り返し）
1回: SELECT * FROM users WHERE id = 12                       ← コース12のコーチを取得
```

合計 13 回のクエリが実行されます。さらにカテゴリ名、Chapter 数、受講者数も表示するなら、12 × 4 + 1 = 49 回のクエリになります。

Laravel では Eager Loading（`with()` や `withCount()`）を使うことで、これを数回のクエリにまとめられます。

```
1回: SELECT * FROM courses WHERE status = 'published' ...   ← コース一覧を取得
1回: SELECT * FROM users WHERE id IN (1, 2, ..., 12)        ← コーチをまとめて取得
1回: SELECT * FROM categories WHERE id IN (1, 3, 5)         ← カテゴリをまとめて取得
```

データ量が少ないうちは気にならなくても、コースが 100 件、1,000 件と増えるに従って画面の表示速度に大きく影響します。

### コース一覧の N+1 問題を特定する

CourseHub のコース一覧画面で N+1 クエリが発生しています。Claude Code に分析を依頼しましょう。

```
> CourseController@index（コース一覧）で N+1 クエリが発生していないか分析してください。
> Controller のクエリと、対応する Blade テンプレートでアクセスしているリレーションを
> 照らし合わせて確認してください。
```

<details>
<summary>分析結果の例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なる分析結果が表示されます。

**コース一覧（`CourseController@index`）**

Controller のクエリ:
```php
$courses = Course::where('status', 'published')->latest()->paginate(12);
```

Blade テンプレートでアクセスしているリレーション:

- `$course->category->name` → カテゴリ（N+1）
- `$course->user->name` → コーチ名（N+1）
- `$course->chapters->count()` → Chapter 数（N+1）
- `$course->enrollments->count()` → 受講者数（N+1）

12 件のコースがある場合、1 + 12 × 4 = **49 回のクエリ** が実行されます。

</details>

### Step 1: コース一覧の N+1 を解消する

分析結果をもとに、Eager Loading を追加して N+1 クエリを解消します。

```
> CourseController@index の N+1 クエリを解消してください。
>
> 現状: Course::where('status', 'published')->latest()->paginate(12) で
> Eager Loading なしのため、Blade で category, user, chapters, enrollments に
> アクセスするたびにクエリが発生しています。
>
> 修正方針:
> - with() で category と user を Eager Loading する
> - withCount() で chapters と enrollments のカウントを取得する
> - Blade テンプレートで chapters->count() を chapters_count に変更する
> - enrollments->count() を enrollments_count に変更する
>
> テストがあれば実行して動作確認してください。
```

<details>
<summary>修正コードの例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なるコードが生成されます。

```php
// app/Http/Controllers/CourseController.php
public function index(Request $request)
{
    $query = Course::where('status', 'published')
        ->with(['category', 'user'])
        ->withCount(['chapters', 'enrollments']);

    // ... 検索・フィルタ処理は変更なし ...

    $courses = $query->latest()->paginate(12);
    $categories = Category::all();

    return view('courses.index', compact('courses', 'categories'));
}
```

Blade テンプレートの変更:
```blade
{{-- 変更前 --}}
{{ $course->chapters->count() }} チャプター
{{ $course->enrollments->count() }}名受講中

{{-- 変更後 --}}
{{ $course->chapters_count }} チャプター
{{ $course->enrollments_count }}名受講中
```

ポイントを確認しましょう。

- `with(['category', 'user'])` でカテゴリとコーチの情報を一括取得します。12 件のコースのコーチを個別に取得する代わりに、1回のクエリで全コーチをまとめて取得します
- `withCount(['chapters', 'enrollments'])` は、リレーション先のレコードを全件取得する代わりに、`COUNT(*)` のサブクエリで件数だけを取得します。Blade テンプレートでは `$course->chapters_count` でアクセスします
- 49 回のクエリが 3〜4 回に削減されます

</details>

### Step 2: テストを実行して動作確認する

```
/test
```

テストが通ったら、ブラウザでコース一覧画面を表示し、表示内容がリファクタリング前と変わっていないことも目視で確認しましょう。

### Step 3: コミットする

```
> N+1 の修正をコミットしてください。rules/git.md の命名規則に従ってください。
```

> 💡 **余裕があれば挑戦**: 生徒一覧（`AdminStudentController@index`）でも同じ N+1 パターンが発生しています。コース一覧で学んだアプローチ（`withCount()` の追加と Blade テンプレートの `_count` プロパティへの変更）をそのまま適用できます。自主課題として取り組んでみてください。

### コンテキスト使用量を確認する

ここまでの作業でコンテキストをどれだけ使ったか確認してみましょう。

```
/context
```

<!-- TODO: 画像追加 - /context の出力例 -->

リファクタリングでは Plan Mode の計画、コードの分析、段階的な修正、テスト実行を繰り返すため、コンテキストの消費が多くなります。コンテキストが上限に近づいている場合は、`/compact` で整理することを検討してください。

### 🔍 見極めチェック: N+1 クエリの解消

> 🧠 先輩エンジニアの思考: 「N+1 の修正はシンプルに見えるけど、`with()` と `withCount()` の使い分けが大事だ。件数だけ必要なら `withCount()` の方が効率的。全データが必要なら `with()` を使う。修正後にブラウザで一覧画面を確認して、表示内容が変わっていないことも目視で確かめておこう。」

- [ ] **正しさ**: コース一覧の表示内容がリファクタリング前と同一か。テストが全て通っているか。`withCount()` で取得した件数が `count()` で取得した件数と一致しているか
- [ ] **品質**: `with()` と `withCount()` が適切に使い分けられているか（件数のみなら `withCount()`、データも必要なら `with()`）。Blade テンプレートで `chapters_count` のように `withCount` の命名規則に従っているか
- [ ] **安全性**: N+1 の解消ではセキュリティ上の問題は発生しにくい。該当なし

> 🔑 この実践では特に「正しさ」に注目してください。パフォーマンス改善でクエリの構造を変えたとき、取得結果が変わっていないことの確認が最重要です。特に `withCount()` に切り替えた場合、Blade テンプレートでのアクセス方法（`->count()` から `_count` プロパティ）も変わるため、表示が正しいことを必ず確認しましょう。

---

## ふりかえり: 構造改善 vs パフォーマンス改善

2つのリファクタリングを振り返り、アプローチの違いを整理しましょう。

| 観点 | Fat Controller（構造改善） | N+1 クエリ（パフォーマンス改善） |
|---|---|---|
| 改善対象 | 1ファイル（CoachCourseController） | コース一覧画面 |
| 事前準備 | テスト追加 + Plan Mode で計画 | 問題の特定（クエリ分析） |
| 作業の進め方 | 段階的（1責務ずつ抽出） | Eager Loading の追加 + Blade の修正 |
| テストの役割 | 各ステップの動作不変の証明 | 修正後の表示内容の確認 |
| Claude Code の活用 | Plan Mode で計画 → 段階実行 | 問題分析 → Eager Loading 提案 |
| 判断が必要だった場面 | Service 層の導入を見送る判断 | `with()` と `withCount()` の使い分け |

どちらのパターンでも共通していたのは以下のポイントです。

- **テストが安全網**: リファクタリング前にテストを確認（なければ追加）し、各ステップで実行する
- **小さく進める**: 一度に全てを変えず、1つの変更→テスト→次の変更のサイクルを守る
- **動作不変が最優先**: 「良くしたい」気持ちに引きずられて動作まで変えてしまわないよう注意する
- **過剰な改善を避ける**: Claude Code の提案を鵜呑みにせず、今の問題に対して十分な改善かを判断する

---

### ✅ 完成チェックリスト

- [ ] Fat Controller: `StoreCourseRequest` が作成され、バリデーションが Form Request に移動している
- [ ] Fat Controller: `store` メソッドが private メソッドに分割され、見通しが良くなっている
- [ ] Fat Controller: リファクタリング前後でテストが全て通っている
- [ ] Fat Controller: `rules/coding.md` の「Form Request を使用する」規約に準拠している
- [ ] N+1: コース一覧で `with()` と `withCount()` が追加されている
- [ ] N+1: Blade テンプレートで `_count` プロパティを使用している
- [ ] N+1: テストが全て通っている
- [ ] 全ての変更がコミットされている

---

## ✨ まとめ

- Fat Controller の責務分離は **Plan Mode で計画を立て、1責務ずつ段階的に進める** 。各ステップでテストを実行し、動作不変を証明する
- Claude Code が Service クラスなど過剰な改善を提案した場合は、「規約に合っているか」「既存パターンと一貫しているか」「今の問題を解決するのに十分か」の3基準で判断する
- N+1 クエリの解消は `with()`（リレーション全体の取得）と `withCount()`（件数のみの取得）を使い分ける。件数だけ必要なら `withCount()` が効率的
- N+1 の解消パターンは汎用的。1箇所で習得すれば、同じアプローチを他の画面（生徒一覧等）にもそのまま適用できる
- `/cost` でセッションのトークン使用量を、`/context` でコンテキスト消費を確認できる。リファクタリングはコンテキスト消費が多いため、定期的に確認する習慣をつける
- 見極めの3観点（正しさ・品質・安全性）のうち、リファクタリングでは **正しさ（動作不変の保証）** が最も重要。テストを安全網として活用し、各ステップで確実に通過させる

---

次の Chapter では、これまでの変更をチームに共有します。リファクタリングで改善したコードを PR にまとめ、レビュー対応、CI/CD の設定、チーム全体での Claude Code 活用の環境整備に取り組みます。
