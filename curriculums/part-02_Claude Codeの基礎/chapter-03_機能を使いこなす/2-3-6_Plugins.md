# 2-3-6 Plugins

## 🎯 このセクションで学ぶこと

- Plugins の仕組みと、拡張機能をパッケージ化して共有する意義を理解する
- Plugin の構造（マニフェスト、ディレクトリ構成）を把握する
- 公式マーケットプレイスから Plugin をインストールして使う

まず Plugins の仕組みとパッケージ化の意義を理解し、次にマーケットプレイスからのインストールと管理方法を学び、最後に cc-practice で Plugin のインストールと自作を体験します。

---

## 導入: Skills と Hooks をチームで共有したい

ここまでのセクションで、Skills（カスタムコマンド）、Hooks（自動処理）、Sub-agents（専門的な分身）、MCP サーバー（外部連携）を学んできました。これらを組み合わせると、Claude Code の能力を大幅に拡張できます。

しかし、1つ困ることがあります。**これらの設定を他のプロジェクトやチームメンバーと共有するのが面倒** です。

たとえば、あなたが「PHP の LSP（Language Server Protocol）で型チェックを走らせる Sub-agent」「コミット前にコード品質をチェックする Hook」「レビュー用の Skill」を組み合わせた環境を構築したとします。これを別のプロジェクトでも使いたい場合、ファイルを1つずつコピーする必要があります。チームメンバーに共有するには、ディレクトリ構造やファイルの配置場所を説明するドキュメントが必要です。

**Plugins** は、これらの拡張機能を **1つのパッケージにまとめて、インストール・共有・管理** できるようにする仕組みです。

### 🧠 先輩エンジニアはこう考える

> Plugins は npm パッケージや Composer パッケージと同じ発想だ。個別のファイルを手動でコピーするのではなく、パッケージとしてまとめてバージョン管理し、コマンド1つでインストールできる。特にチーム開発では、メンバー全員が同じ拡張機能を使える状態にすることが重要だ。「自分の環境では動くけど、あの人の環境では動かない」をなくせる。

---

## Plugins とは

Plugin は、Claude Code の拡張機能を1つのパッケージにまとめたものです。

```
Plugin パッケージ
├── .claude-plugin/
│   └── plugin.json     ← マニフェスト（名前、説明、バージョン）
├── skills/              ← Skills（スラッシュコマンド、Agent Skills）
│   └── review/
│       └── SKILL.md
├── agents/              ← カスタム Sub-agents
│   └── security-audit.md
├── hooks/               ← Hooks
│   └── hooks.json
├── .mcp.json            ← MCP サーバー設定
└── settings.json        ← デフォルト設定
```

Plugin は、これまで個別に学んできた要素を **1つのディレクトリにまとめたもの** です。新しい概念を覚える必要はありません。

### plugin.json（マニフェスト）

Plugin の基本情報を定義するファイルです。

```json
{
  "name": "laravel-toolkit",
  "description": "Laravel 開発に必要な Skills、Hooks、Sub-agents をまとめた Plugin",
  "version": "1.0.0",
  "author": "your-name"
}
```

| フィールド | 説明 |
|---|---|
| `name` | Plugin の識別名 |
| `description` | Plugin の説明 |
| `version` | バージョン（セマンティックバージョニング） |
| `author` | 作者名 |

## Plugin のインストールと管理

Plugin は `/plugin` コマンドで管理します。

### マーケットプレイスからインストールする

Claude Code には **公式マーケットプレイス**（`claude-plugins-official`）があり、すぐに使える Plugin が公開されています。

```
> /plugin install typescript@claude-plugins-official
```

`Plugin名@マーケットプレイス名` の形式でインストールします。

### 主要な公式 Plugin

公式マーケットプレイスで提供されている代表的な Plugin を紹介します。

| カテゴリ | Plugin 例 | 説明 |
|---|---|---|
| **コードインテリジェンス** | `typescript`、`php`、`python`、`go` | LSP による型チェック、定義ジャンプ、参照検索 |
| **外部連携** | `github`、`slack`、`sentry` | 外部サービスとの連携 |
| **開発ワークフロー** | `pr-review-toolkit`、`commit-commands` | PR レビューやコミット操作の効率化 |
| **出力スタイル** | `learning-output-style` | Claude Code の出力形式のカスタマイズ |

> 💡 Pro生 が Laravel で開発する場合、`php` Plugin（PHP の LSP による型チェック）は特に有用です。

### Plugin の管理コマンド

| コマンド | 説明 |
|---|---|
| `/plugin install <name>@<marketplace>` | Plugin をインストールする |
| `/plugin disable <name>@<marketplace>` | Plugin を一時的に無効化する |
| `/plugin enable <name>@<marketplace>` | 無効化した Plugin を再有効化する |
| `/plugin uninstall <name>@<marketplace>` | Plugin をアンインストールする |
| `/reload-plugins` | Plugin の変更を再読み込みする（再起動不要） |

### インストールスコープ

Plugin のインストール先によって、適用範囲が変わります。

| スコープ | 説明 |
|---|---|
| **User** | 自分の全プロジェクトに適用 |
| **Project** | `.claude/settings.json` に記録。チーム共有可能 |
| **Local** | `.claude/settings.local.json` に記録。ローカルのみ |

## Plugin を自作する

既存の Plugin を使うだけでなく、自分で Plugin を作ることもできます。

### 作成の流れ

```
① /plugin コマンドで雛形を作成
       │
       ▼
② Skills、Hooks、Sub-agents を追加
       │
       ▼
③ ローカルでテスト（--plugin-dir フラグ）
       │
       ▼
④ Git リポジトリとして公開（任意）
```

Claude Code 内で `/plugin` と入力すると、対話的に Plugin の雛形を作成できます。

### ローカルでのテスト

作成中の Plugin は、`--plugin-dir` フラグでローカルからロードしてテストできます。

```bash
claude --plugin-dir ./my-plugin
```

変更を加えたら `/reload-plugins` で再読み込みします。Claude Code を再起動する必要はありません。

> 📝 Plugin の自作は、まず個別の Skills や Hooks を作って動作確認してから、それらを Plugin としてまとめる、という順序で進めるのがおすすめです。最初から Plugin 構造で作り始めると、問題の切り分けが難しくなります。

---

## 🏃 実践: Plugin をインストールし、自作 Plugin を作る

公式マーケットプレイスから Plugin をインストールし、さらに自分で Plugin を作成する体験をしてみましょう。

### Step 1: 利用可能な Plugin を確認する

Claude Code を起動し、以下のコマンドを実行します。

```
/plugin install
```

インストール可能な Plugin の一覧が表示されます。公式マーケットプレイスに登録されている Plugin が確認できます。

### Step 2: Plugin をインストールする

開発ワークフローを支援する Plugin をインストールしてみましょう。

```
/plugin install plugin-dev@claude-plugins-official
```

> 📝 あなたの環境ではこの Plugin が利用できない場合があります。その場合は、一覧に表示されている別の Plugin を試してください。

### Step 3: インストールされた Plugin を確認する

Plugin が正しくインストールされたか確認します。

```
/plugin
```

インストール済みの Plugin の一覧が表示されます。先ほどインストールした Plugin が含まれていることを確認してください。Plugin が提供する Skills は `/` と入力して Tab を押すと確認できます。

### Step 4: Laravel レビュー Plugin を自作する

ここまでの学習で作成した Skill（explain）と Sub-agent（quality-check）を Plugin としてまとめてみましょう。

```
> cc-practice-review という名前の Plugin を作成して。
> plugin.json には name: cc-practice-review、description: 「Laravel プロジェクトのコードレビューを支援する Plugin」、version: 0.1.0 を設定して。
> skills/ ディレクトリに、Laravel の Controller をレビューする review-controller Skill を作成して。
> PSR-12 準拠、バリデーションの有無、N+1 問題の観点でレビューする内容にして
```

Claude Code が Plugin のディレクトリ構造を作成します。

> 📝 あなたの環境では異なる内容が生成されますが、`plugin.json` と `skills/` 配下の SKILL.md が作成されていれば成功です。

### Step 5: 作成した Plugin をローカルでテストする

作成された Plugin をローカルでロードしてテストします。Claude Code を一度終了し、`--plugin-dir` フラグ付きで再起動します。

```bash
claude --plugin-dir ./cc-practice-review
```

> 📝 ディレクトリ名は Claude Code が生成したものに合わせてください。

Plugin が読み込まれたら、`/` と入力して Tab を押し、新しい Skill（review-controller など）が一覧に表示されることを確認しましょう。表示されていれば、実際に DailyReportController に対して使ってみてください。

### Step 6: 成果物を確認する

```bash
! ls cc-practice-review/
! cat cc-practice-review/plugin.json
```

Plugin のディレクトリ構造と `plugin.json` の内容を確認しましょう。

---

## 🔍 見極めチェック

> 🧠 先輩エンジニアの思考: 「Plugin は他の人にも使ってもらうものだから、plugin.json の情報や description の品質が大事だ。自分だけの Skill ならラフでもいいが、Plugin として公開するなら、名前や説明は丁寧に書く。」

- [ ] **正しさ**: `plugin.json` の必須フィールド（name、description、version）が記述されているか。Plugin のディレクトリ構造が正しいか
- [ ] **品質**: Skill の `description` が具体的で、自動呼び出しの判定に使えるレベルか。Plugin 名がわかりやすいか
- [ ] **安全性**: 公式マーケットプレイス以外の Plugin をインストールする場合、提供元のリポジトリやメンテナンス状況を確認したか。Plugin は Skills、Hooks、MCP サーバーを含む可能性があるため、信頼できるソースからのみインストールする

> 🔑 この Section では特に「Plugin のディレクトリ構造と plugin.json の整合性」に注目してください。

---

## ✨ まとめ

- **Plugins** は Skills、Hooks、Sub-agents、MCP サーバーを1つのパッケージにまとめる仕組み
- `plugin.json`（マニフェスト）で Plugin の基本情報を定義する
- 公式マーケットプレイス（`claude-plugins-official`）から `/plugin install` でインストールできる
- コードインテリジェンス（PHP、TypeScript など）や外部連携（GitHub、Slack など）の Plugin が公開されている
- 自作 Plugin は `/plugin` コマンドで雛形を作り、`--plugin-dir` でローカルテストできる
- インストールスコープ（User / Project / Local）で適用範囲を制御できる

---

次のセクションでは、Claude Code が得意とする **Git 連携と Worktree** を学びます。変更管理と並列開発の仕組みを理解し、安心してコードを変更できる基盤を作ります。
