# CoaKoza 仕様書

Part 3 提供プロジェクトの設計仕様。この仕様書を元に別セッション・別ディレクトリでプロジェクトを構築する。

## リポジトリ・ローカルパス

- **GitHub**: https://github.com/coachtech-material/pro-cc-coakoza
- **ローカル**: `/Users/yotaro/pro-cc-coakoza`

## プロジェクト概要

**CoaKoza**（コアコザ）— オンライン学習プラットフォーム。コーチがコースを作成し、受講生が受講・進捗管理する構成。

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

初期開発チーム（2〜3名）が退職し、Pro生が途中参加のエンジニアとして加わる。1年ほど運用されたプロジェクトで、コードスタイルのバラつきやテストカバレッジのムラがある。

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
    composer create-project laravel/laravel:^10.0 pro-cc-coakoza

cd pro-cc-coakoza

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

| Chapter | MECE 軸 | Section | カテゴリ | タスク | 整合性 |
|---|---|---|---|---|---|
| 3-3 バグ修正 | 影響領域 | 3-3-1 | データの正しさ | 進捗率の計算バグ | ✅ クエリ不備による出力データの誤り |
| | | 3-3-2 | アクセス制御 | 非公開コースの認可漏れ | ✅ Policy 不備による不正アクセス |
| | | 3-3-3 | 機能不全 | 小テスト送信の500エラー | ✅ 例外未ハンドルによる機能停止 |
| 3-4 機能開発 | 変更スコープ | 3-4-1 | 既存機能の拡張 | 小テスト再受験機能 | ✅ 既存モデル・コントローラの修正のみ |
| | | 3-4-2 | 新規機能の構築 | コースレビュー機能 | ✅ Review モデル・コントローラを新規作成 |
| 3-5 改善 | 改善対象 | 3-5-1 | コード構造 | Fat Controller の責務分離 | ✅ 可読性・保守性の改善 |
| | | 3-5-2 | パフォーマンス | N+1 解消 | ✅ クエリ効率の改善 |

### 全タスク対応表

| タスク | 関連モデル | 関連画面 | ロール | 仕込む問題 |
|---|---|---|---|---|
| 3-1-1 セットアップ | — | — | — | README のズレ |
| 3-1-2 CLAUDE.md 更新 | — | — | — | 不完全な既存 CLAUDE.md |
| 3-2-1 全体像把握 | 全モデル | 全画面 | 全ロール | なし（複雑さ自体が題材） |
| 3-2-2 業務フロー追跡 | Course, Chapter, Lesson, Quiz, Enrollment, LessonProgress, Submission | コース詳細〜小テスト結果、マイコース | student, coach | なし（Claude の説明を検証） |
| 3-3-1 進捗率バグ | LessonProgress, Lesson, Chapter, Course | マイコース | student | 非公開レッスンが総数に含まれる |
| 3-3-2 認可バグ | Course（Policy, Scope） | コース詳細、コース一覧 | student | Policy の status チェック漏れ |
| 3-3-3 小テスト500エラー | Submission, Quiz, Question, Option | 小テスト受験 | student | スコア計算の例外未ハンドル |
| 3-4-1 小テスト再受験 | Submission, Quiz, Question, Option（全て既存） | 小テスト受験、小テスト結果 | student | なし（新規実装） |
| 3-4-2 コースレビュー | Review（新規）, Course, Enrollment, User | コース詳細 | student | なし（新規実装） |
| 3-5-1 Fat Controller | Course, Chapter, Tag, CourseTag | コース作成・編集 | coach | CourseController@store が200行超 |
| 3-5-2 N+1 解消 | Course, User, Chapter, Lesson, Enrollment, LessonProgress | コース一覧 + 生徒一覧 | student + admin | eager loading 漏れ |
| 3-6-1 PR 作成 | — | — | — | なし（3-3〜3-5 の成果物を PR にする） |
| 3-6-2 チーム環境整備 | — | — | — | なし（GitHub Actions・設定・CLAUDE.md 運用） |

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
- 加えて: コース一覧の Scope にも `published` フィルタが不完全な箇所がある

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
| README のズレ | `.env.example` に `DB_HOST=mysql` だが README には `DB_HOST=127.0.0.1` と記載。`QUEUE_CONNECTION` の記載が古い |
| 日本語・英語混在コメント | 初期開発者の日本語コメントと途中参加メンバーの英語コメントが混在 |
| 設計の不統一 | CourseController は Eloquent 直接、一部の検索処理だけ Scope を使用。統一されていない |

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

## 既存 CLAUDE.md・settings.json

前任チームが残した不完全な状態。Pro生が 3-1-2 で不足に気づき更新する。

### 既存 CLAUDE.md

意図的な問題: Sail の記載なし、技術スタックが曖昧、コース構造の説明なし、モデル関連なし、コーディング規約なし、API 記載なし、テスト情報が薄い

```markdown
# CoaKoza

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

### Pro生が 3-1-2 で更新すべき内容

- Sail コマンドへの修正（`./vendor/bin/sail` 体系）
- PHP・MySQL バージョンの追記
- コース構造（Course → Chapter → Lesson → Quiz の階層）の追記
- コーディング規約の方針の追記
- settings.json の修正（Sail・git コマンドの allow 追加）

## Git タグ戦略

### 方針

- 構築時は `initial` タグのみ作成（プロジェクト初期状態）
- `git checkout initial` でいつでも初期状態に戻れる
- タスク単位のタグ（`after-bugfix`, `after-feature`, `after-refactor`）は執筆時に模範解答が固まった段階で追加を検討する
