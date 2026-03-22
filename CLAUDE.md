# COACHTECH Pro生向け Claude Code 教材

> ジュニアエンジニア（Pro生）が Claude Code を活用し、実務開発の生産性と品質を高めるための教材。

## ペルソナ（WHO）

プログラミングスクール COACHTECH の選抜試験を経てフリーランスエージェントに所属しているジュニアエンジニア。COACHTECH ではこの層を「Pro生」と呼ぶ。企業に紹介され、副業・フリーランス・転職などの形で Laravel を使った実務開発に携わる。基礎力はあるが実務はこれから。

### 前提知識

- **Laravel**: MVC、Eloquent ORM、認証（Fortify）、認可（Policy）、バリデーション、ミドルウェア、RESTful API、PHPUnit
- **フロントエンド**: HTML/CSS、Tailwind CSS の基礎
- **データベース**: RDB設計（正規化、ER図）、SQL（JOIN、サブクエリ、集計）
- **開発プロセス**: 要件定義→DB/API設計→実装→テストの一連のフロー
- **開発環境・ツール**: ターミナル、Docker Compose、Git/GitHub（ブランチ運用、PR、コードレビュー）
- **AI活用**: ChatGPT を少し触った程度。AI コーディングツールの経験は問わない

## コンセプト（WHY）

AI で一人の生産性が上がり企業の採用が慎重になる中、Pro生 がミドル・シニア相当のバリューを出せるよう Claude Code を使いこなせるようになることを目指す。

## ゴール（WHAT）

Claude Code と協働して、実務タスク（バグ修正・機能開発・リファクタリング）を高速かつ高品質に遂行できるようにする。**コードリーディング** を前提に、既存プロジェクトのコーディング規約と設計方針に従いながら遂行する。これを支える3つの能力を養う:

1. **使いこなす力（Input）**: Claude Code の機能・設定・制約を把握し、目的に応じて的確に活用する力
2. **見極める力（Output）**: 生成コードを正しさ・品質・安全性の3観点で検証し、責任を持って採用する力
3. **学び続ける力（Time）**: ツール・技術の進化を追い、自ら試し、実務に適応し続ける力

## カリキュラム（HOW）

| Part | 対応する能力 | 概要 | ハンズオン |
|---|---|---|---|
| Part 1: はじめに | — | 教材の導入、Claude Code の概要 | なし |
| Part 2: Claude Code の基礎（3 Chapter） | 使いこなす力 + 見極める力（型の導入） | 主要機能を習得（セットアップ → 基本理解 → 機能実践） | Ch1: 自分のプロジェクト作成 / Ch2: 座学 / Ch3: スターターキットで実践 |
| Part 3: Claude Code の実践 | 見極める力 + 使いこなす力（総合演習） | 既存プロジェクトで実務タスクを遂行 | 提供プロジェクトで実践 |
| Part 4: 継続的な学習 | 学び続ける力 | 情報収集・新機能検証・実務適用の習慣化 | なし |

Part > Chapter > Section の3層構造。各 Part の設計詳細は `outline/` を参照。

CLAUDE.md は教材の哲学（WHO / WHY / WHAT / HOW）を定義し、`outline/` はその哲学を具体的な設計に落とし込む。執筆上の判断（題材の選択・構成のアレンジ・外部調査）は `outline/` の設計に従いつつ、臨機応変に行うこと。

## プロジェクトマップ（MAP）

執筆ルールは `.claude/rules/writing.md` を参照。

### Skills

| Skill | 用途 |
|---|---|
| `/write` | 教材の執筆（Part / Chapter / Section 単位。新規・更新・ブラッシュアップ） |
| `/review` | 教材のレビュー（Part / Chapter / Section 単位。品質・整合性チェック） |
| `/outline` | outline の作成・更新・検証（再構成・MECE 検証・公式ドキュメント照合） |
| `/check-updates` | 公式ドキュメントとの鮮度チェック |

### フォルダ構造・命名規則

```
pro-cc-guide/
├── CLAUDE.md              # 教材の哲学・カリキュラム・プロジェクトマップ
├── outline/               # カリキュラム設計（Part/Chapter/Section 設計）
│   └── part-01.md ~ part-04.md
├── .claude/
│   ├── skills/            # 作業手順（執筆・レビュー・更新・構成変更）
│   └── rules/             # 表記ルール
├── curriculums/           # 教材本体
│   └── part-XX_タイトル/chapter-XX_タイトル/X-X-X_タイトル.md
├── assets/                # 画像（assets/part-XX/chapter-XX/）
└── memo/                  # 作業メモ置き場（教材の執筆プロセスでは参照しない）
```

- Part ディレクトリ: `part-XX_タイトル/`（01始まり、ゼロパディング）
- Chapter ディレクトリ: `chapter-XX_タイトル/`（Part 内で01始まり、ゼロパディング）
- Section ファイル: `X-X-X_タイトル.md`（Part番号-Chapter番号-Section番号、ゼロパディングなし）
- 画像ファイル名: 内容がわかる英語名（例: `install-confirmation.png`）
- Part 設計ファイル: `outline/part-XX.md`（ゼロパディング）
