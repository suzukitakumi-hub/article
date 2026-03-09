---
name: make-article
description: "リライト対象記事を自動調査し、seo-article WFを実行してWPに下書き保存するまでの一連フローを実行する。「今日の記事作って」「記事作って」などのトリガーで起動。"
---

# make-article スキル

## このスキルが起動するとき
- 「今日の記事作って」「記事作って」「/make-article」などのユーザー発話
- seo-article WFの実行とWP下書き投稿をセットで行いたいとき

## このスキルを使わないとき
- キーワード・記事を手動指定して記事を書くとき（通常の seo-article WF を使う）
- WPへの投稿なしで記事を書くだけのとき

---

## フロー概要

```
Step1: リライト候補調査（自動）
Step2: 候補をユーザーに提示 → 承認を得る（必須）
Step3: seo-article WF を実行（Phase1〜5）
Step4: WP 下書き保存（wp_post.py）
Step5: 結果報告
```

---

## Step1: リライト候補調査

**1-A: SERanking MCP で順位データ取得（MCPが使える場合は最優先）**

`seranking-internal` MCPの `get_keyword_rankings` を呼び出す:
- `days`: 7
- `limit`: 100
- `top_n`: 0

**11〜20位のKW**を抽出し、ボリューム順に並べる。これがリライト最優先候補となる。

**1-B: rewrite_queue.py の実行**

```bash
python scripts/rewrite_queue.py --json --top 5
```

- 出力は JSON 形式で取得する
- `top_candidates` の上位3〜5件を取得する
- スクリプトが失敗した場合は、エラーを伝え手動でキーワードを指定してもらう

**1-C: 候補の統合と絞り込み**

1-Aと1-Bの結果を照合し、以下のルールで最終候補を3〜5件に絞る:
- 1-A（MCP順位11〜20位）と1-B（rewrite_queue）の両方に出たKWを最優先
- 1-Aのみ: ボリュームが高い場合は採用
- 1-Bのみ: スコアが高い場合は採用
- 直近30日以内に対応済みのKWは除外

## Step2: 候補提示 → ユーザー承認（必須・スキップ不可）

調査結果を以下の形式でユーザーに見せる：

```
リライト候補 TOP 3（優先度順）

1. 【スコア XX】記事タイトル
   URL: https://...
   理由: ...

2. ...

3. ...

どれをリライトしますか？（番号で回答、またはキーワードを直接入力）
```

**ユーザーの回答を必ず待つ。承認なしに Step3 へ進んではならない。**

ユーザーが「1番」「これ」などと回答したら、以下を確定して Step3 へ進む：
- `{target_url}` : 対象記事の URL
- `{target_slug}`: URL末尾のスラッグ
- `{wp_post_id}` : rewrite_queue の JSON にある `wp_id`（WP投稿ID）

**`wp_id` が JSON に含まれていない場合（WP API 未使用時）は以下で取得する：**
```bash
python -c "
import os, requests
from requests.auth import HTTPBasicAuth
# .env 読み込み
with open('.env') as f:
    for l in f:
        l=l.strip()
        if '=' in l and not l.startswith('#'):
            k,_,v=l.partition('='); os.environ[k.strip()]=v.strip()
slug='{target_slug}'
r=requests.get(os.environ['WP_URL']+'/wp-json/wp/v2/posts',
    auth=HTTPBasicAuth(os.environ['WP_USER'],os.environ['WP_APP_PASSWORD']),
    params={'slug':slug,'status':'any','per_page':1,'_fields':'id,slug,title'})
print(r.json())
"
```
投稿IDが取得できなかった場合は `wp_post_id` を空欄のまま Step4 で通常フローに任せる。

## Step3: seo-article WF を実行

seo-article ワークフローを以下のパラメータで実行する：

- `target_keyword`: ユーザーが指定、または rewrite_queue の top_queries[0] を使用
- `article_purpose`: リード獲得（デフォルト。ユーザーから指示があれば上書き）
- `mode`: rewrite
- `base_article_html_or_url`: Step2 で確定した `{target_url}`

WF は通常どおり Phase1〜5 を順番に実行する。
Phase4 で HTML が `articles/{slug}_rewrite.html` に出力されたら Step4 へ進む。

## Step4: WP 下書き保存

**`{wp_post_id}` が判明している場合（リライト）：**
```bash
python scripts/wp_post.py articles/{slug}_rewrite.html --post-id {wp_post_id} --yes
```
- `--post-id` を明示することで slug推定を完全にバイパス。誤上書きゼロ。

**`{wp_post_id}` が不明の場合（新規 or ID取得失敗）：**
```bash
python scripts/wp_post.py articles/{slug}_rewrite.html --yes
```
- この場合 `wp_post.py` 内でスラッグ検索が走り、既存記事が見つかれば追加確認プロンプトが表示される（`--yes` でもスキップされない安全設計）

実行後、投稿IDと編集URLを Step5 の報告に含める。

## Step5: 結果報告

以下の情報をユーザーに報告する：

```
✅ 完了しました

記事タイトル : {title}
WP 投稿ID   : {post_id}
編集URL     : {wp_url}/wp-admin/post.php?post={post_id}&action=edit

次のステップ:
1. 上記 URL を開いて内容を確認
2. アイキャッチ画像を設定
3. Yoast SEO のスコアを確認
4. 問題なければ「公開」ボタンを押す
```

---

## エラー処理

| エラー状況 | 対応 |
|-----------|------|
| rewrite_queue.py が失敗 | エラーを伝え、キーワードの手動入力を求める |
| .env が未設定 | .env.example を参照して設定するよう案内する |
| wp_post.py が失敗 | エラーログを表示し、HTMLファイルのパスをユーザーに伝える（手動投稿を促す） |
| WF が途中で失敗 | 通常の seo-article WF のエラー処理に従う |

---

## 安全上の制約（変更不可）

- WPへの **DELETE** は絶対に呼ばない
- ステータスは **draft（下書き）固定**。公開はユーザーが手動で行う
- **1回の実行で投稿できるのは1記事のみ**
- Step2 のユーザー承認と Step4 の確認を **絶対にスキップしない**
