# Part 3: Claude Code の実践
→ 能力: 見極める力（主）+ 使いこなす力（総合演習）
→ ゴール: 提供プロジェクトで実務タスク（バグ修正・機能開発・リファクタリング）を Claude Code と協働して遂行し、Part 2 で学んだ機能を総合的に使いこなしながら、AI 出力を自ら検証・判断する力を鍛える
→ ハンズオン: 提供プロジェクト（ProConnect）をモデルケースとして実践。教材側で用意。各タスクで「ガイド付き → 検証 → 自力実践」のリズムで進む。題材の柔軟性は CLAUDE.md「ハンズオンの設計原則」を参照

---

## MECE 設計方針

分類軸: **実務タスクの種類**（コンセプトで定義された3タスク + その前提 + チーム開発文脈）

| 分類軸 | Chapter | 見極める力の重点 | 活用する Part 2 機能 |
|---|---|---|---|
| **前提: 理解** | 3-1 コードリーディング | Claude の説明を自分で検証する | Sub-agents, MCP, `/compact`, `/context`, CLAUDE.md, `/btw` |
| **タスク: 修正** | 3-2 バグ修正 | セキュリティ（認可の漏れ） | プロンプト設計, `/rewind`, `/security-review`, テスト, `/effort` |
| **タスク: 開発** | 3-3 機能開発 | コードレビュー（既存設計との整合性） | Plan Mode, Hooks, Skills, セッション管理, テスト |
| **タスク: 改善** | 3-4 リファクタリング | テスト（動作不変の保証） | Worktree, Fast Mode, `/cost`, Plan Mode, テスト |
| **協働: チーム** | 3-5 チーム開発 | 説明責任を果たす | Git, PR, `/pr-comments`, 権限管理, CLAUDE.md 共有 |

> Part 3 で新たに導入する機能は **GitHub Actions**（3-5）のみ。他は全て Part 2 で習得済みの機能を実務コンテキストで実践する。
> 3-5 はコンセプトの「これらの能力は個人での開発に限らず、チーム開発の文脈でも求められる」を実践する Chapter。3-2〜3-4 で個人として実践したタスクを、チームワークフローに乗せて一気通貫で回す。

### 見極める力の扱い

Part 3 では「実践」レベル。各タスクで **正しさ・品質・安全性** の3観点を繰り返し実践するが、Chapter ごとに重点を変えて形骸化を防ぐ:

| Chapter | 重点観点 | 理由 |
|---|---|---|
| 3-2 バグ修正 | **安全性** | 認可の漏れがバグの本質。Policy・Scope を自分で確認する |
| 3-3 機能開発 | **品質** | 既存設計との整合性判断。Service 層・Event/Listener パターンの理解 |
| 3-4 リファクタリング | **正しさ** | リファクタリング前後で動作が変わらないことの保証 |

---

## 提供プロジェクト概要

### プロダクト

**ProConnect**（架空）— IT エンジニアと開発案件をマッチングするプラットフォーム。企業が案件を掲載し、エンジニアが応募、エージェントが仲介する三者構造。レバテックフリーランスや ITプロパートナーズのような人材マッチングサービスを簡略化したもの。

### 想定シナリオ

ProConnect は 1 年半ほど運用されており、初期開発チーム（2〜3名）が退職。Pro 生は途中参加のエンジニアとして、既存コードの理解からバグ修正・機能追加・リファクタリングを担当する。

### 技術スタック

| 項目 | 内容 |
|---|---|
| Laravel | 10.x |
| PHP | 8.1 |
| DB | MySQL 8.0 |
| 認証 | Fortify（ユーザー種別ごとのガード） |
| フロント | Blade + Tailwind CSS（管理画面・エージェント画面）、API（エンジニア向け SPA 想定） |
| インフラ | Docker Compose（nginx + php-fpm + mysql + redis + mailhog） |
| テスト | PHPUnit |
| その他 | Queue（Redis）、Notification、PDF 出力（契約書） |

### モデル構成（約 20 モデル）

```
User（role: admin / agent / company / engineer）
│
├── Admin 系
│   └── AdminActivityLog
│
├── エージェント系
│   └── AgentProfile
│
├── 企業系
│   ├── CompanyProfile
│   └── CompanyUser（企業内の複数担当者）
│
├── エンジニア系
│   ├── EngineerProfile（自己紹介、希望単価、稼働可能日）
│   ├── WorkHistory（職務経歴）
│   └── EngineerSkill（多対多の中間テーブル）
│
├── 案件系
│   ├── Project（案件情報: 技術スタック、単価レンジ、期間、勤務形態）
│   ├── ProjectSkill（多対多の中間テーブル）
│   └── ProjectImage
│
├── マッチング・選考系
│   ├── Application（応募: エンジニア→案件）
│   ├── SelectionStep（選考ステップ: 書類選考→面談→内定→契約→辞退/不合格）
│   └── Interview（面談日程調整）
│
├── 契約・稼働系
│   ├── Contract（契約情報: 期間、単価、支払サイト）
│   ├── Timesheet（月次稼働報告）
│   └── Invoice（請求情報）
│
├── コミュニケーション系
│   ├── Message（企業⇔エンジニア⇔エージェント間）
│   └── Notification
│
└── マスタ系
    ├── Skill（技術スキルマスタ: PHP, Laravel, React 等）
    ├── Industry（業界マスタ）
    └── Prefecture（都道府県マスタ）
```

### コードベースの「リアルさ」（意図的に仕込む特徴）

| 再現する特徴 | 具体例 |
|---|---|
| **コードスタイルのバラつき** | 古い Controller（ApplicationController）は Fat で200行超。新しい Controller（ProjectController）は Service 層に委譲 |
| **テストカバレッジのムラ** | 選考ステータス遷移は Feature テストあり。管理画面の CRUD・メッセージ機能はテストなし |
| **後付けマイグレーション** | `add_remote_flag_to_projects`、`add_payment_site_to_contracts`、`rename_fee_to_unit_price_in_contracts` 等 |
| **残留物** | 使われていない `OldMatchingController`、TODO コメント（「// TODO: バリデーション追加」）、コメントアウトされた旧ロジック |
| **README のズレ** | セットアップ手順の環境変数名が一部古い（`DB_HOST` の値が変わっている） |
| **N+1 問題** | 案件一覧でスキルを表示する際に `with()` が漏れている |
| **不統一なエラーハンドリング** | API は JSON レスポンス、管理画面は Blade リダイレクト、一部は try-catch なし |
| **設計の不統一** | 一部の箇所は Repository パターン、他は Eloquent 直接呼び出し |
| **日本語・英語混在コメント** | 初期開発者が書いた日本語コメントと、途中参加の外国人が書いた英語コメントが混在 |

### プロジェクトに最初から用意するもの（ハイブリッドアプローチ）

| ファイル | 状態 | 意図 |
|---|---|---|
| `CLAUDE.md` | **存在するが不完全** | 前任チームが書いたもの。基本情報（技術スタック、DB 構成、開発コマンド）はあるが、コーディング規約が曖昧、アーキテクチャ方針の記載が古い |
| `.claude/settings.json` | **存在する** | 基本的な権限設定（`php artisan` 系、`npm run` 系の allow ルール）が設定済み |
| `.env.example` | **微妙にズレている** | 前回の変更で追加された環境変数が反映されていない |

学習者は Chapter を進める中で、既存の `CLAUDE.md` を読み → 不足に気づき → 追記・修正していく。

### 提供方法

- GitHub リポジトリとして公開（教材側で用意）
- `docker compose up` で起動できる状態
- Seeder でリアルなダミーデータを投入済み（企業20社、エンジニア50名、案件30件、応募・選考データ）
- 各 Chapter のスタート地点を Git タグで管理（`chapter-3-2-start` 等）

---

## Section ごとのタスク進行

読者が各 Section で何を実践し、何が残るかを追跡する。プロジェクトが未作成の段階では概要レベルで定義し、作成後に具体化する。

| Section | 実践内容 | 成果物 |
|---|---|---|
| 3-1-1 | ProConnect をクローン・起動し、CLAUDE.md を読む | 動作する開発環境、プロジェクトの概要理解 |
| 3-1-2 | Sub-agents と MCP で全体像を把握、CLAUDE.md を更新 | 更新された CLAUDE.md（モデル関連図・コマンド・方針を追記） |
| 3-1-3 | 業務フローをコードで追跡し、Claude の説明を自分で検証 | フロー理解、検証の実践経験 |
| 3-2-1 | 稼働時間集計バグの原因特定と修正 | バグ修正コード、`/rewind` の実践経験 |
| 3-2-2 | 修正コードを3観点（正しさ・品質・安全性）で検証 | テストコード、セキュリティレビュー結果、CLAUDE.md への知見追記 |
| 3-2-3 | 認可バグを自力で修正・検証 | 2つ目のバグ修正コード、セキュリティ検証の実践経験 |
| 3-3-1 | 通知機能の要件整理、Plan Mode で設計 | 実装計画 |
| 3-3-2 | 通知機能を段階的に実装、Hooks と Skills を活用して検証 | 通知機能の実装コード・テスト |
| 3-3-3 | 追加機能を自力で開発・検証 | 追加機能の実装コード |
| 3-4-1 | Fat Controller を Service 層 + Form Request に分離 | リファクタリング済みコード・テスト |
| 3-4-2 | N+1 問題を Worktree で並列に解消 | N+1 修正コード、Worktree マージ済み |
| 3-4-3 | 改善対象を自分で特定し、リファクタリングを自力で遂行 | 追加リファクタリングコード |
| 3-5-1 | 変更を PR にまとめ、レビュー対応 | PR 作成済み |
| 3-5-2 | GitHub Actions の仕組みを理解、自動レビューのワークフローを把握 | GitHub Actions の理解（設定は API アクセスがある場合のみ） |
| 3-5-3 | チーム設定と CLAUDE.md 運用方針を整備 | `.claude/settings.json` のチーム設定、CLAUDE.md 運用ルール |

## Chapter 構成

### Chapter 3-1 コードリーディング（3セクション）

**ゴール**: Claude Code を使って既存プロジェクトのセットアップから全体像の把握、業務フローの追跡までを行い、途中参加の初動を効率化できる。

> Part 2 の実践: Sub-agents（2-8-2）, MCP（2-8-1）, コンテキスト管理（2-3-2）, CLAUDE.md（2-2-1）, 自動メモリ（2-10-3）, `/btw`（2-4-1）

- **3-1-1 プロジェクトのセットアップ**
  - ゴール: リポジトリをクローンし、Docker Compose で開発環境を起動できる
  - 記述パターン: 混合
  - Subsection:
    - セットアップ — リポジトリのクローンから動作確認までを行う
      - リポジトリのクローンと Docker Compose 起動
      - README のズレに気づき、Claude Code で正しい手順を特定する
      - 動作確認（ブラウザアクセス、ログイン、Seeder データの確認）
    - 既存の CLAUDE.md を読む — プロジェクトの概要を把握し、不足に気づく
      - 既存の `CLAUDE.md` を読み、プロジェクトの概要を把握する
      - 記載内容と実際のコードベースの差異に気づく
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **3-1-2 プロジェクトの全体像を把握する**
  - ゴール: Sub-agents と MCP を活用して、ディレクトリ構成・モデル関連・ルーティングの全体像を効率的に把握できる
  - 記述パターン: 混合
  - Subsection:
    - 全体像の把握 — Claude Code にプロジェクトの概要を説明させる
      - 「このプロジェクトの概要を教えて」で全体像を掴む
      - Sub-agents にモジュール単位の探索を委譲する（Part 2 の復習）
    - DB 構造の確認 — MCP で DB に接続し、テーブル構造とデータを直接確認する
      - MCP で ProConnect の MySQL に接続する（Part 2 の復習）
      - 20テーブルの構造を効率的に把握する
      - `/context` でコンテキスト消費を確認し、`/compact` で整理する
    - CLAUDE.md の更新 — 不足している情報を追記する
      - `CLAUDE.md` にモデル関連図、主要コマンド、アーキテクチャ方針を追記する
  - 公式ドキュメント: [Sub-agents](https://code.claude.com/docs/en/sub-agents), [MCP](https://code.claude.com/docs/en/mcp)

- **3-1-3 業務フローをコードで追う**
  - ゴール: 「案件応募〜選考〜契約」の業務フローをコードレベルで追跡し、Claude の説明を自分で検証できる
  - 記述パターン: 混合
  - Subsection:
    - 業務フローの追跡 — 横断的にコードを読む
      - 「応募から契約までの処理フローを追って」で横断的にコードを読む
      - 選考ステータスの状態遷移を理解する
      - `/btw` で関連する疑問を本筋のコンテキストを汚さずに確認する
    - 見極める力: Claude の説明を検証する — Claude Code の説明が正しいかを自分でコードを見て確認する
      - Claude が説明したフローと実際のコードを照合する
      - 説明の省略・誤り・古い情報に気づく練習
  - 公式ドキュメント: [Best Practices](https://code.claude.com/docs/en/best-practices)

### Chapter 3-2 バグ修正（3セクション）

**ゴール**: Claude Code と協働してバグの原因特定から修正・検証までを遂行し、AI 出力を正しさ・品質・安全性の観点で検証できる。

> Part 2 の実践: プロンプト設計（2-4-1）, `/rewind`（2-7-2）, `/security-review`（2-9-2）, テスト（2-6-1）, `/effort`（2-10-1）, CLAUDE.md（2-2-1）
> 見極める力の重点: **セキュリティ**（認可の漏れ）

- **3-2-1 バグの原因特定と修正**
  - ゴール: バグ報告から Claude Code で原因を特定し、修正できる
  - 記述パターン: 混合
  - Subsection:
    - バグの原因特定 — バグ修正のプロンプトパターンで原因を探索する
      - バグ報告:「月またぎの稼働時間集計が合わない」
      - バグ修正のプロンプトパターン（症状・再現手順・期待値を伝える）
      - 原因: Timesheet の集計クエリが月初〜月末の境界で off-by-one
    - 修正と安全確認 — Claude Code に修正を依頼し、チェックポイントを確認する
      - Claude Code に修正を依頼する
      - チェックポイントの確認: 修正前の状態に `/rewind` で戻れることを体験する
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows), [Checkpointing](https://code.claude.com/docs/en/checkpointing)

- **3-2-2 修正の検証（正しさ・品質・安全性）**
  - ゴール: AI が生成した修正コードを3つの観点で検証できる
  - 記述パターン: 混合
  - Subsection:
    - コードレビュー — 修正コードを自分で読み、境界条件・影響範囲を確認する
      - 修正コードの意図を理解する
      - 境界条件（月初、月末、閏年、年またぎ）のカバー確認
    - テスト — テストケースを作成し、テストの十分性を判断する
      - Claude Code にテストを書かせ、実行する
      - テストの十分性を判断する（正常系・異常系・境界条件）
    - セキュリティ — `/security-review` で修正が新たな脆弱性を生んでいないか確認する
      - `/security-review` を実施する
      - `CLAUDE.md` にバグ修正で得た知見（稼働時間計算の仕様）を追記する
  - 公式ドキュメント: [Security](https://code.claude.com/docs/en/security), [Best Practices](https://code.claude.com/docs/en/best-practices)

- **3-2-3 追加バグの修正（実践）**
  - ゴール: 別のバグを自力で（Claude Code と協働して）原因特定から検証まで遂行できる
  - 記述パターン: 混合
  - Subsection:
    - 自力でのバグ修正 — 原因特定→修正→検証を一気通貫で実施する
      - バグ報告:「他社の非公開案件が検索結果に表示される」（認可の漏れ）
      - `/effort` でモデルの effort level を調整し、調査効率を比較する
      - 自力で原因特定→修正→コードレビュー→テスト→セキュリティチェックを実施
    - 見極める力の重点: セキュリティ — Policy・Scope の認可設計を自分で確認する
      - 認可ロジック（Policy, Scope）の設計意図を理解する
      - 修正が他のロールに影響しないことを確認する
  - 公式ドキュメント: [Permissions](https://code.claude.com/docs/en/permissions)

### Chapter 3-3 機能開発（3セクション）

**ゴール**: 新機能の要件を Claude Code に伝え、設計から実装・検証までを協働して遂行し、Part 2 で学んだ機能を総合的に活用できる。

> Part 2 の実践: Plan Mode（2-4-2）, Hooks（2-6-2）, Skills（2-5-1）, セッション管理（2-3-3）, テスト（2-6-1）, 段階的指示（2-5-2）
> 見極める力の重点: **コードレビュー**（既存設計との整合性）

- **3-3-1 要件の整理と設計**
  - ゴール: 機能要件を Claude Code に伝え、Plan Mode で実装計画を立てられる
  - 記述パターン: 混合
  - Subsection:
    - 要件の整理 — 機能要件を Claude Code に伝える
      - 機能要件:「案件のステータス変更時に、関係者（エンジニア・エージェント）にメール通知を送る」
      - セッションに名前を付けて管理する（`--name "feature/notification"`）
    - 設計 — Plan Mode で実装計画を作成する
      - Plan Mode で実装計画を作成する
      - 見極める力の重点: コードレビュー — 計画が既存コードの設計パターンと整合しているかを確認する（Event/Listener vs Observer、既存の通知実装との一貫性）
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows), [Best Practices](https://code.claude.com/docs/en/best-practices)

- **3-3-2 実装と検証**
  - ゴール: 計画に沿って段階的に実装し、Hooks と Skills を活用して品質を自動担保できる
  - 記述パターン: 混合
  - Subsection:
    - 段階的な実装 — 計画に沿って段階的に指示する
      - 段階的指示で実装する（Event / Listener → Notification / Mailable → Queue 連携）
      - Hooks を活用する（ファイル編集後に php-cs-fixer を自動実行）
      - Skills を活用する（通知テンプレート生成を Skill 化）
    - 検証 — 3つの観点で検証する
      - コードレビュー: 生成コードが既存の設計パターンに合っているかを確認する
      - テスト: Feature テストを作成し、通知の送信・Queue の処理を検証する
      - セキュリティ: 通知内容に機密情報が含まれていないか、送信先が正しいかを確認する
  - 公式ドキュメント: [Skills](https://code.claude.com/docs/en/skills), [Hooks](https://code.claude.com/docs/en/hooks)

- **3-3-3 追加機能開発（実践）**
  - ゴール: 別の機能を自力で（Claude Code と協働して）要件整理から検証まで遂行できる
  - 記述パターン: 混合
  - Subsection:
    - 自力での機能開発 — 要件整理→設計→実装→検証を一気通貫で実施する
      - 機能候補の例:「エンジニアのスキルマッチング度を案件一覧に表示する」
      - 自力で Plan Mode → 段階的実装 → コードレビュー → テスト → セキュリティチェックを実施
    - 見極める力の重点: コードレビュー — 既存設計との整合性を自分で判断する
      - 新規コードが既存の命名規則・レイヤー構造・エラーハンドリングパターンと合っているか
      - Claude が生成したコードの設計意図を自分の言葉で説明できるか
  - 公式ドキュメント: [Best Practices](https://code.claude.com/docs/en/best-practices)

### Chapter 3-4 リファクタリング（3セクション）

**ゴール**: Claude Code を使って既存コードの品質を改善し、Worktree で並列作業を行い、変更前後で動作が変わらないことを検証できる。

> Part 2 の実践: Worktree（2-7-3）, Plan Mode（2-4-2）, Fast Mode（2-10-1）, `/cost`（2-10-1）, テスト（2-6-1）
> 見極める力の重点: **テスト**（リファクタリング前後の動作不変保証）

- **3-4-1 Fat Controller のリファクタリング**
  - ゴール: Fat Controller を Service 層 + Form Request に分離できる
  - 記述パターン: 混合
  - Subsection:
    - 分離計画の作成 — Plan Mode で Fat Controller の分離計画を作成する
      - 対象: ApplicationController@store（200行超の応募処理）
      - Plan Mode で分離計画を作成する
    - 段階的な分離 — Claude Code に段階的に分離を依頼する
      - Claude Code に段階的に分離を依頼する
      - 見極める力の重点: テスト — 既存テストが通ることを確認し、不足分を追加する
    - 検証 — 3つの観点で検証する
      - コードレビュー: 分離後のコードが責務分離の原則に沿っているかを確認する
      - テスト: 既存テストが通ることを確認し、不足分を追加する
      - セキュリティ: リファクタリングで認可ロジックの動作が変わっていないかを確認する
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **3-4-2 N+1 クエリの解消と並列作業**
  - ゴール: N+1 問題を特定・解消し、Worktree を使った並列リファクタリングを体験できる
  - 記述パターン: 混合
  - Subsection:
    - N+1 問題の特定 — Claude Code に N+1 問題を探させ、指摘が正しいかを自分で確認する
      - Claude Code に「N+1 問題を探して」と依頼する
      - 見極める力: 指摘が正しいかを自分で確認する（`barryvdh/laravel-debugbar` 等）
    - Worktree で並列リファクタリング — 複数の N+1 修正を Worktree で並列に進める
      - Worktree で複数の N+1 修正を並列に進める（Part 2 の復習）
      - `/cost` で大規模リファクタリングのコスト消費を確認する
      - Fast Mode を試し、トレードオフを体感する
    - 検証 — 正しさ・品質・安全性の検証を行う
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows), [Costs](https://code.claude.com/docs/en/costs)

- **3-4-3 追加リファクタリング（実践）**
  - ゴール: 別のリファクタリングを自力で（Claude Code と協働して）計画から検証まで遂行できる
  - 記述パターン: 混合
  - Subsection:
    - 自力でのリファクタリング — 対象の特定から検証まで一気通貫で実施する
      - 対象を自分で特定する（Claude Code に「改善すべき箇所を提案して」と依頼）
      - 見極める力: 提案の妥当性を自分で判断する（本当に改善すべきか、優先度は適切か）
      - 自力で計画→実装→コードレビュー→テスト→セキュリティチェックを実施
  - 公式ドキュメント: [Best Practices](https://code.claude.com/docs/en/best-practices)

### Chapter 3-5 チーム開発（3セクション）

**ゴール**: Claude Code をチーム開発のワークフロー（PR・レビュー・CI/CD・共有設定）に組み込み、3タスクをチーム文脈で統合実践できる。

> 新たに導入する機能: GitHub Actions（`/install-github-app`、`@claude`）, Code Review 自動化
> Part 2 の実践: `/commit`（2-7-1）, `/diff`（2-7-1）, PR 作成（2-10-3）, `/pr-comments`（2-10-3）, attribution（2-10-3）, 権限管理（2-9-1）, `.claude/settings.json`（2-9-1）, CLAUDE.md 共有（2-2-1）

- **3-5-1 PR 作成とレビュー対応**
  - ゴール: Claude Code で PR を作成し、レビュー指摘に対応できる
  - 記述パターン: 混合
  - Subsection:
    - PR の作成 — これまでの変更をブランチにまとめ、PR を作成する
      - これまでの変更をブランチにまとめる（`/commit`, `/diff` の活用）
      - PR を作成し、attribution（`Co-Authored-By`）を設定する
    - レビュー対応 — レビュー指摘を取得し、Claude Code と協働して対応する
      - `/pr-comments` でレビュー指摘を取得し対応する
    - 検証 — 3つの観点で自分の変更を検証する
      - コードレビュー: 自分の変更を第三者視点でレビューする習慣
      - テスト: CI で全テストが通ることを確認する
      - セキュリティ: `.env` や認証情報がコミットに含まれていないことを確認する
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **3-5-2 GitHub Actions による Code Review 自動化**
  - ゴール: Claude Code GitHub Actions の仕組みを理解し、自動レビューのワークフローを把握できる
  - 記述パターン: 混合
  - Subsection:
    - GitHub Actions の概要 — Claude Code GitHub Actions の仕組みと課金体系を理解する
      - API キーの作成と課金体系の理解（💡 Pro プラン単体では実行不可。仕組みの理解とデモに重点）
      - `/install-github-app` によるセットアップ手順
    - 自動レビューのワークフロー — `@claude` メンションと自動レビュー設定を把握する
      - `@claude` メンションの使い方
      - 自動レビューのワークフロー設定
      - `CLAUDE.md` との連携（レビュー基準の共有）
  - 公式ドキュメント: [GitHub Actions](https://code.claude.com/docs/en/github-actions), [Code Review](https://code.claude.com/docs/en/code-review)

- **3-5-3 チーム設定と CLAUDE.md の共有運用**
  - ゴール: チーム開発での権限管理と `CLAUDE.md` 運用方針を整備できる
  - 記述パターン: 混合
  - Subsection:
    - チーム設定 — `.claude/settings.json` をチームで共有する
      - `.claude/settings.json` のチーム共有設定（権限ルール、deny 設定）
      - 設定の5レベル階層の復習（Managed > CLI引数 > Local > Project > User）
      - Managed settings と企業ポリシーへの対応（データプライバシー）
    - CLAUDE.md のチーム運用 — チームで CLAUDE.md を効果的に運用する
      - `CLAUDE.md` のチーム運用ルール（何を書くか、レビュー方針）
      - 自動メモリ機能と CLAUDE.md の使い分け
    - 見極める力: 説明責任 — 自分の変更を説明できる状態を保つ
      - 正しさ・品質・安全性をチーム全体のルールとして定着させる
      - AI 出力に対する説明責任の重要性
  - 公式ドキュメント: [Settings](https://code.claude.com/docs/en/settings), [Memory](https://code.claude.com/docs/en/memory), [Data Usage](https://code.claude.com/docs/en/data-usage)

---

## Part 2 機能カバレッジ

Part 2 で学んだ機能が Part 3 のどこで再利用されるかのマッピング。

| Part 2 機能 | 3-1 読解 | 3-2 バグ修正 | 3-3 機能開発 | 3-4 リファクタ | 3-5 チーム |
|---|---|---|---|---|---|
| 基本操作・プロンプト入力 | ○ | ○ | ○ | ○ | ○ |
| CLAUDE.md（読む・更新する） | ◎ | ○ | | | ◎ |
| コンテキスト管理（`/compact`, `/context`） | ◎ | | | | |
| セッション管理（`--name`） | | | ◎ | | |
| `/btw` | ◎ | | | | |
| プロンプト設計 | | ◎ | ◎ | ◎ | |
| Plan Mode | | | ◎ | ◎ | |
| Skills | | | ◎ | | |
| テスト作成・実行 | | ◎ | ◎ | ◎ | ○ |
| Hooks | | | ◎ | ○ | |
| Git（`/commit`, `/diff`） | | | | | ◎ |
| Checkpointing・`/rewind` | | ◎ | | | |
| Worktree | | | | ◎ | |
| MCP | ◎ | ○ | | | |
| Sub-agents | ◎ | | ○ | | |
| 権限管理 | | | | | ◎ |
| `/security-review` | | ◎ | ○ | ○ | |
| モデル選択・`/effort` | | ○ | | ○ | |
| Fast Mode | | | | ◎ | |
| `/cost` | | | | ◎ | |
| PR・`/pr-comments`・attribution | | | | | ◎ |
| 自動メモリ | ○ | | | | ○ |

◎ = その Chapter の中心的な活用、○ = 補助的に使用

### カバレッジ分析

- **Part 2 の主要機能の約 85% が Part 3 で再登場**する
- カバーされない機能（`/doctor`, `/login`, `/init`, `/fork`, `/config`, Plugins, Bundled skills, Claude API）はセットアップ系・任意系であり、実務タスクで繰り返す性質のものではない
