# 2-3-3 Hooks

## 🎯 このセクションで学ぶこと

- Hooks の仕組みと、自動処理を挿入する意義を理解する
- Hook のライフサイクルイベントと設定方法を把握する
- よく使う Hook パターンを知り、自分のプロジェクトに Hook を設定する

まず Hooks の仕組みとライフサイクルイベントを理解し、次に設定方法とよく使うパターンを学び、最後に cc-practice で通知 Hook と安全 Hook を設定します。

---

## 導入: 「また手動でやるのか」を自動化する

Claude Code でコードを書いていると、毎回手動で行っている作業があることに気づきます。Claude Code がファイルを編集するたびにフォーマッターを走らせる。作業が完了したらデスクトップ通知を出す。特定のファイル（`.env` や `package-lock.json`）を Claude Code に触らせたくない。

これらは「ツールが何かをしたタイミングで、決まった処理を自動的に実行する」という共通のパターンです。Skills がプロンプトのテンプレートだったのに対し、**Hooks** はツールの実行に連動するシェルコマンドです。

### 🧠 先輩エンジニアはこう考える

> Hooks は Git hooks と同じ発想だ。`pre-commit` フックで Lint を走らせたり、`post-merge` フックで `npm install` を自動実行したりするのと同じように、Claude Code のツール実行に自分のスクリプトを差し込める。ポイントは「決定論的であること」。AI の判断に委ねるのではなく、「このイベントが起きたら、必ずこのコマンドを実行する」というルールベースの自動化だ。フォーマットの適用やファイルの保護のような、例外なく毎回同じ処理をしたい場面で使う。

---

## Hooks とは

Hooks は、Claude Code のライフサイクルの特定のタイミングで、**あなたが定義したシェルコマンドを自動的に実行する** 仕組みです。

```
あなたの指示: 「このファイルを修正して」
        │
        ▼
┌─ Claude Code のライフサイクル ──────────────────────────┐
│                                                         │
│  ① PreToolUse   ← Hook: 保護ファイルの編集を阻止       │
│       │                                                 │
│       ▼                                                 │
│  ② ツール実行（ファイル編集）                            │
│       │                                                 │
│       ▼                                                 │
│  ③ PostToolUse  ← Hook: Prettier で自動フォーマット     │
│       │                                                 │
│       ▼                                                 │
│  ④ Stop         ← Hook: デスクトップ通知を送信          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

重要なのは、Hooks は **Claude Code の判断ではなく、あなたが定義したルール** に基づいて動くという点です。Skills が Claude Code への「指示」であるのに対し、Hooks は Claude Code の動作に「差し込む」処理です。Claude Code が「今回はフォーマッターを実行しなくていいだろう」と判断する余地はありません。設定した通りに、必ず実行されます。

## 主要なライフサイクルイベント

Hooks を設定できるタイミング（イベント）は多数ありますが、特に使用頻度が高いのは以下の5つです。

| イベント | タイミング | 用途 |
|---|---|---|
| **PreToolUse** | ツールが実行される**前** | 特定のファイルへの編集をブロックする、特定の操作に条件を付ける |
| **PostToolUse** | ツールが実行された**後** | 編集後のフォーマット、ログの記録 |
| **UserPromptSubmit** | あなたがプロンプトを送信した**直後** | 入力内容の検証、コンテキストの追加 |
| **Stop** | Claude Code がタスクを完了した**時** | 通知の送信、最終チェックの実行 |
| **PreCompact** / **PostCompact** | コンテキストの圧縮**前後** | 重要な情報の保全、圧縮後のコンテキスト再注入 |

> 📝 全イベントの一覧は `/hooks` コマンドで確認できます。SessionStart、SessionEnd、Notification など、ここに挙げた以外にも多くのイベントがあります。Hook の種類も `command`（シェルコマンド）以外に、`http`（HTTP リクエスト）、`prompt`（LLM による判定）、`agent`（Sub-agent による検証）がありますが、この教材では最も基本的な `command` タイプに絞って解説します。

## Hooks の設定方法

Hooks は settings.json ファイルに JSON 形式で定義します。

### 設定ファイルの配置場所

| ファイル | スコープ | 共有 |
|---|---|---|
| `.claude/settings.json` | プロジェクト | Git 経由でチーム共有可能 |
| `.claude/settings.local.json` | プロジェクト | ローカルのみ（`.gitignore` 対象） |
| `~/.claude/settings.json` | ユーザー全体 | 自分の全プロジェクトに適用 |

### 設定の書き方

以下は、Claude Code がファイルを編集した後に Prettier を自動実行する Hook の例です。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "FILE=$(jq -r '.tool_input.file_path // empty') && [ -n \"$FILE\" ] && npx prettier --write \"$FILE\"",
        "matcher": "Edit|Write"
      }
    ]
  }
}
```

各フィールドの意味は以下の通りです。

| フィールド | 説明 |
|---|---|
| `type` | Hook の種類。`command`（シェルコマンド）が最も一般的 |
| `command` | 実行するコマンド。標準入力で受け取った JSON からイベント情報を取得する |
| `matcher` | どのツールで発火するかを正規表現で指定。省略するとすべてのツールで発火 |

`matcher` が重要です。`"Edit|Write"` と指定することで、ファイルの編集（Edit）または作成（Write）が行われたときだけ Hook が発火します。ファイルの読み取り（Read）や検索（Grep）では発火しません。これにより、不要な処理の実行を防げます。

### Hook の入出力

Hook のコマンドは、**標準入力（stdin）で JSON データを受け取り、終了コードと標準出力で結果を返す** という仕組みで動きます。

標準入力で受け取る JSON には、`session_id`、`cwd`、`tool_name`、`tool_input` などのイベント情報が含まれています。`jq` コマンドで必要な値を抽出して使います。

先ほどのフォーマッターの例に出てきたコマンドを分解して見てみましょう。

```bash
FILE=$(jq -r '.tool_input.file_path // empty') && [ -n "$FILE" ] && npx prettier --write "$FILE"
```

| 部分 | 説明 |
|---|---|
| `jq -r '.tool_input.file_path // empty'` | 標準入力の JSON から `.tool_input.file_path` の値を取り出す。なければ空文字を返す |
| `FILE=$(...)` | 取り出したファイルパスを変数 `FILE` に格納する |
| `[ -n "$FILE" ]` | `FILE` が空でないことを確認する（空なら以降を実行しない） |
| `npx prettier --write "$FILE"` | そのファイルに Prettier を適用する |

`jq` は JSON を操作するコマンドラインツールです。`.tool_input.file_path` はJSONの中のパスを指定する構文で、`// empty` は値がなかった場合のフォールバックです。

| 終了コード | 意味 |
|---|---|
| **0** | 正常終了。処理を続行する |
| **2** | ブロック。ツールの実行を阻止する（PreToolUse の場合） |
| その他 | エラー。ただしブロックはしない |

たとえば、`.env` ファイルの編集をブロックする PreToolUse Hook は以下のように書きます。

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "jq -r '.tool_input.file_path // empty' | grep -q '\\.env' && exit 2 || exit 0",
        "matcher": "Edit|Write"
      }
    ]
  }
}
```

`jq` が標準入力の JSON からファイルパスを抽出し、`.env` が含まれていれば終了コード 2（ブロック）、含まれていなければ終了コード 0（続行）を返します。

## よく使う Hook パターン

実務でよく使われる Hook のパターンを紹介します。

### パターン1: デスクトップ通知

Claude Code の作業が完了したら通知を受け取ります。長い処理を待っている間、別の作業に集中できます。

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "command",
        "command": "osascript -e 'display notification \"Claude Code の作業が完了しました\" with title \"Claude Code\"'"
      }
    ]
  }
}
```

> 📝 上記は macOS 用のコマンドです。Linux では `notify-send "Claude Code の作業が完了しました"`、Windows（WSL）では `powershell.exe -Command "[System.Windows.Forms.MessageBox]::Show('Claude Code の作業が完了しました')"` を使います。以降の実践でも macOS 用のコマンドを例示しますが、お使いの OS に応じて読み替えてください。

### パターン2: 自動フォーマット

ファイルの編集後にフォーマッターを自動実行します。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "FILE=$(jq -r '.tool_input.file_path // empty') && [ -n \"$FILE\" ] && npx prettier --write \"$FILE\"",
        "matcher": "Edit|Write"
      }
    ]
  }
}
```

### パターン3: 保護ファイルの編集ブロック

特定のファイルを Claude Code に編集させないようにします。

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "jq -r '.tool_input.file_path // empty' | grep -qE '(\\.env|package-lock\\.json)' && exit 2 || exit 0",
        "matcher": "Edit|Write"
      }
    ]
  }
}
```

> ⚠️ Hook のコマンドにバグがあると、Claude Code の動作に影響します。特に PreToolUse で誤ってすべての操作をブロックしてしまうと、Claude Code が何もできなくなります。新しい Hook を追加したら、意図通りに動作するか必ず確認してください。

---

## 🏃 実践: 通知 Hook と安全 Hook を設定する

2種類の Hook を設定して、Hook の仕組みを一通り体験しましょう。1つ目は作業完了時の通知、2つ目は危険なコマンド実行前の確認です。

### Step 1: Stop Hook（通知）を設定する

cc-practice で Claude Code を起動し、以下のように指示します。

```
> .claude/settings.local.json に以下の内容を書いて:
> Claude Code の作業が完了したらデスクトップ通知を送る Stop Hook を設定したい。
> お使いの OS に合わせてデスクトップ通知を送る設定にして。macOS なら osascript、Linux なら notify-send を使って「Claude Code の作業が完了しました」という通知を出すようにして
```

> 📝 `settings.local.json`（ローカル設定）に書くのは、通知の設定が個人の環境に依存するためです。macOS と Linux ではコマンドが異なるため、チーム共有する `settings.json` ではなくローカル設定に書きます。

Claude Code が `.claude/settings.local.json` を作成します。内容を確認してみましょう。

```
> .claude/settings.local.json の内容を見せて
```

以下のような JSON が書かれているはずです（あなたの環境では異なる場合があります）。

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "command",
        "command": "osascript -e 'display notification \"Claude Code の作業が完了しました\" with title \"Claude Code\"'"
      }
    ]
  }
}
```

### Step 2: Stop Hook の動作を確認する

Hook が正しく動作するか確認します。Claude Code に簡単なタスクを依頼してみましょう。

```
> README.md に「## 機能一覧」セクションを追加して。内容は「日報の CRUD 管理」と書いて
```

タスクが完了すると、macOS のデスクトップ通知が表示されるはずです。

<!-- TODO: 画像追加 - macOS のデスクトップ通知画面 -->

### Step 3: PreToolUse Hook（安全確認）を追加する

もう1つ、PreToolUse Hook を追加します。マイグレーションの実行前にログを出力する Hook です。

```
> .claude/settings.local.json に PreToolUse Hook を追加して。
> Bash ツールが使われるとき、コマンドに「migrate」が含まれていたら、
> 標準エラー出力に「⚠️ マイグレーションが実行されます」と表示するシェルスクリプトを設定して。
> 既存の Stop Hook は残して
```

Claude Code が `settings.local.json` を更新します。内容を確認しましょう。

```bash
! cat .claude/settings.local.json
```

Stop Hook と PreToolUse Hook の両方が設定されていることを確認してください。

### Step 4: PreToolUse Hook の動作を確認する

実際にマイグレーションを実行して、Hook が動作するか確認しましょう。

```
> Sail でマイグレーションのステータスを確認して
```

Claude Code が `./vendor/bin/sail artisan migrate:status` を実行する際、PreToolUse Hook が発動し「⚠️ マイグレーションが実行されます」というメッセージが表示されるはずです。

### Step 5: 設定済みの Hook を一覧で確認する

```
/hooks
```

Stop Hook と PreToolUse Hook の両方が表示されることを確認してください。

---

## 🔍 見極めチェック

> 🧠 先輩エンジニアの思考: 「Hooks のミスは厄介だ。設定を間違えると、Claude Code が動くたびに予期しない動作が起きる。特に PreToolUse のブロック設定はミスるとすべての操作が止まる。設定したら必ず動作確認。」

- [ ] **正しさ**: JSON の構文が正しいか（カンマの過不足、括弧の対応）。イベント名（`Stop`、`PreToolUse` 等）が正確か
- [ ] **品質**: `matcher` が適切に設定されているか。不要なタイミングで発火しないか
- [ ] **安全性**: Hook のコマンドが意図しない副作用を起こさないか。PreToolUse で誤って全操作をブロックしていないか

> 🔑 この Section では特に「JSON の構文エラー」に注目してください。

---

## ✨ まとめ

- **Hooks** は Claude Code のライフサイクルイベントに連動してシェルコマンドを自動実行する仕組み
- 主要イベント: PreToolUse（実行前）、PostToolUse（実行後）、Stop（タスク完了時）
- settings.json に JSON 形式で定義し、`matcher` で発火条件を制御する
- 終了コード 0 は続行、終了コード 2 はブロック
- よく使うパターン: デスクトップ通知、自動フォーマット、保護ファイルの編集ブロック
- Skills が「指示のテンプレート」なら、Hooks は「ルールベースの自動処理」

---

次のセクションでは、Claude Code の能力そのものを拡張する **MCP** を学びます。外部のツールやサービスに接続し、Claude Code にできることの幅を広げる仕組みです。
