# CourseHub 仕様書

Part 3 提供プロジェクトの設計仕様。この仕様書を元に別セッション・別ディレクトリでプロジェクトを構築する。

## リポジトリ・ローカルパス

- **GitHub**: https://github.com/coachtech-material/pro-cc-coursehub
- **ローカル**: `/Users/yotaro/pro-cc-coursehub`

## プロジェクト概要

**CourseHub**（コースハブ）— オンライン学習プラットフォーム。コーチがコースを作成し、受講生が受講・進捗管理する構成。

### 技術スタック

- Laravel 10（`composer create-project laravel/laravel:^10`）
- Laravel Sail（Docker ベース開発環境）
- Blade + Tailwind CSS（Vite）
- MySQL 8.0
- phpMyAdmin（compose.yaml に追加）
- PHPUnit
- Laravel Fortify（認証）
- 一部 API エンドポイントあり

### 想定シナリオ

初期開発チーム（2〜3名）が退職し、あなたがジュニアエンジニアとして加わる。1年ほど運用されたプロジェクトで、コードスタイルのバラつきやテストカバレッジのムラがある。

### 環境構築手順

COACHTECH 受講中教材の環境構築手順に準拠する。

```bash
# 1. Laravel プロジェクト作成（Laravel 10）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 pro-cc-coursehub

cd pro-cc-coursehub

# 2. Laravel Sail インストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql

# 3. phpMyAdmin を compose.yaml に追加（mysql サービスの後に追記）
# 4. Sail 起動
./vendor/bin/sail up -d

# 5. Tailwind CSS 導入
sail npm install
sail npm install -D tailwindcss@^3.4.0 postcss autoprefixer
sail npx tailwindcss init -p
# tailwind.config.js の content 設定、resources/css/app.css の Tailwind ディレクティブ追加

# 6. Fortify インストール
sail composer require laravel/fortify
sail artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"

# 7. マイグレーション・シーディング
sail artisan migrate --seed

# 8. 動作確認
# http://localhost（Laravel）、http://localhost:8080（phpMyAdmin）
```

phpMyAdmin の compose.yaml 追加内容:
```yaml
    phpmyadmin:
        image: 'phpmyadmin:latest'
        ports:
            - '${FORWARD_PHPMYADMIN_PORT:-8080}:80'
        environment:
            PMA_HOST: mysql
            PMA_USER: '${DB_USERNAME}'
            PMA_PASSWORD: '${DB_PASSWORD}'
        networks:
            - sail
        depends_on:
            - mysql
```

---

## ロール・権限

### ロール

| ロール | 説明 |
|---|---|
| **admin** | プラットフォーム管理者。全リソースの管理権限 |
| **coach** | コーチ。自分のコース・レッスン・小テストを管理 |
| **student** | 受講生。コースの閲覧・受講・小テスト受験 |

単一の User モデルに `role` カラムで管理。ミドルウェアでルートレベルのアクセス制御、Policy で操作レベルの認可。

### 画面構成

#### 共通（全ロール）

| 画面 | パス | 内容 |
|---|---|---|
| ログイン | `/login` | Fortify 認証 |
| 会員登録 | `/register` | ロール選択（coach or student） |
| プロフィール | `/profile` | 自分の情報編集 |

#### 受講生（student）

| 画面 | パス | 内容 |
|---|---|---|
| コース一覧 | `/courses` | 公開コースの検索・フィルタ |
| コース詳細 | `/courses/{course}` | コース情報、Chapter/Lesson 一覧 |
| レッスン閲覧 | `/courses/{course}/lessons/{lesson}` | レッスン内容、完了マーク |
| 小テスト受験 | `/courses/{course}/quizzes/{quiz}` | 問題表示、回答送信 |
| 小テスト結果 | `/courses/{course}/quizzes/{quiz}/result` | スコア・正誤 |
| マイコース | `/my-courses` | 受講中コース、進捗率 |

#### コーチ（coach）

| 画面 | パス | 内容 |
|---|---|---|
| ダッシュボード | `/coach` | 自分のコース統計 |
| コース管理 | `/coach/courses` | 自分のコース CRUD |
| Chapter 管理 | `/coach/courses/{course}/chapters` | Chapter CRUD、並び順 |
| レッスン管理 | `/coach/courses/{course}/chapters/{chapter}/lessons` | Lesson CRUD、並び順 |
| 小テスト管理 | `/coach/courses/{course}/lessons/{lesson}/quizzes` | Quiz + Question + Option の管理 |
| 受講者一覧 | `/coach/courses/{course}/students` | 受講者の進捗確認 |

#### 管理者（admin）

| 画面 | パス | 内容 |
|---|---|---|
| ダッシュボード | `/admin` | プラットフォーム統計 |
| ユーザー管理 | `/admin/users` | ユーザー一覧、ロール変更 |
| 生徒一覧 | `/admin/students` | 全受講生の一覧（受講コース数、進捗率等） |
| コース管理 | `/admin/courses` | 全コースの管理 |
| カテゴリ管理 | `/admin/categories` | カテゴリ CRUD |

---

## モデル定義

### コース構造

```
Course（コース）
├── Chapter（チャプター）
│   └── Lesson（レッスン）
│       └── Quiz（小テスト）
│           ├── Question（問題）
│           └── Option（選択肢）
```

### 全モデル一覧（13モデル）

※ Review は教材タスク（3-4-2）で新規作成するモデルのため、初期状態には含めない。

#### 1. User

| カラム | 型 | 説明 |
|---|---|---|
| id | bigint PK | |
| name | string | 表示名 |
| email | string unique | |
| password | string | |
| role | enum: admin/coach/student | |
| bio | text nullable | 自己紹介 |
| avatar_url | string nullable | プロフィール画像 URL |
| timestamps | | |

リレーション:
- hasMany: courses（coach として）, enrollments, lessonProgress, submissions

#### 2. Course

| カラム | 型 | 説明 |
|---|---|---|
| id | bigint PK | |
| user_id | FK → users | コーチ |
| category_id | FK → categories | |
| title | string | |
| slug | string unique | URL 用 |
| description | text | コース概要 |
| difficulty | enum: beginner/intermediate/advanced | 難易度 |
| image_path | string nullable | カバー画像 |
| status | enum: draft/published/archived | |
| published_at | timestamp nullable | 公開日時 |
| timestamps | | |

リレーション:
- belongsTo: user（coach）, category
- hasMany: chapters, enrollments
- belongsToMany: tags（pivot: course_tag）

#### 3. Chapter

| カラム | 型 | 説明 |
|---|---|---|
| id | bigint PK | |
| course_id | FK → courses | |
| title | string | |
| order | integer | 並び順 |
| timestamps | | |

リレーション:
- belongsTo: course
- hasMany: lessons

#### 4. Lesson

| カラム | 型 | 説明 |
|---|---|---|
| id | bigint PK | |
| chapter_id | FK → chapters | |
| title | string | |
| body | text | Markdown コンテンツ |
| order | integer | 並び順 |
| is_published | boolean default true | 公開フラグ |
| timestamps | | |

リレーション:
- belongsTo: chapter
- hasOne: quiz
- hasMany: lessonProgress

#### 5. Quiz

| カラム | 型 | 説明 |
|---|---|---|
| id | bigint PK | |
| lesson_id | FK → lessons | |
| title | string | |
| passing_score | integer | 合格点（%） |
| timestamps | | |

リレーション:
- belongsTo: lesson
- hasMany: questions, submissions

#### 6. Question

| カラム | 型 | 説明 |
|---|---|---|
| id | bigint PK | |
| quiz_id | FK → quizzes | |
| body | text | 問題文 |
| order | integer | 並び順 |
| timestamps | | |

リレーション:
- belongsTo: quiz
- hasMany: options

#### 7. Option

| カラム | 型 | 説明 |
|---|---|---|
| id | bigint PK | |
| question_id | FK → questions | |
| body | string | 選択肢の文面 |
| is_correct | boolean | 正解フラグ |
| timestamps | | |

リレーション:
- belongsTo: question

#### 8. Enrollment

| カラム | 型 | 説明 |
|---|---|---|
| id | bigint PK | |
| user_id | FK → users | 受講生 |
| course_id | FK → courses | |
| status | enum: active/completed/cancelled | |
| enrolled_at | timestamp | 受講開始日 |
| completed_at | timestamp nullable | 完了日 |
| timestamps | | |

リレーション:
- belongsTo: user, course
- unique制約: [user_id, course_id]

#### 9. LessonProgress

| カラム | 型 | 説明 |
|---|---|---|
| id | bigint PK | |
| user_id | FK → users | |
| lesson_id | FK → lessons | |
| status | enum: not_started/in_progress/completed | |
| completed_at | timestamp nullable | |
| timestamps | | |

リレーション:
- belongsTo: user, lesson
- unique制約: [user_id, lesson_id]

#### 10. Submission

| カラム | 型 | 説明 |
|---|---|---|
| id | bigint PK | |
| user_id | FK → users | |
| quiz_id | FK → quizzes | |
| score | integer | 得点（%） |
| answers | json | [{question_id, option_id}] |
| submitted_at | timestamp | |
| timestamps | | |

リレーション:
- belongsTo: user, quiz

#### 11. Category

| カラム | 型 | 説明 |
|---|---|---|
| id | bigint PK | |
| name | string | |
| slug | string unique | |
| timestamps | | |

リレーション:
- hasMany: courses

#### 12. Tag

| カラム | 型 | 説明 |
|---|---|---|
| id | bigint PK | |
| name | string | |
| slug | string unique | |
| timestamps | | |

リレーション:
- belongsToMany: courses（pivot: course_tag）

#### 13. CourseTag（pivot）

| カラム | 型 |
|---|---|
| course_id | FK → courses |
| tag_id | FK → tags |

---

## タスク対応表

### MECE 整合性

※ 番号は part-03.md の Section 番号ではなく、各 Section 内のタスク番号。

| Chapter | MECE 軸 | タスク | カテゴリ | 内容 | 整合性 |
|---|---|---|---|---|---|
| 3-3 バグ修正 | 影響領域 | ① | データの正しさ | 進捗率の計算バグ | ✅ クエリ不備による出力データの誤り |
| | | ② | アクセス制御 | 非公開コースの認可漏れ | ✅ Policy 不備による不正アクセス |
| | | ③ | 機能不全 | 小テスト送信の500エラー | ✅ 例外未ハンドルによる機能停止 |
| 3-4 機能開発 | 変更スコープ | ① | 既存機能の拡張 | 小テスト再受験機能 | ✅ 既存モデル・コントローラの修正のみ |
| | | ② | 新規機能の構築 | コースレビュー機能 | ✅ Review モデル・コントローラを新規作成 |
| 3-5 改善 | 改善対象 | ① | コード構造 | Fat Controller の責務分離 | ✅ 可読性・保守性の改善 |
| | | ② | パフォーマンス | N+1 解消 | ✅ クエリ効率の改善 |

### 全タスク対応表

※ Section 番号は part-03.md に準拠。1つの Section 内に複数タスクがある場合はまとめて記載。

| Section | タスク | 関連モデル | 関連画面 | ロール | 仕込む問題 |
|---|---|---|---|---|---|
| 3-1-2 セットアップと動作確認 | セットアップ | — | — | — | README のズレ |
| 3-1-3 規約・設定の確認 | CLAUDE.md・rules 更新 | — | — | — | 不完全な既存 CLAUDE.md |
| 3-2-2 CourseHub のコードを読む | 全体像把握 + 業務フロー追跡 | 全モデル / Course, Chapter, Lesson, Quiz, Enrollment, LessonProgress, Submission | 全画面 / コース詳細〜小テスト結果、マイコース | 全ロール / student, coach | なし（複雑さ自体が題材、Claude の説明を検証） |
| 3-3-2 CourseHub のバグを修正する | 進捗率バグ | LessonProgress, Lesson, Chapter, Course | マイコース | student | 非公開レッスンが総数に含まれる |
| | 認可バグ | Course（Policy, Scope） | コース詳細、コース一覧 | student | Policy の status チェック漏れ |
| | 小テスト500エラー | Submission, Quiz, Question, Option | 小テスト受験 | student | スコア計算の例外未ハンドル |
| 3-4-2 CourseHub に機能を追加する | 小テスト再受験 | Submission, Quiz, Question, Option（全て既存） | 小テスト受験、小テスト結果 | student | なし（新規実装） |
| | コースレビュー | Review（新規）, Course, Enrollment, User | コース詳細 | student | なし（新規実装） |
| 3-5-2 CourseHub のコードを改善する | Fat Controller | Course, Chapter, Tag, CourseTag | コース作成・編集 | coach | CourseController@store が200行超 |
| | N+1 解消 | Course, User, Chapter, Lesson, Enrollment, LessonProgress | コース一覧 + 生徒一覧 | student + admin | eager loading 漏れ |
| 3-6-2 CourseHub の変更をチームに共有する | PR 作成 + チーム環境整備 | — | — | — | なし（3-3〜3-5 の成果物を PR にする、GitHub Actions・設定・CLAUDE.md 運用） |

---

## 仕込む問題の具体仕様

### タスク対応の問題

**3-3-1 進捗率の計算バグ**

```php
// マイコース画面での進捗率計算（バグあり）
public function getProgressRate($userId)
{
    $totalLessons = $this->chapters()->withCount('lessons')->get()
        ->sum('lessons_count');
    // ↑ バグ: is_published = false のレッスンも総数に含めている

    $completedLessons = LessonProgress::where('user_id', $userId)
        ->whereIn('lesson_id', $this->getAllLessonIds())
        ->where('status', 'completed')
        ->count();

    return $totalLessons > 0 ? round($completedLessons / $totalLessons * 100) : 0;
}
```

- 原因: 非公開レッスン（`is_published = false`）が総数に含まれるが、受講生は公開レッスンしか完了できないため 100% に到達しない
- 修正: `lessons()->where('is_published', true)` でフィルタ
- 再現条件: コースに非公開レッスンが1つ以上ある場合

**3-3-2 非公開コースの認可バグ**

```php
// CoursePolicy.php（バグあり）
public function view(User $user, Course $course)
{
    if ($user->role === 'admin' || $course->user_id === $user->id) {
        return true;
    }

    return true;
    // ↑ バグ: student の場合も無条件に true
    // 本来: return $course->status === 'published';
}
```

- 原因: Policy の student 向けチェックで `status === 'published'` の条件が漏れている
- 修正: student の場合は `$course->status === 'published'` を返す
- 再現手順: 下書きコースの URL `/courses/{id}` を直接アクセス
- 補足: コース一覧は `where('status', 'published')` で正しくフィルタ済み。ただし `scopePublished()` が定義されているのに使われていない。品質の見極めとして Scope 活用を検討させる

**3-3-3 小テスト送信の500エラー**

```php
// QuizController@submit（バグあり）
public function submit(Request $request, Course $course, Quiz $quiz)
{
    $answers = $request->input('answers'); // [{question_id, option_id}, ...]

    $correctCount = 0;
    foreach ($quiz->questions as $question) {
        $userAnswer = collect($answers)->firstWhere('question_id', $question->id);
        $selectedOption = Option::find($userAnswer['option_id']);
        // ↑ バグ: 未回答の問題がある場合 $userAnswer が null → null['option_id'] でエラー
        if ($selectedOption && $selectedOption->is_correct) {
            $correctCount++;
        }
    }

    $score = round($correctCount / $quiz->questions->count() * 100);
    // ↑ バグ: questions が0件の場合に0除算

    Submission::create([...]);
}
```

- 原因1: 未回答の問題がある場合に null アクセスで500エラー
- 原因2: 問題が0件の Quiz でスコア計算時に0除算
- 修正: null チェックの追加、0件ガードの追加
- 再現手順: 小テストで一部の問題を未回答のまま送信する

**3-5-1 Fat Controller（CourseController@store）**

200行超のメソッド。以下を全て1メソッドに詰め込む:

```
1. バリデーション（inline、Form Request 未使用）   ~30行
2. スラッグ生成（重複チェック付きループ）           ~15行
3. 画像アップロード処理                              ~20行
4. Course レコード作成                                ~15行
5. タグの同期（新規タグ作成 + pivot 更新）           ~25行
6. 初期 Chapter の自動作成                           ~10行
7. ステータスに応じた published_at の設定            ~10行
8. 成功/失敗のリダイレクト処理                       ~10行
9. try-catch で全体を囲む（エラーハンドリング）      ~10行
10. コメント・空行                                    ~55行
```

**3-5-2 N+1 問題**

コース一覧（student 側）:
```php
// CourseController@index（バグあり）
$courses = Course::where('status', 'published')->paginate(12);

// Blade 内で:
$course->user->name                                    // N+1: coach 名
$course->chapters->count()                             // N+1: Chapter 数
$course->chapters->flatMap->lessons->count()           // N+1: Lesson 数
$course->enrollments->count()                          // N+1: 受講者数
```

生徒一覧（admin 側）:
```php
// AdminController@students（バグあり）
$students = User::where('role', 'student')->paginate(20);

// Blade 内で:
$student->enrollments->count()                         // N+1: 受講コース数
$student->enrollments->where('status', 'active')       // N+1: filter
// 進捗率の計算でさらにネスト
```

### タスクに直接関係しない問題（リアルさの演出）

| 問題 | 具体的な配置 |
|---|---|
| コードスタイルのバラつき | CourseController は inline バリデーション、LessonController は Form Request を使用。ChapterController は途中まで Form Request だがコメントアウトされて inline に戻っている |
| テストカバレッジのムラ | `tests/Feature/CourseTest.php` は CRUD テストあり。Enrollment, LessonProgress, Quiz, Submission はテストなし |
| 残留物 | `OldSearchController.php`（未使用）、`CourseController` 内に `// TODO: バリデーション追加` コメント、`ChapterController` にコメントアウトされた旧ソート処理 |
| README のズレ | `.env.example` に `DB_HOST=mysql` だが README には `DB_HOST=127.0.0.1` と記載。`QUEUE_CONNECTION` の記載が古い。コーディング規約セクションの内容が実際のコードと乖離（後述） |
| 日本語・英語混在コメント | 初期開発者の日本語コメントと途中参加メンバーの英語コメントが混在 |
| 設計の不統一 | CourseController は Eloquent 直接、一部の検索処理だけ Scope を使用。統一されていない |
| 応用的なパターンの使用 | 学習者の前提知識外だが実務では一般的なパターンを2箇所で使用。3-2「既存コードを理解する」の実践題材。詳細は後述 |

### 応用的なパターンの詳細

3-2-1「知らない技術への向き合い方」（方法論）と 3-2-2（実践）の題材として、学習者が COACHTECH で習っていない2つのパターンを使用する。

**1. EnrollmentService（Service クラス）**

場所: `app/Services/EnrollmentService.php`
使用箇所: `EnrollmentController@store` から呼び出し

```php
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

ストーリー: 当初 EnrollmentController@store に全処理が書かれていたが、受講登録ロジックが複雑になり前任チームの1人が Service クラスに切り出した。

**2. CourseCompleted Event + UpdateEnrollmentStatus Listener**

場所:
- `app/Events/CourseCompleted.php`
- `app/Listeners/UpdateEnrollmentStatus.php`
- `app/Providers/EventServiceProvider.php` に登録

```php
// app/Events/CourseCompleted.php
class CourseCompleted
{
    public function __construct(
        public Enrollment $enrollment,
        public User $user,
        public Course $course,
    ) {}
}

// app/Listeners/UpdateEnrollmentStatus.php
class UpdateEnrollmentStatus
{
    public function handle(CourseCompleted $event): void
    {
        $event->enrollment->update([
            'status' => 'completed',
            'completed_at' => now(),
        ]);
    }
}
```

発火条件: レッスン完了時に全公開レッスンが完了済みかを判定し、全完了なら発火。

ストーリー: コース完了時の処理を将来的に追加しやすくするため（完了証明書の発行、コーチへの通知等）、前任チームが Event/Listener パターンで実装した。現時点では Listener は1つだけ。

## Seeder データ設計

### タスクごとのデータ要件

| タスク | 必要なデータ条件 |
|---|---|
| 3-3-1 進捗率バグ | 非公開レッスンを含むコースに受講生が受講中 |
| 3-3-2 認可バグ | status=draft のコースが存在する |
| 3-3-3 500エラー | 問題数0件の Quiz、または未回答を許す Quiz が存在する |
| 3-4-1 小テスト再受験 | 不合格の Submission が存在する |
| 3-4-2 コースレビュー | 受講完了した Enrollment が存在する |
| 3-5-1 Fat Controller | コースが作成できる状態（Category, Tag が存在） |
| 3-5-2 N+1 | コース・受講者が一覧で十分なデータ量 |

### データ量

| モデル | 件数 | 備考 |
|---|---|---|
| User | 55件 | admin 1, coach 3, student 51 |
| Category | 5件 | Web開発, モバイル, データベース, インフラ, AI/ML |
| Tag | 15件 | PHP, Laravel, JavaScript, React, Docker, Git 等 |
| Course | 10件 | coach 3名が各2〜4件。うち1件は draft、1件は archived |
| Chapter | 30件 | 1コースあたり2〜4 Chapter |
| Lesson | 80件 | 1 Chapter あたり2〜4 Lesson。一部 is_published=false を含む |
| Quiz | 15件 | 一部のレッスンにのみ紐づく。1件は問題0件の空 Quiz |
| Question | 60件 | 1 Quiz あたり3〜5問 |
| Option | 240件 | 1 Question あたり4選択肢 |
| Enrollment | 100件 | 各 student が1〜3コースを受講。active/completed/cancelled 混在 |
| LessonProgress | 500件 | 受講中コースのレッスンに対する進捗。完了/未完了混在 |
| Submission | 50件 | 小テスト受験結果。不合格（passing_score 未達）を含む |

### 特記事項

- N+1 の体感に十分なデータ量（student 51名、コース10件 × 各種リレーション）
- 進捗率バグの再現: 少なくとも1コースに `is_published=false` のレッスンがあり、そのコースに受講中の student がいる
- 500エラーの再現: 問題0件の Quiz がある、または全問未回答で送信できる状態
- 不合格 Submission: passing_score 未達の Submission が存在し、再受験機能の開発タスクで使える
- Factory を使用し、データの自然さを確保する

## 既存 README

前任チームが書いた README。環境構築手順に加えて、コーディング規約と設計方針が記載されている。ただし実際のコードとの乖離がある。

README に含めるセクション:
1. プロジェクト概要
2. 環境構築手順（一部古い: DB_HOST の値、QUEUE_CONNECTION の記載）
3. コーディング規約
4. 設計方針

### README のコーディング規約セクション

```markdown
## コーディング規約

### バリデーション
- Controller ではバリデーションに Form Request を使用する
- Form Request は `app/Http/Requests/` に配置する

### 命名規則
- 変数名・メソッド名は camelCase
- テーブル名・カラム名は snake_case
- Controller 名は単数形 + Controller（例: CourseController）

### エラーハンドリング
- Blade 画面はリダイレクトでエラーを返す
- フラッシュメッセージで結果を通知する

### テスト
- 新機能には Feature テストを書く
- テストメソッド名は `test_` プレフィックス
```

意図的な乖離:
- 「Form Request を使用する」→ CourseController は inline バリデーション
- 「新機能には Feature テストを書く」→ Enrollment, Quiz 等はテストなし

### README の設計方針セクション

```markdown
## 設計方針

### Controller
- Controller は薄く保つ。ビジネスロジックが複雑な場合は Service クラスに切り出す

### Service クラス
- 複数モデルにまたがる処理は Service クラスに集約する（例: EnrollmentService）
- `app/Services/` に配置する

### Policy
- リソースのアクセス制御は Policy で実装する
- Controller で `$this->authorize()` を使用する

### イベント
- 重要なドメインイベントは Event/Listener パターンで実装する
```

意図的な乖離:
- 「Controller は薄く保つ」→ CourseController@store が200行超
- 「Service クラスに切り出す」→ EnrollmentService のみ。他は直接 Eloquent
- 「Event/Listener パターン」→ CourseCompleted のみ

### .claude/rules/ との関係

`.claude/rules/coding.md` は README のコーディング規約のサブセット（Claude Code が参照する簡潔版）。README に「詳細な背景」、rules に「簡潔なルール」という役割分担。

---

## 既存 Claude Code 設定ファイル

前任チームが残した不完全な状態。学習者が 3-1-3 で不足に気づき更新する。

### 既存 CLAUDE.md

意図的な問題: Sail の記載なし、技術スタックが曖昧、コース構造の説明なし、モデル関連なし、コーディング規約なし、API 記載なし、テスト情報が薄い

```markdown
# CourseHub

オンライン学習プラットフォーム。

## 技術スタック

- Laravel 10
- MySQL
- Blade + Tailwind CSS

## 開発環境

Docker Compose で起動:

｀｀｀bash
docker compose up -d
｀｀｀

マイグレーション:

｀｀｀bash
php artisan migrate
｀｀｀

シーディング:

｀｀｀bash
php artisan db:seed
｀｀｀

## ユーザーロール

- admin: 管理者
- coach: コーチ（コース作成）
- student: 受講生

## テスト

｀｀｀bash
php artisan test
｀｀｀
```

※ 上記の｀は仕様書内のネスト回避のための全角表記。実際は半角バッククォート。

### 既存 .claude/settings.json

```json
{
  "permissions": {
    "allow": [
      "Bash(php artisan *)",
      "Bash(composer *)",
      "Bash(npm *)"
    ]
  }
}
```

問題点: `php artisan` ではなく `./vendor/bin/sail artisan` を使うべき、`sail` コマンドの allow がない、`git` コマンドの allow がない、deny ルールがない

### 既存 .claude/rules/

```markdown
# .claude/rules/coding.md
---
description: コーディング規約
globs: "app/**/*.php"
---

- Controller ではバリデーションに Form Request を使用する
- モデルのリレーションは明示的に定義する
- 変数名・メソッド名は camelCase、テーブル名・カラム名は snake_case
```

```markdown
# .claude/rules/git.md
---
description: Git 運用ルール
---

- コミットメッセージは英語で記述する
- ブランチ名は feature/xxx, fix/xxx, refactor/xxx の形式
```

問題点:
- coding.md に「Form Request を使用する」と書いてあるが、実際のコードは一部しか従っていない（CourseController は inline バリデーション）
- git.md に「コミットメッセージは英語」と書いてあるが、実際のコミットは日本語混在
- rules の内容が薄く、設計方針（Service クラスの使い方等）に触れていない

### 既存 .claude/skills/

```markdown
# .claude/skills/test/SKILL.md
---
name: test
description: テストを実行する
---

テストを実行してください。

｀｀｀bash
php artisan test
｀｀｀
```

```markdown
# .claude/skills/lint/SKILL.md
---
name: lint
description: コードの静的解析を実行する
---

PHP CS Fixer でコードをチェックしてください。

｀｀｀bash
./vendor/bin/php-cs-fixer fix --dry-run --diff
｀｀｀
```

※ 上記の｀は仕様書内のネスト回避のための全角表記。実際は半角バッククォート。

問題点:
- test Skill は `php artisan test` と書いてあるが Sail 環境では `sail artisan test` が正しい
- lint Skill は php-cs-fixer がインストールされていないため動作しない（前任チームが途中で導入を断念した残骸）。Laravel 10 にはプリインストールの Pint（`./vendor/bin/pint`）があるため、Pint に切り替えるのが正しい修正
- どちらもシンプルすぎて Skill としての価値が薄い

### 3-1-3 で発見・更新すべき内容

- CLAUDE.md: Sail コマンドへの修正、PHP・MySQL バージョン追記、コース構造追記、コーディング規約の方針追記
- settings.json: Sail・git コマンドの allow 追加
- rules/coding.md: 実際のコードとの乖離を認識し、方針を明確化
- rules/git.md: 実態に合わせて更新
- skills/test: Sail コマンドに修正
- skills/lint: php-cs-fixer が動作しないことを確認 → Laravel Pint（プリインストール済み）に切り替え

## Git タグ戦略

### 方針

- 構築時は `initial` タグのみ作成（プロジェクト初期状態）
- `git checkout initial` でいつでも初期状態に戻れる
- タスク単位のタグ（`after-bugfix`, `after-feature`, `after-refactor`）は執筆時に模範解答が固まった段階で追加を検討する
