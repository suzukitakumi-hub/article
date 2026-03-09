# SE Ranking 内部API MCPサーバー 構築ドキュメント

**構築日**: 2026-03-05

---

## 概要

SERankingの内部API（非公式）をPythonで叩き、Antigravityから自然言語でキーワード順位・検索ボリュームを取得できるMCPサーバー。

```
AI（Antigravity）
    ↓
MCP（seranking-internal）
    ↓
SE Ranking 内部API（online.seranking.com）
    ↓
キーワード順位・検索ボリュームデータ
```

---

## ファイル構成

```
mcp_servers/seranking/
├── server.py          # MCPサーバー本体
├── .env               # セッションクッキー・サイトID設定（要更新）
└── requirements.txt   # 依存パッケージ
```

`mcp_config.json`（`C:\Users\suzuki.takumi\.gemini\antigravity\`）に `seranking-internal` として登録済み。

---

## 使用しているAPIエンドポイント

| 用途 | エンドポイント |
|---|---|
| キーワード一覧・ボリューム | `GET /api.projects.site.positions.html?do=keywordsList` |
| 順位データ（日別） | `GET /api.projects.site.positions.html?do=positions` |
| LLM/AI検索順位 | `GET /api.llm_rankings.html` |
| 競合KW比較 | `GET /api.competitors.overall.html?do=keywords` |
| 競合平均順位推移 | `GET /admin.site.competitors.chart.site_id-*.do-avgpos.html` |
| KW調査メイン（ボリューム・難易度） | `GET /research.keywords.html?json=appWrapData` |
| KWサジェスト（類似・関連・疑問文・ロングテール） | `POST /research.api.suggestion.html?do={type}` |

**固定パラメータ**
- `site_id`: `10028792`（TCJ プロジェクトID）
- `site_se_id`: `3025525`（Google Japan）
- 競合サイトID: `.env` の `SERANKING_COMPETITOR_IDS` で管理
- キーワードグループID: `.env` の `SERANKING_GROUP_ID` で管理

---

## 認証

SERankingはセッションクッキーで認証します。公式APIキーは不使用。

`.env` ファイルで管理：

```env
SERANKING_PHPSESSID=xxxx
SERANKING_SESUID=xxxx
SERANKING_SITE_ID=10028792
SERANKING_SITE_SE_ID=3025525
```

### クッキーの取得方法

1. ChromeでSERankingにログイン（`https://online.seranking.com`）
2. F12 → Network タブ → Fetch/XHR
3. 任意のAPIリクエストをクリック
4. Headers → Request Headers → `cookie:` の値から `PHPSESSID` と `SESUID` をコピー
5. `.env` を更新

**有効期限**: 数日〜数週間（ログアウトまたはセッション期限切れで無効化）

---

## MCPツール仕様

### `get_keyword_rankings`

キーワード一覧・現在の順位・検索ボリュームを返す。

| パラメータ | 型 | デフォルト | 説明 |
|---|---|---|---|
| `days` | int | 7 | 直近何日分のデータを取得するか |
| `page` | int | 1 | ページ番号 |
| `limit` | int | 100 | 1ページあたりのキーワード数 |
| `top_n` | int | 0 | 上位N位以内のみ返す（0=全件） |

### `get_llm_rankings`

ChatGPT・Gemini・PerplexityなどAI検索でのブランド言及データを返す。

### `get_competitor_keywords`

競合サイトとのキーワード重複状況・検索ボリューム・おすすめ単価を返す。

| パラメータ | 型 | デフォルト | 説明 |
|---|---|---|---|
| `days` | int | 30 | 調査期間の日数 |
| `limit` | int | 50 | 返却キーワード数 |
| `page` | int | 1 | ページ番号 |

### `get_competitor_avg_positions`

自サイトと競合サイトの平均順位推移を返す。

| パラメータ | 型 | デフォルト | 説明 |
|---|---|---|---|
| `period` | str | `week` | `week` または `month` |
| `top_range` | int | 10 | 上位N位までのKWで平均算出 |

### `research_keyword`

任意のキーワードをSERankingのキーワード調査機能で分析する。

| パラメータ | 型 | デフォルト | 説明 |
|---|---|---|---|
| `keyword` | str | 必須 | 調査するキーワード（例: 外国人 採用） |
| `limit` | int | 20 | 各サジェストカテゴリの取得件数 |

返却内容：
- `main` — ボリューム・難易度スコア・CPC等
- `suggestions.similar` — 類似キーワード
- `suggestions.related` — 関連キーワード
- `suggestions.questions` — 疑問文キーワード
- `suggestions.longtail` — ロングテールキーワード

**使用例（Antigravityへの指示）**
```
「SERankingで直近7日のキーワード順位を取得して」
「順位10位以内のキーワードを全部見せて」
「外国人 採用 のキーワード調査をして」
「特定技能 ドライバー の関連KWとボリュームを確認して」
「競合サイトとのKW重複を分析して」
「競合との平均順位推移を週次で見せて」
```

---

## セッション切れ時の更新手順

1. ChromeでSERankingにログイン
2. DevToolsでクッキーを取得（上記「クッキーの取得方法」参照）
3. `.env` の `PHPSESSID` と `SESUID` を新しい値に書き換える
4. Antigravityを再起動（MCPサーバーが自動的に新しい値を読み込む）

---

## 今後追加可能な機能

- 被リンク分析（被リンクタブのAPIをキャプチャすれば追加可能）
- サイト監査（SEOエラー）
- レポートビルダーデータ

---

## 注意事項

- SE Rankingの利用規約上、内部APIの直接利用は非推奨。利用は自己責任。
- 内部APIは予告なく変更される可能性がある。
- Core プラン（¥17,455/月）では公式APIは使用不可（Growth以上が必要）。
