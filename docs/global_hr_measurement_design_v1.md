# グローバル事業部 計測設計 v1（GA4 + GTM）

最終更新: 2026-02-25

## 1. 対象と目的
- 対象メディア: `https://gaikoku-jinzai.tcj-education.com/`（オウンド）
- 対象LP: `https://tcj-education.com/ja/tcj-recruitment/`
- 目的KPI: `CV`, `CVR`（Paidは `CPA` 追加）
- 集計粒度: チャネル別・月次（MBAシート形式に準拠）

## 1.1 現状課題（2026-02-25時点）
1. `https://tcj-education.com/ja/foreign-recruitment/` の既存フォームはメール通知のみで、CV計測基盤として不十分。
2. まずは問い合わせ/資料請求を `Zohoフォーム -> CV別サンクスページ` に統一する。
3. UTM整備は「CV導線が計測可能になった後」に実施する。

## 2. CV定義（固定）
主CVと副CVを分けず、4CVを同列管理する。

1. `lead_webinar_submit`（ウェビナー申込完了）
2. `lead_doc_request_submit`（資料請求完了）
3. `lead_whitepaper_submit`（ホワイトペーパーDL完了）
4. `lead_contact_submit`（お問い合わせ完了）

補助イベント（任意）:
- `form_start`
- `form_submit_attempt`

## 3. CV成立条件（重要）
「クリック」ではなく「完了到達」をCV成立条件にする。

推奨実装:
- CVごとに完了URLを分ける。
- 例:
  - `/seminar-thanks`
  - `/doc-request-thanks`
  - `/whitepaper-thanks`
  - `/contact-thanks`

暫定実装（完了URLを分けられない場合）:
- 共通完了URLに `?cv_type=webinar|doc_request|whitepaper|contact` を付与して判定。
- 例: `/seminar-thanks?cv_type=webinar`

## 4. GTM実装ルール（Web）
### 4.1 トリガー
- `Page View` で完了URL判定（または `cv_type` クエリ判定）。

### 4.2 GA4イベントタグ
- タグ種別: `Google Analytics: GA4 Event`
- 計測ID: GA4 Webストリーム（プロパティ `517064395` 側）
- 送信イベント:
  - `lead_webinar_submit`
  - `lead_doc_request_submit`
  - `lead_whitepaper_submit`
  - `lead_contact_submit`

### 4.3 付与パラメータ（全CV共通）
- `cv_type`（`webinar` / `doc_request` / `whitepaper` / `contact`）
- `form_provider`（`zoho`）
- `page_type`（`owned_media` / `service_lp`）

## 5. GA4設定ルール
1. 上記4イベントを受信確認。
2. 4イベントを「キーイベント」に設定。
3. `cv_type` をカスタムディメンション登録。
4. 探索で「チャネル × cv_type × 月次」レポートを作成。

## 6. チャネル設計（まずは最小）
分析時の主分類:
1. Paid Meta
2. Paid Google
3. Email (Zoho Campaigns)
4. Organic
5. Direct
6. Referral

初期判定ルール（UTM前提）:
- Paid Meta: `source=meta` かつ `medium=paid_social`
- Paid Google: `source=google` かつ `medium=cpc`
- Email: `source=zoho` かつ `medium=email`

## 7. UTM命名規則（固定）
### 7.1 必須パラメータ
- `utm_source`
- `utm_medium`
- `utm_campaign`

### 7.2 ルール
- 小文字スネークケースのみ
- 日本語・全角スペースは使わない
- 例:
  - Meta広告:
    - `utm_source=meta`
    - `utm_medium=paid_social`
    - `utm_campaign=2026_02_webinar_cv`
  - Google検索広告:
    - `utm_source=google`
    - `utm_medium=cpc`
    - `utm_campaign=2026_02_doc_request_cv`
    - `utm_term={keyword}`
  - Zohoメール:
    - `utm_source=zoho`
    - `utm_medium=email`
    - `utm_campaign=2026_02_newsletter`
    - `utm_content=cta_top`

## 8. Zoho周りの実装方針
### 8.1 Zoho Forms
- 可能な限り全CVフォームをZoho Formsへ統一。
- 送信完了時の遷移URLをCV別に分離（または `cv_type` 付与）。

### 8.2 Zoho Campaigns（配信リンク仕様の見方）
1. メール内リンクは手動でUTMを付ける（最優先）。
2. 送信前にテストメールを自分へ送る。
3. リンククリック後URLの `utm_source / utm_medium / utm_campaign` を確認。
4. GA4リアルタイムで `source/medium` が想定通りか確認。

## 9. レポート項目（月次）
チャネル別に以下を出力:
- `Sessions`
- `CV`（4CV合算）
- `CVR = CV / Sessions`
- `Cost`（Paidのみ）
- `CPA = Cost / CV`（Paidのみ）

推奨で4CV内訳も別列で保持:
- Webinar CV
- Doc Request CV
- Whitepaper CV
- Contact CV

## 10. 直近実装順（2週間）
1. CV別サンクスURL（または `cv_type`）を確定。
2. GTMで4イベント実装。
3. GA4キーイベント化。
4. Meta/Google/ZohoのUTM統一運用開始。
5. 月次レポート（チャネル別）を運用開始。

## 11. 確定事項（2026-02-18時点）
1. サンクスURLはCV別に分離する。
2. フォームはZoho埋め込み、送信後はサンクスページへ自動遷移。
3. 既存フォームはまずZoho化を優先（切替日程は別途）。
4. メルマガ運用は委託運用（UTMルールを先に固定して共有必須）。

## 12. GTM実装仕様（そのまま設定可）
### 12.1 サンクスURL
- `https://gaikoku-jinzai.tcj-education.com/seminar-thanks`
- `https://gaikoku-jinzai.tcj-education.com/doc-request-thanks`
- `https://gaikoku-jinzai.tcj-education.com/whitepaper-thanks`
- `https://gaikoku-jinzai.tcj-education.com/contact-thanks`

### 12.2 トリガー（Page View）
- `PV - thanks webinar`
  - 条件: `Page URL contains /seminar-thanks`
- `PV - thanks doc request`
  - 条件: `Page URL contains /doc-request-thanks`
- `PV - thanks whitepaper`
  - 条件: `Page URL contains /whitepaper-thanks`
- `PV - thanks contact`
  - 条件: `Page URL contains /contact-thanks`

### 12.3 GA4イベントタグ
- `GA4 - lead_webinar_submit`
  - Event Name: `lead_webinar_submit`
  - Trigger: `PV - thanks webinar`
  - Params: `cv_type=webinar`, `form_provider=zoho`
- `GA4 - lead_doc_request_submit`
  - Event Name: `lead_doc_request_submit`
  - Trigger: `PV - thanks doc request`
  - Params: `cv_type=doc_request`, `form_provider=zoho`
- `GA4 - lead_whitepaper_submit`
  - Event Name: `lead_whitepaper_submit`
  - Trigger: `PV - thanks whitepaper`
  - Params: `cv_type=whitepaper`, `form_provider=zoho`
- `GA4 - lead_contact_submit`
  - Event Name: `lead_contact_submit`
  - Trigger: `PV - thanks contact`
  - Params: `cv_type=contact`, `form_provider=zoho`

### 12.4 QA（公開前チェック）
1. GTM Previewで各サンクスURLにアクセスし、該当イベントのみ1回発火する。
2. GA4 Realtimeでイベント名が一致して受信される。
3. GA4 DebugViewで `cv_type` が期待通り入る。
4. 同一ページのリロードで重複計測しないか確認する（必要なら再読込除外）。

## 13. 外部運用（委託先）へ渡す必須ルール
1. 全リンクにUTMを付与する（Meta/Google/Zoho共通）。
2. 命名規則は本書 7章の値を厳守。
3. 新キャンペーン作成時は `utm_campaign` を月次単位で更新。
4. 例外命名を使う場合は事前承認制にする。

## 14. 実装手順（初心者向け / これを上から実施）
ここからは「実際に何を押すか」を順番に記載する。

### Step 0. 事前準備（10分）
実施前に、次の管理権限を確認する。
1. サイト管理画面（オウンドメディア側）
2. Zoho Forms
3. GTM（`GTM-MV6T9CMX`）
4. GA4（プロパティ `517064395`）

チェック用の対応表を先に作る。

| CV種別 | サンクスURL | GA4イベント名 |
|---|---|---|
| Webinar | `/seminar-thanks` | `lead_webinar_submit` |
| Doc Request | `/doc-request-thanks` | `lead_doc_request_submit` |
| Whitepaper | `/whitepaper-thanks` | `lead_whitepaper_submit` |
| Contact | `/contact-thanks` | `lead_contact_submit` |

### Step 1. サンクスページを4つ作成（30-60分）
1. オウンドメディア管理画面で固定ページを新規作成。
2. 下記4URLで公開する。
   - `/seminar-thanks`
   - `/doc-request-thanks`
   - `/whitepaper-thanks`
   - `/contact-thanks`
3. 各ページに「送信ありがとうございました」等の文言を入れる。
4. 可能なら `noindex` にする（検索流入防止）。

完了条件:
- ブラウザで4URLを直接開いて、全て `200` で表示される。

### Step 2. Zohoフォームの送信後遷移を設定（30-60分）
1. Zoho Formsで対象フォームを開く。
2. `Settings` もしくは `Confirmation`（完了画面設定）を開く。
3. 「送信後に別ページへ遷移」を選び、CVごとのサンクスURLを設定。
4. 保存。

完了条件:
- テスト送信で、想定したサンクスURLに遷移する。

### Step 3. GTMでトリガーを4つ作成（20-30分）
1. GTM > `Triggers` > `New`
2. Trigger Typeは `Page View`
3. `Some Page Views` を選択
4. 下記条件で4つ作成
   - `PV - thanks webinar`: `Page Path equals /seminar-thanks`
   - `PV - thanks doc request`: `Page Path equals /doc-request-thanks`
   - `PV - thanks whitepaper`: `Page Path equals /whitepaper-thanks`
   - `PV - thanks contact`: `Page Path equals /contact-thanks`

補足:
- `Page Path` が選べない場合は、`Variables` で組み込み変数 `Page Path` を有効化する。

### Step 4. GTMでGA4イベントタグを4つ作成（30-45分）
#### 4-1. GA4設定タグが未作成なら先に作る
1. GTM > `Tags` > `New`
2. Tag Type: `Google tag`（または GA4 Configuration）
3. Measurement ID（`G-XXXX`）を入力
4. Trigger: `All Pages`
5. 保存（例: `GA4 - base`）

#### 4-2. CVイベントタグ4つ
1. GTM > `Tags` > `New`
2. Tag Type: `Google Analytics: GA4 Event`
3. Configuration Tag（または Google tag）に `GA4 - base` を指定
4. Event NameとEvent Parameterを入力
5. Triggerに該当PVトリガーを指定

入力値:
- `GA4 - lead_webinar_submit`
  - Event Name: `lead_webinar_submit`
  - Parameters: `cv_type=webinar`, `form_provider=zoho`
  - Trigger: `PV - thanks webinar`
- `GA4 - lead_doc_request_submit`
  - Event Name: `lead_doc_request_submit`
  - Parameters: `cv_type=doc_request`, `form_provider=zoho`
  - Trigger: `PV - thanks doc request`
- `GA4 - lead_whitepaper_submit`
  - Event Name: `lead_whitepaper_submit`
  - Parameters: `cv_type=whitepaper`, `form_provider=zoho`
  - Trigger: `PV - thanks whitepaper`
- `GA4 - lead_contact_submit`
  - Event Name: `lead_contact_submit`
  - Parameters: `cv_type=contact`, `form_provider=zoho`
  - Trigger: `PV - thanks contact`

### Step 5. GTM Previewで動作確認（20-30分）
1. GTM右上 `Preview`
2. 対象サイトURLを入力して接続
3. 各フォームをテスト送信してサンクスページへ遷移
4. Tag Assistantで、該当イベントタグが1回だけ発火することを確認

完了条件:
- Webinar送信時は `lead_webinar_submit` のみ発火（他3つは発火しない）
- 他CVも同様

### Step 6. GTMを公開（5分）
1. GTM右上 `Submit`
2. Version Name例: `2026-02-18_cv4_events`
3. Publish

### Step 7. GA4側の設定（15-30分）
1. GA4 > `管理` > `カスタム定義` > `カスタムディメンションを作成`
   - `cv_type`（イベントスコープ）
   - `form_provider`（イベントスコープ）
2. GA4 > `管理` > `イベント`
3. 4イベントが表示されたら、各イベントを `キーイベント` ON

注意:
- カスタム定義の反映や標準レポート反映には時間がかかる（最大24時間程度）。
- Realtime/DebugViewはほぼ即時確認可。

### Step 8. UTM付き流入の最終確認（20-30分）
テストリンク例:
- Meta想定:
  - `...?utm_source=meta&utm_medium=paid_social&utm_campaign=2026_02_test`
- Google想定:
  - `...?utm_source=google&utm_medium=cpc&utm_campaign=2026_02_test`
- Zoho想定:
  - `...?utm_source=zoho&utm_medium=email&utm_campaign=2026_02_test`

確認箇所:
1. GA4 Realtimeで `source/medium` が意図通り
2. CVイベントが受信される
3. `cv_type` パラメータが入っている

## 15. よくある失敗と対処
1. 4CVが全部同じイベントで入る
- 原因: サンクスURLが共通
- 対処: URL分離 or `cv_type` 付与で判別

2. GTMで発火しない
- 原因: `Page Path` 条件ミス（`contains`/`equals` の誤り）
- 対処: Previewで実際のURLを確認して条件修正

3. GA4にイベントが見えない
- 原因: GTM未公開 or 測定ID違い
- 対処: GTM publish確認、GA4測定IDを再確認

4. チャネルが `(direct) / (none)` になる
- 原因: UTM未付与
- 対処: 配信リンクにUTMを必須化


