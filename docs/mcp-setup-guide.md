# MCP設定ガイド（AI向け）

このドキュメントはAntigravityで利用可能な3つのMCPサーバーの構成・起動方法・使い方をまとめたものです。

---

## 設定ファイルの場所

```
C:\Users\suzuki.takumi\.gemini\antigravity\mcp_config.json
```

Antigravityを起動すると、このファイルを読み込んで3つのMCPサーバーが自動起動します。手動での起動操作は不要です。

---

## 1. GA4（Google Analytics 4）

**サーバー名**: `google-analytics`

```json
{
  "command": "C:\\Users\\suzuki.takumi\\.local\\bin\\uvx.exe",
  "args": ["--from", "google-analytics-mcp", "ga4-mcp-server"],
  "env": {
    "GOOGLE_APPLICATION_CREDENTIALS": "C:\\Users\\suzuki.takumi\\Desktop\\AI\\記事作成_TCJ\\micro-environs-470717-j2-41ae07afc25f.json",
    "GA4_PROPERTY_ID": "517064395"
  }
}
```

**主なツール例**
- セッション数・ユーザー数・コンバージョン数の取得
- ページ別・流入元別の分析

**使用例（AIへの指示）**
```
「先週のGA4のセッション数を取得して」
「2月のオーガニック流入数を教えて」
```

---

## 2. Google Search Console

**サーバー名**: `gsc`

```json
{
  "command": "npx",
  "args": ["-y", "mcp-server-gsc"],
  "env": {
    "GOOGLE_APPLICATION_CREDENTIALS": "C:\\Users\\suzuki.takumi\\Desktop\\AI\\記事作成_TCJ\\micro-environs-470717-j2-41ae07afc25f.json",
    "GSC_SITE_URL": "https://gaikoku-jinzai.tcj-education.com/"
  }
}
```

**主なツール例**
- クリック数・表示回数・CTR・平均掲載順位の取得
- クエリ別・ページ別の検索パフォーマンス

**使用例（AIへの指示）**
```
「昨日のSearch ConsoleのCTRを教えて」
「先月クリックが多かったページTOP10を教えて」
```

---

## 3. SE Ranking（内部API）

**サーバー名**: `seranking-internal`

```json
{
  "command": "python",
  "args": ["C:\\Users\\suzuki.takumi\\Desktop\\AI\\記事作成_TCJ\\mcp_servers\\seranking\\server.py"]
}
```

**設定ファイル**
```
C:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\mcp_servers\seranking\.env
```

**利用可能なツール**

| ツール名 | 機能 |
|---|---|
| `get_keyword_rankings` | 自サイトのKW順位・ボリューム（登録済みKW） |
| `get_llm_rankings` | AI検索（ChatGPT/Gemini/Perplexity）での言及順位 |
| `get_competitor_keywords` | 競合サイトとのKW重複・順位比較 |
| `get_competitor_avg_positions` | 競合との平均順位推移（週次/月次） |
| `research_keyword` | 任意KWの調査（ボリューム・難易度・関連KW等） |

**使用例（AIへの指示）**
```
「SERankingで直近7日のキーワード順位を取得して」
「外国人採用 についてキーワード調査して」
「競合サイトとのKW重複を分析して」
```

**セッション更新（Cookieが切れたとき）**
```powershell
cd C:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\mcp_servers\seranking
python refresh_cookies.py
```
→ 実行後、次のSERanking呼び出しから自動反映（Antigravity再起動不要）

---

## よくある問題

| 症状 | 対処 |
|---|---|
| SE Ranking が `403 No access` | `refresh_cookies.py` を実行してCookieを更新 |
| SE Ranking が `unknown tool` | Antigravityを再起動（初回設定後のみ） |
| GA4/GSC が認証エラー | サービスアカウントJSONファイルの存在を確認 |
