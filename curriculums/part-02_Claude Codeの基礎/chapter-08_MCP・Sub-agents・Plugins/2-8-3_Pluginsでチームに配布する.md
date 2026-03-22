# 2-8-3 Plugins でチームに配布する

## 概要

2-5-1 で Skills を作り、2-6-2 で Hooks を設定しました。どちらもプロジェクトの `.claude/` ディレクトリに保存され、日々の開発を支えています。

しかし、チームメンバーにも同じ Skills や Hooks を使ってもらいたい場合、ファイルを1つずつ共有するのは手間です。「この Skill をコピーして」「この Hooks の設定をこう書いて」と伝えるのは非効率ですし、バージョンが揃わなくなる原因にもなります。

Plugins は、Skills・Hooks・Sub-agents・MCP サーバーの設定を **1つのパッケージにまとめて配布する仕組み** です。インストールコマンド1つでチーム全員が同じ環境を使えるようになります。

このセクションでは、Plugins の概念を理解し、テック記事プラットフォームで作った Skills と Hooks を Plugin にパッケージ化します。

## Plugins の概念

### Standalone 設定と Plugin の違い

これまでの設定方法（`.claude/skills/`、`.claude/settings.json` の hooks）は **Standalone 設定** と呼ばれます。プロジェクトに直接配置する方法で、そのプロジェクト内でのみ有効です。

Plugin は、これらの設定を **プロジェクトの外に切り出してパッケージ化** したものです。

| 項目 | Standalone（`.claude/`） | Plugin |
|---|---|---|
| 用途 | 個人のワークフロー、単一プロジェクト | チーム・コミュニティへの配布 |
| Skill の呼び出し | `/skill-name` | `/plugin-name:skill-name` |
| バージョン管理 | プロジェクトの Git に含まれる | Plugin 単体で管理 |
| 再利用性 | そのプロジェクトのみ | 複数プロジェクトで使い回せる |

Plugin の Skill は **名前空間付き** で呼び出します。たとえば `my-plugin` という Plugin に `hello` という Skill がある場合、`/my-plugin:hello` で実行します。

### Plugin の構造

Plugin のディレクトリ構造を見てみましょう。

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # マニフェスト（ここだけ .claude-plugin/ に置く）
├── commands/                 # スラッシュコマンドとして実行される Skill
├── agents/                   # カスタム Sub-agent 定義
├── skills/                   # SKILL.md によるエージェント向け Skill
├── hooks/
│   └── hooks.json            # Hooks 設定
├── .mcp.json                 # MCP サーバー設定
└── settings.json             # デフォルト設定
```

重要なのは、`.claude-plugin/` ディレクトリには `plugin.json`（マニフェスト）**だけ** を置くことです。`commands/`、`agents/`、`skills/` などはプロジェクトルート直下に配置します。

## Plugin を作成する

### マニフェストの作成

テック記事プラットフォームのプロジェクトとは別のディレクトリに、Plugin を作成します。

```bash
mkdir -p tech-article-plugin/.claude-plugin
```

まず、マニフェストファイル `plugin.json` を作成します。

以下の内容で `tech-article-plugin/.claude-plugin/plugin.json` を作成します。

```json
{
  "name": "tech-article-plugin",
  "description": "テック記事プラットフォーム開発用の Skills と Hooks",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

`name` は Plugin の識別子で、Skill の名前空間にもなります。`description` は Plugin の用途を説明します。

### Skills の移行

2-5-1 で作成した `/add-model` Skill を Plugin に移行します。テック記事プラットフォームの `.claude/skills/add-model/SKILL.md` の内容を Plugin にコピーします。

Plugin には Skill を配置する場所が2つあります。

| ディレクトリ | 呼び出し方 | 用途 |
|---|---|---|
| `commands/` | `/plugin-name:command-name` で直接実行 | スラッシュコマンドとして使う Skill |
| `skills/` | Claude Code が文脈に応じて自動適用 | エージェント向けのナレッジ Skill |

`/add-model` は手動で呼び出すスラッシュコマンドなので、`commands/` に配置します。

```
tech-article-plugin/
├── .claude-plugin/
│   └── plugin.json
└── commands/
    └── add-model.md
```

`commands/` に置いた Markdown ファイルはスラッシュコマンドとして呼び出せます。ファイル名がコマンド名になるため、`add-model.md` は `/tech-article-plugin:add-model` で実行できます。

### Hooks の移行

2-6-2 で設定した Hooks（フォーマッタの自動実行）を Plugin に移行します。`hooks/hooks.json` に設定を書きます。

`tech-article-plugin/hooks/hooks.json` に以下の内容を書きます。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "sail pint --dirty 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

`.claude/settings.json` の `hooks` セクションと同じ構造ですが、Plugin では外側に `"hooks"` キーで囲む点に注意してください。

### ローカルでテストする

Plugin が正しく動作するか、`--plugin-dir` フラグでテストします。テック記事プラットフォームのディレクトリで Claude Code を起動してください。

```bash
claude --plugin-dir ../tech-article-plugin
```

起動したら、Plugin の Skill が認識されているか確認します。

```
> /help
```

スラッシュコマンドの一覧に `/tech-article-plugin:add-model` が表示されていれば成功です。

実際に実行して動作を確かめましょう。ここではテストとして `Notification` と入力しますが、実際にモデルを追加する必要はありません。Skill が正しく読み込まれ、Claude Code が指示を受け取ることを確認するだけです。

```
> /tech-article-plugin:add-model Notification
```

Skill の内容が展開され、Claude Code が「Notification モデルを追加する」手順を進めようとすれば、Plugin の設定は成功です。確認できたら `Esc` で中断して構いません。

💡 開発中に Plugin のファイルを変更した場合、`/reload-plugins` コマンドで再読み込みできます。Claude Code を再起動する必要はありません。

### マーケットプレイスと配布

作成した Plugin は、いくつかの方法でチームに配布できます。

- **Git リポジトリ**: Plugin のディレクトリを Git リポジトリとして管理し、チームメンバーにクローンしてもらう
- **`/plugin install`**: Claude Code 内から `/plugin install` コマンドでマーケットプレイスの Plugin をインストールできる

マーケットプレイスには、コミュニティが作成した実用的な Plugin が公開されています。`/plugin install` で探してみると、開発ワークフローのヒントが見つかるかもしれません。

💡 実用的な Plugin の例として、Skill の作成を支援する `/skill-creator` などがあります。Plugin エコシステムは発展途上ですが、チームでの Claude Code 活用が広がるにつれて、共有できるナレッジも増えていきます。

## 公式ドキュメント

- [Plugins](https://code.claude.com/docs/en/plugins)（Plugin の構造、作成、テスト、配布）
- [Features Overview](https://code.claude.com/docs/en/features-overview)（Skills・Sub-agents・Hooks・MCP・Plugins の比較と使い分け）

## まとめ

- Plugins は Skills・Hooks・Sub-agents・MCP サーバーの設定を1つのパッケージにまとめて配布する仕組みです
- `.claude-plugin/plugin.json` にマニフェストを置き、`commands/`・`agents/`・`hooks/` などをプロジェクトルート直下に配置します
- Plugin の Skill は名前空間付き（`/plugin-name:skill-name`）で呼び出します
- `--plugin-dir` フラグでローカルテストができます。`/reload-plugins` で開発中の変更を再読み込みできます
- 個人の `.claude/` に閉じていた工夫を Plugin にすることで、チーム全体の生産性を上げられます

次の Chapter では、Claude Code の権限システムを体系的に学びます。これまで「何となく承認」していた許可ダイアログの仕組みを理解し、セキュリティレビューで安全性を確認する方法を身につけます。
