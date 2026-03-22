# Part 2: Claude Code の基礎
→ 能力: 使いこなす力（主）+ 見極める力（型の導入）
→ ゴール: テック記事プラットフォームをゼロから構築しながら Claude Code の主要機能を習得し、AI 出力を確認する習慣の土台を作る
→ ハンズオン: テック記事プラットフォームを Chapter を通して段階的に構築。各 Section の `記述パターン:` が執筆構造を決定する（手順 / 概念 / 混合）

## ハンズオンプロジェクト（モデルケース）

**テック記事プラットフォーム**（Laravel 10 / Laravel Sail / Blade + Tailwind CSS / PHPUnit）

Pro生 が日常的に使う Zenn や Qiita のようなテック記事プラットフォームを、Claude Code と協働してゼロから構築する。

> **題材の柔軟性**: テック記事プラットフォームはモデルケースであり、必須の手順書ではない。別のアプリを作りたい場合はそれで構わない。大切なのは各 Chapter の Claude Code 機能を使い、見極めチェックで検証すること。詳細は CLAUDE.md「ハンズオンの設計原則 > 題材の柔軟性」を参照。

モデル構成（10モデル + 中間テーブル）:

```
User（role: admin / author）
├── Profile（自己紹介、SNSリンク）+ 著者ダッシュボード（統計）
├── Article（title, body_markdown, status: draft/review/published）
│   ├── ArticleTag（多対多の中間テーブル）
│   ├── Comment（ネスト対応）
│   ├── Like + トレンドランキング
│   ├── Bookmark + コレクション管理
│   └── Series（シリーズ名・説明）+ article_series 中間テーブル（順序管理）
└── Follow（ユーザー間フォロー）+ フォローフィード

Category（記事カテゴリ）
Tag（技術タグ）
```

10モデル: User, Profile, Article, Comment, Like, Bookmark, Series, Follow, Category, Tag
中間テーブル: article_tag, article_series

主要機能:
- 検索・フィルタ・ソート・ページネーション付き記事一覧
- Markdown 記事の作成・プレビュー
- 状態遷移ルール付き公開ワークフロー（draft → review → published）
- ロール別アクセス制御（admin / author）
- 記事シリーズ（Zenn の「本」に相当。記事の順序管理）
- トレンド記事ランキング（いいね数 × 新着度）
- ブックマークコレクション（フォルダ分類・並び順管理）
- 著者ダッシュボード（総記事数・総いいね・投稿ストリーク）
- フォローフィード（フォロー中ユーザーの記事を時系列表示）

### 難易度段階

CLAUDE.md「ハンズオンの設計原則」で定義した難易度段階と Chapter の対応:

| 段階 | Chapter | 指示の抽象度 | 生成コード量 |
|---|---|---|---|
| 序盤 | 2-1, 2-2 | 具体寄り（テーブル設計・カラム型を詳細に伝える） | 少（3モデル + CRUD） |
| 中盤 | 2-3〜2-6 | ビジネス要件レベル（「認証機能を追加して」「タグ機能を追加して」） | 中（機能単位で追加） |
| 終盤 | 2-7, 2-8 | まとめて指示（「2機能を並列で」「3モデルをまとめて」） | 多（複数機能を一括生成） |
| 締め | 2-9, 2-10 | 設定・最適化・PR（アプリ実装は完了） | — |
| 応用 | 2-11 | 知らない技術への挑戦（Pro生の技術レベル外） | 中（検証方法が変わる） |

### 依存関係とアプリ進行

Part 2 の Chapter は線形依存（2-1→2-2→...→2-10→2-11）。各 Chapter は前の Chapter の完了を前提とする（ハンズオンのアプリ状態が引き継がれるため）。2-11（応用）はスキップ可。Part 3 は別プロジェクト（既存プロジェクト）を使うため、Part 2 のアプリ状態への依存はない（Part 2 で習得した Claude Code の機能知識が前提）。

アプリに変更を加える Section の入力状態・追加内容・出力状態・コミット指針を明示する。概念中心の Section（2-1, 2-3, 2-4-1, 2-9 等）はアプリ状態を変更しないため省略。アプリ状態を変更する Section では、実装後にブラウザで動作確認することを原則とする。


| Section | 入力状態 | 追加するもの | 出力状態 | コミット |
|---|---|---|---|---|
| 2-2-1 | なし | Laravel 10 + Sail プロジェクト（Tailwind CSS + Alpine.js）、CLAUDE.md | 空の Laravel プロジェクト + CLAUDE.md | — |
| 2-2-2 | 空の Laravel プロジェクト | User, Article, Category + CRUD + 検索（keyword × category × status）+ ソート + ページネーション + Markdown 表示 + Seeder + GitHub リポジトリ | 3モデル、検索・フィルタ付き一覧、GitHub リポジトリ | 初回コミット + push |
| 2-4-2 | 3モデル、検索付き一覧 | Fortify 認証、ロール別アクセス制御（admin/author）、状態遷移ルール（draft→review: 本文300字以上、review→published: admin のみ）、遷移ログ | 認証・認可済みアプリ、ビジネスルール付き状態遷移 | 💡 コミット推奨 |
| 2-5-1 | 認証済み 3モデル | Skill ファイル（`.claude/skills/`） | Skill 設定済み（モデル変更なし） | — |
| 2-5-2 | 認証済み 3モデル + Skill | Tag, Comment（ネスト）、Series + 中間テーブル（article_tag, article_series） | 6モデル + 中間テーブル2つ | 💡 コミット推奨 |
| 2-5-3 | 6モデル | 公開ワークフロー UI（ステータス表示・遷移ボタン・admin 承認画面）、Tailwind コンポーネント化 UI | 6モデル + UI 完成 | 💡 コミット推奨 |
| 2-6-1 | 6モデル | Form Request（状態遷移ルールのバリデーション含む）、Feature テスト | テスト付き | 💡 コミット推奨 |
| 2-6-2 | テスト付き 6モデル | Hooks 設定（`.claude/settings.json`） | Hooks でフォーマッタ自動実行 | — |
| 2-7-1 | 6モデル + テスト + Hooks | Git 整理、コミット、GitHub push | Git 管理済み、GitHub に push | コミット + push（Chapter の主題） |
| 2-7-3 | Git 管理済み 6モデル | Like + トレンド記事一覧、Bookmark + コレクション管理（Worktree で並列実装） | 8モデル、トレンド・コレクション付き、マージ済み | マージ後コミット |
| 2-8-1 | 8モデル | MCP 設定（MySQL 接続） | MCP 設定済み（モデル変更なし） | — |
| 2-8-2 | 8モデル + MCP | Profile + 著者ダッシュボード（統計）、Follow + フォローフィード | 10モデル（全モデル完成）、ダッシュボード・フィード付き | 💡 コミット推奨 |
| 2-8-3 | 10モデル + Skills + Hooks | Plugin パッケージ | Plugin 作成済み | — |
| 2-10-1 | 10モデル | （モデル追加なし。モデル切り替え・コスト管理の実践題材として既存機能を使用） | モデル・コスト設定済み | — |
| 2-10-2 | 10モデル | PR 作成 | PR 作成完了 | PR 作成（Chapter の主題） |
| 2-11-2 | 10モデル | Notification + 通知設定（種類ごと ON/OFF）+ 未読管理 | 11モデル | 💡 コミット推奨 |
| 2-11-3 | 11モデル | (任意) Claude API アシスタント | AI 機能付き | 💡 コミット推奨 |

### コミット方針

2-2-2 で初回コミット + GitHub push を行った後、2-7（Git 操作の Chapter）までの間は Git を体系的に扱わない。この間、各 Section 末尾に「💡 ここまでの変更をコミットしておきましょう」と案内し、変更が失われないようにする。上記テーブルの「コミット」列が「💡 コミット推奨」の Section が対象。2-7 以降は Git 操作が日常的になるため、明示的な案内は不要。

## 見極める力の扱い

Part 2 では「型の導入」として、3観点（正しさ・品質・安全性）はAI生成コードに対して常に意識すべきものとして伝える。コード生成を伴う混合パターンの Section 末尾に「見極めチェック」を配置し、3観点すべての具体的なチェック項目を MECE に列挙する。各 Chapter では文脈に応じた重点観点を設定する。深い実践は Part 3 に委ねる。

| Chapter | 重点観点 | 見極めチェックの例 |
|---|---|---|
| 2-2 | 正しさ | 生成されたモデル・リレーションが要件通りか確認する |
| 2-4 | 品質 | Plan Mode の計画と実装の設計的一貫性を確認する |
| 2-5 | 正しさ | 段階的実装の各ステップで生成コードが要件を満たすか確認する |
| 2-6 | 正しさ | テストの十分性（正常系・異常系・境界条件）を確認する |
| 2-7 | 品質 | diff に意図しない変更・debug コードがないか確認する |
| 2-8 | 正しさ | Sub-agents の探索結果が正しいか自分で検証する |
| 2-9 | 安全性 | `/security-review` の結果を鵜呑みにせず自分で確認する |
| 2-10 | 正しさ + 品質 | PR 前に生成コードとテストを総合確認する |
| 2-11 | 正しさ | 自分が知らない技術の生成コードを、Claude の説明を聞いて理解し検証する |

---

## Chapter 2-1 インストールと最初の体験（3セクション）

**ゴール**: Claude Code をインストール・認証し、最初の対話で基本操作を体験する。バイブコーディングの驚きと危うさの両方を知り、「見極める力」の必要性を実感する。

執筆メモ（Chapter レベル）: Part 2 の入口であり、教材全体の印象を決める Chapter。2-1-3 のバイブコーディング体験は教材のコンセプト（見極める力）への動機付けとして重要。驚き → 気づき → 次への意欲、の流れを大切にする。

- **2-1-1 インストールと認証**
  - ゴール: Claude Code をインストールし、認証を完了して利用開始できる
  - 記述パターン: 手順
  - Subsection:
    - インストール — 推奨方法と代替手段で Claude Code をインストールする
      - インストール手順（macOS / WSL）
      - 代替インストール方法（Homebrew / WinGet）。npm は非推奨である旨を明記
      - `claude --version` でインストール確認
    - 認証 — アカウント登録・ブラウザ認証を完了する
      - アカウント登録手順
      - 認証フロー（ブラウザ認証、`claude auth login` / `/logout`）、プラン確認
      - 認証完了後、最初の対話を体験する（「あなたは何ができますか？」）
    - 環境確認 — 動作環境を確認し開発に備える
      - `/doctor` による環境診断
      - VS Code ターミナルでの利用、ターミナル推奨設定
      - VS Code 拡張機能の紹介（インライン diff、会話履歴パネル、`@` メンション。ターミナル CLI と併用できる）
      - 💡 その他の利用環境の紹介（Desktop アプリ、Web/Mobile、JetBrains、Remote Control の存在）
  - 公式ドキュメント: [Quickstart](https://code.claude.com/docs/en/quickstart), [Setup](https://code.claude.com/docs/en/setup), [Authentication](https://code.claude.com/docs/en/authentication), [Terminal Config](https://code.claude.com/docs/en/terminal-config), [VS Code](https://code.claude.com/docs/en/vs-code)

- **2-1-2 インタラクティブモードとワンショットモード**
  - ゴール: 2つのモードを使い分け、ファイル生成と diff 承認を体験できる
  - 記述パターン: 混合
  - 執筆メモ: Sub-subsection が多い Section。入力テクニックのうち Prompt Suggestions、Background Bash、Voice Input は 💡 として「今すぐ覚えなくてよい。使いながら少しずつ身につける」と明示し、初回で全部覚える必要がないことを伝える。核は「2つのモード」と「diff 承認」の2つ。ハンズオンの題材はモダンで視覚的に楽しいものにする（Markdown ライブプレビューエディタなど）
  - Subsection:
    - 2つのモード — インタラクティブモードとワンショットモードの違いを理解する
      - インタラクティブモード（`claude`）の起動と終了（`exit` / `Ctrl+D`）
      - ワンショットモード（`claude -p`）と Pipe/stdin 連携（`cat file | claude -p`）
    - 入力テクニック — 効率的な入力方法を知る
      - 複数行入力、`@` ファイル添付、`!` Bash モード
      - Prompt Suggestions（自動サジェスト。Tab で受け入れ）
      - Background Bash（`Ctrl+B`。長時間実行コマンドのバックグラウンド化）
      - キーボードショートカット
    - ファイル生成と diff 承認 — ファイル生成を指示し、diff を読んで承認・却下できる
      - diff の読み方と承認・却下（`y` / `n` / `e`）
      - 💡 権限モードの予告: Claude Code が許可を求めてくる仕組みの概要。詳細は 2-9 で体系的に学ぶ
      - エージェントループの簡潔な紹介（ツール実行を見ながら「こう動いている」と把握する）
      - Claude Code に Markdown ライブプレビューエディタを作らせる（PHP 組み込みサーバーで動作。1プロンプトで生成 → diff 承認 → ブラウザで動作確認）
      - 追加機能を指示し、既存コードの変更 diff（追加行 + 削除行の混在）を体験する
      - ワンショットモード（`claude -p`）でも変更を試す
      - 💡 Voice Input（`Hold Space` でプッシュトゥトーク）の存在紹介
  - 見極めチェック（重点: 正しさ）
  - 公式ドキュメント: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode), [CLI Reference](https://code.claude.com/docs/en/cli-reference)

- **2-1-3 バイブコーディングの光と影**
  - ゴール: バイブコーディングの威力と危険性を体験し、「見極める力」の必要性を実感する
  - 記述パターン: 混合
  - 執筆メモ: この Section は教材全体の動機付けとして重要。バイブコーディングの「すごい！」を先に体験させ、その直後に「でもあなたはコードを1行も読んでいない」と気づかせる構成にする。恐怖を煽るのではなく、Pro生 が COACHTECH で学んだ知識（バリデーション、認証、テスト）が AI 時代にこそ武器になるというポジティブなメッセージで締める。2-1-2 の `~/claude-test` 環境をそのまま使い、Sail は使わない
  - Subsection:
    - バイブコーディングを体験する — 一言の指示で大規模なアプリを生成し、AI コーディングの威力を体感する
      - 2-1-2 で作ったアプリに対して「フル機能ブログアプリに拡張して」と一言で丸投げ
      - Claude Code が大量のファイルを生成する過程を観察
      - ブラウザで動作確認 → 動いている！
    - バイブコーディングとは何か — 用語の起源と定義を知り、自分が今やったことの意味を理解する
      - Andrej Karpathy による造語（2025年2月）と定義
      - Simon Willison の区別: 「AI にコードを書かせること」≠ バイブコーディング。「書かれたコードをレビューせずに受け入れること」= バイブコーディング
    - なぜ危険なのか — バイブコーディングの具体的なリスクを知る
      - セキュリティ: AI 生成コードの45%が OWASP Top-10 脆弱性を含む（Kaspersky 調査）。SQL インジェクション、XSS、認証欠如などの具体例
      - 品質: ロジックエラー1.7倍、セキュリティ脆弱性2.74倍（CodeRabbit 分析）
      - 実際のインシデント: 本番 DB 削除（SaaStr）、ユーザーデータ公開（Enrichlead）など
      - 認知バイアス: 「速くなった」と感じるが実際は遅くなっている（METR 研究。約40%の認知ギャップ）
      - Rachel Thomas の "junk flow"（偽のフロー状態）: 達成感はあるが実質的な成長を伴わない
    - 見極める力が武器になる — COACHTECH で学んだ知識が AI 時代の差別化要因になることを理解する
      - Simon Willison: 「レビューし、テストし、説明できるなら、それはバイブコーディングではなくソフトウェア開発」
      - Pro生 の知識（バリデーション、認証、テスト、DB 設計）は AI 出力を検証するための武器
      - 次の Chapter から、Claude Code を「使いこなし」ながら「見極める」実践が始まる
      - `~/claude-test` は削除してよい旨を伝える

## Chapter 2-2 CLAUDE.md とアプリの土台作り（2セクション）

**ゴール**: Laravel Sail でプロジェクトを作成し、`CLAUDE.md` を整備した上で、Claude Code に記事プラットフォームの土台を実装させ、生成コードを自分で確認する。

- **2-2-1 CLAUDE.md と `/init` でプロジェクトを準備する**
  - ゴール: テック記事プラットフォームの全体像を把握し、Laravel Sail でプロジェクトを作成し、`CLAUDE.md` を整備して見極めチェックの仕組みを理解する
  - 記述パターン: 混合
  - 執筆メモ: プロジェクト作成手順は COACHTECH の環境構築と同じなので簡潔に。Claude Code の学習が主目的であることを忘れない。見極めチェックの導入 Subsection で「この教材では毎回チェックリストが出る」ことを自然に伝え、構えさせすぎない
  - Subsection:
    - テック記事プラットフォームの全体像 — Part 2 を通して構築するアプリの完成イメージを把握する
      - テック記事プラットフォームのコンセプト（Pro生が日常的に使う Zenn や Qiita のようなサービス）
      - 完成時の機能一覧（検索・フィルタ付き記事一覧、Markdown エディタ、公開ワークフロー、タグ・コメント・シリーズ、いいね・トレンド、ブックマーク・コレクション、プロフィール・ダッシュボード、フォロー・フィード）
      - モデル構成（10モデル + 中間テーブル）の概要
    - プロジェクト作成 — Laravel 10 + Sail でプロジェクトを作成する（COACHTECH の環境構築手順を踏襲。Pro生にとって既知の手順のため簡潔に記載する）
      - `composer create-project laravel/laravel:^10.0` でプロジェクト作成（Docker 経由。`laravel.build` は最新版がインストールされるため使用しない）
      - `composer require laravel/sail --dev` + `sail:install --with=mysql` で Sail 導入
      - `.env` のDB接続設定確認（`DB_HOST=mysql`）
      - Tailwind CSS + Alpine.js のセットアップ（`sail npm install`）
      - `sail up -d` + `sail artisan key:generate` で起動確認
      - `sail npm run dev` の常時実行（開発中は常に実行しておく。Tailwind CSS のスタイルがビルドされないとUIが反映されない）
      - ⚠️ .env の取り扱い注意（Claude Code に .env を渡さない）
    - CLAUDE.md の整備 — CLAUDE.md の役割を理解し、プロジェクトに合わせて記述できる
      - Why: Claude Code はプロジェクトの文脈を知らない。CLAUDE.md がなければ的外れなコードを生成する
      - What: CLAUDE.md の役割と仕組み、配置場所と読み込み順序
      - How: `/init` による自動生成 + 手動追記（技術スタック、Sail コマンド体系、ディレクトリ構成）
      - ⚠️ Sail コマンド体系を CLAUDE.md に書かないと、Claude Code が `php artisan` を直接実行して Sail 外で失敗する。`./vendor/bin/sail artisan` を使うことを CLAUDE.md に明記する重要性
      - 💡 `.claude/rules/` でルールをファイル分割する方法
    - 見極めチェックの導入 — AI 生成コードに対する検証の習慣を理解する
      - Claude Code が生成したコードの責任は自分にある（1-2-1 で学んだ「AI 生成コードに対する責任」の振り返り）
      - この教材ではコード生成のたびに「見極めチェック」として3観点（正しさ・品質・安全性）のチェックリストを提示する
      - 3観点の意味と確認方法の概要（正しさ: 要件通りに動くか / 品質: 保守性・設計の一貫性 / 安全性: 脆弱性・機密情報）
      - 次の Section（2-2-2）から実践が始まる
      - 💡 セッションの継続: 作業を中断して翌日再開するときは `claude -c` で直前のセッションを継続できる。ターミナルを閉じても会話の文脈は保持されるので、翌日 `claude -c` を実行すれば続きから作業できる（体系的な解説は 2-3-3 で行う）
  - 公式ドキュメント: [Memory](https://code.claude.com/docs/en/memory), [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **2-2-2 コード生成と GitHub リポジトリ作成**
  - ゴール: Claude Code にモデル設計と CRUD を依頼し、生成コードを自分で確認して GitHub に保存できる
  - 記述パターン: 混合
  - スコープ外: 認証・認可は扱わない（2-4-2 で実装）。検索・フィルタ・ソート・ページネーション・Markdown 表示は1つのプロンプトで一括生成させ、生成結果の確認に重点を置く
  - 執筆メモ: 初回の見極めチェックが登場する Section。2-2-1 で導入した仕組みを実践する形なので、チェックリストの使い方を丁寧に案内する。ブラウザでの動作確認（CRUD 操作）を必ず含める
  - Subsection:
    - コード生成と確認 — Claude Code にモデル・Controller・Route を生成させ、内容を確認する
      - Why: Claude Code はテーブル設計やリレーションを具体的に伝えるほど的確なコードを生成する。序盤では実装の粒度で指示を出す
      - How: Claude Code にモデル設計を依頼（User, Article, Category）→ マイグレーション・リレーション・Controller・Blade・Route・Seeder を一括生成
      - 生成されたコードの確認（migration のカラム型・Controller のクエリ構築・Blade の構造・Route 定義）
      - ブラウザでの動作確認（記事一覧の表示、CRUD 操作）
    - GitHub リポジトリの作成 — `gh` CLI でリポジトリを作成し初回コミットする
      - `gh` CLI のインストールと認証（`gh auth login`）
      - GitHub リポジトリの作成（`gh repo create`）
      - `git init` + 初回コミット + push
      - 見極めチェック（正しさ）: 生成された migration のカラム型・制約・インデックスを自分で読む。意図と異なる箇所があれば Claude に理由を聞き、修正を依頼する
  - 公式ドキュメント: [Interactive Mode](https://code.claude.com/docs/en/interactive-mode), [Tools Reference](https://code.claude.com/docs/en/tools-reference), [Commands](https://code.claude.com/docs/en/commands)

## Chapter 2-3 エージェントループとコンテキスト管理（2セクション）

**ゴール**: エージェントループの仕組みを理解し、コンテキストとセッションを効率的に管理できるようにする。

執筆メモ（Chapter レベル）: 元は3セクションだったが、座学が続く問題を解消するため2セクションに統合。2-2 で生成したコードを例に「あのとき裏でこう動いていた」と振り返る形にし、座学感を減らす。セッション管理は日常的に必要な知識なので、コンテキスト管理と一緒に「長い作業を効率よく進めるための知識」として1セクションにまとめる。

- **2-3-1 エージェントループとツール実行ログ**
  - ゴール: Claude Code の動作サイクル（gather context → take action → verify results）を理解し、うまくいかないときの対処ができる
  - 記述パターン: 概念
  - 執筆メモ: トラブルシューティングの判断フローは Part 2 全体を通して使う重要な知識。印象に残るように書く
  - Subsection:
    - エージェントループ — gather context → take action → verify results の3フェーズを理解する
      - Why: Claude Code に指示を出したとき、裏で何が起きているかを知ることで、うまくいかないときの対処ができるようになる
      - 3フェーズの詳細と繰り返しの仕組み
      - ⚠️ うまくいかないときの判断フロー: 修正指示を出す → 2回以上同じ問題が続いたら `/rewind` で巻き戻す → それでもダメなら `/clear` でやり直す。無限探索ループ（Claude が同じエラーを繰り返す）は介入のサイン
    - ツールと実行ログ — Claude Code が使うツールの種類と実行結果の確認方法を知る
      - ツール種類（File operations / Search / Execution / Web / Code intelligence）
      - ツール実行ログの見方
      - Task List（`Ctrl+T`）: 複雑なタスクで Claude が自動生成する進捗リストの読み方
  - 公式ドキュメント: [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works), [Tools Reference](https://code.claude.com/docs/en/tools-reference), [Troubleshooting](https://code.claude.com/docs/en/troubleshooting)

- **2-3-2 コンテキスト管理とセッション管理**
  - ゴール: コンテキストとセッションを効率的に管理し、長時間・複数日にまたがる作業を品質を保って進められる
  - 記述パターン: 混合
  - 執筆メモ: コンテキスト管理とセッション管理は「長い作業を効率よく進めるための両輪」。別々に学ぶよりも、「作業が長くなるとコンテキストが溢れる → コンパクションで整理する → それでも限界が来たらセッションを分ける → 翌日再開するときは `-c` で継続」という流れで教える方が実感が湧く
  - Subsection:
    - コンテキストウィンドウ — コンテキストの仕組みと管理を理解する
      - Why: コンテキストが溢れると Claude Code の応答品質が落ちる。長時間の作業で品質を維持するための管理方法を知る
      - コンテキストウィンドウの概念と Claude Code が持つコンテキスト（CLAUDE.md, `@` import, 会話履歴, ファイル読み取り）
      - `/context` による使用量の可視化
      - `/compact`（フォーカスパラメータ含む）と `/clear` の使い分け
      - 自動コンパクション
      - ⚠️ CLAUDE.md 過剰記述（コンテキストを圧迫し、指示が無視される原因に）
      - 💡 Compact Instructions（CLAUDE.md に `## Compact Instructions` セクションを追加し、compaction 時に保持する内容を制御する）
    - セッション管理 — 作業を中断・再開・整理できる
      - Why: 実務では1日で作業が終わらないことがほとんど。セッションを適切に管理することで、翌日に文脈を失わずに作業を再開できる
      - セッション継続（`claude -c`）とセッション再開（`claude -r`）
      - セッション命名（`--name` / `-n`）と `/rename`
      - セッション分岐（`/branch`。エイリアス: `/fork`）
      - 💡 コンテキストとセッションの使い分け: コンテキストが溢れたら `/compact`、話題が変わったら `/clear`、翌日再開なら `claude -c`、別ブランチの作業は `claude -r` で切り替え
  - 公式ドキュメント: [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works), [Interactive Mode](https://code.claude.com/docs/en/interactive-mode), [CLI Reference](https://code.claude.com/docs/en/cli-reference)

## Chapter 2-4 プロンプト設計と Plan Mode（2セクション）

**ゴール**: 効果的なプロンプト設計を身につけ、Plan Mode を活用して認証機能を実装する。

- **2-4-1 効果的なプロンプト設計**
  - ゴール: 良い指示の条件を理解し、質問を活用して計画的に進められる
  - 記述パターン: 概念
  - Subsection:
    - 良い指示の書き方 — 良い指示の条件を理解する
      - Why: 同じ機能を作らせても、指示の書き方で生成コードの品質が大きく変わる。ここからは中盤として、ビジネス要件レベルの指示で Claude Code に実装判断を委ねていく
      - 良い指示の条件と比較例（曖昧 vs 具体的）
      - コンテキストの与え方（`@` ファイル参照、スクリーンショット、URL）
    - 質問の活用 — 質問を活用し、Claude と対話しながら進められる
      - 質問の仕方・させ方（インタビュー型プロンプト、`AskUserQuestion` パターン）
      - `/btw` でサイド質問（本筋のコンテキストを汚さない）
  - 公式ドキュメント: [Best Practices](https://code.claude.com/docs/en/best-practices), [Interactive Mode](https://code.claude.com/docs/en/interactive-mode)

- **2-4-2 Plan Mode で認証機能を実装する**
  - ゴール: Plan Mode で実装計画を立て、認証機能と記事ステータスの状態遷移バックエンドを実装できる。権限モードの基本を理解する
  - 記述パターン: 混合
  - スコープ外: 公開ワークフローの UI（ボタン・ステータス表示・admin 承認画面）は 2-5-3 で実装。権限ルールの詳細設定（allow/deny ルール構文、`.claude/settings.json`）は 2-9 で体系的に扱う
  - 執筆メモ: 中盤の開始。指示の抽象度が上がることを読者に意識させる。ここからビジネス要件レベルの指示。認証後にブラウザでログイン動作を確認させる。状態遷移ルールは UI がないためブラウザ確認できない。tinker やテストでの動作確認を案内し、UI は 2-5-3 で作ることを伝える。認証・認可を実装する文脈で Permission Mode の基本を導入する（「認証機能を作る皆さん自身が、Claude Code の権限を理解していないのは皮肉」という切り口）
  - Subsection:
    - Plan Mode — Plan Mode（`Shift+Tab`）で実装計画を立てる
      - Why: 認証・認可・状態遷移のように複数ファイルにまたがる変更は、事前に計画を立ててから実装する方が品質が高い。Plan Mode はこの「計画→実装」の分離を支援する
      - What: Plan Mode の使い方（`Shift+Tab` で切り替え、`Ctrl+G` でエディタ編集）
      - How: 認証機能（Fortify）+ ロール別アクセス制御 + 状態遷移ルールの実装計画を Plan Mode で作成する
      - 計画の整合性・影響範囲・見落としを確認する
    - 実装の実行 — 計画に基づき認証・認可・状態遷移バックエンドを実装する
      - Plan Mode → Normal Mode に切り替えて実装を実行
      - Fortify 認証 + admin/author のロール別アクセス制御（Policy）
      - Article に status フィールド + 状態遷移ルール（draft→review: 本文300字以上、review→published: admin のみ、published→draft: published_at リセット）
      - 状態遷移ログの記録
    - 権限モードの基本 — Claude Code に「何を許可するか」を意識する
      - Why: 認証・認可を実装している皆さん自身が、Claude Code の権限を「何となく y で承認」しているのは矛盾。ここで Claude Code 側の権限管理も意識し始める
      - What: 権限モードの概要（default / acceptEdits / plan の3つを紹介。残りは 2-9 で）
      - `Shift+Tab` での切り替え実践
      - 💡 ここまでの変更をコミットしておく
      - 見極めチェック（品質）: 計画と実装の整合性・影響範囲を確認する。見落としがあれば Plan Mode に戻って計画を修正し、再実装する
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows), [Best Practices](https://code.claude.com/docs/en/best-practices), [Permissions](https://code.claude.com/docs/en/permissions)

## Chapter 2-5 Skills と機能の作り込み（3セクション）

**ゴール**: Skills で再利用可能なプロンプトを作成し、それを活用しながら段階的な指示でテック記事プラットフォームの主要機能を完成させる。

- **2-5-1 Skills でプロンプトを再利用する**
  - ゴール: Skills の仕組みを理解し、プロジェクト用のカスタムスラッシュコマンドを作成できる
  - 記述パターン: 混合
  - Subsection:
    - Skills の仕組み — Skills の概念と SKILL.md の書き方を理解する
      - Why: 同じような指示を毎回書くのは非効率。Skills を使えば、プロジェクトに合わせた定型プロンプトをスラッシュコマンドとして再利用できる
      - What: Skills とは（再利用可能なプロンプト、`/skill-name` で呼び出し）
      - What: SKILL.md の構成（主要 frontmatter: name, description, argument-hint, allowed-tools, model, effort 等。全フィールドは公式ドキュメント参照）
      - What: 配置場所（`.claude/skills/`）とスコープ（Personal / Project）
      - How: テック記事プラットフォーム用の Skill を作成する（例: モデル追加テンプレート。CLAUDE.md のコマンド体系・テスト方針を踏まえた指示を Skill 化する）
    - Bundled skills — Claude Code に標準搭載された Skills を知る
      - `/simplify`（コード品質改善）、`/batch`（大規模変更）、`/debug`（デバッグ）
      - `/loop`（Scheduled Tasks の紹介。セッション内の定期実行）
  - 公式ドキュメント: [Skills](https://code.claude.com/docs/en/skills)

- **2-5-2 Skill を使ってモデルを追加する**
  - ゴール: 2-5-1 で作成した Skill を活用し、段階的指示で Tag・Comment・Series を実装できる
  - 記述パターン: 混合
  - 執筆メモ: 中盤の指示の抽象度を意識させる。各モデル追加後にブラウザで動作確認を入れる。機能単位でセッションを分ける実践が重要
  - Subsection:
    - Tag の追加 — Skill を使って多対多リレーションを追加する
      - Why: 中盤ではビジネス要件レベルの指示に移行する。「タグ機能を追加して」のように機能単位で指示し、Claude Code に実装判断を委ねる
      - How: 2-5-1 で作成した Skill（モデル追加テンプレート）を使って Tag + article_tag 中間テーブル（多対多リレーション）を追加
    - Comment・Series の追加 — ネスト構造と順序管理を追加する
      - Comment（ネスト対応）の追加
      - Series モデル + article_series 中間テーブル（記事の順序管理。Zenn の「本」に相当）
      - セッション命名（`--name`）の実践
      - ⚠️ Kitchen Sink セッション（1セッションに詰め込みすぎない。機能単位でセッションを分ける）
      - 💡 ここまでの変更をコミットしておく
      - 見極めチェック（正しさ）: 各ステップで生成されたコードを読み、多対多リレーション・ネスト構造・シリーズの順序管理を理解する。不明点は Claude に「なぜこう書いたか」を質問し、納得してから次のステップに進む
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows), [Best Practices](https://code.claude.com/docs/en/best-practices)

- **2-5-3 公開ワークフロー UI と Blade コンポーネント**
  - ゴール: 状態遷移ルールに対応する UI と、記事関連画面の Blade コンポーネントを実装できる
  - 記述パターン: 混合
  - スコープ外: 状態遷移のバックエンドロジック（ルール・ログ）は 2-4-2 で実装済み。ここでは UI（ボタン・ステータス表示・admin 承認画面）を追加する
  - 執筆メモ: `sail npm run dev` が動いていないと Tailwind が反映されないので注意喚起する。UI 実装後にブラウザで動作確認を入れる
  - Subsection:
    - 公開ワークフロー UI — 状態遷移ルールに対応するフロントを作成する
      - Why: 2-4-2 でバックエンドを実装したが、UI がないため実際の操作ができなかった。ここで UI を追加して完成させる
      - How: ステータス表示・遷移ボタン・admin 承認画面を Claude Code に生成させる
    - Blade コンポーネント化 — 記事関連画面を Tailwind CSS でコンポーネント化する
      - 記事一覧・詳細・シリーズの Blade UI（Tailwind CSS コンポーネント化）
      - 💡 ここまでの変更をコミットしておく
      - 見極めチェック（正しさ + 品質）: 公開ワークフロー UI が 2-4-2 の状態遷移ルールと正しく連動するか確認する。ブラウザで draft → review → published の遷移を実際に操作して動作確認する
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows), [Best Practices](https://code.claude.com/docs/en/best-practices)

## Chapter 2-6 テスト・デバッグと Hooks（2セクション）

**ゴール**: Claude Code にテストを書かせて実行し、テスト失敗時のデバッグを体験し、Hooks で品質チェックを自動化できるようにする。

執筆メモ（Chapter レベル）: テスト → デバッグ → Hooks は「品質を検証する → 問題を見つけたら直す → その検証を自動化する」という流れで接続する。デバッグは独立したセクションにせず、テストが失敗したときの自然な流れとして組み込む。`/debug` bundled skill もここで紹介する。

- **2-6-1 テストの作成・実行とデバッグ**
  - ゴール: Claude Code にテストを書かせ、テスト失敗時のデバッグを体験できる
  - 記述パターン: 混合
  - 執筆メモ: テストが全部通ってしまうと「デバッグ」の体験ができない。意図的にバリデーションルールを変更して失敗させ、Claude Code にデバッグさせる流れを作る。エラーメッセージの読み方と Claude Code への伝え方を実践で教える
  - Subsection:
    - テストの作成 — バリデーションを追加し、Claude Code にテストを書かせる
      - Why: Claude Code が生成したコードが要件通りに動くかを確認する最も確実な方法はテスト。ただし Claude が書くテストにも偏りがあるため、テスト自体も見極める必要がある
      - How: バリデーション（Form Request）の追加 → Claude Code に Feature テストを書かせる（記事公開ワークフローのテスト）
      - テストの実行と結果の確認（`sail test`）
      - ⚠️ Trust-then-Verify ギャップ（テストが通る ≠ 正しい。Claude のテストは正常系に偏りがち）
    - テスト失敗時のデバッグ — エラーを読み、Claude Code と一緒に原因を特定する
      - Why: 実務で最も頻繁に使うのがデバッグ。エラーメッセージを正しく読み、Claude Code に的確に伝える力は毎日の仕事に直結する
      - テスト失敗時のエラーメッセージの読み方
      - エラーを Claude Code に伝えてデバッグさせる実践（エラーメッセージのコピペ → 原因特定 → 修正 → 再テスト）
      - 💡 `/debug` bundled skill の紹介（問題の切り分けと修正を体系的に行う）
    - CLAUDE.md へのテスト方針追記 — テスト方針を CLAUDE.md に記録する
      - テストフレームワーク、実行コマンド、カバレッジ方針を CLAUDE.md に追記する
      - 💡 ここまでの変更をコミットしておく
      - 見極めチェック（正しさ）: 生成されたテストが正常系・異常系・境界条件を網羅しているか確認する。不足があれば Claude に追加を依頼するか、自分でテストケースを書く
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows), [Best Practices](https://code.claude.com/docs/en/best-practices)

- **2-6-2 Hooks でフォーマッタを自動実行する**
  - ゴール: Hooks の仕組みを理解し、ファイル編集後のフォーマッタ自動実行を設定できる
  - 記述パターン: 混合
  - 執筆メモ: 公式ドキュメントでは Hooks イベントが24種あるが、教材では主要4種（PreToolUse, PostToolUse, SessionStart, Notification）に絞る。全イベントの一覧は公式ドキュメントへの参照で補完する。Stop, UserPromptSubmit, PermissionRequest 等は実用上重要だが、ハンズオンの文脈で必要になったときに触れる程度でよい
  - Subsection:
    - Hooks の仕組み — Hooks の概念とイベントタイプを理解する
      - Why: Claude Code がファイルを編集するたびに手動でフォーマッタを実行するのは非効率。Hooks を使えば、ファイル編集後に自動でフォーマッタを走らせるなど、品質チェックを自動化できる
      - What: Hooks とは（ライフサイクルイベントに応じて実行されるスクリプト）
      - What: 主要イベント（PreToolUse, PostToolUse, SessionStart, Notification）
      - What: ハンドラタイプ（command, http, prompt, agent）
      - What: 設定場所（`~/.claude/settings.json`, `.claude/settings.json`）と `/hooks` コマンド
    - Hooks の設定 — PostToolUse で php-cs-fixer を自動実行する
      - Why: 仕組みを理解したら実際に設定する。PHP ファイルを編集するたびにフォーマッタが自動で走るようにして、コードスタイルの一貫性を保つ
      - How: `.claude/settings.json` に PostToolUse Hook を設定
      - matcher でツール名をフィルタリング（`Edit|Write`）
  - 公式ドキュメント: [Hooks](https://code.claude.com/docs/en/hooks), [Hooks Guide](https://code.claude.com/docs/en/hooks-guide), [Features Overview](https://code.claude.com/docs/en/features-overview)

## Chapter 2-7 Git・Checkpointing・Worktree（3セクション）

**ゴール**: Claude Code の Git 統合・チェックポイント・Worktree を使いこなし、コードの変更を安全かつ並列に管理できるようにする。

- **2-7-1 Git 操作と `/diff`**
  - ゴール: Claude Code から Git 操作ができ、diff を確認する習慣を身につける
  - 記述パターン: 混合
  - 執筆メモ: ここまでの「💡 コミットしておきましょう」を体系的に学ぶ転換点。2-2-2 から蓄積された変更を整理する実践なので、受講生のプロジェクトの状態がそれぞれ異なる前提で書く
  - Subsection:
    - Git 操作 — Claude Code から Git 操作ができる
      - Why: ここまでは「💡 コミットしておきましょう」で済ませていた Git 操作を、Claude Code の機能として体系的に学ぶ。終盤に向けて、変更の管理が重要になる
      - How: `claude commit` でこれまでの変更を整理
      - `/diff` でインタラクティブに確認
      - ブランチ作成と管理
    - GitHub への push — 変更を GitHub に push する
      - Why: ローカルで管理しているだけではコードを失うリスクがある。GitHub に push して安全に保管し、チームで共有する準備をする
      - `git push` と GitHub 上での確認
      - .env や認証情報がコミットに含まれていないことを確認
      - 見極めチェック（品質）: diff に意図しない変更・.env 混入・debug コードの残留がないか確認する。見つけたら `git reset` で staging から外すか、Claude に修正を依頼する
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **2-7-2 Checkpointing と `/rewind`**
  - ゴール: チェックポイントの仕組みを理解し、`/rewind` で安全に巻き戻せる
  - 記述パターン: 混合
  - Subsection:
    - チェックポイントの仕組み — ファイル編集の自動スナップショットを理解する
      - Why: Claude Code に大きな変更をさせて失敗したとき、Git で戻すのは面倒。チェックポイントは Claude Code 内で即座に巻き戻せる安全ネットである
      - What: チェックポイントの概念（ローカル undo。Git とは別の仕組み）
      - What: 追跡される変更と追跡されない変更（Bash コマンドの副作用は追跡外）
    - `/rewind` による巻き戻し — `/rewind` と `Esc+Esc` で変更を巻き戻せる
      - 5つのアクション（コード復元 / 会話復元 / 両方復元 / ここから要約 / キャンセル）
      - `/rewind` コマンドと `Esc+Esc` ショートカット
  - 公式ドキュメント: [Checkpointing](https://code.claude.com/docs/en/checkpointing)

- **2-7-3 Worktree で並列作業する**
  - ゴール: Worktree を使って複数機能を並列に開発できる
  - 記述パターン: 混合
  - 執筆メモ: 終盤の「まとめて指示」が始まる。2つの Worktree を同時に走らせるのは受講生にとって初体験。手順を明確にし、マージ時のコンフリクト対処も含める。マージ後のブラウザ確認で両機能が動くことを確認させる
  - Subsection:
    - Worktree の仕組み — Git Worktree と `--worktree` フラグを理解する
      - Why: 終盤では「まとめて指示」に移行する。2つの機能を同時に並列開発し、大量の生成コードを検証する体験をする
      - What: Worktree の概念（同一リポジトリの別作業ディレクトリ）
      - What: `claude --worktree <name>` でセッションごとに隔離された環境を作る
      - What: Worktree のクリーンアップ（変更なし→自動削除、変更あり→確認）
    - 並列実装 — 2つの機能を Worktree で並列に開発する
      - How: Like モデル + トレンド記事一覧（いいね数×新着度でスコア計算）を1つの Worktree で実装
      - Bookmark モデル + コレクション管理（フォルダ作成・記事の分類・並び順）をもう1つの Worktree で実装
      - 両方をマージ
      - 見極めチェック（品質）: 並列実装された2つの機能が互いに干渉していないか、マージ後のコードを確認する。コンフリクトや動作不良があれば `/rewind` で戻してやり直す
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows)

## Chapter 2-8 MCP・Sub-agents・Plugins（3セクション）

**ゴール**: MCP で外部ツールに接続し、Sub-agents で探索を委譲し、Plugins でチームに配布する方法を習得する。

- **2-8-1 MCP で DB に接続する**
  - ゴール: MCP の概念を理解し、MySQL に接続してテーブル構造やデータを直接確認できる
  - 記述パターン: 混合
  - Subsection:
    - MCP の概念 — MCP（Model Context Protocol）が何を解決するかを理解する
      - Why: Claude Code は単体でもファイルの読み書きやコマンド実行ができるが、データベースの中身を直接見ることはできない。MCP を使えば、Claude Code がDBに接続してテーブル構造やデータを確認しながら作業できる
      - What: MCP とは（AI ツールと外部データソースを接続するオープンスタンダード）
      - What: MCP でできること（DB クエリ、GitHub 操作、Slack 連携、ブラウザ操作など）
    - DB への接続 — `claude mcp add` で MySQL に接続する
      - How: `claude mcp add` コマンドと transport タイプ（stdio / http / sse / ws）
      - MySQL への接続設定
      - `/mcp` で接続状態を確認
      - MCP スコープ（local / project / user）
    - ブラウザとの接続 — Playwright MCP でアプリの画面を Claude Code に見せる
      - Why: DB だけでなくブラウザも接続できる。Claude Code にアプリの画面を見せながら UI の確認や修正を指示できる
      - How: Playwright MCP の追加と接続設定
      - テック記事プラットフォームの画面をスクリーンショットで撮影させ、Claude Code に見せる
      - 画面の状態を見た上で「この UI を修正して」と指示する体験
  - 公式ドキュメント: [MCP](https://code.claude.com/docs/en/mcp)

- **2-8-2 Sub-agents で探索を委譲する**
  - ゴール: Sub-agents の概念を理解し、コードベースの探索を委譲しながら残りの機能を実装できる
  - 記述パターン: 混合
  - 設計意図: 残りの2モデル（Profile, Follow）をまとめて追加するのは、Sub-agents に複数モジュールの探索を委譲する実践題材とするため。終盤の「まとめて指示して大量の生成コードを検証する」体験を優先する
  - 執筆メモ: 10モデル完成の節目。ここまで来たことへの達成感を伝えつつ、大量の生成コードを検証する見極めチェックを丁寧に。ブラウザでダッシュボードとフォローフィードの動作確認を入れる。Sub-sub が12個と多いため、概念解説（Sub-agents とは）とアプリ実装（Profile + Follow）のバランスに注意。概念は簡潔に、実装と検証に紙面を割く
  - Subsection:
    - Sub-agents の概念 — Sub-agents が何を解決するかを理解する
      - Why: プロジェクトが大きくなると、コードベース全体の文脈をメインセッションに読み込むとコンテキストを圧迫する。Sub-agents に探索を委譲すれば、メインの文脈を汚さずに調査できる
      - What: Sub-agents とは（隔離されたコンテキストで動く専門ワーカー）
      - What: built-in Sub-agents（Explore, Plan, general-purpose）
      - What: メインコンテキストを汚さずに探索・検証できるメリット
    - Sub-agents の活用 — Profile, Follow を追加しながら Sub-agents で探索する
      - How: Profile モデル + 著者ダッシュボード（総記事数・総いいね・投稿ストリーク）の追加
      - Follow モデル + フォローフィード（フォロー中ユーザーの記事を時系列表示）の追加
      - Sub-agents にモジュール単位の探索を委譲する
      - `/agents` コマンドとカスタム Sub-agent の概要
      - 💡 Sub-agent の persistent memory（`memory` フィールドで user/project/local スコープのメモリを保持できる）
      - 💡 Agent Teams の存在紹介（複数セッションの協調。実験的機能）
      - 💡 ここまでの変更をコミットしておく
      - 見極めチェック（正しさ）: Sub-agents が返した探索結果を、自分でコードを見て検証する。誤りや省略があれば Claude に指摘し、正確な情報を引き出す
  - 公式ドキュメント: [Sub-agents](https://code.claude.com/docs/en/sub-agents), [Agent Teams](https://code.claude.com/docs/en/agent-teams)

- **2-8-3 Plugins でチームに配布する**
  - ゴール: Plugins の概念を理解し、Skills・Hooks をパッケージ化してチームに配布できる
  - 記述パターン: 混合
  - Subsection:
    - Plugins の概念 — Plugins が何を解決するかを理解する
      - Why: 2-5 で作った Skills、2-6 で設定した Hooks をチームメンバーにも使ってもらいたい場合、1つずつ共有するのは手間。Plugins を使えば、まとめてパッケージ化して配布できる
      - What: Plugins とは（Skills, Hooks, Sub-agents, MCP をパッケージ化して配布する仕組み）
      - What: Plugin の構造（`.claude-plugin/plugin.json`, `skills/`, `hooks/`, `agents/`, `.mcp.json`, `settings.json` 等）
      - What: Standalone 設定との違いと使い分け
    - Plugin の作成 — 既存の Skills・Hooks を Plugin にパッケージ化する
      - How: Plugin manifest の作成
      - `--plugin-dir` でローカルテスト
      - `/plugin` でのインストールとマーケットプレイスの紹介
      - 💡 実用的なプラグインの紹介（`/skill-creator` 等）
  - 公式ドキュメント: [Plugins](https://code.claude.com/docs/en/plugins), [Features Overview](https://code.claude.com/docs/en/features-overview)

## Chapter 2-9 権限設定とセキュリティ（2セクション）

**ゴール**: Claude Code の権限システムを理解し、セキュリティレビューで安全性を確認できるようにする。

- **2-9-1 権限モードと権限ルール**
  - ゴール: 権限モード・権限ルールを理解し、プロジェクトに応じた設定ができる
  - 記述パターン: 混合
  - Subsection:
    - ツールと許可 — どのツールがどのタイミングで許可を求めるか理解する
      - Why: これまで Claude Code が許可を求めてきたとき「何となく承認」していた仕組みを体系的に理解する。実務では、許可すべき操作とそうでない操作を区別する必要がある
      - 許可ダイアログの仕組み
    - 権限モード — 5種の権限モード（重点: default, acceptEdits）を理解し使い分ける
      - default / acceptEdits / plan / dontAsk / bypassPermissions
      - `--permission-mode` フラグと `Shift+Tab` での切り替え
    - 権限ルール — allow / ask / deny ルールを設定できる
      - allow / ask / deny ルールとルール構文（`Tool(specifier)` パターン、ワイルドカード `*`、WebFetch の `domain:` 指定、Read/Edit のパス指定等）
      - ルール評価順序（deny → ask → allow）
      - `.claude/settings.json` での設定とチーム共有
  - 公式ドキュメント: [Permissions](https://code.claude.com/docs/en/permissions), [Settings](https://code.claude.com/docs/en/settings)

- **2-9-2 `/security-review` とサンドボックス**
  - ゴール: `/security-review` とサンドボックスを理解し、セキュリティ確認の習慣を知る
  - 記述パターン: 混合
  - Subsection:
    - `/security-review` — セキュリティレビューの使い方と確認観点を理解する
      - Why: 見極める力の3観点のうち「安全性」を実践する Chapter。AI が「問題なし」と言っても、それは「見つけられなかった」であって「存在しない」ではない
      - What: `/security-review` の使い方と確認観点
      - 見極めチェック（安全性）: CSRF, XSS, 認可を自分の目で確認し、気になる箇所があれば Claude に「ここは安全か？」と具体的に問い詰める
    - サンドボックス — OS レベルの隔離で安全性を確保する仕組みを理解する
      - What: サンドボックスの概要（macOS は Seatbelt、Linux は bubblewrap）
      - ファイルシステム・ネットワークの隔離範囲
  - 公式ドキュメント: [Security](https://code.claude.com/docs/en/security), [Sandboxing](https://code.claude.com/docs/en/sandboxing)

## Chapter 2-10 モデル・コスト管理・PR（2セクション）

**ゴール**: モデル選択とコスト管理で開発効率を最適化し、PR を作成して Part 2 の本編アプリを完成させる。

- **2-10-1 モデル選択・`/effort`・`/cost`**
  - ゴール: モデルの特徴とコストを理解し、タスクに応じて使い分けられる
  - 記述パターン: 混合
  - Subsection:
    - モデル選択 — タスクに応じたモデルを選択できる
      - Why: Claude Code はデフォルトのモデルで動作するが、タスクの複雑さに応じてモデルを切り替えることで、速度とコストを最適化できる
      - What: モデルエイリアス（opus, sonnet, haiku, opusplan 等）と各モデルの特徴。opusplan は Plan Mode で opus、実行時に sonnet を自動切り替え
      - タスクの複雑さに応じた使い分け
    - 推論とコストの調整 — `/effort` と `/cost` で効率を管理する
      - `/effort`（low / medium / high / max / auto）と Extended Thinking
      - Fast Mode（`/fast`）のトレードオフ（Extra Usage が必要。サブスクリプション枠外課金）
      - `/cost` で使用量を確認し、コスト削減テクニックを知る
      - 💡 Output Styles の紹介（Explanatory / Learning / Custom。特に Learning モードは Claude が `TODO(human)` を残して読者自身にコードを書かせる。見極める力の実践と親和性が高い）
  - 公式ドキュメント: [Model Configuration](https://code.claude.com/docs/en/model-config), [Fast Mode](https://code.claude.com/docs/en/fast-mode), [Costs](https://code.claude.com/docs/en/costs), [Output Styles](https://code.claude.com/docs/en/output-styles)

- **2-10-2 PR 作成と振り返り**
  - ゴール: Claude Code で PR を作成し、Part 2 での学びを振り返る
  - 記述パターン: 混合
  - 執筆メモ: Part 2 本編の締めくくり。振り返りは説教臭くならないように。「ここまでできた」という手応えを残して Part 3 へ接続する。2-11 は応用編としてスキップ可であることを明確にする。GitHub Actions / Code Review は存在紹介のみ。Part 3（チーム開発）で実践する接続を明示する（Part 3 outline 確定時に要同期）
  - Subsection:
    - PR の作成 — Claude Code で PR を作成し、attribution を設定する
      - Why: 実務ではコードを書いたら PR を作成してレビューを受ける。Claude Code は PR 作成からレビュー対応までを支援する
      - How: Claude Code による PR 作成（`gh pr create`）
      - attribution（`Co-Authored-By`）
      - `/pr-comments` でレビュー指摘を取得・対応
      - `--from-pr` でのセッション再開
      - 💡 GitHub Actions / Code Review 自動化の存在紹介（`@claude` メンションによる自動レビュー。詳細は Part 3 のチーム開発で実践する）
    - 振り返りと次への準備 — Part 2 で身につけた習慣を整理し、Part 3 に備える
      - ⚠️ 過度な修正指示（2回以上同じ修正を指示したら `/clear` でやり直す判断）
      - タスク分割と介入のタイミング
      - 💡 設定の体系（5レベル階層）と自動メモリ機能の概要紹介（詳細は Part 3 以降で必要に応じて学ぶ）
      - 見極めチェック（正しさ + 品質）: PR の差分を第三者視点で読み返す。テストが通ること・意図しない変更がないことを確認し、問題があれば PR を出す前に修正する
      - 💡 Part 3 への接続: Part 2 の本編はここまで。Part 2 で習得した Claude Code の機能を、Part 3 では既存プロジェクトの実務タスクで実践する。次の Chapter 2-11 は応用編（スキップ可）
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows), [Settings](https://code.claude.com/docs/en/settings), [Memory](https://code.claude.com/docs/en/memory), [Code Review](https://code.claude.com/docs/en/code-review)

## Chapter 2-11 応用: 知らない技術に Claude Code で挑む（3セクション）

**ゴール**: 自分が経験していない技術領域で Claude Code を活用する方法を理解し、検証方法を切り替えて実践できる。

> 💡 この Chapter はスキップしても Part 3 に影響しません。2-10 までの本編で学んだ知識で Part 3 に進めます。

- **2-11-1 知らない技術への向き合い方**
  - ゴール: 自分の技術レベル外の領域で Claude Code を使うときの心構えと検証方法を理解する
  - 記述パターン: 概念
  - 執筆メモ: ここまでの「知っている技術を高速に実装する」体験との対比が重要。「検証方法が変わる」ことを具体的に伝え、次の 2-11-2 で実践する流れを作る。思考の放棄との違いを丁寧に
  - Subsection:
    - 知っている技術と知らない技術の違い — 検証方法が変わることを理解する
      - Why: 実務では、自分が経験していない技術を使う場面がある。Claude Code はそのような場面でも実装を生成してくれるが、「見極める力」の使い方が変わる
      - 知っている技術: コードを読んで正しいか判断できる → コードを検証する
      - 知らない技術: コードを読んでも判断できない → Claude の説明を聞いて理解し、自分の知識にしてから検証する
      - 思考の放棄との違い: 「分からないから受け入れる」ではなく「分からないから聞いて理解してから受け入れる」
    - 検証のステップ — 知らない技術の生成コードを検証する方法
      - Claude に設計判断の理由を質問する
      - 公式ドキュメントを参照して裏取りする
      - テストを書いて動作を確認する
      - 理解できない部分を明確にし、それでも採用するかを判断する

- **2-11-2 Notification 機能を実装する**
  - ゴール: Laravel の通知機能を Claude Code で実装し、知らない技術の検証を実践する
  - 記述パターン: 混合
  - Subsection:
    - Notification の実装と検証 — Laravel Notifications を Claude Code に実装させ、検証ステップを実践する
      - Why: Laravel Notifications は Pro生 が COACHTECH では学んでいない可能性がある機能。実装しながら 2-11-1 の検証ステップを適用する
      - How: Notification モデル + 通知設定（種類ごと ON/OFF）+ 未読管理を Claude Code に実装させる
      - 検証ステップの適用: 「なぜこの設計にしたか」「Laravel Notifications を使わずに自前実装した理由は何か」等を質問する → 公式ドキュメントで裏取り → テストで動作確認
      - 💡 ここまでの変更をコミットしておく
      - 見極めチェック（正しさ）: 自分が理解できていない部分を特定し、Claude に説明を求める。説明を聞いて納得してからコードを採用する
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **2-11-3 外部 API 連携で検証をさらに実践する（任意）**
  - ゴール: 外部 API 連携という未経験の領域で、2-11-1 の検証ステップを再度実践し、知らない技術への向き合い方を定着させる
  - 記述パターン: 混合
  - Subsection:
    - 外部 API 連携の実装 — Claude Code に Claude API を使った AI 記事アシスタントを実装させる（💡 任意セクション: API 料金が発生します。スキップしても Part 3 に影響しません）
      - Why: 外部 API 連携、Service クラスパターン、API モックテストなど、Pro生が COACHTECH では経験していない可能性が高い技術が複数含まれる。2-11-2 と同じ検証ステップを別の技術領域で繰り返すことで、向き合い方を定着させる
      - How: Claude API を使った AI 記事アシスタントを Claude Code に実装させる（API キー設定、Service クラス設計、エラーハンドリング、テスト）
      - 検証ステップの適用: Claude に「なぜ Service クラスに切り出したのか」「このモック方法は適切か」等を質問する → 公式ドキュメントで裏取り → テストで動作確認
      - 💡 ここまでの変更をコミットしておく
      - 見極めチェック（正しさ）: 自分が理解できていない部分を特定し、Claude に説明を求める。説明を聞いて納得してからコードを採用する
  - 公式ドキュメント: [Claude API Documentation](https://platform.claude.com/docs/en/api/messages), [Skills](https://code.claude.com/docs/en/skills)（`/claude-api` Bundled skill）
