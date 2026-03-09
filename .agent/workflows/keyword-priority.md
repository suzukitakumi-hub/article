---
description: キーワード優先度分析（SE Ranking MCP×既存記事）
---

# キーワード優先度分析ワークフロー

このワークフローは、SERanking MCP（リアルタイム）から順位データ・競合KWギャップを取得し、次に書くべきキーワードの優先度リストを生成します。CSVエクスポートファイルへの依存は不要です。

## 前提条件

- SERanking MCP（`seranking-internal`）が利用可能なこと
- `data/existing_articles/` または `reports/indexes/articles_master_index.csv` が整備されていること
- `data/article_archives/posts/` — 記事原稿アーカイブ（任意）

## 実行手順

### Step 1: SERanking MCP でライブデータ取得（必須）

**1-A: 現在のキーワード順位データ**

`seranking-internal` MCPの `get_keyword_rankings` を呼び出す:
- `days`: 7（直近7日）
- `limit`: 100
- `top_n`: 0（全件）

取得後、以下のセグメントに分類する:
- **11〜20位帯**（2ページ目前半）: リライト最優先候補。少しの改善で1ページ目に入れる
- **21〜50位帯**（2〜5ページ目）: ボリュームがあればリライト候補
- **圏外（null）かつボリューム≥200**: 新規記事候補
- **1〜10位**（1ページ目）: 維持確認のみ

**1-B: 競合KWギャップ**

`get_competitor_keywords` を呼び出す:
- `days`: 30
- `limit`: 50

競合が上位表示しているがTCJが取れていないKWを抽出する。

### Step 2: KW絞り込みと深掘り調査

Step1で上位候補として残ったKW（最大10件）を `research_keyword` で個別調査する。

各KWについて取得する情報:
- `main`: ボリューム・難易度スコア（difficulty）・CPC
- `suggestions.similar`: 類似KW（ボリュームtop3）
- `suggestions.questions`: 疑問文KW（記事構成に活用）

**優先度スコアリング基準**（合計点で順位付け）:
| 条件 | 加点 |
|---|---|
| 現在11〜20位 | +3点 |
| 現在21〜50位 | +1点 |
| ボリューム ≥ 500 | +3点 |
| ボリューム 200〜499 | +2点 |
| ボリューム 50〜199 | +1点 |
| 難易度スコア ≤ 30 | +2点 |
| 難易度スコア 31〜50 | +1点 |
| 競合KWギャップあり | +2点 |
| 既存記事なし（重複なし） | +2点 |
| 業界特化KW（特定技能・業種） | +1点 |

### Step 3: 既存記事との重複チェック

以下で既存記事リストと照合し、重複するKWを除外する:
```bash
python scripts/rewrite_queue.py --json --top 20
```
または `reports/indexes/articles_master_index.csv` を参照する。

直近30日以内に対応済みのKWも除外する。

### Step 4: 優先度リストの出力

上位5〜10件を以下の形式で出力し、`reports/keyword_priority_{YYYY-MM-DD}.md` に保存する:

```markdown
# キーワード優先度リスト {YYYY-MM-DD}

## TOP候補（リライト）

| 順位 | KW | 現在順位 | ボリューム | 難易度 | スコア | 推奨モード |
|---|---|---|---|---|---|---|
| 1 | ... | 15位 | 480 | 28 | 9点 | rewrite |

## TOP候補（新規）

| 順位 | KW | 現在順位 | ボリューム | 難易度 | スコア | 推奨モード |
|---|---|---|---|---|---|---|
| 1 | ... | 圏外 | 320 | 22 | 8点 | new |

## データソース
- 順位データ取得日時: {datetime}
- 競合KWギャップ期間: 直近30日
```

### Step 5: 次のアクション決定

優先度リストの上位3〜5件を確認し、記事作成を開始。
`make-article` スキルを起動するか、`seo-article` WFに直接渡す。

## フォールバック（MCP不達時）

SERanking MCPが利用不可（セッション切れ等）の場合:
1. `.agent/lessons.md` のセッション更新手順を確認
2. 一時的に `SERanking/` フォルダの最新CSVエクスポートで代替:
   ```bash
   python scripts/analyze_keyword_priority.py
   ```

## 出力ファイル

- `reports/keyword_priority_YYYY-MM-DD.md` — 優先度リスト（毎回上書き）

## 注意事項

- SERankingのセッションクッキーは数日〜数週間で失効する。401エラーが出たら `mcp_servers/seranking/.env` を更新すること
- 業界特化KW（特定技能×業種）は難易度が低くても戦略的に優先する
- 優先度リストは毎回上書きされるため、過去のリストは保存されない
