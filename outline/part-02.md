# Part 2: Claude Code の基礎

→ 能力: 使いこなす力（主）+ 見極める力（型の導入）
→ ゴール: Claude Code の主要機能を習得し、AI 出力を確認する習慣の土台を作る
→ ハンズオン: Chapter 1 で自分のプロジェクトを作成、Chapter 2 は座学、Chapter 3 はスターターキットで各機能を実践

---

## Chapter 2-1: セットアップ（4 Section）

**ゴール**: Claude Code をインストールし、プロジェクトの土台を作り、最初のコード生成を体験する。

意図: 各 Section で概念を学びながらすぐに手を動かす混合パターン。セットアップの性質上「学ぶ→やる」を順次進める

- **2-1-1 インストールと認証**
  - 種類: 混合
  - ゴール: Claude Code をインストール・認証し、最初のコード生成を体験する
  - 公式ドキュメント: [Setup](https://code.claude.com/docs/en/setup), [Interactive Mode](https://code.claude.com/docs/en/interactive-mode)

- **2-1-2 権限とセキュリティ**
  - 種類: 混合
  - ゴール: Claude Code の権限モデルを理解し、安全に使うための設定を行う
  - 意図: 権限ダイアログは初回起動で即遭遇するため早期に教える
  - 公式ドキュメント: [Permissions](https://code.claude.com/docs/en/permissions), [Settings](https://code.claude.com/docs/en/settings), [Security](https://code.claude.com/docs/en/security)

- **2-1-3 モデル選択とコスト管理**
  - 種類: 混合
  - ゴール: タスクに応じたモデル選択とコスト管理の方法を理解する
  - 公式ドキュメント: [Model Configuration](https://code.claude.com/docs/en/model-config), [Costs](https://code.claude.com/docs/en/costs), [Fast Mode](https://code.claude.com/docs/en/fast-mode)

- **2-1-4 CLAUDE.md とプロジェクト作成**
  - 種類: 混合
  - ゴール: CLAUDE.md の設計原則を理解し、プロジェクトの土台を作る
  - 公式ドキュメント: [Memory](https://code.claude.com/docs/en/memory)

---

## Chapter 2-2: 基本を理解する（3 Section）

**ゴール**: Claude Code の動作原理、コンテキスト管理、プロンプト設計を理解し、効果的に使うための土台を作る。

意図: 純粋な座学 Chapter。Chapter 3 で機能を使いこなすための前提知識を固める

- **2-2-1 エージェントループ**
  - 種類: 概念
  - ゴール: Claude Code の動作原理を理解し、ツール実行ログから何が起きているかを読み取れるようになる
  - 公式ドキュメント: [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works)

- **2-2-2 コンテキストとセッション管理**
  - 種類: 概念
  - ゴール: コンテキストの制約を理解し、セッションを効果的に管理する方法を身につける
  - 意図: コンテキスト管理は最重要スキル。ここで強く印象づけ、以降で繰り返し参照する起点にする
  - 公式ドキュメント: [Context Management](https://code.claude.com/docs/en/context-management), [Sessions](https://code.claude.com/docs/en/sessions), [Checkpointing](https://code.claude.com/docs/en/checkpointing)

- **2-2-3 プロンプト設計**
  - 種類: 概念
  - ゴール: Claude Code に的確な指示を出すための設計原則を理解する
  - 公式ドキュメント: [Best Practices](https://code.claude.com/docs/en/best-practices)

---

## Chapter 2-3: 機能を使いこなす（16 Section）

**ゴール**: Claude Code の主要機能をスターターキットで実践し、それぞれの機能を自分のプロジェクトにも適用できるようにする。

### スターターキット

こちらで提供する Laravel プロジェクト。Pro生 は clone して使う。各機能のハンズオンはこのスターターキットに対して行い、機能ごとに独立した体験ができる。

> スターターキットの詳細（モデル構成、初期状態、提供方法）は別途設計する。

- **2-3-1 Plan Mode**
  - 種類: 混合
  - ゴール: 計画と実装を分離する意義と、Plan Mode の使いどころを理解する
  - 🏃 実践: Plan Mode で機能の実装計画を立てて実装する
  - 公式ドキュメント: [Sub-agents - Plan](https://code.claude.com/docs/en/sub-agents#plan)

- **2-3-2 Skills**
  - 種類: 混合
  - ゴール: 再利用可能なカスタムコマンドの仕組みと設計方法を理解する
  - 🏃 実践: Skill を1から作成する
  - 公式ドキュメント: [Skills](https://code.claude.com/docs/en/skills)

- **2-3-3 Hooks**
  - 種類: 混合
  - ゴール: ツール実行のライフサイクルに処理を自動挿入する仕組みを理解する
  - 🏃 実践: Hook を1から設定する
  - 公式ドキュメント: [Hooks Guide](https://code.claude.com/docs/en/hooks-guide), [Hooks Reference](https://code.claude.com/docs/en/hooks)

- **2-3-4 MCP**
  - 種類: 混合
  - ゴール: 外部ツール・サービスに接続して Claude Code の能力を拡張する仕組みを理解する
  - 🏃 実践: MCP サーバーを追加・接続する
  - 公式ドキュメント: [MCP](https://code.claude.com/docs/en/mcp)

- **2-3-5 Sub-agents**
  - 種類: 混合
  - ゴール: コンテキストを分離して探索や検証を委譲する仕組みを理解する
  - 🏃 実践: カスタム Sub-agent を定義する
  - 公式ドキュメント: [Sub-agents](https://code.claude.com/docs/en/sub-agents)

- **2-3-6 Plugins**
  - 種類: 混合
  - ゴール: 拡張機能をパッケージ化して共有する仕組みを理解する
  - 🏃 実践: 公式マーケットプレイスから Plugin をインストールし、`/skill-creator` で Plugin を作成する
  - 公式ドキュメント: [Plugins](https://code.claude.com/docs/en/plugins), [Discover Plugins](https://code.claude.com/docs/en/discover-plugins)

- **2-3-7 Git と Worktree**
  - 種類: 混合
  - ゴール: Claude Code の Git 連携と並列開発の仕組みを理解する
  - 🏃 実践: チェックポイントからの Rewind を体験し、Worktree で並列作業する
  - 公式ドキュメント: [Git Integration](https://code.claude.com/docs/en/git-integration), [Checkpointing](https://code.claude.com/docs/en/checkpointing), [Worktrees](https://code.claude.com/docs/en/worktrees)

- **2-3-8 GitHub Actions**
  - 種類: 混合
  - ゴール: Claude Code を CI/CD に統合して開発ワークフローを自動化する仕組みを理解する
  - 🏃 実践: ワークフローファイルを1から作成する
  - 公式ドキュメント: [GitHub Actions](https://code.claude.com/docs/en/github-actions)

- **2-3-9 【ハンズオン】Plan Mode**
  - 種類: ハンズオン
  - ゴール: Plan Mode で計画を立て、計画に沿って機能を実装する体験をする

- **2-3-10 【ハンズオン】Skills**
  - 種類: ハンズオン
  - ゴール: カスタム Skill を設計・作成し、実際のタスクに適用する

- **2-3-11 【ハンズオン】Hooks**
  - 種類: ハンズオン
  - ゴール: Hook を設定し、ツール実行に連動して自動処理が走ることを体験する

- **2-3-12 【ハンズオン】MCP**
  - 種類: ハンズオン
  - ゴール: MCP サーバーを追加し、外部ツール経由で情報を取得・活用する

- **2-3-13 【ハンズオン】Sub-agents**
  - 種類: ハンズオン
  - ゴール: Sub-agents にコードベースの探索や検証を委譲し、結果を活用する

- **2-3-14 【ハンズオン】Plugins**
  - 種類: ハンズオン
  - ゴール: 作成した Skills と Hooks を Plugin としてパッケージ化する

- **2-3-15 【ハンズオン】Git と Worktree**
  - 種類: ハンズオン
  - ゴール: Git 連携で変更を管理し、Worktree で並列開発を実践する

- **2-3-16 【ハンズオン】GitHub Actions**
  - 種類: ハンズオン
  - ゴール: GitHub Actions で PR 自動レビューを設定し、CI/CD を体験する
