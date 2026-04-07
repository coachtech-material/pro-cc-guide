# Part 3: Claude Code の実践

> 能力: 見極める力（主）+ 使いこなす力（総合演習）
> ゴール: 提供プロジェクトで実務タスク（バグ修正・機能開発・リファクタリング）を Claude Code と協働して遂行し、AI 出力を自ら検証・判断する力を鍛える
> ハンズオン: 提供プロジェクト CourseHub を使い、概念 + 混合パターンで実践

### 実践の方針

- 全 Chapter は概念 Section（方法論）+ 混合 Section（実践）の2 Section で構成する（3-1 は概念 + 混合 + 混合、3-2 は概念 + 概念 + 混合の 3 Section）
- 概念 Section: その Chapter に共通する方法論（Why・What）を教える。提供プロジェクトに依存しない
- 混合 Section: 🏃 実践パートで提供プロジェクトを使って手を動かす。MECE カテゴリに沿って複数の実践を1 Section 内で段階的に進める
- Part 2 で学んだ機能を実務コンテキストで活用する。各🏃 実践に使用する Part 2 機能を明記
- 見極めチェック（正しさ・品質・安全性）を Chapter ごとに重点を変え、各タスクの検証フェーズとして統合する
- 教材で扱うタスクは必要最低限。教材を終えた後、提供プロジェクトで自由に取り組むことを推奨
- Claude Code が実務タスクをどれだけ効率化するかの「驚き」と、自分で判断・検証する「面白さ」を体験として届ける

### 執筆メモ

**リサーチ**: `方法論:` フィールドに記載されたテーマは必ず WebSearch でリサーチしてから書く。リサーチ結果は具体的な手法として咀嚼して書く。以下の3方向でリサーチする:
- 方法論の一般的なベストプラクティス（例: 「bug investigation best practices」「refactoring workflow」）
- Claude Code 固有のベストプラクティス（例: 「Claude Code bug fix workflow」「Claude Code Plan Mode」）
- Laravel 固有の実務プラクティス（例: 「Laravel debugging best practices」「Laravel N+1 detection」「Laravel Policy testing」「Laravel Form Request refactoring」）

**方法論の根拠**（概念 Section の執筆時に活用）:
- 「AI エージェントを正しく使うとはコードレビューのプロセスである」（Sean Goedecke）
- Addy Osmani の「70-30 モデル」: AI はルーティンの 70% を処理、残り 30% に人間の価値が集中
- Anthropic の学習パターン研究: 「生成→理解」は学習効果あり、「丸投げ」は理解度 40% 以下
- シニアは AI で 2.5 倍のコードを出荷（Fastly 調査）。差は問題検出能力
- AI 生成コードの 40% に脆弱性（ksred.com）

**実践パートとコードの整合性**: 🏃 実践で言及する CourseHub のコード（ファイルパス、メソッド名、行の内容）は、サブエージェントで実在を検証してから書く

### 提供プロジェクト

**CourseHub** — オンライン学習プラットフォーム（Laravel 10 + Sail）。詳細は `outline/coursehub-spec.md` を参照。

---

## Chapter 3-1: 実践の準備（3 Section + 地図）

**ゴール**: Claude Code で実務タスクを遂行する考え方を理解し、提供プロジェクトの環境を整えて初動を完了する。

- **3-1-0 Chapter 1 の地図**（Chapter 地図 / 学習者向けの導入ページ）

- **3-1-1 Claude Code で実務タスクを遂行する考え方**
  - 種類: 概念
  - ゴール: Part 2 で学んだ機能を実務で活かすための考え方と、AI 出力を判断する力の重要性を理解する
  - 方法論: 70-30 モデル（人間が担う 30% の価値）、「AI エージェントの活用 = コードレビュー」という考え方、AI 生成コードの検証が必要な理由（脆弱性リスク、設計判断、説明責任）、Part 3 の全体像
  - 公式ドキュメント: [Best Practices](https://code.claude.com/docs/en/best-practices)

- **3-1-2 セットアップと動作確認**
  - 種類: 混合
  - ゴール: リポジトリのクローンから Sail 起動・動作確認までを完了する
  - 🏃 実践: CourseHub をクローンし、Sail で起動して動作確認する
  - 意図: README のズレに気づき、Claude Code で正しい手順を特定する体験を含む
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **3-1-3 プロジェクトの規約・設定を確認する**
  - 種類: 混合
  - ゴール: 前任チームが残したドキュメントと設定（README のコーディング規約・設計方針、CLAUDE.md、rules、skills、settings.json）を確認し、不足や乖離に気づいて更新できる
  - 🏃 実践: CourseHub のドキュメントと設定を確認・更新する
    - README: コーディング規約と設計方針のセクションを読み、実際のコードとの乖離を確認する（Form Request の不使用箇所、Fat Controller 等）
    - CLAUDE.md: Sail コマンド・コース構造を追記する
    - .claude/rules/: coding.md が README の規約と整合しているか確認し、不足を補う
    - .claude/skills/: test Skill の Sail コマンド修正、lint Skill の動作確認（php-cs-fixer → Laravel Pint に切り替え）
    - .claude/settings.json: Sail・git コマンドの allow 追加
  - 意図: 実務では規約と実態のズレが日常的に存在する。README・rules・実コードの3者を照合し、「何に従うべきか」を判断する体験。以降の Chapter で「規約に従って遂行する」ための基盤を作る
  - 公式ドキュメント: [Memory](https://code.claude.com/docs/en/memory), [Settings](https://code.claude.com/docs/en/settings), [Skills](https://code.claude.com/docs/en/skills)

---

## Chapter 3-2: 既存コードを理解する（3 Section + 地図）

**ゴール**: Claude Code を使ってプロジェクトの全体像と業務フローを把握し、Claude の説明を自分で検証できる。知らない技術に出会っても対処フローに沿って段階的に理解を深められる。コードリーディングは参画時だけでなく、以降の全ての実務タスク（バグ修正・機能開発・リファクタリング）の前提として継続的に行うものであることを理解する。

- **3-2-0 Chapter 2 の地図**（Chapter 地図 / 学習者向けの導入ページ）

- **3-2-1 コードリーディングの方法論**
  - 種類: 概念
  - ゴール: 既存プロジェクトを効率的に理解する方法論と、Claude の説明を検証する力を身につける
  - 方法論: 認知科学に基づく5ステップの方法論（探索→検索→転写→理解→増強）、既存プロジェクトの読み方（全体像→構造→フロー）、Claude Code を使ったコードリーディング（Sub-agents での分割探索、MCP での DB 確認）、Claude の説明を検証する方法（省略・誤り・古い情報の検出）、コードリーディングは参画時の全体理解だけでなく各タスク着手前にも行うこと（タスクに関連するコードを読み、既存の設計パターンと規約を把握してから着手する）
  - 公式ドキュメント: [Best Practices](https://code.claude.com/docs/en/best-practices), [Sub-agents](https://code.claude.com/docs/en/sub-agents)

- **3-2-2 知らない技術への向き合い方**
  - 種類: 概念
  - ゴール: 実務プロジェクトで未知の技術やパターンに出会ったとき、パニックにならず段階的に理解を深める対処フローと心構えを身につける
  - 方法論:
    - **Why（なぜこの力が必要か）**: ジュニアが実務で最初にぶつかる壁は「知らない技術が大量にある」こと。Laravel の基本 MVC を学んでいても、実務プロジェクトには Service クラス、Event/Listener、Observer、Form Request、Policy、Jobs/Queues 等のパターンが使われている。Dan Abramov（Redux 共同作成者）でさえ自分が知らない技術の一覧を公開している（[Things I Don't Know as of 2018](https://overreacted.io/things-i-dont-know-as-of-2018/)）。知らないこと自体は問題ではなく、「知らない技術にどう向き合うか」のプロセスを持つことが重要
    - **What（対処フロー）**: 理解する→評価する→判断する→説明できる の4ステップ。(1) Claude Code に「これは何か」を質問し概要を掴み、公式ドキュメントで裏付ける。(2)「なぜこのプロジェクトでこのパターンが使われているか」を考える（コード上のメリット、使わなかった場合を想像する）。(3)「今の自分に必要な理解の深さ」を見極める（全体像把握なら概要で十分、担当タスクなら深掘り）。(4) 最終ゴールは「これは○○で、○○のために使われている」と自分の言葉で説明できる状態
    - **What（理解の深さの判断基準）**: 深掘りすべきとき（担当タスクに直結する / コアの技術スタックである / セキュリティやパフォーマンスのクリティカルパスにある / 概要だけでは繰り返し混乱する）。概要で十分なとき（今の担当範囲外 / 隣接領域で自分の責務ではない / 必要になったときに公式ドキュメントで補える）。Itamar Turner-Trauring の「5分ルール」: 5分の学習で80%の理解が得られることが多い。残り20%は実際に使うときに深掘りすればよい（[On learning new technologies: why breadth beats depth](https://codewithoutrules.com/2019/03/29/learn-new-technologies/)）
    - **What（心構え: 知らないことは普通）**: Dreyfus モデル（スキルごとに初心者→上級者の段階がある。シニアでも特定技術では初心者）。インポスター症候群への対処（開発者の58%が経験。他のエンジニアの「超能力」に見えるものは、単にそのコードベースへの慣れである場合が多い）。成長マインドセット（「できない」ではなく「まだできない」。Carol Dweck のフレームワーク）。T 字型エンジニア（1つの領域で深い専門性 + 広い領域の実用的な知識。AI 時代にはルーティンな広さを AI が補うため、深さがより重要になる）
    - **How（AI 時代の学び方の注意点）**: AI が「知らない技術」への対処を劇的に加速してくれる一方、「理解せずに使う」リスクも増大する。Anthropic の RCT 研究（2026年1月）では、AI にコード生成を丸投げした開発者の理解度は40%以下、概念的な質問をしながら自分でコードを書いた開発者は65%以上。Addy Osmani の「説明できないコードは受け入れるな」ルール。対処フローのステップ4「説明できる」が最終ゴールである理由はここにある
    - **How（実務で出会う Laravel パターンの地図）**: CourseHub で遭遇するパターン（Service クラス、Event/Listener）を具体例として紹介しつつ、実務でよく見るパターンの全体像を地図として示す。各パターンについて「何をするか」「どんな課題を解決するか」「どんな信号が出たら使うか」を簡潔に整理する。全てを今理解する必要はなく、「こういうものがある」と知っておくことで実際に遭遇したときの心理的負担を下げる
  - 参考文献:
    - Dan Abramov, [Things I Don't Know as of 2018](https://overreacted.io/things-i-dont-know-as-of-2018/)
    - Itamar Turner-Trauring, [On learning new technologies: why breadth beats depth](https://codewithoutrules.com/2019/03/29/learn-new-technologies/)
    - Anthropic, [How AI assistance impacts the formation of coding skills](https://www.anthropic.com/research/AI-assistance-coding-skills)
    - Addy Osmani, [The 70% Problem: Hard truths about AI-assisted coding](https://addyo.substack.com/p/the-70-problem-hard-truths-about)
    - Addy Osmani, [Avoiding Skill Atrophy in the Age of AI](https://addyo.substack.com/p/avoiding-skill-atrophy-in-the-age)
    - Carol Dweck, [Revisits the Growth Mindset](https://www.edweek.org/leadership/opinion-carol-dweck-revisits-the-growth-mindset/2015/09)
    - Samuel Taylor, [new codebase, who dis?](https://www.samueltaylor.org/articles/how-to-learn-a-codebase.html)
    - Brittany Ellich, [How GitHub engineers learn new codebases](https://github.blog/developer-skills/application-development/how-github-engineers-learn-new-codebases/)
    - Built In, [Reading Code Is an Important Skill](https://builtin.com/software-engineering-perspectives/reading-code)
  - 公式ドキュメント: [Best Practices](https://code.claude.com/docs/en/best-practices)

- **3-2-3 CourseHub のコードを読む**
  - 種類: 混合
  - ゴール: プロジェクトの全体像と業務フローを把握し、知らないパターンに対処できる
  - 🏃 実践: CourseHub のコードを読み、理解する
    - 全体像の把握: Sub-agents でディレクトリ構成・モデル関連・ルーティングを探索する。`/context` でコンテキスト消費を確認し、`/compact` で整理する（Sub-agents, MCP, `/context`, `/compact`）
    - 業務フローの追跡: 受講フロー（コース閲覧→受講登録→レッスン完了→小テスト受験）をコードで追い、Claude の説明を実コードで検証する（`/btw`）
    - 知らない技術との遭遇: EnrollmentService や CourseCompleted Event を見つけ、3-2-2 の対処フロー（理解→評価→判断→説明できる）を実践する。Claude Code に「これは何か」「なぜこのパターンか」を質問し、公式ドキュメントで裏付け、理解の深さを判断する
  - 公式ドキュメント: [Sub-agents](https://code.claude.com/docs/en/sub-agents), [MCP](https://code.claude.com/docs/en/mcp)

---

## Chapter 3-3: バグを修正する（2 Section + 地図）

**ゴール**: Claude Code と協働してバグの原因特定から修正・検証までを遂行し、バグの種類に応じた見極めができる。

- **3-3-0 Chapter 3 の地図**（Chapter 地図 / 学習者向けの導入ページ）

> 見極める力の重点: **安全性**（認可の漏れ）

MECE 軸: **バグの影響領域**（データの正しさ / アクセス制御 / 機能不全）

- **3-3-1 バグ修正の方法論**
  - 種類: 概念
  - ゴール: バグ修正の全体フロー（報告→再現→調査→修正→検証）と、Claude Code を活用した各フェーズの進め方を理解する
  - 方法論: バグ報告を受けたらまず関連コードを読む（3-2 で学んだコードリーディングの実践）、バグ報告から技術的な原因仮説を立てる方法、Claude Code への調査指示の組み立て方（症状・再現手順・期待値を伝える）、修正後の影響範囲の検証方法、バグの3類型（データの正しさ・アクセス制御・機能不全）ごとの調査アプローチの違い
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **3-3-2 CourseHub のバグを修正する**
  - 種類: 混合
  - ゴール: 3種類のバグを段階的に自律度を上げながら修正・検証できる
  - 🏃 実践: CourseHub の3つのバグを修正する
    - 進捗率バグ（データの正しさ）: プロンプト設計を意識して調査指示を組み立てる。修正が既存の設計パターンを壊していないか確認する。修正後に `/rewind` で戻れることを確認し、`/test` でテスト実行する（プロンプト設計, `/rewind`, `/test`）
    - 認可バグ（アクセス制御）: Policy の認可設計を確認・修正し、テストを書いて `/test` で検証する。scopePublished が定義されているのに使われていない点を品質の観点で指摘する。修正が rules/coding.md の規約に従っているかも確認する。安全性の見極めを重点的に実践（テスト, `/test`）
    - 500エラー（機能不全）: エラーログを Claude Code に貼って診断させ、より自律的に修正する。`/test` で修正を検証（`/test`）
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows), [Checkpointing](https://code.claude.com/docs/en/checkpointing), [Security](https://code.claude.com/docs/en/security)

---

## Chapter 3-4: 機能を開発する（2 Section + 地図）

**ゴール**: 既存機能への追加と新規機能の開発を Claude Code と協働して遂行し、既存設計との整合性を自分で判断できる。

- **3-4-0 Chapter 4 の地図**（Chapter 地図 / 学習者向けの導入ページ）

> 見極める力の重点: **品質**（既存設計との整合性）

MECE 軸: **変更のスコープ**（既存機能の拡張 / 新規機能の構築）

- **3-4-1 機能開発の方法論**
  - 種類: 概念
  - ゴール: 機能開発の全体フロー（要件理解→設計→実装→検証）と、Claude Code を活用した各フェーズの進め方を理解する
  - 方法論: 着手前に関連する既存コードを読み設計パターンとコーディング規約（rules）を把握する（3-2 で学んだコードリーディングの実践）、要件をタスクに分解する方法、既存パターンを指示に含める方法、AI の設計提案の妥当性を判断する基準（70-30 モデル）、拡張と新規構築のアプローチの違い
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows), [Best Practices](https://code.claude.com/docs/en/best-practices)

- **3-4-2 CourseHub に機能を追加する**
  - 種類: 混合
  - ゴール: 既存機能の拡張と新規機能の構築を、既存設計との整合性を検証しながら遂行できる
  - 🏃 実践: CourseHub に2つの機能を開発する
    - 小テスト再受験機能（既存機能の拡張）: 既存の Quiz・Submission フローを読み取り、rules/coding.md のコーディング規約と既存パターンに従って拡張する。セッションに名前を付け、`--continue` で途中再開する体験を含む（セッション管理）
    - コースレビュー機能（新規機能の構築）: Plan Mode で設計し、段階的に実装・検証する。Review モデルを新規作成。CourseHub 用に Hooks を新たに設定し（Laravel Pint による自動フォーマット）、実装後に `/simplify` で品質チェック、`/test` でテスト実行（Plan Mode, Hooks, `/simplify`, `/test`）
  - 公式ドキュメント: [Hooks](https://code.claude.com/docs/en/hooks), [Common Workflows](https://code.claude.com/docs/en/common-workflows)

---

## Chapter 3-5: コードを改善する（2 Section + 地図）

**ゴール**: Claude Code を使って既存コードの品質を改善し、変更前後で動作が変わらないことをテストで保証できる。

- **3-5-0 Chapter 5 の地図**（Chapter 地図 / 学習者向けの導入ページ）

> 見極める力の重点: **正しさ**（動作不変の保証）

MECE 軸: **改善対象**（コード構造 / パフォーマンス）

- **3-5-1 リファクタリングの方法論**
  - 種類: 概念
  - ゴール: リファクタリングの全体フロー（対象特定→テスト確認→改善→テスト再実行）と、Claude Code の改善提案を判断する方法を理解する
  - 方法論: 改善対象のコードを読み現状の設計と問題点を把握する（3-2 で学んだコードリーディングの実践）、改善対象の特定基準、テストによる動作保証の方法、Claude Code の改善提案を評価する基準、構造改善とパフォーマンス改善のアプローチの違い
  - 公式ドキュメント: [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **3-5-2 CourseHub のコードを改善する**
  - 種類: 混合
  - ゴール: コード構造とパフォーマンスを改善し、テストで動作保証できる
  - 🏃 実践: CourseHub の2つの問題を改善する
    - Fat Controller の責務分離（コード構造）: CourseController@store を Form Request 抽出 + private メソッド分割でリファクタリングする。リファクタリング後のコードが rules/coding.md の規約に準拠しているか確認する。各ステップで `/test` を実行して動作保証する。Claude Code が Service 層を提案した場合は 3-2-2 で学んだ「知らない技術への向き合い方」を実践する（Plan Mode, `/test`, `/cost`）
    - N+1 クエリの解消（パフォーマンス）: コース一覧（student 側）と生徒一覧（admin 側）の N+1 を Worktree で並列に解消する。`/test` で動作確認、`/context` でコンテキスト使用量を確認しながら進める（Worktree, `/test`, `/cost`, `/context`）
  - 公式ドキュメント: [Worktrees](https://code.claude.com/docs/en/worktrees), [Costs](https://code.claude.com/docs/en/costs)

---

## Chapter 3-6: チームに共有する（2 Section + 地図）

- **3-6-0 Chapter 6 の地図**（Chapter 地図 / 学習者向けの導入ページ）

**ゴール**: AI 生成コードに対する説明責任を理解し、チーム開発での Claude Code 活用の環境を整備できる。

MECE 軸: **共有の対象**（コード / 環境）

- **3-6-1 AI 時代のチーム開発**
  - 種類: 概念
  - ゴール: AI 生成コードをチームに共有する際の説明責任と、AI がチーム開発にもたらす変化を理解する
  - 方法論: 説明責任（コミットした人が全責任を負う。「AI が書いた」は言い訳にならない）、AI でレビューがボトルネックになる問題と対策（AI + 人間の役割分担）、帰属表示（Co-Authored-By の意味とチームでの方針決定）、「このコードを説明できるか」テスト、CLAUDE.md・rules・skills がチームの知識を AI に伝える新しい成果物であること
  - 公式ドキュメント: [Git Integration](https://code.claude.com/docs/en/git-integration), [Common Workflows](https://code.claude.com/docs/en/common-workflows)

- **3-6-2 CourseHub の変更をチームに届ける**
  - 種類: 混合
  - ゴール: 説明責任を意識した PR 作成と、チーム開発の環境整備を遂行できる
  - 🏃 実践: CourseHub での変更をチームに届ける
    - コードの共有（PR）: Part 2（2-3-7）で学んだ手順で PR を作成する。AI 生成コードの説明責任を意識し、「なぜこの修正か」「どう検証したか」を PR 本文に書く（Git `/commit` `/diff`, PR・レビュー）
    - 環境の共有（チーム設定）: GitHub Actions は Part 2（2-3-8）で学んだ手順で設定する。settings.json のチーム共有設定と CLAUDE.md 運用方針を整備する（GitHub Actions, 権限管理, CLAUDE.md）
    - ワークフローの Skill 化: これまでの作業を振り返り、繰り返し使えるワークフロー（コードレビュー手順、バグ調査手順等）を Skill として定義し、チームで共有する（Skills, Plugins）
  - 公式ドキュメント: [GitHub Actions](https://code.claude.com/docs/en/github-actions), [Settings](https://code.claude.com/docs/en/settings), [Memory](https://code.claude.com/docs/en/memory), [Skills](https://code.claude.com/docs/en/skills), [Plugins](https://code.claude.com/docs/en/plugins)

---

## Part 2 機能カバレッジ

| Part 2 機能 | 3-1 準備 | 3-2 理解 | 3-3 バグ修正 | 3-4 機能開発 | 3-5 改善 | 3-6 チーム |
|---|---|---|---|---|---|---|
| 基本操作・プロンプト入力 | ○ | ○ | ○ | ○ | ○ | ○ |
| CLAUDE.md / rules | ◎ | ○ | ○ | ○ | ○ | ◎ |
| コンテキスト管理（`/compact`, `/context`） | | ◎ | | | ○ | |
| セッション管理（`--continue`） | | | | ◎ | | |
| `/btw` | | ◎ | | | | |
| プロンプト設計 | | | ◎ | | | |
| Plan Mode | | | | ◎ | ◎ | |
| `/simplify` | | | | ◎ | | |
| Skills | | | | | | ◎ |
| Hooks | | | | ◎ | | |
| Plugins | | | | | | ○ |
| テスト | | | ◎ | ◎ | ◎ | |
| MCP | | ◎ | | | | |
| Sub-agents | | ◎ | | | | |
| Git（`/commit`, `/diff`） | | | | | | ◎ |
| `/rewind` | | | ◎ | | | |
| Worktree | | | | | ◎ | |
| 権限管理 | | | | | | ◎ |
| `/cost` | | | | | ◎ | |
| PR・レビュー | | | | | | ◎ |
| GitHub Actions | | | | | | ◎ |

◎ = Chapter の中心的な活用、○ = 補助的に使用
