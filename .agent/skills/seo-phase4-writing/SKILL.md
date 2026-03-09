---
name: seo-phase4-writing
description: "SEO記事作成のPhase4を実行する。Phase3の構成案に基づき記事全文をHTML形式で執筆する。seo-articleワークフローのPhase4で使用。"
---

# Phase4：完全執筆（HTML出力）

## このスキルを使うとき
- seo-articleワークフローのPhase4実行時
- Phase3の構成案に基づいて記事を執筆するとき

## このスキルを使わないとき
- Phase3が未完了のとき

## セッション開始前チェック（必須・スキップ禁止）
1. `.agent/lessons.md` を読み、Phase4または執筆に関連する教訓を確認する
2. `data/phase_outputs/phase3_output.json` の存在を確認する（なければPhase3からやり直す）
3. `data/phase_outputs/phase4_output.json` が存在する場合は削除してから開始する

## 大前提
- .agent/rules/writing-rules.md のルールを最初から適用して書く。書いた後に直すのではなく、最初から人間が書いたように書く。
- references/html-template.html のパーツを使ってHTML形式で出力する。
- references/llmo-rules.md のルールを適用する。
- 内部リンク実装時は `references/internal-link-selection-rules.md` と `references/topic-cluster-map.md` を参照する。
- **CTA・WP選定は必ず `references/cta-wp-reference.md` を参照する。記事トピックに対応するフォームURLとWPを選んでテンプレートに埋め込む。URLを手打ちしない。**
- **アイキャッチ画像（`<img>` タグ）を記事冒頭に出力しない。** プレースホルダー画像（placehold.jp等）も含め、アイキャッチ目的のimgタグは本文HTMLに一切含めない。アイキャッチはWordPress側で個別設定する。

## 手順

### Step1：タイトル・メタディスクリプションの作成
タイトル：
- {target_keyword}を左側に含める
- 32文字前後（最大36文字）
- 数字を入れる（例：「5つのポイント」「2026年版」）

メタディスクリプション：
- 120文字前後
- {target_keyword}を自然に含める

HTML本文の前にプレーンテキストで出力する。

### Step2：リード文の執筆
パーツ1（リード文）を使う。
- 第1〜2文：Phase1のゴールシナリオ「参考にしなかった場合」で共感
- 第3〜4文：悩みの背景にある課題を端的に伝える
- 第5〜6文：この記事で何がわかるか、権威性を伝える

{context_injection}が渡されている場合はFailure & RegretとStrong Stanceをリード文の核にする。

### Step3：本文の執筆（セクション単位）
Phase3の構成案のH2/H3/H4を上から順に、1セクションずつ執筆する。

各セクションの書き出し方：
- 見出し直下の第1〜2文でそのセクションの結論を端的に述べる（LLMO対策）
- その後に詳細解説、具体例、データを展開する
- 抽象論で終わらせず、読者が判断・行動できる具体的な情報を入れる
- Phase3のClaim-Evidence Mapを参照し、結論文に対応する根拠（出典・年）を同一セクション内に配置する

1次情報の扱い：
- 公的データは出典と年を必ず明記する
- 「厚生労働省のデータ（2025年1月発表）によれば〜です」のように、データを主語にする
- Phase3にない新規主張を追加した場合は、対応する根拠を追加してから確定する

自社USPの埋め込み方：
- 押し売りにしない。課題の解決策を語る流れの中で、自社の強みを根拠として自然に提示する
- 1つのH2セクション内で自社に言及するのは1〜2箇所が目安

CTAの配置（**3箇所必須・省略禁止**）：

| # | 配置位置 | 形式 | 選定URL |
|---|---|---|---|
| CTA-A | **リード文の終わり**（リード文を閉じる段落の直後） | **ボタン型** | Phase3で選定したCTA-A |
| CTA-B | **本文中盤**（全体の40〜60%位置、H2セクションの区切り） | **テキストリンク型** | Phase3で選定したCTA-B |
| CTA-C | **まとめ文の直後**（FAQまたはまとめセクションを閉じた直後） | **ボタン型** | Phase3で選定したCTA-C |

**テキストリンク vs ボタンの使い分けルール**：
- **ボタン型**（CTA-A・C）：読者がひとつの読み区切りを迎えた場面。行動を促す力が強い。WP・資料請求・お問い合わせ全種類で使用可。
- **テキストリンク型**（CTA-B）：本文の流れを壊さず自然に誘導する場面。本文の文脈に溶け込ませる。「〜については[こちらの資料]で詳しく解説しています」のように文章に埋め込む。

**ペルソナ逆算ルール**：Phase3で選定したCTAを使うこと（URLの手打ち禁止）。

---

**CTA-A / CTA-C 用：ボタン型HTMLテンプレート**

WPダウンロード・資料請求向け：
```html
<div style="background: linear-gradient(135deg, #1a3a5c 0%, #0e6ba8 100%); border-radius: 12px; padding: 36px 32px; margin: 48px 0; text-align: center; color: #fff;">
  <p style="font-size: 13px; letter-spacing: 0.1em; opacity: 0.7; margin: 0 0 6px;">— TCJ Global —</p>
  <p style="font-size: 21px; font-weight: 700; line-height: 1.5; margin: 0 0 8px;">（Phase3のキャッチコピー）</p>
  <p style="font-size: 14px; opacity: 0.85; margin: 0 0 24px; line-height: 1.6;">全○ページ・無料でダウンロードできます</p>
  <a href="（Phase3で選定したURL）" target="_blank" rel="noopener"
     style="display: inline-block; background: #f0a500; color: #1a1a1a; font-weight: 700; font-size: 16px; padding: 14px 36px; border-radius: 40px; text-decoration: none; letter-spacing: 0.04em;">
    無料でダウンロードする
  </a>
</div>
```

お問い合わせ向け：
```html
<div style="background: linear-gradient(135deg, #1a3a5c 0%, #0e6ba8 100%); border-radius: 12px; padding: 36px 32px; margin: 48px 0; text-align: center; color: #fff;">
  <p style="font-size: 13px; letter-spacing: 0.1em; opacity: 0.7; margin: 0 0 6px;">— TCJ Global —</p>
  <p style="font-size: 21px; font-weight: 700; line-height: 1.5; margin: 0 0 8px;">（Phase3のキャッチコピー）</p>
  <p style="font-size: 14px; opacity: 0.85; margin: 0 0 24px; line-height: 1.6;">初回相談無料・通常2営業日以内にご返信</p>
  <a href="（Phase3で選定したURL）" target="_blank" rel="noopener"
     style="display: inline-block; background: #f0a500; color: #1a1a1a; font-weight: 700; font-size: 16px; padding: 14px 36px; border-radius: 40px; text-decoration: none; letter-spacing: 0.04em;">
    無料で相談してみる
  </a>
</div>
```

---

**CTA-B 用：テキストリンク型HTMLテンプレート**

本文の文章末尾に自然に溶け込ませる：
```html
<p style="margin: 24px 0; padding: 16px 20px; background: #f4f8ff; border-left: 3px solid #0e6ba8; border-radius: 0 6px 6px 0; font-size: 14px; line-height: 1.7;">
  （本文の流れに合わせた一文。例：「採用コストの全体像と費用対効果の試算については、）<a href="（Phase3で選定したURL）" target="_blank" rel="noopener" style="color: #0e6ba8; font-weight: 600; text-decoration: underline;">（CTAタイトル）</a>（でまとめています。）」
</p>
```




FAQセクション：
- まとめの直前にパーツ12で5問以上
- Phase2のPAA質問を優先的に採用
- 回答の第1文で結論を端的に述べる

視覚要素：
- 1,000文字ごとに1つ以上の視覚要素（表、図、ボックス、画像）を配置する

### Step4：HTML組み立て
全コンテンツをreferences/html-template.htmlのパーツを使って1つのHTMLファイルに組み立てる。
- 全体をパーツ「WRAPPER」で囲む
- **テンプレ厳守（選択不可）**
  - `references/html-template.html` のパーツ以外の独自デザイン・独自構造を追加しない
  - 既存テーマ依存クラス（例：`p-column-detail`, `p-column-detail__body`, `scroll-box`, `table-default`, `step-process`, `p-faq-part`, `c-cta-part`）を本文に出力しない
  - 見出し（`h2/h3/h4`）はテンプレ定義のインラインスタイル付きパーツを使用する
- **【重要】内部リンクカード（`.tcj-blogcard`）のCSSは本文に埋め込まない**
  - WordPressの「外観 > カスタマイズ > 追加CSS」またはテーマCSSで事前に定義している前提で実装する
  - 本文（投稿コンテンツ）内に`<style>`タグや`<head>`要素を出力しない
- インラインスタイルは本文装飾に限定して使用する（内部リンクカードの共通CSSは除く）
- 画像のalt属性を適切に設定
- 内部リンクはreferences/internal-link-list.mdから選定して挿入する。以下のルールに従うこと：
  - 記事内で言及しているトピックと関連度が高い記事のみ選ぶ
  - 1記事あたり3〜5件。過剰に入れない
  - リンクリストに存在しないURLは絶対に使わない
  - コメントアウト部分（<!-- 記事内容の説明 -->）は出力しない
  - リンクの装飾はreferences/internal-link-design.htmlを使う
  - Markdownリンク形式（`[text](url)`）を本文に出力しない。HTMLカードのみを使う
  - 運用デフォルト（厳格クラスタ制約）では最大3件までに制限する
  - 3件のうち、原則2件以上は同一クラスターから選ぶ
  - クラスター外リンクは原則禁止（例外時は本文文脈と採用理由を明記）
  - 内部リンクカードは `references/internal-link-design.html` のDOM構造をそのまま使用する（許可される変更は`href/src/alt/タイトル文字列`のみ）
  - `tcj-blogcard__*` のような派生クラス名を新規作成しない
- **内部リンクカード画像の自動取得（必須）**
  - HTML出力後に `scripts/fetch_internal_link_images.py` を実行し、`tcj-blogcard-link` の遷移先URLから画像を解決する
  - `src` がプレースホルダー（`placehold.jp` 等）やロゴ画像のままの場合、取得したサムネイルURLに置換する
  - 実行例: `python .agent/skills/seo-phase4-writing/scripts/fetch_internal_link_images.py output/article.html`
### Step5：執筆直後の自己チェック（Phase5前の手戻り削減）
HTML組み立て後、Phase5に進む前に以下を確認する。

- 本文プレーンテキスト文字数が、Phase3で定義した目標の±20%以内か
- 内部リンクカードが最大3件以内か
- 内部リンクURLが `references/internal-link-list.md` に存在するか
- 内部リンクがHTMLカード形式のみで実装されているか
- 内部リンクカード画像にプレースホルダーURL（`placehold.jp` / `placeholder`）が残っていないか
- テンプレ未準拠クラス（`p-column-detail` 等）を出力していないか
- 見出し（`h2/h3/h4`）がテンプレ指定のインラインスタイル付きで出力されているか
- Claim-Evidence Mapの主要主張5件以上が本文内で根拠付きで表現されているか

## ゲート条件（すべて満たすまでPhase5に進めない）

**【機械ゲート】Phase5を開始する前に必ず実行すること：**
```bash
python .agent/scripts/gate_check.py --phase 4 --file data/phase_outputs/phase4_output.json
```
→ EXIT 0 になるまでPhase5を開始しない。

**Step5完了後、`data/phase_outputs/phase4_output.json` に実際の内容を埋めて出力すること（必須） 。**
主要キー：`html_path`, `title`, `meta_description`, `self_check_passed`(true), `char_count_check`, `cta_count`(≥ 3), `faq_count`(≥ 5)

- [ ] タイトル（32文字前後）とメタディスクリプション（120文字前後）を出力済み
- [ ] 記事全文をHTML形式で出力済み
- [ ] Phase3の構成案で指定した全セクションが含まれている
- [ ] CTAが3箇所（リード文直後・中盤・末尾）に配置されている
- [ ] FAQが5問以上含まれている
- [ ] 1,000文字ごとに1つ以上の視覚要素が配置されている
- [ ] 内部リンクカードが厳格クラスタ制約（最大３件）を満たしている
- [ ] 本文プレーンテキスト文字数の自己チェック結果を確認済み
- [ ] Claim-Evidence Mapの整合を確認済み
- [ ] `data/phase_outputs/phase4_output.json` を出力し、機械ゲートがEXIT 0になった
