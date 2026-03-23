# Part 3: Claude Code の実践

> 能力: 見極める力（主）+ 使いこなす力（総合演習）
> ゴール: 提供プロジェクトで実務タスク（バグ修正・機能開発・リファクタリング）を Claude Code と協働して遂行し、AI 出力を自ら検証・判断する力を鍛える
> ハンズオン: 提供プロジェクトを使い、全 Section 混合パターンで実践

### 🏃 実践の方針

- 「途中参加のエンジニア」として既存プロジェクトに入り、準備からチーム共有まで一気通貫で体験する
- Part 2 で学んだ機能を実務コンテキストで総合的に使いこなす
- 見極めチェック（正しさ・品質・安全性）を Chapter ごとに重点を変えて実践し、形骸化を防ぐ
- 見極めは独立した Section ではなく、各タスクの検証フェーズとして統合する
- 各 Chapter は原則 2 Section 構成（3-3 のみ MECE 3カテゴリのため 3 Section）。Section が進むにつれ自律度を上げる
- この教材で扱うタスクは必要最低限の体験。教材を終えた後、提供プロジェクトで自由に機能追加やリファクタリングに取り組むことを推奨する

### 提供プロジェクト概要

**CoaKoza**（コアコザ）— オンライン学習プラットフォーム。コーチがコースを作成し、受講生が受講・進捗管理する構成。Pro生自身が COACHTECH の学習プラットフォームを利用しており、ドメイン理解コストが低い。

- 技術スタック: Laravel 10 + Sail + Blade + Tailwind CSS（一部 API エンドポイントあり）
- 規模: 初期13モデル（User, Course, Chapter, Lesson, Quiz, Question, Option, Enrollment, LessonProgress, Submission, Category, Tag, CourseTag）
- コース構造: Course → Chapter → Lesson → Quiz（3層 + 小テスト）
- ユーザーロール: admin（管理者）、coach（コーチ）、student（受講生）
- 想定シナリオ: 初期開発チーム（2〜3名）が退職し、Pro生が途中参加のエンジニアとして加わる
- 提供状態: Docker Compose で即起動、Seeder でダミーデータ投入済み
- CLAUDE.md は存在するが不完全（前任チームが書いたもの）、`.claude/settings.json` は基本的な allow ルールのみ

詳細設計は `outline/coakoza-spec.md` を参照。

---

## Chapter 3-1: 開発環境の準備（2 Section）

**ゴール**: リポジトリをクローンして開発環境を起動し、既存の CLAUDE.md を確認・更新してプロジェクトの初動を完了する。

意図: Part 3 の導入。教材で扱うタスクは必要最低限であること、教材を終えた後に自由に機能追加などに取り組んでほしいことを伝える

- **3-1-1 セットアップと動作確認**
  - 種類: 混合
  - ゴール: リポジトリのクローンから Docker Compose 起動・動作確認までを完了する
  - 意図: README のズレに気づき、Claude Code で正しい手順を特定する体験を含む
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **3-1-2 CLAUDE.md の確認と更新**
  - 種類: 混合
  - ゴール: 前任チームの CLAUDE.md を読み、不足や古い情報に気づき、自分で更新できる
  - 意図: Part 2 で学んだ CLAUDE.md の設計原則を既存プロジェクトに適用する
  - 公式ドキュメント: [Memory](https://code.claude.com/docs/en/memory)

---

## Chapter 3-2: 既存コードを理解する（2 Section）

**ゴール**: Claude Code を使ってプロジェクトの全体像と業務フローを把握し、Claude の説明を自分で検証できる。

> Part 2 の実践: Sub-agents, MCP, コンテキスト管理（`/compact`, `/context`）, `/btw`, CLAUDE.md

- **3-2-1 プロジェクトの全体像を把握する**
  - 種類: 混合
  - ゴール: Sub-agents と MCP を活用して、ディレクトリ構成・モデル関連・ルーティングの全体像を効率的に把握できる
  - 公式ドキュメント: [Sub-agents](https://code.claude.com/docs/en/sub-agents), [MCP](https://code.claude.com/docs/en/mcp)

- **3-2-2 業務フローをコードで追う**
  - 種類: 混合
  - ゴール: コース作成〜受講〜進捗管理の業務フローをコードレベルで追跡し、Claude の説明を自分で検証できる
  - 意図: Claude の説明に省略や誤りがある可能性に気づき、自分でコードを確認する習慣を作る
  - 公式ドキュメント: [Best Practices](https://code.claude.com/docs/en/best-practices)

---

## Chapter 3-3: バグを修正する（3 Section）

**ゴール**: Claude Code と協働してバグの原因特定から修正・検証までを遂行し、バグの種類に応じた見極めができる。

> 見極める力の重点: **安全性**（認可の漏れ）
> Part 2 の実践: プロンプト設計, `/rewind`, テスト, `/effort`

MECE 軸: **バグの影響領域**（ユーザー視点の症状で分類）

- **3-3-1 データの正しさに関わるバグの修正**
  - 種類: 混合
  - ゴール: バグ報告から Claude Code で原因を特定し、修正・検証できる
  - タスク: 進捗率の計算が実際と合わない（非公開レッスンが総数に含まれている等のクエリ不備）
  - 意図: ガイド付きでバグ修正の一連の流れ（報告→原因特定→修正→検証）を体験する
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows), [Checkpointing](https://code.claude.com/docs/en/checkpointing)

- **3-3-2 アクセス制御に関わるバグの修正**
  - 種類: 混合
  - ゴール: 認可に関わるバグを原因特定から検証まで、より自律的に遂行できる
  - タスク: 非公開コースに受講生が直接 URL でアクセスできる（Policy のステータスチェック漏れ）
  - 意図: 安全性の見極めを重点的に実践する。3-3-1 より自律度を上げる
  - 公式ドキュメント: [Security](https://code.claude.com/docs/en/security), [Best Practices](https://code.claude.com/docs/en/best-practices)

- **3-3-3 機能不全に関わるバグの修正**
  - 種類: 混合
  - ゴール: エラーで動作しないバグを、エラーログとスタックトレースを手がかりに自力で修正できる
  - タスク: 小テストで全問不正解の場合に500エラーが発生する（スコア計算処理の例外未ハンドル）
  - 意図: 3-3-1, 3-3-2 よりさらに自律度を上げる。エラーログの読み方と Claude Code による診断を実践する
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows)

---

## Chapter 3-4: 機能を開発する（2 Section）

**ゴール**: 既存機能への追加と新規機能の開発を Claude Code と協働して遂行し、既存設計との整合性を自分で判断できる。

> 見極める力の重点: **品質**（既存設計との整合性）
> Part 2 の実践: Plan Mode, Hooks, Skills, セッション管理, テスト

MECE 軸: **変更のスコープ**

- **3-4-1 既存機能への追加開発**
  - 種類: 混合
  - ゴール: 既存の設計パターンに沿って機能を追加し、整合性を検証できる
  - タスク: 小テスト再受験機能（不合格時に再受験できるようにする。既存の Quiz・Submission モデルとコントローラを修正）
  - 意図: 既存の小テストフローを読み取り、既存パターンに従って拡張する体験。新規モデルは作らない
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows), [Best Practices](https://code.claude.com/docs/en/best-practices)

- **3-4-2 新規機能の開発**
  - 種類: 混合
  - ゴール: Plan Mode で設計し、段階的に実装・検証できる
  - タスク: コースレビュー機能（受講完了した受講生がコースを評価・コメントできる。Review モデルを新規作成）
  - 意図: Model〜Test まで一連の新規作成を Plan Mode で設計してから実装する体験
  - 公式ドキュメント: [Skills](https://code.claude.com/docs/en/skills), [Hooks](https://code.claude.com/docs/en/hooks)

---

## Chapter 3-5: コードを改善する（2 Section）

**ゴール**: Claude Code を使って既存コードの品質を改善し、変更前後で動作が変わらないことをテストで保証できる。

> 見極める力の重点: **正しさ**（動作不変の保証）
> Part 2 の実践: Worktree, Fast Mode, `/cost`, Plan Mode, テスト

MECE 軸: **改善対象**

- **3-5-1 コード構造のリファクタリング**
  - 種類: 混合
  - ゴール: Fat Controller の責務を分離し、テストで動作保証できる
  - タスク: CourseController@store の責務分離（バリデーション → Form Request、処理の分割 → private メソッド）
  - 意図: Pro生の前提知識の範囲でリファクタリングする。Claude Code が未知のパターン（Service 層等）を提案した場合の向き合い方はコラムで扱う
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **3-5-2 パフォーマンスの改善**
  - 種類: 混合
  - ゴール: N+1 問題を特定・解消し、Worktree を使った並列リファクタリングを体験できる
  - タスク: コース一覧（student 側）と生徒一覧（admin 側）の N+1 を Worktree で並列に解消する
  - 公式ドキュメント: [Worktrees](https://code.claude.com/docs/en/worktrees), [Costs](https://code.claude.com/docs/en/costs)

---

## Chapter 3-6: チームに共有する（2 Section）

**ゴール**: Claude Code をチーム開発のワークフローに組み込み、PR・レビュー・CI/CD・共有設定を整備できる。

> Part 2 の実践: Git（`/commit`, `/diff`）, PR, GitHub Actions, 権限管理, CLAUDE.md

MECE 軸: **共有のスコープ**

- **3-6-1 PR 作成とレビュー対応**
  - 種類: 混合
  - ゴール: Claude Code で PR を作成し、レビュー指摘に対応できる
  - 公式ドキュメント: [Git Integration](https://code.claude.com/docs/en/git-integration), [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **3-6-2 チーム開発の環境整備**
  - 種類: 混合
  - ゴール: GitHub Actions による自動化、チーム設定、CLAUDE.md の運用方針を整備できる
  - 公式ドキュメント: [GitHub Actions](https://code.claude.com/docs/en/github-actions), [Settings](https://code.claude.com/docs/en/settings), [Memory](https://code.claude.com/docs/en/memory)

---

## Part 2 機能カバレッジ

| Part 2 機能 | 3-1 準備 | 3-2 理解 | 3-3 バグ修正 | 3-4 機能開発 | 3-5 改善 | 3-6 チーム |
|---|---|---|---|---|---|---|
| 基本操作・プロンプト入力 | ○ | ○ | ○ | ○ | ○ | ○ |
| CLAUDE.md | ◎ | ○ | ○ | | | ◎ |
| コンテキスト管理 | | ◎ | | | | |
| セッション管理 | | | | ◎ | | |
| `/btw` | | ◎ | | | | |
| プロンプト設計 | | | ◎ | ◎ | ◎ | |
| Plan Mode | | | | ◎ | ◎ | |
| Skills | | | | ◎ | | |
| Hooks | | | | ◎ | | |
| テスト | | | ◎ | ◎ | ◎ | ○ |
| MCP | | ◎ | | | | |
| Sub-agents | | ◎ | | ○ | | |
| Git（`/commit`, `/diff`） | | | | | | ◎ |
| `/rewind` | | | ◎ | | | |
| Worktree | | | | | ◎ | |
| 権限管理 | | | | | | ◎ |
| モデル選択・`/effort` | | | ○ | | ○ | |
| Fast Mode | | | | | ◎ | |
| `/cost` | | | | | ◎ | |
| PR・レビュー | | | | | | ◎ |
| GitHub Actions | | | | | | ◎ |

◎ = Chapter の中心的な活用、○ = 補助的に使用
