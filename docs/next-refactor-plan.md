# Next Refactor Direction Overview

## 1. Slash Command Audit (upstream/master)

| Command | Primary Purpose | Claude Code 標準コマンドとの重複 | 評価メモ |
|---------|-----------------|------------------------------------|----------|
| `analyze` | 多角的なコード品質/脆弱性/性能分析 | ❌ | 総合診断ワークフロー。既存標準より深い分析シナリオ指定が可能。維持候補。 |
| `brainstorm` | 要件発散とマルチエージェント協調 | ❌ | サブエージェントと MCP を組み合わせる高度モード。独自価値が大きい。 |
| `build` | 実装着手前の詳細計画と編集波制御 | ⚠️ (一部類似) | 標準 `/build` とは別物で Wave/Checkpoint 指針が記載。差別化を確認の上維持検討。 |
| `business-panel` | ビジネス視点レビュー | ❌ | 標準にない経営・PM 観点でのレビュー。保持推奨。 |
| `cleanup` | 後片付け・リファクタリング整理 | ⚠️ | Claude 標準 `/cleanup` に近いが、PM Agent 手順・証跡要求が追加されている。要再評価。 |
| `design` | アーキテクチャ設計プロトコル | ❌ | マルチエージェントで設計ドキュメントを生成。保持推奨。 |
| `document` | ドキュメント整備ワークフロー | ❌ | 情報取得・検証・更新を含む詳細フロー。 |
| `estimate` | 工数/リスク見積もり | ❌ | プロダクトマネジメント寄り。保持推奨。 |
| `explain` | 仕様/コード説明生成 | ⚠️ | 標準 `/explain` と役割が近い。独自の証跡・自己チェックがあるか確認要。 |
| `git` | Git 操作ガイドライン | ✅ | Claude 標準の Git コマンド群と機能的に重複。削除候補。 |
| `help` | SuperClaude コマンド一覧 | ✅ | `/sc:help` 専用。最小構成には必要。 |
| `implement` | 実装フェーズ全体の進行管理 | ⚠️ | 標準 `/implement` よりテレメトリ・証跡要求が厳密。差分把握の上で統合/維持を判断。 |
| `improve` | 改善・リファクタリング提案 | ⚠️ | 構造は標準 `/improve` に類似だが、confidence 連動が追加。 |
| `index` | リポジトリ理解/探索指針 | ❌ | インデックス生成や利用まで含む。保持推奨。 |
| `load` | セッションコンテキスト読込 | ❌ | 外部記憶活用プロトコル。保持推奨。 |
| `pm` | PM Agent 本体仕様 | ❌ | フレームワークの中核。必須。 |
| `reflect` | Reflexion ループ | ❌ | 自己評価・再試行フレーム。保持推奨。 |
| `research` | 深掘りリサーチ手順 | ⚠️ | `/research` は標準にもあるが、MCP 指定と証跡要件が詳細。差別化方針を確認。 |
| `save` | 成果物まとめ・終了処理 | ❌ | アーカイブとメモリ更新フロー。保持推奨。 |
| `select-tool` | ツール選択判断 | ❌ | MCP 含むツールポリシー。保持推奨。 |
| `spawn` | サブエージェント分派 | ❌ | マルチエージェント編成。保持推奨。 |
| `spec-panel` | 仕様レビュー委員会モード | ❌ | 標準にない専門家レビュー。保持推奨。 |
| `task` | タスク分解・進捗管理 | ⚠️ | 標準 `/task` と重なるが、PM Agent 計測が追加。差分分析要。 |
| `test` | テスト戦略と証跡管理 | ⚠️ | `/test` 類似。追加要件有無を精査。 |
| `troubleshoot` | 障害調査プロトコル | ❌ | incident 対応ワークフロー。保持推奨。 |
| `workflow` | 波動的ワークフロー制御 | ❌ | Wave/Checkpoint 概念まとめ。保持推奨。 |

**分類ルール**
- ✅: 完全重複（Claude Code 標準で代替可能） → 削除/統合候補  
- ⚠️: 部分重複（差別化内容を再確認して決定）  
- ❌: 独自価値が高い → 再収録優先

後続作業で `⚠️` グループについて差分調査と戻し方針を決める。

### 1.1 `⚠️` グループ詳細調査（upstream/master 抜粋）

- **build**  
  - Playwright MCP を結合し、ビルド完了時レポート生成・最適化指針まで含めた DevOps 専用フロー。  
  - Claude 標準 `/build` より CI/CD 文脈の最適化・エラー解析が充実。→ **維持価値高**。  
- **cleanup**  
  - Architect/Quality/Security personas の多面的チェック、Sequential + Context7 MCP 連携、安全ロールバック付き。  
  - 標準 `/cleanup` より「安全性評価・ペルソナ連携」が差別化要素。→ **SuperClaude 版として再収録推奨**。  
- **explain**  
  - Educator persona と MCP を連動させ受講者レベル別の説明を生成。標準 `/explain` では扱わない学習指向の段階制御が特徴。  
  - → **教育用途で独自価値**。  
- **implement**  
  - Context7, Magic, Playwright, Sequential などを自動起動し multi-persona でコード生成～検証まで進める大規模フロー。  
  - 標準 `/implement` は単体生成寄りなので差別化が明確。→ **維持必須**。  
- **improve**  
  - 種別（quality/performance/maintainability/security）ごとに専門 persona を起用し、安全な改善ループを提供。  
  - 技術負債削減や安全面で強い価値。→ **維持推奨**。  
- **research**  
  - Tavily/Serena/Sequential/Playwright MCP を組み合わせた深掘り調査。タスク分解比率やアウトプット保存先まで定義。  
  - 標準 `/research` より高度な multi-hop 指針。→ **維持必須**。  
- **task**  
  - Epic→Story→Task の階層構造、マルチエージェント協調、Serena を利用したセッション継続など PM 特化。  
  - 標準機能では提供されない高機能タスク管理。→ **維持必須**。  
- **test**  
  - QA persona と Playwright MCP を活用し、テスト種別ごとの検出・監視・自動修復提案まで含む。  
  - 標準 `/test` よりカバレッジレポートや e2e 自動化指針が詳細。→ **維持価値高**。

=> 上記 8 コマンドは「名称の偶然一致はあるが、SuperClaude 仕様として明確に強化された振る舞い」を持つ。  
   → Framework 再集約時に **すべて再収録** し、標準との違いをドキュメントに残す方針で合意したい。

### 1.2 コマンド別ソースと今後の扱い案

| Command | Source of truth | 推奨ハンドリング | 補足 |
|---------|-----------------|-------------------|------|
| `analyze` | SuperClaude オリジナル | Super Agent が自動発火（必要なら `/sc:analyze` も維持） | 調査フェーズ開始時に自動診断として呼び出し候補。 |
| `brainstorm` | SuperClaude オリジナル | Super Agent 内部モードへ吸収 | 初動ヒアリング時に自動呼び出し、ユーザー入力は任意化。 |
| `build` | Claude 標準名 + SuperClaude拡張 | Super Agent 内部（CI/CD 監視に連動） | 人手で呼ぶより build wave 中に自動判断させる。 |
| `business-panel` | SuperClaude オリジナル | Super Agent から選択的に提示 | 経営観点レビューが必要なときだけ案内。 |
| `cleanup` | Claude 標準名 + 拡張版 | Super Agent の実装後フェーズに統合 | self-review 後に必要なら自動で走らせる。 |
| `design` | SuperClaude オリジナル | Super Agent 内の設計モードとして保持 | 明示コマンドも残し、設計特化タスクで案内。 |
| `document` | SuperClaude オリジナル | 自動ドキュメント更新ワークフローに組み込み | 成果報告時にトリガー。 |
| `estimate` | SuperClaude オリジナル | 明示コマンド維持 + Super Agent から提案 | 工数見積り要求時の専用エントリ。 |
| `explain` | Claude 標準名 + 拡張版 | Super Agent が教育モードとして起動 | 学習支援目的なら明示コマンドも残す。 |
| `git` | Claude 標準そのもの | 削除候補 | 標準 `/git` へ誘導。 |
| `help` | SuperClaude 専用 | 維持必須 | `/sc:*` 列挙のトップレベル。 |
| `implement` | Claude 標準名 + 拡張版 | Super Agent 実装フェーズのコアとして保持 | ユーザーにはフェーズ説明のみ提示。 |
| `improve` | Claude 標準名 + 拡張版 | Reflexion / Self-review ループに統合 | メンテナンスモードで自動使用。 |
| `index` | SuperClaude オリジナル | `/sc:index-repo` として維持 | インデックス生成専用。 |
| `load` | SuperClaude オリジナル | Super Agent SessionStart に統合 | 手動コマンド不要化。 |
| `pm` | SuperClaude オリジナル | Super Agent 起動プロトコル（非公開） | 仕様書としては保持するが slash コマンドは廃止方向。 |
| `reflect` | SuperClaude オリジナル | Reflexion ループへ統合 | 状況に応じ自動で回す。 |
| `research` | Claude 標準名 + 拡張版 | `/sc:research` 維持（深度指定付き） | 深堀り案件で Super Agent が推奨。 |
| `save` | SuperClaude オリジナル | Super Agent 完了処理に統合 | 終了時に自動実行。 |
| `select-tool` | SuperClaude オリジナル | Super Agent の MCP 選定ロジック内で活用 | 手動入力は廃止方向。 |
| `spawn` | SuperClaude オリジナル | Super Agent のサブエージェント管理で利用 | 並列タスク時だけ内部的に使用。 |
| `spec-panel` | SuperClaude オリジナル | エキスパートレビュー要請時に Super Agent が提示 | slash コマンドはオプションとして残す。 |
| `task` | Claude 標準名 + 拡張版 | Super Agent の計画フェーズで利用 | 直接コマンドは軽量版に統合検討。 |
| `test` | Claude 標準名 + 拡張版 | 実装波後に自動実行 | 明示 `/sc:test` は e2e/coverage 指定が必要な場合のみ案内。 |
| `troubleshoot` | SuperClaude オリジナル | インシデント時の自動ハンドラー | slash コマンドも残しつつ、失敗検知で自動案内。 |
| `workflow` | SuperClaude オリジナル | Super Agent の全体フレーム説明用に保持 | 参考ドキュメントとして提示。 |

### 1.3 Agent Audit（upstream/master）

| Agent | 役割 | Claude 標準重複 | 推奨ハンドリング |
|-------|------|-----------------|-------------------|
| backend-architect | バックエンド設計 | ❌ | Super Agent 内で必要時に招集 |
| business-panel-experts | ビジネス視点パネル | ❌ | `/sc:business-panel` 連動 or Super Agent 推奨 |
| deep-research-agent | 深掘り調査 | ❌ | `/sc:research` の中核（既に再配置済み） |
| devops-architect | DevOps 専門家 | ❌ | build/CI 流れで自動呼び出し |
| frontend-architect | フロント設計 | ❌ | UI 系タスクで Super Agent がアサイン |
| learning-guide | 学習支援 | ❌ | `/sc:explain` の補助エージェント |
| performance-engineer | 性能最適化 | ❌ | `/sc:analyze` / `/sc:improve` で使用 |
| pm-agent | PM オーケストレータ | ❌ | Super Agent 自身として再定義済み |
| python-expert | Python 専門家 | ❌ | 実装対象言語に応じ自動招集 |
| quality-engineer | 品質管理 | ❌ | テスト/レビュー段階で起動 |
| refactoring-expert | リファクタ専門家 | ❌ | `/sc:improve` 内部に吸収 |
| requirements-analyst | 要件分析 | ❌ | 初期探索で自動呼び出し |
| root-cause-analyst | 根本原因分析 | ❌ | `/sc:troubleshoot` に組み込み |
| security-engineer | セキュリティ | ❌ | 高リスクタスクで招集 |
| socratic-mentor | 問答法ガイド | ❌ | `/sc:brainstorm` 補助 |
| system-architect | システム全体設計 | ❌ | 大規模設計で自動招集 |
| technical-writer | 技術ライター | ❌ | `/sc:document` や完了報告で使用 |

- 現時点で Framework 側に戻したのは `deep-research`, `repo-index`, `self-review` の 3 件のみ。  
- 他エージェントは Super Agent のモジュール化計画と合わせて `plugins/superclaude/agents/` へ随時再配置する。

## 2. ドキュメント鮮度・外部記憶フロー骨子

1. **SessionStart Hook**  
   - `PROJECT_INDEX.json` 存在確認 → 読込。  
   - 生成日時と `git diff --name-only` から変化量スコアを算出。  
   - しきい値（例: 7 日超または変更ファイル 20 超）でステータスを `fresh|warning|stale` 判定。
2. **着手前スカフォールド**  
   - ステータスをユーザーへ表示（例: `📊 Repo index freshness: warning (last updated 9 days ago)`）。  
   - `warning/stale` なら `/sc:index-repo` 提案、同時に差分ドキュメント一覧を提示。  
   - Memory（例: `docs/memory/*.md`）の更新日時と最終利用時刻を比較し、古いものをリストアップ。
3. **ドキュメント検証ループ**  
   - タスクで参照した docs/ ファイルごとに `mtime` を記録。  
   - 処理中に矛盾を検知した場合は `🛎️ Stale doc warning: docs/foo.md (last update 2023-08-01)` を即時出力。  
   - 自己評価（confidence/reflection）ループ内で docs 状態を再確認し、必要に応じて質問や再調査を要求。
4. **完了時アウトプット**  
   - 使用したドキュメントとインデックス状態を成果報告に含める。  
   - 必要なら `PROJECT_INDEX` の再生成結果をメモリに書き戻し、鮮度メトリクス（更新日/対象ファイル数/差分）を記録。

## 3. サブエージェント・自己評価テレメトリ指針

- **起動ログ**: エージェントやスキルを呼び出すたび短い行で表示  
  - 例: `🤖 Sub-agent: repo-index (mode=diagnose, confidence=0.78)`  
  - 例: `🧪 Skill: confidence-check → score=0.92 (proceed)`  
- **自己評価ループ**: `confidence >= 0.9` で進行、閾値未満なら自動で再調査フェーズへ遷移  
  - ループ開始時に `🔁 Reflection loop #2 (reason=confidence 0.64)` のように表示。  
- **出力レベル**: デフォルトは簡潔表示、`/sc:agent --debug` 等で詳細ログ（投入パラメータ、MCP 応答要約）を追加。  
- **HUD メトリクス**: タスク完了報告に最新 confidence/self-check/reflection 状態をまとめる  
  - `Confidence: 0.93 ✅ | Reflexion iterations: 1 | Evidence: tests+docs`

## 4. Framework ↔ Plugin 再編ロードマップ（骨子）

1. **資産の再導入**  
   - `plugins/superclaude/commands/`, `agents/`, `skills/`, `hooks/`, `scripts/` を Framework リポに新設し、upstream/master のコンテンツを復元。  
   - `manifest/` テンプレートと `tests/` を併設し、ここを唯一の編集ポイントにする。
2. **ビルド・同期タスク**  
   - `make build-plugin`: テスト→テンプレート展開→`dist/plugins/superclaude/.claude-plugin/` 出力。  
   - `make sync-plugin-repo`: 上記成果物を `../SuperClaude_Plugin/` へ rsync（クリーンコピー）。PR 時にも生成物を同梱。  
3. **Plugin リポの役割変更**  
   - 生成物のみを保持し、「直接編集禁止」の README と CI ガードを配置。  
   - 必要に応じて Git subtree/submodule で `dist` を取り込む運用も検討。
4. **ドキュメント更新**  
   - `CLAUDE.md`, `README.*`, `PROJECT_INDEX.*` を新構成に合わせて刷新。  
   - 旧 25 コマンドに関する説明はアーカイブへ移し、現行仕様を明確化。

この整理をベースに、分類 `⚠️` の追加調査やワークフロー/ログ出力の詳細設計を次段階で実施する。

## 5. 計測・検証ロードマップ

1. **コマンド効果測定**  
   - 代表タスク（軽微修正／バグ修正／大規模実装）を定義し、Super Agent のみ vs `sc:*` 併用でセッションログを取得。  
   - 計測項目: 総トークン数、経過時間、試行回数、残タスク有無。
2. **ビルド & 配布検証**  
   - `make build-plugin` 実行 → `dist/plugins/superclaude/.claude-plugin/` のサイズ・構成を記録。  
   - `make test` および `.claude-plugin/tests/` をフル実行し、失敗時ログを保存。  
3. **SessionStart 診断ベンチ**  
   - リポジトリの変更量を操作し、インデックス鮮度判定の挙動と出力ログ（fresh/warning/stale）の正確性を検証。  
   - ドキュメント矛盾検出時のアナウンス内容を確認。  
4. **トークンコスト可視化**  
   - それぞれのコマンド・エージェントを有効／無効にしたケースで平均トークン消費を算出し、`docs/next-refactor-plan.md` にグラフ/表で追加。  
5. **成果共有**  
   - 上記結果をもとに「残す／統合する／削除する」の意思決定表を更新。  
   - 変更内容をまとめたドラフト PR 用メモを作成（最終決定前に再レビューを受ける）。
