# 3-6-2 CourseHub の変更をチームに届ける

## 🎯 このセクションで学ぶこと

- 説明責任を意識した PR を Claude Code で作成できる
- GitHub Actions を設定し、PR への自動レビューを導入できる
- settings.json のチーム共有設定と CLAUDE.md の運用方針を整備できる
- 繰り返し使えるワークフローを Skill として定義し、チームに共有できる

Part 3 で取り組んできた変更をチームに届ける実践です。「コードの共有」「環境の共有」「ワークフローの共有」の3段階で進めます。

> 📝 このセクションで使う機能: `/commit`・`/diff`（[2-3-7 Git と Worktree](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-7_GitとWorktree.md) で学習）、GitHub Actions（[2-3-8 GitHub Actions](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-8_GitHub%20Actions.md) で学習）、権限管理（[2-1-2 権限とセキュリティ](../../part-02_Claude%20Codeの基礎/chapter-01_セットアップ/2-1-2_権限とセキュリティ.md) で学習）、Skills（[2-3-2 Skills](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-2_Skills.md) で学習）、Plugins（[2-3-6 Plugins](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-6_Plugins.md) で学習）

---

## 導入: これまでの変更をチームに届ける

Part 3 を通じて、CourseHub には多くの変更が加わりました。

- **Chapter 3-1**: CLAUDE.md の更新、rules の整備、skills の修正、settings.json の更新
- **Chapter 3-3**: 進捗率バグ、認可バグ、500 エラーの修正
- **Chapter 3-4**: 小テスト再受験機能、コースレビュー機能の追加
- **Chapter 3-5**: Fat Controller の責務分離、N+1 クエリの解消

これらの変更はローカルのブランチにコミットされていますが、まだチームには届いていません。実務では、コードをチームに届けるために PR（プルリクエスト）を作成し、レビューを受け、マージします。

> 📝 以降の実践は、Part 3 のどの Chapter まで取り組んでいても実行できます。1つでもコミット済みの変更があれば、その変更を PR にまとめられます。すべての Chapter を完了していなくても問題ありません。
>
> Part 3 では、各 Chapter のハンズオンを **`main` から切った独立した作業ブランチ** で進めてきました（`fix/bugfixes`、`feature/quiz-retake`、`feature/course-review`、`refactor/fat-controller`、`refactor/n-plus-one` など）。PR を作成する前に、これらを1つのブランチに統合します。Claude Code に「Part 3 で作成したブランチを1つにまとめたい」と相談すれば、マージの手順を案内してくれます。または、以下のように手動でまとめることもできます。
>
> ```bash
> git checkout main
> git checkout -b feature/part3-all
> git merge fix/bugfixes
> git merge feature/quiz-retake
> git merge feature/course-review
> git merge refactor/fat-controller
> git merge refactor/n-plus-one
> # （他のブランチも同様にマージ）
> ```
>
> マージ時にコンフリクトが起きた場合は、Claude Code に解決を依頼できます。各ブランチが独立した領域を変更している場合（例: バグ修正と機能追加が別ファイル）はコンフリクトせずに統合できますが、同じファイルを触っている場合は手動またはAIの支援で解消します。

### 🧠 先輩エンジニアはこう考える

> PR を出すのが一番緊張する瞬間かもしれない。特に最初のうちは「こんなコードで大丈夫かな」と不安になる。でも、Part 3 で毎回やった見極めチェックを通過しているなら、自信を持って出していい。大事なのは、レビュアーに「何をなぜ変えたか」を伝えること。変更の意図が伝われば、レビューはスムーズに進む。

---

## 🏃 実践①: コードの共有（PR の作成）

Part 3 で取り組んだ変更を PR にまとめます。ここでは、[3-6-1 AI時代のチーム開発](3-6-1_AI時代のチーム開発.md) で学んだ説明責任を意識して PR を作成します。

### Step 1: 変更の全体像を確認する

まず、現在のブランチにどのような変更があるかを Claude Code で確認します。

```
> このブランチの main ブランチからの変更を全て確認してください。
> コミット一覧と、変更されたファイルの概要を教えてください。
```

Claude Code が `git log` と `git diff` を使って変更の全体像を整理してくれます。

> 💡 取り組んだ Chapter の範囲によって、表示されるコミットとファイルは異なります。自分の変更内容を確認しましょう。

### Step 2: PR を出す前の自己レビュー

[3-6-1 AI時代のチーム開発](3-6-1_AI時代のチーム開発.md) で学んだ通り、PR を出す前に自己レビューを行います。Claude Code に依頼しましょう。

```
> このブランチの全変更をレビューしてください。
> 以下の観点で問題がないか確認してください:
> - rules/coding.md のコーディング規約に従っているか
> - テストが十分か
> - セキュリティ上の問題がないか
> - 不要なファイルやデバッグコードが残っていないか
```

Claude Code が変更を分析し、問題があれば指摘してくれます。指摘された内容を確認し、必要に応じて修正します。

> ⚠️ **よくあるエラー**: デバッグ用の `dd()` や `dump()`、`console.log()` がコミットに残っている
>
> **原因**: 調査中に追加したデバッグコードを消し忘れている
>
> **対処法**: 自己レビューで検出するか、後述の Hooks で自動チェックする

### Step 3: PR を作成する

自己レビューで問題がなければ、PR を作成します。

```
> PR を作成してください。
>
> 以下の情報を PR の説明に含めてください:
> - 変更の目的（どのタスクに対応しているか）
> - 変更のアプローチ（なぜこの実装方法を選んだか）
> - 検証内容（どうテストしたか、見極めチェックで何を確認したか）
> - 影響範囲（この変更が他の機能に影響するか）
```

Claude Code が `gh pr create` コマンドで PR を作成します。

> 📌 **リモートリポジトリの準備**: CourseHub は `coachtech-material/pro-cc-coursehub` からクローンしていますが、このリポジトリに直接 push する権限はありません。PR を作成するには、事前に GitHub 上でリポジトリを **Fork** し、Fork 先をリモートとして設定する必要があります。
>
> ```bash
> # GitHub 上で Fork した後
> git remote set-url origin https://github.com/あなたのユーザー名/pro-cc-coursehub.git
> git push -u origin HEAD
> ```
>
> Fork の手順がわからない場合は、Claude Code に「このリポジトリを Fork して PR を作成できるようにしたい」と相談してください。

<details>
<summary>PR の説明の例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では、取り組んだ Chapter に応じた異なる PR が生成されます。

以下は、Chapter 3-5 のリファクタリング（Fat Controller の責務分離）を PR にした場合の例です。

```markdown
## Summary

- CoachCourseController@store の責務分離: インラインバリデーションを
  StoreCourseRequest に抽出し、画像処理・スラッグ生成・タグ同期を
  private メソッドに分割
- 200行超の単一メソッドを、各責務が明確な構造に改善

## Approach

- Form Request の抽出を優先（rules/coding.md の規約に準拠）
- Service クラスの導入は見送り（現時点では Controller 内の private メソッドで十分）
- 段階的にリファクタリングし、各ステップでテストを実行して動作不変を確認

## Testing

- 各リファクタリングステップで `./vendor/bin/sail artisan test` を実行し全テスト通過を確認
- バリデーションルールの移動後、エラーメッセージの表示が変わっていないことを確認
- 見極めチェック: 正しさ（動作不変）、品質（規約準拠）、安全性（バリデーションルールの維持）

## Impact

- CoachCourseController のみの変更
- 外部 API や他の Controller への影響なし
- バリデーションルール自体は変更なし（移動のみ）
```

</details>

ポイントを確認しましょう。

- **Summary** で変更の目的を端的に伝えています。レビュアーは最初の数行で「何を変えたか」を把握します
- **Approach** で「なぜこの方法か」を説明しています。Service クラスを見送った判断理由も記載することで、レビュアーからの「なぜ Service に切り出さなかったのか」という質問を先回りしています
- **Testing** で検証内容を具体的に記載しています。「テスト通過」だけでなく、何を確認したかを明示しています
- **Impact** で影響範囲を明示しています。「この変更で壊れる可能性がある箇所はどこか」をレビュアーが判断しやすくなります

### 「説明できるか」テストを実践する

PR を作成したら、[3-6-1 AI時代のチーム開発](3-6-1_AI時代のチーム開発.md) で学んだ「説明できるか」テストを行いましょう。PR の説明を読み返し、以下の質問に答えられるか確認します。

- **「このコードが何をしているか」**: 変更内容を自分の言葉で説明できるか
- **「なぜこの方法を選んだか」**: 代替案を検討した上での判断を説明できるか
- **「どう検証したか」**: テスト内容と見極めチェックの結果を説明できるか
- **「影響範囲はどこか」**: 他の機能への影響を把握しているか

すべての質問に答えられるなら、この PR に対する説明責任を果たす準備ができています。

> 💡 実務では、PR を出した後にレビュアーから質問やフィードバックを受けます。Claude Code はレビューへの対応にも活用できます。レビュアーの指摘を Claude Code に伝えて修正し、追加コミットをプッシュするのが一般的な流れです。

---

## 🏃 実践②: 環境の共有（チーム設定の整備）

コードだけでなく、Claude Code の設定もチームで共有します。ここでは GitHub Actions の設定、settings.json のチーム共有設定、CLAUDE.md の運用方針を整備します。

### GitHub Actions を設定する

[2-3-8 GitHub Actions](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-8_GitHub%20Actions.md) で学んだ手順で、CourseHub に GitHub Actions を導入します。

> 📌 GitHub Actions の利用には Anthropic API キーが必要です。[2-3-8 GitHub Actions](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-8_GitHub%20Actions.md) で API キーを取得済みであることを前提とします。まだの場合は [2-3-8 GitHub Actions](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-8_GitHub%20Actions.md) の手順を参照してください。

#### 方法 A: `/install-github-app` を使う（推奨）

Claude Code のセッション内で以下を実行します。

```
/install-github-app
```

画面の指示に従って、GitHub リポジトリに Claude GitHub App をインストールし、API キーを設定します。この方法が最も簡単です。

#### 方法 B: 手動で設定する

手動で設定する場合は、以下の手順で進めます。

**1. GitHub リポジトリの Secrets に API キーを登録する**

GitHub リポジトリの Settings → Secrets and variables → Actions から、`ANTHROPIC_API_KEY` を登録します。

> ⚠️ API キーをコードに直接書かないでください。必ず GitHub Secrets を使って管理します。

**2. ワークフローファイルを作成する**

```
> CourseHub に GitHub Actions のワークフローファイルを作成してください。
> PR が作成されたときに Claude Code が自動レビューする設定にしてください。
> コスト管理のため --max-turns 5 に制限してください。
```

<details>
<summary>生成されるワークフローの例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なるコードが生成されます。

```yaml
# .github/workflows/claude.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]
  issue_comment:
    types: [created]

jobs:
  claude-review:
    if: |
      (github.event_name == 'pull_request') ||
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude'))
    runs-on: ubuntu-latest
    timeout-minutes: 30
    permissions:
      contents: read
      pull-requests: write
      issues: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          claude_args: "--max-turns 5"
          prompt: |
            このリポジトリの CLAUDE.md と .claude/rules/ を読み、
            コーディング規約に従ってレビューしてください。
            特に以下を重点的に確認してください:
            - Form Request の使用（rules/coding.md）
            - Policy による認可（設計方針）
            - テストの有無
            - セキュリティ上の問題
```

</details>

ポイントを確認しましょう。

- `timeout-minutes: 30` でタイムアウトを設定しています。CI が無限に実行されるのを防ぎます
- `--max-turns 5` でターン数を制限しています。API のコストを管理するための設定です。[2-3-8 GitHub Actions](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-8_GitHub%20Actions.md) で学んだ通り、学習段階では 5 ターンで十分です
- `prompt` で CLAUDE.md と rules を参照するよう指示しています。CourseHub のコーディング規約に基づいたレビューが行われます

> 💡 GitHub Actions で Claude Code が実行されると、PR にレビューコメントが自動的に追加されます。これは「AI によるレビュー」であり、人間のレビューの代わりではありません。AI のレビュー指摘を確認し、必要に応じて修正した上で、チームメンバーの人間レビューを受けましょう。

### settings.json のチーム共有設定を整備する

[3-1-3 プロジェクトの規約・設定を確認する](../chapter-01_実践の準備/3-1-3_プロジェクトの規約・設定を確認する.md) で `.claude/settings.json` と `.claude/settings.local.json` を更新しましたが、改めてチーム共有の観点で整理します。

```
> .claude/settings.json を確認して、チームで共有すべき設定が揃っているか確認してください。
> 以下の観点でチェックしてください:
> - Sail コマンドの許可が設定されているか
> - Git コマンドの許可が設定されているか
> - 帰属表示（attribution の commit / pr）の方針が設定されているか
> - 個人設定が混入していないか
```

Claude Code が現在の settings.json を分析し、不足や問題を指摘してくれます。

チーム共有設定のポイントを整理しましょう。

**`.claude/settings.json`（Git にコミット）に含めるもの**:

```json
{
  "permissions": {
    "allow": [
      "Bash(./vendor/bin/sail *)",
      "Bash(./vendor/bin/sail artisan *)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git push *)",
      "Bash(git checkout *)",
      "Bash(git branch *)",
      "Bash(git merge *)",
      "Bash(git log *)",
      "Bash(git diff *)",
      "Bash(git status)"
    ]
  }
}
```

> 📝 あなたの環境では、[3-1-3 プロジェクトの規約・設定を確認する](../chapter-01_実践の準備/3-1-3_プロジェクトの規約・設定を確認する.md) での更新内容に応じて異なる設定になっている場合があります。上記はチーム共有に最低限必要な設定の目安です。

**`.claude/settings.local.json`（Git にコミットしない）に入れるもの**:

```json
{
  "permissions": {
    "allow": [
      "Read(/Users/yourname/**)"
    ]
  }
}
```

個人のディレクトリパスに依存する設定は Local scope に分離します。これにより、チームメンバーの環境が異なっても設定が衝突しません。

> ⚠️ `.claude/settings.local.json` が `.gitignore` に含まれていることを確認してください。個人の設定が誤ってリポジトリにプッシュされると、他のメンバーの環境で問題が発生します。

### CLAUDE.md の運用方針を確認する

[3-1-3 プロジェクトの規約・設定を確認する](../chapter-01_実践の準備/3-1-3_プロジェクトの規約・設定を確認する.md) で CLAUDE.md を更新しましたが、今後の運用方針を確認しておきましょう。

CLAUDE.md はプロジェクトの進行とともに更新される「生きたドキュメント」です。[3-6-1 AI時代のチーム開発](3-6-1_AI時代のチーム開発.md) で学んだ通り、以下のタイミングで更新します。

- **新しいライブラリの導入時**: 技術スタック欄に追記
- **コーディング規約の変更時**: `.claude/rules/` を更新
- **新しいコマンド体系の追加時**: コマンド欄に追記
- **PR レビューで規約の不備が見つかったとき**: rules に規約を追記

```
> CLAUDE.md の現在の内容を確認して、
> 以下が記載されているかチェックしてください:
> - Sail コマンド体系（sail artisan, sail composer 等）
> - コース構造（Course > Chapter > Lesson > Quiz）
> - ユーザーロールと権限の概要
> - コーディング規約の方針（またはrules への参照）
> - テスト実行コマンド
```

不足があれば Claude Code に追記を依頼します。

> 💡 CLAUDE.md の変更もコードの変更と同じく、PR でレビューを受けてマージするのが理想です。「AI への指示」もチームの合意で管理する文化を作りましょう。

---

## 🏃 実践③: ワークフローの Skill 化

Part 3 を通じて、いくつかの作業パターンを繰り返してきました。こうした繰り返しのワークフローを Skill として定義すると、チーム全員が同じ手順で作業できます。

### どのワークフローを Skill 化するか

Part 3 で繰り返した作業パターンを振り返りましょう。

| 作業パターン | 登場 Chapter | Skill 化の価値 |
|---|---|---|
| コードレビュー（自己レビュー） | 3-6（実践①） | 高: PR 前に毎回実行する |
| バグ調査（症状→再現→調査→修正） | 3-3 | 中: バグ報告のたびに使う |
| テスト実行 | 3-3, 3-4, 3-5 | 既存（`/test`）: [3-1-3 プロジェクトの規約・設定を確認する](../chapter-01_実践の準備/3-1-3_プロジェクトの規約・設定を確認する.md) で修正済み |
| リファクタリング計画 | 3-5 | 中: 改善タスクのたびに使う |

ここでは、最も汎用性が高い「コードレビュー」を Skill として定義します。

### Step 1: Skill ファイルを作成する

```
> .claude/skills/review/ ディレクトリに、コードレビュー用の Skill を作成してください。
>
> 要件:
> - ブランチの全変更を対象にレビューする
> - rules/coding.md のコーディング規約への準拠を確認する
> - テストの有無を確認する
> - セキュリティ上の問題を確認する
> - 不要なデバッグコードの検出
> - 結果をカテゴリ別（規約違反・テスト不足・セキュリティ・その他）に報告する
```

<details>
<summary>生成される Skill の例を確認する（クリックで展開）</summary>

> 📝 あなたの環境では異なるコードが生成されます。

```markdown
# .claude/skills/review/SKILL.md
---
name: review
description: ブランチの変更をコーディング規約・テスト・セキュリティの観点でレビューする
user-invocable: true
---

main ブランチからの差分を対象にコードレビューを実行してください。

## レビュー観点

1. **コーディング規約**（`.claude/rules/coding.md` を参照）
   - Form Request の使用
   - 命名規則（camelCase / snake_case）
   - Controller の責務（薄く保つ）

2. **テスト**
   - 新機能に Feature テストがあるか
   - 既存テストが壊れていないか

3. **セキュリティ**
   - Policy による認可が適切か
   - バリデーションが十分か
   - デバッグコード（dd, dump, console.log）が残っていないか

4. **品質**
   - N+1 クエリの可能性
   - 不要なファイルや残留コード

## 出力形式

カテゴリ別に問題を報告してください:

- 🔴 **必須修正**: 規約違反、セキュリティ問題
- 🟡 **推奨修正**: テスト不足、品質改善
- 🟢 **問題なし**: 特記事項なし

問題がない場合もその旨を報告してください。
```

</details>

ポイントを確認しましょう。

- `user-invocable: true` で、`/review` と入力するだけで実行できます
- レビュー観点に `.claude/rules/coding.md` への参照を含めています。規約が更新されれば、Skill のレビュー内容も自動的に最新の規約に基づきます
- 出力形式を指定することで、レビュー結果が読みやすくなります

### Step 2: 動作確認

作成した Skill を実行して動作を確認します。

```
/review
```

<!-- TODO: 画像追加 - /review Skill の実行結果 -->

レビュー結果がカテゴリ別に表示されます。指摘内容が的確か、漏れがないかを確認しましょう。

> 💡 Skill の内容は運用しながら改善していくものです。実際にレビューを繰り返す中で「この観点が抜けている」「この指摘は不要」と気づいたら、SKILL.md を更新してください。

### Skill のチーム共有

作成した Skill は `.claude/skills/` ディレクトリにあるため、リポジトリにコミットすればチーム全員が使えます。

```
> review Skill をコミットしてください。
```

### Plugin への発展

Skill は単一プロジェクト向けの仕組みですが、複数のプロジェクトで同じ Skill を使いたい場合は **Plugin** にまとめることができます。

[2-3-6 Plugins](../../part-02_Claude%20Codeの基礎/chapter-03_機能を使いこなす/2-3-6_Plugins.md) で学んだ通り、Plugin は以下の構造で Skill・Hooks・MCP 設定などをパッケージ化します。

```
my-laravel-plugin/
├── .claude-plugin/
│   └── plugin.json        # マニフェスト（名前・バージョン・説明）
├── skills/
│   ├── review/SKILL.md    # コードレビュー Skill
│   ├── test/SKILL.md      # テスト実行 Skill
│   └── lint/SKILL.md      # Lint 実行 Skill
└── settings.json          # デフォルト設定
```

Plugin にすると、以下のメリットがあります。

- **バージョン管理**: Plugin のバージョンを指定して利用できる
- **名前空間**: Skill 名が `my-laravel-plugin:review` のように名前空間付きになり、他の Plugin との衝突を避けられる
- **配布**: チーム内の他のプロジェクトにも導入できる

> 📝 Plugin への変換は、今すぐ必要ではありません。CourseHub の Skill が安定してきたら、他のプロジェクトでも使えるよう Plugin 化を検討してみてください。

---

## 🔍 見極めチェック

> 🧠 先輩エンジニアの思考: 「PR は"動くコード"を届けるだけじゃない。"なぜこう変えたか"の説明と、"チームが使える環境"を届けるのが本当の仕事。特に settings.json や CLAUDE.md は、自分がいなくなった後のチームメンバーのために整備する。次に入ってくるジュニアが Claude Code をスムーズに使い始められるかを想像しよう。」

- [ ] **正しさ**: PR の説明が変更内容を正確に反映しているか。GitHub Actions のワークフローが正しく動作するか（テスト PR で確認）
- [ ] **品質**: settings.json の Project scope と Local scope が適切に分離されているか。CLAUDE.md に必要な情報が記載されているか。Skill が再利用可能な形で定義されているか
- [ ] **安全性**: API キーが GitHub Secrets に格納されているか（コードに直接書いていないか）。settings.json に過剰な権限（`Bash(rm *)` 等）が含まれていないか

> 🔑 この Section では特に「品質」に注目してください。コードの品質だけでなく、チーム全体の開発環境の品質を整備することが、この Chapter のテーマです。

---

## Part 3 ふりかえり

Part 3 の全 Chapter を振り返り、学んだことを整理しましょう。

### Chapter ごとの学び

| Chapter | テーマ | 方法論（概念） | 実践（混合） | 見極めの重点 |
|---|---|---|---|---|
| 3-1 実践の準備 | 環境と基盤 | 70-30 モデル、説明責任の導入 | セットアップ、規約・設定の確認 | - |
| 3-2 既存コードを理解する | コードリーディング | 全体像→構造→フロー、知らない技術への向き合い方 | Sub-agents での探索、業務フロー追跡 | - |
| 3-3 バグを修正する | バグ修正 | 報告→再現→調査→修正→検証 | 進捗率バグ、認可バグ、500 エラー | **安全性** |
| 3-4 機能を開発する | 機能開発 | 要件理解→設計→実装→検証 | 小テスト再受験、コースレビュー | **品質** |
| 3-5 コードを改善する | リファクタリング | 対象特定→テスト確認→改善→テスト再実行 | Fat Controller 分離、N+1 解消 | **正しさ** |
| 3-6 チームに共有する | チーム開発 | 説明責任、レビュー、帰属表示 | PR 作成、GitHub Actions、Skill 化 | **品質** |

### Part 2 機能の実務活用

Part 2 で学んだ機能が、Part 3 の実務コンテキストでどのように活用されたかを振り返ります。

| Part 2 機能 | Part 3 での活用 |
|---|---|
| CLAUDE.md / rules | プロジェクトの規約を Claude Code に伝え、規約に従ったコードを生成させる（全 Chapter） |
| Sub-agents | コードベースの広範な探索、複数ファイルの並列分析（3-2） |
| MCP | データベースの直接確認、外部ツール連携（3-2） |
| `/compact` / `/context` | 長い作業セッションでのコンテキスト管理（3-2, 3-5） |
| `/btw` | コードリーディング中の補足質問（3-2） |
| プロンプト設計 | バグの症状・再現手順・期待値を構造化して伝える（3-3） |
| `/rewind` | 修正が期待通りでない場合の巻き戻し（3-3） |
| `/test` | 修正・開発・リファクタリングの各フェーズでの動作確認（3-3, 3-4, 3-5） |
| セッション管理 | `--continue` / `--resume` で長い機能開発を途中再開（3-4） |
| Plan Mode | 設計の計画立案、段階的なリファクタリング計画（3-4, 3-5） |
| Hooks | コミット前の自動フォーマット（3-4） |
| `/simplify` | 機能開発後の品質チェック（3-4） |
| Worktree | 独立した改善の並列作業（3-5） |
| `/cost` | トークン使用量の確認（3-5） |
| `/commit` / `/diff` | 変更の確認とコミット（3-6） |
| GitHub Actions | PR への自動レビュー（3-6） |
| 権限管理 | settings.json のチーム共有設定（3-6） |
| Skills | ワークフローの定義とチーム共有（3-6） |
| Plugins | Skill のパッケージ化と配布（3-6） |

### 2つの能力の成長

この教材では「使いこなす力」「見極める力」「学び続ける力」の3つの能力を養うことをゴールとしています。Part 3 で鍛えた2つの能力を確認しましょう。

**使いこなす力**: Claude Code の機能を実務タスクの種類（バグ修正・機能開発・リファクタリング）に応じて使い分けられるようになりました。「どの機能を使うか」ではなく「このタスクにどの機能が有効か」という判断ができるようになっています。

**見極める力**: 正しさ・品質・安全性の3観点で AI 生成コードを検証し、責任を持って採用する判断ができるようになりました。Chapter ごとに重点を変えた見極めチェックを通じて、バグの種類や変更の性質に応じた検証の勘所を身につけました。

残る **学び続ける力** は Part 4 で扱います。知らない技術（Service クラス、Event/Listener）に遭遇したときの対処フローを Part 3 で体験しましたが、この力を習慣として定着させる方法を Part 4 で学びます。

---

### ✅ 完成チェックリスト

- [ ] 説明責任を意識した PR が作成されている（変更の目的・アプローチ・検証内容・影響範囲が記載されている）
- [ ] GitHub Actions のワークフローファイルが作成されている
- [ ] API キーが GitHub Secrets に格納されている（コードに直接書いていない）
- [ ] `.claude/settings.json` にチーム共有設定が整備されている
- [ ] `.claude/settings.local.json` に個人固有の設定が分離されている
- [ ] CLAUDE.md にプロジェクトの主要情報が記載されている
- [ ] コードレビュー Skill が作成され、動作確認済みである
- [ ] 上記の変更がコミットされている

---

## ✨ まとめ

- **説明責任を意識した PR**: 「なぜこの変更か」「どう検証したか」を PR 本文に明記する。Claude Code で自己レビューを行い、レビュアーの負荷を下げる
- **GitHub Actions**: PR への自動レビューを設定する。`--max-turns` と `timeout-minutes` でコストを管理する。AI レビューは人間レビューの補助であり、代替ではない
- **チーム設定の整備**: `.claude/settings.json`（Project scope）にチーム共有設定、`.claude/settings.local.json`（Local scope）に個人設定を分離する。CLAUDE.md は「生きたドキュメント」として継続的に更新する
- **Skill 化**: 繰り返し使うワークフローを Skill として定義し、チーム全員が同じ手順で作業できるようにする。安定したら Plugin にまとめて複数プロジェクトで共有する
- **Part 3 の集大成**: コードを書くだけでなく、チームに届けるまでが仕事。説明責任・環境整備・ワークフロー共有の3つを通じて、チーム全体の生産性を高める

---

Part 3 はこれで完了です。ここまでで、Claude Code と協働して実務タスクを遂行する力と、AI 生成コードを自ら検証・判断する力を身につけました。

Part 4 では、この力を **維持し、進化させ続ける** 方法を学びます。AI ツールは急速に進化しており、今日のベストプラクティスが明日には変わっている可能性があります。情報収集・新機能検証・実務適用の習慣を作り、変化に適応し続けるエンジニアを目指しましょう。
