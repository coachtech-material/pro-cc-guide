# 2-7-1 Git 操作と `/diff`

## 概要

ここまでの Chapter では、セクションの終わりに「💡 ここまでの変更をコミットしておきましょう」と案内してきました。皆さんはそのたびに Git 操作を行い、変更を記録してきたはずです。

しかし、振り返ってみてください。コミットメッセージは適切でしたか? 不要なファイルがコミットに含まれていませんでしたか? 本当に意図した変更だけが記録されていますか? 実務では、コードを書く時間と同じくらい、変更を整理して共有する時間が重要です。レビュー担当者が読むのはコードそのものではなく、**差分（diff）** だからです。

Claude Code は Git と深く統合されています。コミットメッセージの自動生成、差分のインタラクティブな確認、ブランチの作成と管理。これらの操作を Claude Code から行うことで、変更の管理を効率化しつつ、diff を確認する習慣を身につけましょう。

## Git 操作

### ここまでの変更を整理する

2-2-2 で初回コミットと GitHub push を行ってから、多くの機能を追加してきました。認証・認可、Tag、Comment、Series、公開ワークフロー UI、Form Request、テスト、Hooks。皆さんのプロジェクトにはこれらの変更が蓄積されています。

まず、現在の状態を確認しましょう。新しいセッションを起動します。

```bash
claude -n "git-management"
```

プロジェクトの Git 状態を確認するところから始めます。

```
> 現在の Git の状態を確認して、未コミットの変更やファイルの一覧を教えてください。
```

Claude Code は `git status` や `git diff --stat` を実行し、変更されたファイル、新規追加されたファイル、未追跡のファイルを一覧で報告します。皆さんのプロジェクトの状態はそれぞれ異なりますが、多くのファイルが変更・追加されているはずです。

### `claude commit` でコミットする

Claude Code には、変更を分析してコミットメッセージを自動生成する機能があります。インタラクティブモードの外から直接実行できます。

一度セッションを終了して、ターミナルから以下を実行します。

```bash
claude commit
```

Claude Code は変更内容を分析し、適切なコミットメッセージを提案します。提案されたメッセージを確認し、承認するとコミットが作成されます。

変更が多い場合は、機能ごとに分けてコミットしたいこともあります。その場合は、インタラクティブモードで Claude Code に指示します。

```bash
claude -n "git-organize"
```

```
> ここまでの未コミットの変更を、機能ごとにまとめてコミットしてください。
> 例えば認証・認可、タグ・コメント・シリーズ、UI、テスト、Hooks のように分けてください。
```

皆さんの環境では異なるコードが生成されます。以下は一例です。Claude Code が `git add` と `git commit` を機能単位で繰り返し、以下のようなコミット履歴を作成します。

```
feat: add authentication with Fortify and role-based authorization
feat: add Tag, Comment, and Series models with relationships
feat: add publishing workflow UI with status badges and admin approval
feat: add Form Request validation and feature tests
chore: configure PHP CS Fixer with PostToolUse hook
```

コミットメッセージの形式（`feat:` や `chore:` など）は Conventional Commits という慣習に従っています。Claude Code はプロジェクトの既存のコミット履歴を参考にメッセージのスタイルを合わせるため、皆さんのプロジェクトでは異なるスタイルになることもあります。

### `/diff` で差分を確認する

コミットする前に、差分を確認する習慣をつけましょう。Claude Code には `/diff` コマンドが用意されています。

インタラクティブモード内で以下を実行します。

```
> /diff
```

`/diff` はインタラクティブな diff ビューアを開きます。

- **左右の矢印キー**: 現在の Git diff と、Claude Code の各ターンごとの diff を切り替え
- **上下の矢印キー**: ファイル間を移動

Git diff は `git diff` コマンドの結果と同じですが、Claude Code のターンごとの diff は独自の機能です。Claude Code がどのターン（指示）でどのファイルを変更したかを個別に確認できます。「この指示でどのファイルが変わったのか」を追跡するのに便利です。

💡 `/diff` はコミット前の最終確認に使いましょう。意図しない変更が含まれていないか、debug 用のコードが残っていないかを確認してからコミットする習慣が、実務でのコードレビューの質を上げます。

### ブランチの作成と管理

実務では、機能ごとにブランチを作成して開発します。Claude Code からブランチを作成してみましょう。

```
> 新しいブランチ「feature/git-practice」を作成して切り替えてください。
```

Claude Code は `git checkout -b feature/git-practice` を実行します。ブランチの作成、切り替え、削除といった Git 操作は、Claude Code に自然言語で指示するだけで実行できます。

## GitHub への push

### 変更を GitHub に push する

ローカルでコミットしただけでは、コードは皆さんのマシンにしか存在しません。GitHub に push して安全に保管しましょう。

main ブランチに戻してから push します。

```
> main ブランチに切り替えて、GitHub に push してください。
```

Claude Code は `git checkout main` と `git push` を実行します。2-2-2 で GitHub リポジトリを作成して push しているので、リモートリポジトリの設定は済んでいるはずです。

### push 前の安全確認

push する前に、必ず確認すべきことがあります。

```
> .env ファイルや認証情報がコミットに含まれていないか確認してください。
```

Claude Code は `.gitignore` の設定と、コミット履歴に機密ファイルが含まれていないかをチェックします。

⚠️ よくあるエラー: `.env` がコミットに含まれている

```
warning: .env is tracked by git
```

**原因**: `.gitignore` に `.env` が含まれていない、または `.gitignore` の設定前に `.env` をコミットしてしまった

**対処法**: Claude Code に「.env を Git の追跡から外してください」と指示します。`git rm --cached .env` で追跡を解除し、`.gitignore` に追加する対応を行います

実務では、`.env` や API キー、データベースの接続情報がリポジトリに含まれていると、重大なセキュリティインシデントになります。push 前の確認は省略しないでください。

## 見極めチェック

- [ ] **正しさ**: コミット履歴が機能単位で整理されているか。各コミットに意図した変更だけが含まれているか
- [ ] **品質**: `/diff` で確認したとき、debug 用の `dd()` や `dump()`、`console.log()` が残っていないか。テスト用のハードコードされた値や、コメントアウトされたコードが放置されていないか
- [ ] **安全性**: `.env` ファイルや認証情報（API キー、パスワード、トークン）がコミットに含まれていないか。`.gitignore` が適切に設定されているか

> このセクションでは特に「品質」に注目してください。diff を確認する習慣は、実務でのプルリクエストレビューに直結します。レビュー担当者の視点で差分を読み、「この変更は意図通りか?」を自分で判断できることが重要です。

## 公式ドキュメント

- [Common Workflows](https://code.claude.com/docs/en/common-workflows)（Git 操作・PR 作成・Worktree を含むワークフロー集）
- [Built-in commands](https://code.claude.com/docs/en/commands)（`/diff` コマンドのリファレンス）

## まとめ

- Claude Code は Git と深く統合されており、`claude commit` で変更分析とコミットメッセージ自動生成を行えます
- `/diff` コマンドでインタラクティブな diff ビューアを開き、Git diff と Claude Code のターンごとの diff を切り替えて確認できます
- 機能ごとにコミットを分け、push 前に `.env` や認証情報の混入を確認する習慣を身につけましょう
- これらの Git 操作は、この先の Chapter では日常的に行います。「コードを書いたら diff を確認してコミット」を当たり前にしていきましょう

次のセクションでは、Git とは別の安全ネットである「チェックポイント」を学びます。Claude Code に大きな変更をさせて失敗したとき、即座に巻き戻せる仕組みです。
