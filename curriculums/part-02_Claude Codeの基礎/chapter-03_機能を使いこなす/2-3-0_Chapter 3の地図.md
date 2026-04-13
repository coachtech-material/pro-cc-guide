# 2-3-0 Chapter 3 の地図

> Claude Code の真価は、個々の機能を組み合わせて実務タスクを遂行できる点にあります。この Chapter では、Claude Code の主要機能を1つずつ学び、それぞれの「なぜ必要か」「何ができるか」「どう使うか」を理解します。各セクションで概念を学んだら、cc-practice で実際に手を動かし、機能を一通り使い切ります。

## セクション一覧

### 2-3-1 Plan Mode ｜ 📖🏃 読んで手を動かす

- 計画と実装を分離する意義と Plan Mode の読み取り専用モード
- Shift+Tab での切り替えと、調査 → 計画 → 実装の流れ
- 効果が高い場面（複数ファイル変更・設計選択肢検討・大規模リファクタ・初見コードベース）

### 2-3-2 Skills ｜ 📖🏃 読んで手を動かす

- `SKILL.md` の構造（frontmatter と本文）
- 配置場所によるスコープ（プロジェクト用 `.claude/skills/` とユーザー全体 `~/.claude/skills/`）
- `$ARGUMENTS` での引数受け取りと、`` !`<command>` `` での動的コンテキスト注入

### 2-3-3 Hooks ｜ 📖🏃 読んで手を動かす

- ライフサイクルイベント（PreToolUse・PostToolUse・Stop など）の使い分け
- `settings.json` での type・command・matcher の定義方法
- 終了コード 0／2 によるブロック制御と、よくある失敗パターン

### 2-3-4 MCP ｜ 📖🏃 読んで手を動かす

- MCP の役割（ツール提供・リソース提供）と接続タイプ（stdio / http）
- `claude mcp add` コマンドと `.mcp.json` での設定共有
- 公開 MCP サーバー（Playwright・GitHub・Sentry・Slack・Figma）の使いどころ

### 2-3-5 Sub-agents ｜ 📖🏃 読んで手を動かす

- ビルトイン Sub-agents（Explore / Plan / General-purpose）の使い分け
- カスタム Sub-agent の定義（`.claude/agents/<name>.md` の frontmatter と本文）
- `mcpServers` でのスコープ限定と `maxTurns` での暴走防止

### 2-3-6 Plugins ｜ 📖🏃 読んで手を動かす

- `plugin.json` マニフェストと配下のフォルダ構造
- 公式マーケットプレイス（claude-plugins-official）からの `/plugin install`
- ローカル作成 Plugin のテストと `/reload-plugins` での再読み込み

### 2-3-7 Git と Worktree ｜ 📖🏃 読んで手を動かす

- 自然言語での Git 操作と GitHub CLI（`gh`）連携
- チェックポイントと `Esc+Esc` / `/rewind` での巻き戻し
- `claude --worktree <name>` による独立作業ディレクトリで並列開発

### 2-3-8 GitHub Actions ｜ 📖🏃 読んで手を動かす

- `claude-code-action` と Anthropic API（従量課金）の関係
- `.github/workflows/claude.yml` の構造（イベントトリガー・permissions・with パラメータ）
- `--max-turns` でのコスト管理と GitHub Secrets での API キー安全管理

## 📖 この Chapter の進め方

8つのセクションすべてが混合型です。各セクションで機能の概念を学び、すぐに cc-practice で実践します。Part 3 に入る前の唯一の機能実践なので、各実践では機能を「小さいけど一通り使い切る」レベルで体験します。

### 実践は2つの軸で進む

- **A. 日報管理機能の開発**: cc-practice 上に小さな日報アプリを作りながら、Claude Code に「実プロダクト開発」をさせる練習
- **B. Claude Code 自体のカスタマイズ**: Claude Code の振る舞いを設定ファイルで拡張し、自分専用のセットアップを育てる練習

各セクションがどちらの軸に対応するかは下表のとおりです。順番には意味があるので、上から順に進めてください（軽い概念 → 重い拡張、A と B を交互に扱うことで飽きずに進められる構成）。

| セクション | 軸 | 実践で得る成果物 |
|---|---|---|
| 2-3-1 Plan Mode | A | 日報画面の設計案（実装前の計画） |
| 2-3-2 Skills | B | 自分用のスラッシュコマンド |
| 2-3-3 Hooks | B | ファイル保存時などの自動処理 |
| 2-3-4 MCP | B | 外部サービスと連携する追加ツール |
| 2-3-5 Sub-agents | B | 専門タスクを任せる子エージェント |
| 2-3-6 Plugins | B | 機能をまとめて配布できる拡張パッケージ |
| 2-3-7 Git と Worktree | A | 日報開発の Git 履歴と並列作業環境 |
| 2-3-8 GitHub Actions | B | PR 上で動く Claude Code |

どちらの成果物も cc-practice に蓄積されていきます。

> 📝 この Chapter の各機能は、すべて必須ではありません。 Claude Code は Chapter 2-1〜2-2 で学んだ基本操作だけでも十分に活用できます。この Chapter で紹介する機能（Plan Mode、Skills、Hooks、MCP、Sub-agents、Plugins、Git 連携、GitHub Actions）は、Claude Code をさらに効率的に使いこなすための**任意の拡張機能** です。すべてを一度に覚える必要はなく、実務で必要になったときに該当するセクションに戻って活用してください。
