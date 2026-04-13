# 2-3-0 Chapter 3 の地図

> Claude Code の真価は、個々の機能を組み合わせて実務タスクを遂行できる点にあります。この Chapter では、Claude Code の主要機能を1つずつ学び、それぞれの「なぜ必要か」「何ができるか」「どう使うか」を理解します。各セクションで概念を学んだら、cc-practice で実際に手を動かし、機能を一通り使い切ります。

## セクション一覧

| # | セクション | 学び方 | 概要 |
|---|---|---|---|
| 2-3-1 | Plan Mode | 🏃 実践 | 計画と実装を分離する意義、Shift+Tab での切り替え、効果が高い場面 |
| 2-3-2 | Skills | 🏃 実践 | `SKILL.md` の構造、配置場所によるスコープ、`$ARGUMENTS` と動的コンテキスト注入 |
| 2-3-3 | Hooks | 🏃 実践 | ライフサイクルイベントの使い分け、`settings.json` での定義、終了コードによるブロック制御 |
| 2-3-4 | MCP | 🏃 実践 | MCP の役割と接続タイプ、`claude mcp add` と `.mcp.json`、公開 MCP サーバーの使いどころ |
| 2-3-5 | Sub-agents | 🏃 実践 | ビルトイン Sub-agents、カスタム Sub-agent の定義、`mcpServers` と `maxTurns` |
| 2-3-6 | Plugins | 🏃 実践 | `plugin.json` マニフェスト、公式マーケットプレイスからの `/plugin install`、ローカル作成と再読み込み |
| 2-3-7 | Git と Worktree | 🏃 実践 | 自然言語での Git 操作、チェックポイントと `/rewind`、Worktree による並列開発 |
| 2-3-8 | GitHub Actions | 🏃 実践 | `claude-code-action` と Anthropic API、`.github/workflows/claude.yml`、Secrets での API キー管理 |

## 📖 この Chapter の進め方

8つのセクションすべてが実践型です。各セクションで機能の概念を学び、すぐに cc-practice で実践します。Part 3 に入る前の唯一の機能実践なので、各実践では機能を「小さいけど一通り使い切る」レベルで体験します。

実践は2つの軸で進みます。**日報管理機能の開発**（Plan Mode で画面を設計、Git で変更を管理、Blade でページを改善）と、**Claude Code 自体のカスタマイズ**（Skills、Hooks、MCP、Sub-agents、Plugins、GitHub Actions の設定）です。どちらの成果物も cc-practice に蓄積されていくので、上から順に進めてください。

> 📝 この Chapter の各機能は、すべて必須ではありません。 Claude Code は Chapter 2-1〜2-2 で学んだ基本操作だけでも十分に活用できます。この Chapter で紹介する機能（Plan Mode、Skills、Hooks、MCP、Sub-agents、Plugins、Git 連携、GitHub Actions）は、Claude Code をさらに効率的に使いこなすための**任意の拡張機能** です。すべてを一度に覚える必要はなく、実務で必要になったときに該当するセクションに戻って活用してください。
