# Part 4: 継続的な学習
→ 能力: 学び続ける力
→ ゴール: ツール・技術の進化を追い、自ら試し、実務に適応し続けるための習慣を身につける
→ ハンズオンなし（読み物中心）

## MECE 設計方針

分類軸: **学習サイクルのフェーズ**（CLAUDE.md「学び続ける力」の3要素に対応）

| 分類軸 | Chapter | Section MECE 軸 | Section 1 | Section 2 |
|---|---|---|---|---|
| **収集** | 4-1 情報収集 | 情報源の種類 | 一次情報源 | SNS・コミュニティ |
| **検証** | 4-2 新機能の検証 | 検証プロセスのフェーズ | 準備と実施 | 確認と記録 |
| **判断** | 4-3 実務への適用判断 | 判断のフェーズ | 判断基準 | 導入と定着 |

## Chapter 4-1 情報収集（2セクション）

**ゴール**: Claude Code と AI ツールの最新動向を効率的に把握し、破壊的変更にも速やかに追従できる。

MECE 軸: **情報源の種類**

- **4-1-1 一次情報源の活用**
  - ゴール: 公式ドキュメント・変更履歴から正確な情報を把握し、破壊的変更に追従できる
  - 記述パターン: 概念
  - Subsection:
    - 公式ドキュメント — 公式ドキュメントの構成と読み方を理解する
      - 公式ドキュメント（code.claude.com/docs）の構成と読み方
      - ドキュメントの更新頻度と信頼性
    - 変更履歴とアップデート — 変更を検知し追従する
      - Changelog・リリースノートの確認方法（`/release-notes`）
      - Claude Code のアップデート確認と追従（`claude update`、Homebrew / WinGet の場合）
      - 破壊的変更・非推奨化を検知したときの対応フロー
  - 公式ドキュメント: [Overview](https://code.claude.com/docs/en/overview)

- **4-1-2 SNS・コミュニティでのキャッチアップ**
  - ゴール: X やコミュニティから最新の活用事例・ベストプラクティスを収集できる
  - 記述パターン: 概念
  - Subsection:
    - SNS での情報収集 — X でのフォロー推奨アカウント・ハッシュタグを知る
      - X でのフォロー推奨アカウント・ハッシュタグ
      - GitHub Discussions・Issues での情報収集
    - コミュニティとブログ — 日本語圏の活用事例を収集する
      - 日本語コミュニティ・ブログでの活用事例
      - AI コーディングツール全般の動向を追う（Claude Code に限定しない視野）
  - 公式ドキュメント: なし（外部リソース中心）

## Chapter 4-2 新機能の検証（2セクション）

**ゴール**: 新しい機能やツールを自ら手を動かして試し、動作・制約・互換性を確認できる。

MECE 軸: **検証プロセスのフェーズ**

- **4-2-1 検証の準備と実施**
  - ゴール: 新機能のリリースを知ってから、手を動かして試すまでの手順を理解する
  - 記述パターン: 概念
  - Subsection:
    - 検証の準備 — リリースノートから変更内容を読み解き、検証環境を用意する
      - リリースノートから変更内容を読み解く
      - 検証環境を用意する（使い捨てプロジェクト、Git ブランチ）
    - 検証の実施 — 公式ドキュメントの例を再現し、自分のユースケースで試す
      - 公式ドキュメントの例を再現する → 自分のユースケースで試す
      - 教材で深く扱わなかった機能の検証例:
        - Agent Teams（複数セッションの協調。実験的機能）
        - Agent SDK / Headless Mode（プログラマティックな実行。CI/CD 連携）
        - Remote Control（ローカルセッションを他デバイスから継続）
        - Desktop アプリの Scheduled Tasks（永続的な定期実行。セッション内 `/loop` との違い）
        - Chrome 連携（ライブ Web アプリのデバッグ）
        - Slack 連携（`@Claude` でバグ報告から PR 作成）
        - GitLab CI/CD（GitHub Actions の GitLab 版）
  - 公式ドキュメント: [Agent Teams](https://code.claude.com/docs/en/agent-teams), [Headless](https://code.claude.com/docs/en/headless), [Remote Control](https://code.claude.com/docs/en/remote-control), [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks), [Chrome](https://code.claude.com/docs/en/chrome), [Slack](https://code.claude.com/docs/en/slack), [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd)

- **4-2-2 結果の確認と記録**
  - ゴール: 検証で何を確認すべきかを理解し、結果を記録・共有できる
  - 記述パターン: 概念
  - Subsection:
    - 確認の観点 — 何を確認すべきかを理解する
      - 動作・制約・既存ワークフローとの互換性
    - 記録と共有 — 検証結果を記録し、チームに共有する
      - 検証結果の記録方法（`CLAUDE.md` への反映、チームへの共有）
      - 「使わない」判断の記録も残す重要性
  - 公式ドキュメント: [Memory](https://code.claude.com/docs/en/memory)

## Chapter 4-3 実務への適用判断（2セクション）

**ゴール**: 検証した機能やツールを自分の開発フローに取り入れるべきかを評価・判断し、学び続ける習慣を定着させる。

MECE 軸: **判断のフェーズ**

- **4-3-1 適用判断の基準**
  - ゴール: 新機能の採用・見送りを論理的に判断できる
  - 記述パターン: 概念
  - Subsection:
    - 判断基準 — 採用・見送りの判断軸を理解する
      - 判断基準: 生産性向上・品質向上・学習コスト・リスク
      - 見送る判断の重要性（新しい＝良いとは限らない）
    - ポリシーとの整合 — 企業・チームのポリシーとの整合性を確認する
      - 企業・チームのポリシーとの整合性確認
      - Managed settings による制約の理解
  - 公式ドキュメント: [Settings](https://code.claude.com/docs/en/settings), [Data Usage](https://code.claude.com/docs/en/data-usage)

- **4-3-2 導入と定着のプロセス**
  - ゴール: 判断した機能を段階的に導入し、学び続けるサイクルを習慣化できる
  - 記述パターン: 概念
  - Subsection:
    - 段階的な導入 — 個人からチームへ段階的に導入する
      - 段階的な導入（個人で試す → チームに提案 → 全体導入）
    - 学び続けるサイクル — 情報収集 → 検証 → 判断の反復を習慣化する
      - 月次の振り返り: `CLAUDE.md` と設定の定期的な見直し
      - 学び続けるサイクルの定着（情報収集 → 検証 → 判断 の反復）
  - 公式ドキュメント: [Memory](https://code.claude.com/docs/en/memory), [Best Practices](https://code.claude.com/docs/en/best-practices)
