---
name: seo-phase1-intent
description: "SEO記事作成のPhase1を実行する。ターゲットキーワードの検索意図分析、記事の本軸決定、ゴールシナリオ設定を行う。seo-articleワークフローのPhase1で使用。"
---

# Phase1：入力受付＋検索意図分析

## このスキルを使うとき
- seo-articleワークフローのPhase1実行時
- ユーザーが検索意図の分析を依頼したとき

## このスキルを使わないとき
- Phase2以降の作業時（別のスキルを使う）

## セッション開始前チェック（必須・スキップ禁止）
1. `.agent/lessons.md` を読み、Phase1または検索意図分析に関連する教訓を確認する
2. `data/phase_outputs/phase1_output.json` が存在する場合は削除してから開始する（前回の残骸を引き継がない）

## 手順

### Step0：既存GSC実績の解決（任意）
以下の優先順位で `gsc_csv_path` を決定する。

1. `{gsc_csv_path}` が渡されている場合はそれを採用
2. `{gsc_property}` と `{gsc_service_account_json}` がある場合は `scripts/export_gsc_api_csv.py` を実行して生成
3. どちらもない場合はGSC実績なしで進行

自動生成時の実行例（必要に応じて日付を調整）：

```bash
python scripts/export_gsc_api_csv.py \
  --property "{gsc_property}" \
  --start-date {gsc_start_date} \
  --end-date {gsc_end_date} \
  --service-account-json "{gsc_service_account_json}" \
  --output "data/gsc/gsc_{gsc_start_date}_{gsc_end_date}.csv"
```

`gsc_csv_path` が解決できた場合、CSVを読み込み、`{target_keyword}` に関連する実績を先に確認する。
最低限、以下を抽出してStep1の分析に反映する。

- 主要クエリ（Impressions上位）
- クエリ別CTRと平均掲載順位
- 低CTR（表示は多いがクリックされていない）クエリ
- 11〜20位帯のクエリ（改善余地が高い）

このStepは「ウェブ検索の代替」ではなく「自サイト実績の補強情報」として扱う。
`gsc_csv_path` を解決できなかった場合は、未使用理由を1行で明記してStep1へ進む。

### Step0.5：SERanking KW調査（必須・GSC取得の直後に実行）

`seranking-internal` MCPの `research_keyword` を呼び出す:
- `keyword`: `{target_keyword}`
- `limit`: 20

取得した情報をStep1〜Step3の分析に反映する:

| 取得項目 | 活用箇所 |
|---|---|
| `main.volume` / `main.difficulty` | 狙い甲斐の評価（難易度が高すぎる場合は類似KWへシフトを検討） |
| `suggestions.similar` | Step1のサジェストKW補強・関連検索KWとして活用 |
| `suggestions.questions` | Step3のPAA代替・記事内Q&Aセクションの設問候補 |
| `suggestions.longtail` | 記事タイトル・H2/H3候補・内部リンク対象KWの把握 |
| `suggestions.related` | ギャップ分析（Phase2）の事前インプットとして記録しておく |

加えて、`get_keyword_rankings` で `{target_keyword}` の**現在のTCJ順位**を確認する（`top_n: 0` で全件取得後に検索）:
- 1〜10位: 維持戦略で書く（情報更新・CTA改善が主）
- 11〜30位: リライトで1ページ目入りを狙う（内容の深化が主）
- 圏外: 競合に対して差別化できる切り口が必須

SERanking MCPが利用不可の場合は、この手順をスキップし「SERanking MCPなし」と1行記載して次へ進む。

### Step1：検索意図の4要素分析
{target_keyword}でウェブ検索し、最新の検索結果・サジェストキーワード・関連キーワードを確認する。
**Step0.5で取得した `suggestions.similar` / `suggestions.questions` も合わせて参照**し、ウェブ検索だけでは拾えない意図を補完する。
以下の4要素で分析する。各要素について「記事でどう扱うか」を具体的に明記すること。

1. **顕在ニーズ**：読者が明確に認識している問題や疑問
2. **心理的負担**：検索背景にある不安、ストレス、迷い
3. **心理的負担を和らげる対策**：安心感を与える表現や提案
4. **潜在ニーズ**：読者がまだ気づいていないが関連する課題

### Step2：記事の本軸の決定
以下の2択から決定し、選定理由を明記する。
- 解決手順：読者の目の前のトラブルを解決するための手順・方法
- 事実：この世の事象の原因や事実を説明

### Step3：読者のゴールシナリオ設定
2パターンを設定する。
- 記事内容を参考にした場合：記事の提案を実行した理想の未来
- 記事内容を参考にしなかった場合：記事を読まずに行動した場合の失敗シナリオ

記事への反映方針：
- リード文 →「参考にしなかった場合」の失敗シナリオで共感を作る
- 本文 →「参考にした場合」の成功シナリオを具体的に描く
- まとめ → 成功シナリオで締める

### Step4：Phase1ゲートJSON出力（必須・省略禁止）

Step1〜3が全て完了したら、以下の形式で `data/phase_outputs/phase1_output.json` を出力する。
値は実際に分析した内容を埋めること。空文字・nullは禁止。
`mode=rewrite` の場合は `existing_article_diagnosis` も必須。

```json
{
  "intent_4elements": {
    "latent_needs": "（分析内容）",
    "psychological_burden": "（分析内容）",
    "psychological_relief": "（分析内容）",
    "explicit_needs": "（分析内容）",
    "article_handling": "（記事での扱い方）"
  },
  "article_axis": "解決手順 or 事実",
  "article_axis_reason": "（選定理由）",
  "goal_scenario": {
    "if_read": "（参考にした場合のシナリオ）",
    "if_not_read": "（参考にしなかった場合のシナリオ）"
  },
  "existing_article_diagnosis": null
}
```

## ゲート条件（すべて満たすまで次のPhaseに進めない）

**【機械ゲート】Phase2を開始する前に必ず実行すること：**
```bash
python .agent/scripts/gate_check.py --phase 1 --file data/phase_outputs/phase1_output.json --mode {mode}
```
→ EXIT 0 になるまでPhase2を開始しない。EXIT 1 の場合はStep4のJSONを修正して再実行する。

- [ ] 検索意図4要素の分析を出力済み（各要素の「記事での扱い方」含む）
- [ ] 記事の本軸（解決手順/事実）を決定済み
- [ ] ゴールシナリオ2パターンを出力済み
- [ ] `data/phase_outputs/phase1_output.json` を出力し、機械ゲートがEXIT 0になった
