# 2-5-1 Skills でプロンプトを再利用する

## 概要

前の Chapter では、Plan Mode で計画を立ててから認証・認可・状態遷移を実装しました。Claude Code に大きな機能を任せる流れが掴めてきたところです。

ここから先、テック記事プラットフォームにはタグ、コメント、シリーズといった機能を次々に追加していきます。モデルを追加するたびに「マイグレーション、リレーション、Controller、Blade、Route、Seeder を作って。CLAUDE.md のコマンド体系に従って」と毎回書くのは、率直に言って面倒です。

**Skills** を使えば、こうした定型的な指示を `/add-model` のようなスラッシュコマンドとして保存し、何度でも再利用できます。このセクションでは、Skills の仕組みを理解し、テック記事プラットフォーム用のカスタム Skill を実際に作ります。

## Skills の仕組み

### Skills とは何か

Skills は、Claude Code に追加できる **再利用可能なプロンプト** です。`SKILL.md` というファイルに指示を書いておくと、`/skill-name` で呼び出せるスラッシュコマンドになります。

たとえば、モデル追加の手順をまとめた Skill を `/add-model` として登録すれば、次のように使えます。

```
> /add-model Tag
```

これだけで、SKILL.md に書いた指示が Claude Code に渡され、Tag モデルに必要なファイル一式が生成されます。毎回同じ指示を書く必要はありません。

Skills には2つの使い方があります。

- **直接呼び出し**: `/skill-name` とタイプして手動で実行する
- **自動適用**: Claude Code が会話の文脈から「この Skill が関連しそうだ」と判断し、自動的に読み込む

今回作る `/add-model` のような作業手順は直接呼び出しが適しています。一方、コーディング規約のような「常に意識してほしい知識」は自動適用が便利です。

### SKILL.md の書き方

Skill は `SKILL.md` というファイルで定義します。ファイルは2つの部分で構成されます。

1. **フロントマター**（`---` で囲まれた YAML）: Skill のメタ情報
2. **本文**（Markdown）: Claude Code への指示

```yaml
---
name: add-model
description: プロジェクトの規約に従ってモデルを追加する
---

# モデル追加手順

1. マイグレーションを作成する
2. モデルクラスにリレーションを定義する
3. Controller と Blade テンプレートを作成する
...
```

フロントマターの主要なフィールドを見ていきましょう。

| フィールド | 説明 |
|---|---|
| `name` | Skill の名前。`/name` で呼び出せる。省略するとディレクトリ名が使われる |
| `description` | Skill の説明。Claude Code が自動適用するかどうかの判断に使う |
| `argument-hint` | 引数のヒント。オートコンプリート時に表示される（例: `[model-name]`） |
| `allowed-tools` | この Skill の実行中に許可するツール |
| `disable-model-invocation` | `true` にすると自動適用を無効にし、手動呼び出し専用になる |

これ以外にも `model`（使用するモデルの指定）、`effort`（推論の深さ）、`context`（サブエージェントでの実行）などのフィールドがあります。全フィールドの詳細は公式ドキュメントを参照してください。

### 配置場所とスコープ

Skill の配置場所によって、誰がその Skill を使えるかが変わります。

| スコープ | 配置場所 | 適用範囲 |
|---|---|---|
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | 自分のすべてのプロジェクト |
| Project | `.claude/skills/<skill-name>/SKILL.md` | このプロジェクトのみ |

この他に、組織全体に適用する **Enterprise** スコープや、Plugin 経由で配布する **Plugin** スコープもあります。詳細は公式ドキュメントを参照してください。ここでは、個人開発で日常的に使う Personal と Project の2つを押さえておきましょう。

Personal スコープは、どのプロジェクトでも共通して使いたい Skill に向いています。たとえば、自分のコードレビューの観点をまとめた Skill は、プロジェクトを問わず使えるので Personal に置くのが適切です。

Project スコープは、プロジェクト固有の Skill です。CLAUDE.md のコマンド体系やテスト方針を踏まえた Skill は、そのプロジェクトでしか意味がないため Project に配置します。`.claude/skills/` ディレクトリごと Git にコミットすれば、チームメンバーも同じ Skill を使えます。

💡 2-2-1 で作成した CLAUDE.md は「毎回のセッションで読み込まれるプロジェクトの基本情報」でした。Skills は「必要なときだけ呼び出す専門的な指示」です。CLAUDE.md に書きすぎるとコンテキストを圧迫しますが（2-3-2 で学びました）、Skills は呼び出されたときだけコンテキストに入るため、この問題が起きません。

### 引数を受け取る

Skills は呼び出し時に引数を受け取れます。引数は `$ARGUMENTS` プレースホルダーで参照します。

```yaml
---
name: add-model
description: プロジェクトの規約に従ってモデルを追加する
argument-hint: [model-name]
---

$ARGUMENTS モデルを以下の手順で追加してください。
```

`/add-model Tag` と実行すると、`$ARGUMENTS` が `Tag` に置き換わり、Claude Code は「Tag モデルを以下の手順で追加してください」という指示を受け取ります。

個別の引数にアクセスしたい場合は `$ARGUMENTS[0]`、`$ARGUMENTS[1]`（または短縮形の `$0`、`$1`）も使えます。

## モデル追加用 Skill を作る

### Skill ファイルを作成する

それでは、テック記事プラットフォーム用のモデル追加 Skill を作りましょう。プロジェクトの規約（CLAUDE.md に書いたコマンド体系やテスト方針）を踏まえた指示を Skill 化します。

Claude Code に Skill の作成を依頼します。

```
> .claude/skills/add-model/SKILL.md を作成してください。
> モデル追加用の Skill で、以下の内容を含めます。
>
> - name: add-model
> - description: プロジェクトの規約に従って新しいモデルを追加する
> - argument-hint: [model-name]
> - disable-model-invocation: true
>
> 本文には以下の手順を書いてください:
> 1. 引数で指定されたモデルのマイグレーション、モデルクラス、Controller、Blade テンプレート、Route、Seeder を作成する
> 2. 既存のモデルとのリレーションがあれば設定する
> 3. CLAUDE.md のコマンド体系に従い、sail artisan でマイグレーションを実行する
> 4. sail artisan db:seed で Seeder を実行してダミーデータを作成する
> 5. 実装後にブラウザで動作確認できるよう、主要な画面の URL を提示する
```

皆さんの環境では異なるコードが生成されます。以下は一例です。

```yaml
# .claude/skills/add-model/SKILL.md
---
name: add-model
description: プロジェクトの規約に従って新しいモデルを追加する
argument-hint: [model-name]
disable-model-invocation: true
---

# $ARGUMENTS モデルの追加

以下の手順で $ARGUMENTS モデルを追加してください。

## 手順

1. マイグレーションファイルを作成する
2. モデルクラスを作成し、fillable とリレーションを定義する
3. 既存モデルとのリレーションがあれば、既存モデル側にも逆リレーションを追加する
4. Controller を作成し、CRUD アクションを実装する
5. Blade テンプレートを作成する（既存の UI スタイルに合わせる）
6. Route を追加する
7. Seeder を作成してダミーデータを生成する

## 実行

- `sail artisan migrate` でマイグレーションを実行する
- `sail artisan db:seed --class=<Seeder名>` でダミーデータを投入する

## 確認

実装が完了したら、ブラウザで確認できる主要な URL を提示してください。
```

`disable-model-invocation: true` を指定しているため、Claude Code が自動的にこの Skill を使うことはありません。`/add-model Tag` のように手動で呼び出す専用です。モデル追加のような副作用のある操作は、意図しないタイミングで実行されると困るため、手動呼び出し専用にしておくのが安全です。

### Skill を確認する

作成した Skill が認識されているか確認しましょう。Claude Code に聞いてみてください。

```
> どんな Skills が使えますか？
```

Claude Code がプロジェクトの Skill 一覧を表示し、`/add-model` が含まれていれば成功です。

💡 Skill は `.claude/skills/` に配置した時点で自動的に認識されます。Claude Code の再起動は不要です。ファイルを編集した場合も、次回の呼び出しから変更が反映されます。

## Bundled Skills

Claude Code には最初から組み込まれた **Bundled Skills** があります。自分で作る Skills とは別に、すぐに使える便利なスラッシュコマンドです。代表的なものを紹介します。

| Skill | 用途 |
|---|---|
| `/simplify` | 直近の変更を3つの観点（コードの再利用・品質・効率性）で並列レビューし、改善を適用する |
| `/batch` | 大規模な変更を並列エージェントで処理する。コードベースを調査し、作業を分解して並列実行する |
| `/debug` | セッションのデバッグログを読み取り、問題を分析する |
| `/loop` | プロンプトを一定間隔で繰り返し実行する（例: `/loop 5m デプロイの状態を確認して`） |

特に `/simplify` は、機能を実装した後のコード品質改善に便利です。3つの並列エージェントが同時にコードをレビューし、重複コードの統合や不要な複雑さの除去を提案してくれます。

これらの Bundled Skills は、今後の Chapter でも場面に応じて使っていきます。

## 見極めチェック

- [ ] **正しさ**: SKILL.md のフロントマターが正しい YAML 構文で書かれているか。`name`, `description`, `argument-hint`, `disable-model-invocation` の各フィールドが適切に設定されているか
- [ ] **正しさ**: `/add-model Tag` と実行したとき、`$ARGUMENTS` が `Tag` に正しく置き換わるか。Claude Code が SKILL.md の手順に沿ってモデル追加を進めるか
- [ ] **品質**: SKILL.md の指示が CLAUDE.md のコマンド体系（`sail artisan` 等）と一致しているか。SKILL.md と CLAUDE.md で矛盾する指示を書いていないか
- [ ] **安全性**: この Section では該当なし

> この Section では特に「Skill の指示内容とプロジェクトの規約の一致」に注目してください。SKILL.md に書いた手順が CLAUDE.md の方針と矛盾していると、Claude Code が混乱した出力を返す原因になります。

## 公式ドキュメント

- [Skills](https://code.claude.com/docs/en/skills)（Skills の作成・設定・共有の詳細、全フロントマターフィールドのリファレンス）

## まとめ

- **Skills** は再利用可能なプロンプトを `/skill-name` で呼び出せるようにする仕組みです。`SKILL.md` ファイルに指示を書き、`.claude/skills/` に配置します
- `$ARGUMENTS` プレースホルダーで引数を受け取れます。`/add-model Tag` のように、Skill に動的な値を渡せます
- `disable-model-invocation: true` で手動呼び出し専用にすると、意図しないタイミングでの実行を防げます
- **Bundled Skills**（`/simplify`, `/batch`, `/debug`, `/loop`）は Claude Code に標準搭載されたスラッシュコマンドです

次のセクションでは、ここで作った `/add-model` Skill を実際に使って、テック記事プラットフォームに Tag・Comment・Series を追加していきます。
