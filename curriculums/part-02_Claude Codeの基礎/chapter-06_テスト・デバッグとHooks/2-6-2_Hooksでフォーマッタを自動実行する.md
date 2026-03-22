# 2-6-2 Hooks でフォーマッタを自動実行する

## 概要

前のセクションでは、`sail test` でテストを実行して生成コードの正しさを検証しました。テストは強力ですが、毎回手動で実行する必要があります。

このセクションでは、Claude Code の **Hooks** の仕組みを理解した上で、実際に PostToolUse Hook を設定してフォーマッタを自動実行します。Hooks を設定すると、Claude Code がファイルを編集するたびに、自動でフォーマッタが走ります。「テスト実行を忘れた」「フォーマッタをかけ忘れた」といったヒューマンエラーがなくなります。

テスト（手動で実行する検証）から Hooks（自動で実行される検証）へ。品質を守る手段がレベルアップします。

## Hooks の仕組み

### Hooks とは

Hooks は、Claude Code のライフサイクルの特定のタイミングで自動実行されるスクリプトです。

たとえば「Claude Code がファイルを編集した後に、自動でフォーマッタを実行する」「Claude Code がセッションを開始したときに、環境変数を設定する」といった自動化ができます。CLAUDE.md に「フォーマッタを実行してください」と書いても Claude Code が従うかは保証されませんが、Hooks を設定すれば **確実に** 実行されます。この確実性が Hooks の最大の強みです。

### イベントタイプ

Hooks は「いつ実行するか」を決めるイベントタイプと、「何を実行するか」を決めるハンドラで構成されます。

Claude Code には多くのイベントタイプがありますが、まずは主要な4つを覚えれば十分です。

| イベント | いつ実行されるか | 使用例 |
|---|---|---|
| **PreToolUse** | ツールの実行**前** | 危険なコマンドをブロックする |
| **PostToolUse** | ツールの実行**後** | 編集後にフォーマッタを走らせる |
| **SessionStart** | セッションの開始時 | 環境変数を設定する |
| **Notification** | Claude Code が通知を送るとき | デスクトップ通知を表示する |

**PreToolUse** はツールの実行前に発火し、実行をブロックすることもできます。たとえば、`rm -rf` を含むコマンドを実行前にブロックする、といった使い方です。

**PostToolUse** はツールの実行後に発火します。このセクションで使うのはこのイベントです。「ファイルを編集した後にフォーマッタを実行する」という用途に最適です。

💡 Claude Code には上記以外にも `Stop`、`UserPromptSubmit`、`SubagentStart` など、合計20種以上のイベントタイプがあります。すべてのイベントは[公式ドキュメント](https://code.claude.com/docs/en/hooks)で確認できます。

### ハンドラタイプ

「何を実行するか」を決めるハンドラには4つのタイプがあります。

| タイプ | 動作 |
|---|---|
| **command** | シェルコマンドを実行する |
| **http** | HTTP エンドポイントにリクエストを送る |
| **prompt** | Claude モデルに判断を委ねる |
| **agent** | サブエージェントを起動して検証する |

最もよく使うのは **command** です。シェルコマンドを実行するシンプルなハンドラで、フォーマッタの実行やログの記録などに使います。このセクションでも command タイプを使います。

### 設定場所

Hooks は JSON 形式の設定ファイルに記述します。

| 設定ファイル | 適用範囲 | チームで共有 |
|---|---|---|
| `~/.claude/settings.json` | すべてのプロジェクト | いいえ（自分のマシンのみ） |
| `.claude/settings.json` | このプロジェクトのみ | はい（リポジトリにコミット可） |
| `.claude/settings.local.json` | このプロジェクトのみ | いいえ（gitignore 対象） |

個人的な通知設定は `~/.claude/settings.json` に、プロジェクト共通のフォーマッタ設定は `.claude/settings.json` に配置するのが一般的です。

設定した Hooks は `/hooks` コマンドで一覧を確認できます。

```
> /hooks
```

イベントごとに設定されている Hook の数が表示され、選択すると詳細（イベント、matcher、コマンドなど）を確認できます。`/hooks` は読み取り専用のブラウザです。Hook の追加や変更は設定ファイルを直接編集するか、Claude Code に依頼します。

## Hooks の設定

### PostToolUse で Laravel Pint を自動実行する

仕組みがわかったところで、実際に設定しましょう。PHP のコードスタイルを統一する **Laravel Pint** を、Claude Code がファイルを編集するたびに自動で実行する Hook を設定します。

Laravel Pint は Laravel に標準でバンドルされているコードフォーマッタです。追加のインストールは不要で、`sail pint` コマンドですぐに使えます。

では、Hook を設定しましょう。

```
> PostToolUse の Hook を .claude/settings.json に設定してください。
>
> - イベント: PostToolUse
> - matcher: Edit|Write（ファイル編集ツールのみに反応する）
> - タイプ: command
> - コマンド: 変更されたファイルだけを対象に sail pint --dirty を実行する
```

皆さんの環境では異なる設定が生成されます。以下は `.claude/settings.json` に追加する内容の一例です。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
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

この設定を読み解きましょう。

1. **`"matcher": "Edit|Write"`**: Claude Code が `Edit` または `Write` ツールを使ったときだけ Hook が発火します。`Read` や `Bash` などの他のツールでは発火しません
2. **`sail pint --dirty`**: `--dirty` フラグは、Git で変更があったファイルだけを対象にフォーマットします。すべてのファイルを毎回チェックするのではなく、変更されたファイルだけを効率的に整形します
3. **`2>/dev/null || true`**: エラー出力を抑制し、フォーマッタが失敗しても Hook 全体がエラーにならないようにしています。Claude Code のターミナルを見やすく保ちます

### 動作を確認する

設定を確認しましょう。

```
> /hooks
```

PostToolUse に Hook が1つ表示されていれば、設定は正しく読み込まれています。

実際に動作を確認します。Claude Code に PHP ファイルを編集させてみましょう。

```
> 任意の PHP ファイルに不要な空行やインデントのずれを追加してから、元に戻してください。
```

Claude Code がファイルを編集した後、自動的に Laravel Pint が実行されます。ターミナルの verbose モード（`Ctrl+O`）を有効にすると、Hook の実行ログを確認できます。

> ⚠️ よくあるエラー: Hook が実行されない
>
> ```
> /hooks で Hook が表示されない
> ```
>
> **原因**: 設定ファイルの JSON が不正（カンマの過不足、括弧の閉じ忘れなど）か、設定ファイルの場所が間違っています。
>
> **対処法**: `cat .claude/settings.json | jq .` を実行して JSON の構文エラーがないか確認してください。エラーがある場合は `jq` がエラー箇所を教えてくれます。

> ⚠️ よくあるエラー: Pint が実行されない
>
> ```
> sail: command not found
> ```
>
> **原因**: Laravel Sail が起動していないか、`sail` コマンドにパスが通っていません。
>
> **対処法**: `sail up -d` で Sail を起動し、`sail pint --test` で Pint が動作するか確認してください。

### Hooks と CLAUDE.md の使い分け

Hooks と CLAUDE.md は、どちらも Claude Code の振る舞いをコントロールする仕組みですが、性質が異なります。

- **CLAUDE.md**: 「こうしてほしい」という **指示**。Claude Code はできる限り従いますが、従わないこともあります
- **Hooks**: 「こうなったら必ずこうする」という **ルール**。設定されていれば、必ず実行されます

「フォーマッタを実行してください」と CLAUDE.md に書いても、Claude Code が忘れることがあります。しかし PostToolUse Hook に設定すれば、ファイルを編集するたびに確実にフォーマッタが走ります。

判断の基準はシンプルです。**例外なく毎回実行したいなら Hooks、状況に応じて判断させたいなら CLAUDE.md** です。

## 見極めチェック

- [ ] **正しさ**: `/hooks` コマンドで PostToolUse に Hook が1つ表示されているか
- [ ] **正しさ**: Claude Code で PHP ファイルを編集した後、Laravel Pint が自動実行されているか（verbose モードで確認）
- [ ] **正しさ**: PHP 以外のファイル（Markdown、JSON など）を編集したとき、Hook がエラーにならず正常にスキップされるか
- [ ] **品質**: Hook の設定が `.claude/settings.json` に配置されており、チームで共有可能な状態か
- [ ] **品質**: `--dirty` フラグにより、変更ファイルだけを対象にした効率的なフォーマットになっているか
- [ ] **安全性**: この Section では該当なし

> この Section では特に「正しさ」に注目してください。Hook の設定ミス（JSON の構文エラー、matcher の typo）は、エラーが表示されずに黙って無視されることがあります。`/hooks` コマンドでの確認と、verbose モードでの実行ログの確認を必ず行いましょう。

## 公式ドキュメント

- [Hooks](https://code.claude.com/docs/en/hooks)（Hooks のリファレンス。全イベントタイプ・設定フォーマット・入出力スキーマ）
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)（Hooks の実践ガイド。通知・ファイル保護・コンパクション後のコンテキスト再注入などのユースケース）
- [Features Overview](https://code.claude.com/docs/en/features-overview)（Skills・Hooks・MCP・Sub-agents の使い分け）

## まとめ

- Hooks は Claude Code のライフサイクルイベントに応じて自動実行されるスクリプトです。CLAUDE.md の指示とは異なり、設定すれば **確実に** 実行されます
- PostToolUse イベントと `Edit|Write` matcher を組み合わせて、変更ファイルに対して Laravel Pint を自動実行する Hook を設定しました
- Hooks は `.claude/settings.json`（プロジェクト共有）と `~/.claude/settings.json`（個人設定）に配置でき、`/hooks` コマンドで一覧を確認できます
- 例外なく毎回実行したい処理は Hooks、状況に応じた判断は CLAUDE.md と使い分けましょう

次の Chapter では、ここまでの変更を Git で整理し、GitHub に push します。Claude Code の Git 統合、チェックポイントによる安全な巻き戻し、Worktree による並列開発を学びます。
