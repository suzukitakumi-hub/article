# グローバル事業部 GTM/GA4 実装手順書（初心者向け）

最終更新: 2026-02-25

## 進捗（2026-02-25時点）
- ~~Step 1: サンクスページ作成~~（完了）
- ~~Step 2: Zohoフォーム送信後遷移設定~~（完了）
- ~~Step 3: GTMトリガー作成~~（完了）
- ~~Step 4: GTM GA4イベントタグ作成~~（完了）
- ~~Step 5: GTM Preview確認~~（完了）
- ~~Step 6: GTM公開~~（完了）
- ~~Step 7-1: GA4カスタム定義作成（`cv_type`, `form_provider`）~~（完了）
- ~~Step 7-2: GA4で`lead_*`イベント作成（page_view条件）~~（完了）
- ~~Step 7-3: GA4キーイベントON（`lead_*` 4件）~~（完了）
- Step 8: UTM付き流入の最終テスト

## 結論（最初にここだけ）
- UTM整理は「先」ではない。先に `問い合わせ/資料請求` のCV導線を `Zohoフォーム -> サンクスページ` に置換する。
- 理由: CV自体が取れない状態でUTMだけ整備しても、チャネル別CV集計が成立しないため。
- 今の優先順位は `CV導線の統一 -> 計測方式の一本化 -> UTM統一 -> 最終テスト -> スプシ`。

## ここからの流れ（混乱しない順）
1. 問い合わせ/資料請求を `Zohoフォーム -> サンクスページ` に置換する
2. サンクスURLを固定する（現状ウェビナーは `/seminar-thanks`）
3. CV判定方式を1本化する（推奨: GTMの `lead_*` を正とし、GA4「イベントを作成」は停止）
4. UTM命名規則を確定して、広告・メルマガの全リンクへ適用
5. UTM付きテスト流入を実施（Step 8）
6. チャネルレポート（スプシ）に着手

## 現時点の前提
- `https://tcj-education.com/ja/foreign-recruitment/` の既存フォームは、送信メール通知のみで計測しづらい
- 今後は WordPress上のZohoフォームへ置換し、サンクスページ到達でCV判定する

## 現時点で「測れる / 測れない」
1. 測れる: `gaikoku-jinzai.tcj-education.com` 配下で、サンクスページ到達まで完結するCV
2. 測れない/不安定: `tcj-education.com/ja/foreign-recruitment/` でメール送信だけのフォームCV
3. 測れない/不安定: 広告遷移先が `tcj-education.com` 側のみで、CVが別ドメイン完結かつUTM受け渡しが未整備のケース

## ここからの実行チェックリスト（短縮版）
1. 問い合わせ・資料請求フォームをZoho化し、送信後URLを固定
2. 4サンクスページURLでPage View条件が一致するか再確認
3. GTM/GA4でCV計測方式を一本化（GTM送信を正とし、GA4「イベントを作成」は停止または削除）
4. UTM命名規則を確定し、Meta/Google/YouTube/Zohoの全配信リンクに適用
5. UTM付きURLで4CVを再テスト（Realtime + DebugView + Tag Assistant）
6. その後にスプシのチャネルレポート実装

## 0. 先に用意するもの
1. サイト管理権限
2. Zoho Forms編集権限
3. GTMコンテナ編集権限（`GTM-MV6T9CMX`）
4. GA4編集権限（プロパティ `517064395`）

## ~~1. サンクスページを4つ作る~~（完了）
作るURL:
1. `/seminar-thanks`
2. `/doc-request-thanks`
3. `/whitepaper-thanks`
4. `/contact-thanks`

チェック:
1. 各URLがブラウザで開ける
2. 404にならない

## ~~2. Zohoフォームの送信後遷移を設定~~（完了）
1. Zoho Formsで対象フォームを開く
2. `Settings` / `Confirmation` を開く
3. 送信後遷移先に上記4URLをCVごとに設定
4. 保存

チェック:
1. テスト送信で想定サンクスURLに遷移する

## ~~3. GTMでトリガーを4つ作成~~（完了）
作成場所: GTM > `Triggers` > `New`

設定:
1. `PV - thanks webinar`
- Type: `Page View`
- 条件: `Page Path equals /seminar-thanks`

2. `PV - thanks doc request`
- Type: `Page View`
- 条件: `Page Path equals /doc-request-thanks`

3. `PV - thanks whitepaper`
- Type: `Page View`
- 条件: `Page Path equals /whitepaper-thanks`

4. `PV - thanks contact`
- Type: `Page View`
- 条件: `Page Path equals /contact-thanks`

補足:
- `Page Path` が見えない場合はGTMの `Variables` で有効化する

## ~~4. GTMでGA4イベントタグを4つ作成~~（完了）
### 4-1. GA4ベースタグがない場合
1. GTM > `Tags` > `New`
2. `Google tag`（またはGA4 Configuration）を選択
3. GA4のMeasurement ID（`G-...`）を設定
4. Triggerを `All Pages` にして保存

### 4-2. CVイベントタグ
作成場所: GTM > `Tags` > `New`
- Type: `Google Analytics: GA4 Event`

1. `GA4 - lead_webinar_submit`
- Event Name: `lead_webinar_submit`
- Parameters: `cv_type=webinar`, `form_provider=zoho`
- Trigger: `PV - thanks webinar`

2. `GA4 - lead_doc_request_submit`
- Event Name: `lead_doc_request_submit`
- Parameters: `cv_type=doc_request`, `form_provider=zoho`
- Trigger: `PV - thanks doc request`

3. `GA4 - lead_whitepaper_submit`
- Event Name: `lead_whitepaper_submit`
- Parameters: `cv_type=whitepaper`, `form_provider=zoho`
- Trigger: `PV - thanks whitepaper`

4. `GA4 - lead_contact_submit`
- Event Name: `lead_contact_submit`
- Parameters: `cv_type=contact`, `form_provider=zoho`
- Trigger: `PV - thanks contact`

## ~~5. GTM Previewでテスト~~（完了）
1. GTM右上 `Preview`
2. 対象サイトを接続
3. 各フォームを1回ずつ送信
4. 該当CVイベントだけ1回発火することを確認

判定:
1. Webinar送信で `lead_webinar_submit` のみ発火
2. 他3CVも同様

## ~~6. GTMを公開~~（完了）
1. GTM右上 `Submit`
2. バージョン名例: `2026-02-18_cv4_events`
3. `Publish`

## 7. GA4でキーイベント化（一部完了）
1. GA4 > `管理` > `カスタム定義`
2. `cv_type` と `form_provider` をイベントスコープで作成
3. GA4 > `管理` > `イベント`
4. 4イベントを `キーイベント` ON

補足（現在の運用）:
- GTMの`lead_*`送信に加えて、GA4の「イベントを作成」で`lead_*`を作成済み。
- 二重計測を避けるため、最終的に「GTM送信」か「GA4作成イベント」のどちらかに統一する。

## 8. UTMの最終テスト（未着手）
実施前提:
- 問い合わせ/資料請求フォームが Zoho + サンクス遷移に置換済みであること

テストURL例:
1. `...?utm_source=meta&utm_medium=paid_social&utm_campaign=2026_02_test`
2. `...?utm_source=google&utm_medium=cpc&utm_campaign=2026_02_test`
3. `...?utm_source=zoho&utm_medium=email&utm_campaign=2026_02_test`

確認:
1. GA4 Realtimeで `source / medium` が期待通り
2. CVイベントが受信される
3. `cv_type` が入っている

## 9. ここまで終わったら
この時点で、月次のスプシ集計に進んでよい。

