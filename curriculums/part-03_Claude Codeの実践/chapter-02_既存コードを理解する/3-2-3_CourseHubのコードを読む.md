# 3-2-3 CourseHub のコードを読む

## 🎯 このセクションで学ぶこと

- Sub-agents を使ってプロジェクトの全体像を効率的に把握する
- モデル・リレーション、認可の仕組み、設計パターンからコードの構造を理解する
- 業務フロー（受講登録からコース完了まで）をコードで追跡し、Claude の説明を自分の目で検証する
- 知らない技術パターン（Service クラス、Event/Listener）に遭遇し、対処フローを実践する

[3-2-1 コードリーディングの方法論](3-2-1_コードリーディングの方法論.md) で学んだ方法論（探索→検索→転写→理解→増強の5ステップ）を、全体像→構造→フローの流れで CourseHub のコードに適用し、実際に読み解きます。

> 📝 このセクションで使う機能: Sub-agents（[2-3-5 Sub-agents](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-5_Sub-agents.md) で学習）、MCP（[2-3-4 MCP](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-4_MCP.md) で学習）、`/context`・`/compact`・`/btw`（[2-2-2 コンテキストとセッション管理](../../part-02_Claude%20Codeの基礎/chapter-02_基本を理解する/2-2-2_コンテキストとセッション管理.md) で学習）

---

## 🏃 実践 1: 全体像を把握する

最初のステップは、CourseHub がどんなプロジェクトなのかを俯瞰的に把握することです。[3-1-2 セットアップと動作確認](../chapter-01_実践の準備/3-1-2_セットアップと動作確認.md) でセットアップし、[3-1-3 プロジェクトの規約・設定を確認する](../chapter-01_実践の準備/3-1-3_プロジェクトの規約・設定を確認する.md) で README やコーディング規約を確認しましたが、まだ「コードそのもの」には深く踏み込んでいません。

ここでは Claude Code の Sub-agents を活用して、大量のファイルを一気に探索します。

### Step 1: Sub-agents でプロジェクトを探索する

CourseHub のディレクトリで Claude Code を起動してください（すでに起動している場合はそのまま進めます）。

以下のプロンプトを入力します。

```
> CourseHub のプロジェクト構造を調べて全体像を教えて。
> 以下の3点をそれぞれ調査してほしい:
> 1. ディレクトリ構成（app/ 配下の主要ディレクトリとその役割）
> 2. 全 Eloquent モデルの一覧とリレーション（belongsTo, hasMany 等）
> 3. routes/web.php のルーティング定義（どんな画面・操作があるか）
```

Claude は内部で Sub-agents を起動し、複数のファイルを並行して探索します。メインのコンテキストウィンドウを消費せずにファイルを読んでくれるので、大量のファイルを効率的に調査できます。

> 💡 あなたの環境では、Claude の応答が異なる場合があります。Claude はプロンプトに応じて探索方法を判断するため、Sub-agents の使い方や出力の形式は実行ごとに変わることがあります。重要なのは、結果として「ディレクトリ構成」「モデル・リレーション」「ルーティング」の情報が得られることです。

### Step 2: 探索結果を確認する

Claude が返す探索結果には、おおよそ以下のような情報が含まれるはずです。

**ディレクトリ構成:**

```
app/
├── Console/             # Artisan コマンド
├── Events/              # イベントクラス
├── Exceptions/          # 例外ハンドラ
├── Http/
│   ├── Controllers/     # 16個の Controller
│   ├── Middleware/       # RoleMiddleware 等
│   └── Requests/        # Form Request（一部のみ使用）
├── Listeners/           # イベントリスナー
├── Models/              # 12個の Eloquent モデル
├── Policies/            # 認可 Policy
├── Providers/           # サービスプロバイダ
└── Services/            # ビジネスロジック（EnrollmentService のみ）
```

**モデルのリレーション（主要なもの）:**

```
User ─── hasMany ──→ Course（coach として作成）
  │                     │
  │                     ├── hasMany ──→ Chapter ──→ hasMany ──→ Lesson
  │                     │                                         │
  │                     ├── hasMany ──→ Enrollment                ├── hasOne ──→ Quiz
  │                     │                                         │               │
  │                     └── belongsToMany ──→ Tag                 │           hasMany → Question
  │                                                               │                       │
  ├── hasMany ──→ Enrollment                                      │                   hasMany → Option
  ├── hasMany ──→ LessonProgress ←── belongsTo ─── Lesson ←──────┘
  └── hasMany ──→ Submission ←── belongsTo ─── Quiz
```

**ルーティングの概要:**

| グループ | パス | 内容 |
|---|---|---|
| 全ロール共通 | `/courses`, `/courses/{course}` | コース閲覧 |
| student | `/my-courses`, `/courses/{course}/enroll` 等 | 受講・進捗・小テスト |
| coach（`/coach` prefix） | `/coach/courses`, `/coach/courses/{course}/chapters` 等 | コース・Chapter・Lesson・Quiz の管理 |
| admin（`/admin` prefix） | `/admin/users`, `/admin/courses`, `/admin/categories` | ユーザー・コース・カテゴリ管理 |

これらの情報から、CourseHub が「コース→チャプター→レッスン→小テスト」の階層構造を持ち、3つのロール（admin / coach / student）で機能が分かれていることが把握できます。

### Step 3: `/context` でコンテキスト使用量を確認する

ここで、Claude Code に `/context` と入力してコンテキストの使用量を確認してみましょう。

```
> /context
```

<!-- TODO: 画像追加 - /context の出力画面 -->

Sub-agents がファイルを読んでくれたため、メインのコンテキストにはその分の消費が抑えられていることがわかります。もし Sub-agents を使わずに、Claude Code のメイン会話の中で全ファイルを読んでいたら、コンテキスト使用量はかなり大きくなっていたはずです。

> 💡 Sub-agents はメインのコンテキストとは独立したコンテキストウィンドウで動作するため、探索結果のサマリーだけがメインに返されます。これが「コードリーディングで Sub-agents を使う」ことの最大のメリットです。

---

## 🏃 実践 2: 構造を理解する

全体像を把握できたら、次は解像度を一段上げて、コードの構造を理解します。[3-2-1 コードリーディングの方法論](3-2-1_コードリーディングの方法論.md) の Step 2 で学んだ「モデル・リレーション」「認可の仕組み」「設計パターン」に注目します。

### Step 1: モデルのリレーションを深掘りする

実践 1 でモデルの一覧とリレーションの概要は把握できました。ここでは、CourseHub の中心的なデータ構造をもう少し具体的に理解します。

```
> Course モデルのリレーションを詳しく教えて。
> chapters, enrollments, tags それぞれの関係と、
> Course から Lesson にアクセスするにはどういう経路をたどるかを説明して
```

Claude は、`Course` → `Chapter`（`hasMany`）→ `Lesson`（`hasMany`）という階層構造と、`Course` から直接 `Lesson` にアクセスするメソッド（`getAllLessonIds()`）の存在を説明してくれます。

> 💡 モデルのリレーションを理解すると、「このデータを取得するにはどのモデルを経由すればいいか」がわかるようになります。これは以降の Chapter でバグ修正や機能開発を行うときの基礎知識になります。

### Step 2: MCP で DB 構造を確認する

コードから読み取ったモデルのリレーションが、実際のデータベースと一致しているかを確認します。[3-2-1 コードリーディングの方法論](3-2-1_コードリーディングの方法論.md) で学んだ「Claude の説明を検証する」の実践として、MCP でデータベースに直接アクセスします。

Part 2 では Playwright の MCP サーバーを追加してブラウザ操作を体験しました。同じ仕組みで、MySQL への接続もできます。以下のコマンドで MySQL 用の MCP サーバーを追加します。

```bash
claude mcp add mysql-coursehub \
  -e MYSQL_HOST=127.0.0.1 \
  -e MYSQL_PORT=3306 \
  -e MYSQL_USER=sail \
  -e MYSQL_PASSWORD=password \
  -- npx -y @benborla29/mcp-server-mysql
```

> 📝 `MYSQL_USER` と `MYSQL_PASSWORD` は CourseHub の `.env` ファイルの `DB_USERNAME` / `DB_PASSWORD` と同じ値です。`MYSQL_HOST` は `127.0.0.1` を指定します（MCP サーバーはホストマシン上で動作するため、Docker 内のサービス名 `mysql` ではなく、ポートフォワーディング経由の `127.0.0.1` を使います）。

> ⚠️ **よくあるエラー**: MCP サーバーの追加に失敗する場合
>
> ```
> Error: Could not connect to MySQL server
> ```
>
> **原因**: Sail のコンテナが起動していないか、ポート 3306 が他のプロセスに使われている
>
> **対処法**: `./vendor/bin/sail up -d` でコンテナを起動してください。ポート 3306 が競合している場合は、`.env` の `FORWARD_DB_PORT` を別の値（例: `33060`）に変更し、Sail を再起動した上で、MCP コマンドの `-e MYSQL_PORT=33060` も合わせて変更してください。

MCP サーバーが追加できたら、Claude Code からデータベースのテーブル一覧を確認します。

```
> データベースのテーブル一覧を見せて
```

Claude は MCP を使って `SHOW TABLES` を実行し、テーブル一覧を返してくれます。コードで確認したモデル（`Course`、`Chapter`、`Lesson` など）に対応するテーブル（`courses`、`chapters`、`lessons` など）が存在していることを確認してください。

次に、実際のデータを確認してみましょう。

```
> enrollments テーブルのカラム構成と、レコードがあれば数件見せて
```

Claude は `DESCRIBE enrollments` と `SELECT * FROM enrollments LIMIT 5` を実行し、テーブルの構造と実データを返してくれます。`EnrollmentService` のコードで見た `user_id`、`course_id`、`status`、`enrolled_at`、`completed_at` カラムが実際に存在することを、自分の目で確認できます。

> 💡 コードだけを読んでいると「このカラムは本当に存在するのか」「実際にどんなデータが入っているのか」がわかりません。MCP でデータベースに直接アクセスすることで、コードリーディングの理解を実データで裏付けることができます。これは「Claude の説明を自分で検証する」サイクルの一つです。

### Step 3: 認可の仕組みを確認する

CourseHub では3つのロール（admin / coach / student）が存在することがルーティングからわかりました。この認可がどう実装されているかを確認します。

```
> CourseHub の認可の仕組みを教えて。
> Middleware、Policy がそれぞれどう使われているか、
> 具体例を挙げて説明して
```

Claude は `RoleMiddleware` によるロールベースのアクセス制御と、`CoursePolicy` 等の Policy による操作単位の認可を説明してくれます。ルーティングの `middleware('role:coach')` が Middleware で、Controller 内の `$this->authorize('update', $course)` が Policy です。

### Step 4: 設計パターンを把握する

CourseHub で使われている設計パターンを確認します。

```
> CourseHub の app/ ディレクトリを見て、
> 標準的な Laravel の MVC 以外に使われている設計パターン
> （Service、Event/Listener、Form Request など）を教えて。
> それぞれどこで使われているかも具体的に
```

Claude は以下のパターンの存在を報告してくれるはずです。

- **Service クラス**: `app/Services/EnrollmentService.php`（受講登録のビジネスロジック）
- **Event/Listener**: `app/Events/CourseCompleted.php` + `app/Listeners/UpdateEnrollmentStatus.php`（コース完了時の処理）
- **Form Request**: `app/Http/Requests/StoreLessonRequest.php` 等（バリデーションの分離）
- **Policy**: `app/Policies/` 配下の6クラス（認可ロジックの分離）

ここで注目してほしいのは、**Service クラスと Event/Listener は COACHTECH の教材では直接は扱っていないパターン** だということです。これらは実践 4 で詳しく向き合います。今は「こういうパターンが使われている」という存在の把握で十分です。

> 📝 「全てのパターンを完璧に理解してから次に進む」必要はありません。構造の理解は、次のフロー追跡で「このコードがなぜここにあるか」を理解するための土台です。

---

## 🏃 実践 3: 業務フローを追跡する

構造を理解できたら、次は具体的な業務フローをコードで追跡します。CourseHub の中心的な業務フローである「受講フロー」を端から端まで追いかけます。

### 受講フローの全体像

CourseHub の受講フローは以下のステップで構成されています。

```
受講生の操作:

1. コース一覧を閲覧する        GET /courses
       ↓
2. コース詳細を確認する        GET /courses/{course}
       ↓
3. 受講登録する                POST /courses/{course}/enroll
       ↓
4. レッスンを学習する          GET /courses/{course}/lessons/{lesson}
       ↓
5. レッスンを完了する          POST /courses/{course}/lessons/{lesson}/complete
       ↓
6. 小テストを受験する          GET /courses/{course}/quizzes/{quiz}
       ↓
7. 小テストを送信する          POST /courses/{course}/quizzes/{quiz}/submit
       ↓
8. 結果を確認する              GET /courses/{course}/quizzes/{quiz}/result
```

このフローの中から、特に重要な「受講登録」と「レッスン完了」の処理を詳しく追跡します。

### Step 1: 受講登録のフローを Claude に質問する

以下のプロンプトで、受講登録の処理フローを Claude に質問します。

```
> 受講生がコースに受講登録する処理の流れを追いたい。
> routes/web.php のルーティングから、Controller、Service、Model の呼び出しまで、
> 処理の流れを順番にコードを引用しながら説明して
```

Claude はルーティング定義から `EnrollmentController@store` を見つけ、そこから `EnrollmentService@enroll` への呼び出し、そして `Enrollment` モデルと `LessonProgress` モデルの作成まで、処理の流れを説明してくれます。

### Step 2: Claude の説明を実コードで検証する

ここが重要です。Claude の説明を受け取ったら、**自分でコードを開いて確認します**。

まず、`EnrollmentController` のコードを確認します。

```php
// app/Http/Controllers/EnrollmentController.php

class EnrollmentController extends Controller
{
    public function __construct(
        private EnrollmentService $enrollmentService
    ) {}

    public function store(Course $course)
    {
        try {
            $this->enrollmentService->enroll(auth()->user(), $course);
        } catch (\Exception $e) {
            return redirect()->route('courses.show', $course)
                ->with('error', $e->getMessage());
        }

        return redirect()->route('courses.show', $course)
            ->with('success', 'コースに登録しました。');
    }
}
```

Controller 自体は非常にシンプルです。`EnrollmentService` に処理を委譲し、例外があればエラーメッセージをフラッシュ、成功すればコース詳細にリダイレクトしています。実際のビジネスロジックは `EnrollmentService` にあります。

次に、`EnrollmentService` を確認します。

```php
// app/Services/EnrollmentService.php

class EnrollmentService
{
    public function enroll(User $user, Course $course): Enrollment
    {
        // 受講済みチェック（重複登録防止）
        if ($user->enrollments()->where('course_id', $course->id)->exists()) {
            throw new \Exception('既に受講登録済みです');
        }

        // コース公開チェック
        if ($course->status !== 'published') {
            throw new \Exception('このコースは現在受講できません');
        }

        // Enrollment 作成
        $enrollment = Enrollment::create([
            'user_id' => $user->id,
            'course_id' => $course->id,
            'status' => 'active',
            'enrolled_at' => now(),
        ]);

        // 全公開レッスンの進捗レコードを一括作成
        $lessonIds = $course->chapters()
            ->with(['lessons' => fn($q) => $q->where('is_published', true)])
            ->get()
            ->flatMap->lessons
            ->pluck('id');

        foreach ($lessonIds as $lessonId) {
            LessonProgress::create([
                'user_id' => $user->id,
                'lesson_id' => $lessonId,
                'status' => 'not_started',
            ]);
        }

        return $enrollment;
    }
}
```

Claude の説明と実コードを照合します。以下のポイントを確認してください。

- **重複登録の防止**: `$user->enrollments()->where('course_id', $course->id)->exists()` で既に受講中でないかチェックしている。Claude はこの処理に触れていたか？
- **コース公開チェック**: `$course->status !== 'published'` で公開コースのみ受講可能にしている。Claude はこの条件を正確に説明していたか？
- **LessonProgress の一括作成**: 受講登録時に全公開レッスン分の `LessonProgress` レコードを `not_started` ステータスで作成している。Claude はこの処理まで説明していたか？

> 🔑 Claude の説明が「だいたい合っている」ことが多いですが、細かい条件（`is_published` のフィルタリングなど）を省略していることがあります。コードを自分で確認することで、こうした省略に気づけます。

### Step 3: レッスン完了のフローを追跡する

次に、レッスン完了時の処理を追跡します。ここでは「隠れた処理」の存在に注目してください。

```
> レッスン完了ボタンを押した後の処理を追いたい。
> LessonController の complete メソッドから、全ての処理（Event も含めて）を
> 順番に教えて
```

Claude は `LessonController@complete` の処理を説明してくれます。ここで、Claude の説明に `checkCourseCompletion()` メソッドと `CourseCompleted` Event が含まれているかを確認します。

実際のコードを確認しましょう。

```php
// app/Http/Controllers/LessonController.php

public function complete(Course $course, Lesson $lesson)
{
    LessonProgress::updateOrCreate(
        [
            'user_id' => auth()->id(),
            'lesson_id' => $lesson->id,
        ],
        [
            'status' => 'completed',
            'completed_at' => now(),
        ]
    );

    // 全公開レッスンが完了済みかチェックし、完了ならイベント発火
    $this->checkCourseCompletion($course);

    return redirect()->route('courses.lessons.show', [$course, $lesson])
        ->with('success', 'レッスンを完了しました。');
}
```

`complete` メソッドの中で `$this->checkCourseCompletion($course)` が呼ばれています。この private メソッドを見てみましょう。

```php
// app/Http/Controllers/LessonController.php（続き）

private function checkCourseCompletion(Course $course): void
{
    $user = auth()->user();

    $publishedLessonIds = $course->getAllLessonIds();

    if (empty($publishedLessonIds)) {
        return;
    }

    $completedCount = LessonProgress::where('user_id', $user->id)
        ->whereIn('lesson_id', $publishedLessonIds)
        ->where('status', 'completed')
        ->count();

    if ($completedCount >= count($publishedLessonIds)) {
        $enrollment = $user->enrollments()
            ->where('course_id', $course->id)
            ->where('status', 'active')
            ->first();

        if ($enrollment) {
            event(new CourseCompleted($enrollment, $user, $course));
        }
    }
}
```

全公開レッスンの完了数が総数以上になると、`CourseCompleted` Event が発火します。この Event を `UpdateEnrollmentStatus` Listener が受け取り、Enrollment のステータスを `completed` に更新します。

```
受講生が「完了」ボタンを押す
    ↓
LessonController@complete
    ↓
LessonProgress を completed に更新
    ↓
checkCourseCompletion() を呼び出し
    ↓
全公開レッスンが完了済みか？ ── No → 何もしない
    │
   Yes
    ↓
CourseCompleted Event を発火
    ↓
UpdateEnrollmentStatus Listener が処理
    ↓
Enrollment を completed に更新、completed_at を記録
```

[3-2-1 コードリーディングの方法論](3-2-1_コードリーディングの方法論.md) で説明した「Claude の説明を検証する: パターン 1 省略」を実践する場面です。Claude が `checkCourseCompletion()` の存在を省略していなかったか、Event の発火条件を正確に説明していたかを確認してください。

### Step 4: `/btw` で脱線質問する

フローを追跡している途中で、「`updateOrCreate` って `firstOrCreate` とどう違うの？」のような疑問が湧くかもしれません。こうした脱線質問は `/btw` で処理します。

```
> /btw updateOrCreate と firstOrCreate の違いを教えて。どういうときにどちらを使う？
```

`/btw` は現在の会話コンテキストに影響を与えずに回答を返してくれるので、フロー追跡の流れを中断せずに疑問を解消できます。

### Step 5: `/compact` でコンテキストを整理する

実践 3 の業務フロー追跡が終わったら、`/compact` でコンテキストを整理します。

```
> /compact
```

これまでの会話で読み込んだファイル内容や中間的なやり取りが圧縮され、次の実践に向けてコンテキストの余裕が確保されます。

> 💡 `/compact` は会話の内容を要約して圧縮することでコンテキストを節約します。コードパターン、ファイルの状態、重要な判断など、必要な情報は要約に含まれるため、それまでの作業文脈は失われません。長い探索の後は、こまめに `/compact` を実行する習慣をつけましょう。

---

## 🏃 実践 4: 知らない技術と向き合う

実践 2 と 3 を通じて、あなたは COACHTECH では学んでいない2つのパターンに遭遇しました。

1. **`EnrollmentService`**（Service クラス）: `app/Services/` ディレクトリにあり、`EnrollmentController` から呼び出されている
2. **`CourseCompleted` Event + `UpdateEnrollmentStatus` Listener**（Event/Listener パターン）: レッスン完了時にイベントが発火し、Listener がステータスを更新している

ここでは、[3-2-2 知らない技術への向き合い方](3-2-2_知らない技術への向き合い方.md) で学んだ「対処フロー（理解→評価→判断→説明できる）」を実践します。

### Service クラスに向き合う

#### 理解する: Claude に質問する

```
> app/Services/EnrollmentService.php を読んで。
> 1. このクラスは何をしているか
> 2. なぜ Controller に直接書かず、Service クラスに分離しているのか
> 3. Service クラスを使うメリットとデメリットは何か
```

Claude は、Service クラスがビジネスロジックを Controller から分離するためのパターンであること、テストのしやすさや再利用性のメリットがあること、過度な分離はかえって複雑になるデメリットがあることなどを説明してくれます。

#### 評価する: なぜここで使われているか考える

Claude の説明を踏まえて、CourseHub で `EnrollmentService` が使われている理由を考えます。

`EnrollmentService@enroll` には以下の処理が含まれています。

1. 重複登録チェック（`enrollments` テーブルへのクエリ）
2. コース公開状態チェック（`courses` テーブルの `status` カラム）
3. `Enrollment` レコードの作成
4. 全公開レッスンの取得（`chapters` → `lessons` を跨ぐクエリ）
5. `LessonProgress` レコードの一括作成

これら5つの処理は、複数のモデル（`Enrollment`、`Course`、`Chapter`、`Lesson`、`LessonProgress`）にまたがっています。CourseHub の README の設計方針にも「複数モデルにまたがる処理は Service クラスに集約する」と書かれていました（[3-1-3 プロジェクトの規約・設定を確認する](../chapter-01_実践の準備/3-1-3_プロジェクトの規約・設定を確認する.md) で確認済み）。

一方で、CourseHub の他の Controller を見ると、`CoachCourseController@store` は200行超のメソッドに全てのロジックが詰め込まれています（Fat Controller）。Service クラスへの分離はプロジェクト内でも一貫しておらず、`EnrollmentService` だけが切り出されている状態です。

> 📝 このように「規約や方針はあるが、一貫して適用されていない」状態は、実務のプロジェクトでは非常によくあります。前任チームの誰かが EnrollmentService を切り出し、他の Controller はそのまま残ったのでしょう。[3-1-3 プロジェクトの規約・設定を確認する](../chapter-01_実践の準備/3-1-3_プロジェクトの規約・設定を確認する.md) で確認した「規約と実コードの乖離」の具体例です。

#### 判断する: 今の自分にどの程度の理解が必要か

現段階（プロジェクト全体の理解フェーズ）では、以下のレベルで十分です。

- Service クラスは「複数モデルにまたがるビジネスロジックを Controller から分離するパターン」
- CourseHub では `EnrollmentService` のみ使われている
- Controller からコンストラクタインジェクションで受け取り、メソッドを呼び出す

Service クラスの設計原則（単一責任の原則、インターフェースの分離など）を今深掘りする必要はありません。Chapter 3-5（リファクタリング）で Fat Controller を改善するときに、必要に応じて深掘りします。

#### 説明できるか確認する

自分の言葉で説明してみましょう。

「`EnrollmentService` は受講登録のビジネスロジックを Controller から分離した Service クラス。受講済みチェック、コース公開確認、Enrollment 作成、全レッスンの LessonProgress 一括作成の4つの処理をまとめている。README の設計方針に沿ったパターンだが、CourseHub 全体では一貫して適用されておらず、この Service だけが切り出されている状態。」

ここまで言えれば、Service クラスについての理解は十分です。

### Event/Listener パターンに向き合う

#### 理解する: Claude に質問する

```
> app/Events/CourseCompleted.php と app/Listeners/UpdateEnrollmentStatus.php を読んで。
> 1. Event/Listener パターンとは何か
> 2. この CourseCompleted Event はどこから発火されるか
> 3. なぜ LessonController の中で直接 Enrollment を更新せず、Event/Listener を使っているのか
```

Claude は Event/Listener パターンの概要と、Observer パターンとの類似性、発火元の `LessonController@checkCourseCompletion` メソッドの説明、そして直接更新ではなく Event を使う理由（将来の拡張性）を説明してくれます。

#### 評価する: なぜここで使われているか考える

`CourseCompleted` Event のコードを見ると、コメントに意図が書かれています。

```php
// app/Events/CourseCompleted.php

/**
 * コースの全レッスン完了時に発火するイベント
 *
 * 将来的に完了証明書の発行やコーチへの通知等を追加しやすくするため、
 * Event/Listener パターンで実装。
 */
```

現時点では `UpdateEnrollmentStatus` という Listener が1つだけ登録されています。

```php
// app/Providers/EventServiceProvider.php

protected $listen = [
    CourseCompleted::class => [
        UpdateEnrollmentStatus::class,
    ],
];
```

つまり、**今は1つの Listener しかないが、将来の拡張を見越して Event/Listener パターンを採用している** ということです。たとえば将来「コース完了時にコーチにメール通知を送る」「完了証明書の PDF を生成する」といった処理を追加するとき、新しい Listener を追加するだけで済みます。`LessonController` を修正する必要はありません。

#### 判断する: 今の自分にどの程度の理解が必要か

現段階では以下のレベルで十分です。

- Event/Listener は「あるイベントが起きたときに、それに反応する処理を疎結合に登録するパターン」
- `CourseCompleted` は全レッスン完了時に発火し、`UpdateEnrollmentStatus` が Enrollment のステータスを `completed` に更新する
- Event の登録は `EventServiceProvider` の `$listen` 配列で管理される

Event のキューイング（非同期実行）、ブロードキャスト、Job との違いなどは今は理解不要です。

#### 説明できるか確認する

「`CourseCompleted` Event は、受講生が全公開レッスンを完了したときに `LessonController` から発火される。`UpdateEnrollmentStatus` Listener がこの Event を受け取り、Enrollment のステータスを `completed` に更新する。将来的にコーチへの通知や完了証明書の発行を追加しやすくするために、直接更新ではなく Event/Listener パターンが採用されている。」

### 🧠 先輩エンジニアはこう考える

> 初めて Event/Listener を見たとき、「なんでこんな回りくどいことをするんだろう」と思った。Enrollment のステータス更新なんて、`LessonController` の中で直接 `$enrollment->update(...)` って書けば1行で済むのに。
>
> でも、実際にプロジェクトが成長してくると、「コース完了時にやること」がどんどん増えていく。メール送信、ログ記録、ダッシュボードの統計更新、ポイント付与。全部 Controller に書いたらどうなるか。そう、200行超の Fat Controller のもう一つのバージョンが生まれる。
>
> Event/Listener は「今は必要以上に見える設計が、後で救いになる」パターンの典型。ただし、何でも Event にすればいいわけではない。1つしか Listener がないなら直接呼び出しでも十分な場合もある。CourseHub の場合は、コメントに「将来の拡張のため」と明記されているので、意図的な設計判断だとわかる。こういうコメントがあるのは良いプロジェクトの証拠だと思う。

### ✅ 完成チェックリスト

- [ ] Sub-agents を使って CourseHub のディレクトリ構成・モデル・ルーティングを探索し、全体像を把握した
- [ ] `/context` でコンテキスト使用量を確認した
- [ ] MCP で MySQL に接続し、テーブル一覧やカラム構成を確認してコードの理解を裏付けた
- [ ] モデルのリレーション、認可の仕組み（Middleware + Policy）、設計パターン（Service、Event/Listener）を把握した
- [ ] 受講登録フロー（`EnrollmentController` → `EnrollmentService`）をコードで追跡し、Claude の説明と実コードを照合した
- [ ] レッスン完了フロー（`LessonController@complete` → `checkCourseCompletion` → `CourseCompleted` Event）をコードで追跡した
- [ ] `/compact` でコンテキストを整理した
- [ ] `EnrollmentService`（Service クラス）が何をしているか、なぜ使われているかを自分の言葉で説明できる
- [ ] `CourseCompleted` Event と `UpdateEnrollmentStatus` Listener の関係を自分の言葉で説明できる

> 📝 このセクションの実践はコードリーディングが目的であり、コード生成を伴わないため、🔍 見極めチェックは省略します。

---

## ✨ まとめ

- Sub-agents を使えば、メインのコンテキストを消費せずにプロジェクト全体を一気に探索できる。コードリーディングでは特に有効
- MCP でデータベースに直接アクセスすることで、コードから読み取った構造を実データで裏付けられる。「コードの理解を検証する」手段の一つ
- 業務フローの追跡では、Claude の説明を受け取った後に必ず自分でコードを読んで検証する。省略されている処理（`checkCourseCompletion` のような private メソッド）がないか確認する
- 知らない技術に出会ったら、「理解→評価→判断→説明できる」の対処フローで段階的に理解を深める。全てを今すぐ完璧に理解する必要はない
- `/btw` で脱線質問をし、`/compact` でコンテキストを定期的に整理することで、長いコードリーディングセッションでも Claude Code を効率的に使い続けられる
- コードリーディングで得た理解（モデル構造、設計パターン、規約と実態のズレ）は、以降の Chapter で実際のタスクに取り組む際の基盤になる

---

次の Chapter では、CourseHub のバグを修正します。ここで把握した全体像と業務フローの理解を活かし、バグ報告から原因特定、修正、テスト検証までを Claude Code と協働して遂行します。
