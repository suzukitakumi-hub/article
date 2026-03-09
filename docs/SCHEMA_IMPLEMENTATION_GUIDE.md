# Schema.org実装ガイド
**対象サイト:** TCJ外国人材Times (https://gaikoku-jinzai.tcj-education.com/)
**作成日:** 2026年2月17日

---

## 目次

1. [即時対応が必要な項目](#1-即時対応が必要な項目)
2. [Organizationスキーマの実装](#2-organizationスキーマの実装)
3. [WebSite descriptionの修正](#3-website-descriptionの修正)
4. [BlogPostingへの変更](#4-blogpostingへの変更)
5. [著者情報の改善](#5-著者情報の改善)
6. [実装後の検証方法](#6-実装後の検証方法)
7. [トラブルシューティング](#7-トラブルシューティング)

---

## 1. 即時対応が必要な項目

以下の3つは**1週間以内に実装**してください:

| 項目 | 優先度 | 作業時間 | 影響度 |
|-----|-------|---------|-------|
| Organizationスキーマの追加 | 🔴 高 | 30分 | リッチリザルト表示に直結 |
| WebSite descriptionの修正 | 🔴 高 | 5分 | サイト説明の表示改善 |
| wordCount問題の修正 | 🔴 高 | 10分 | データ品質の改善 |

---

## 2. Organizationスキーマの実装

### 方法1: WordPressテーマのheader.phpに追加（推奨）

**手順:**

1. WordPress管理画面にログイン
2. 「外観」→「テーマファイルエディター」を選択
3. 右側のファイル一覧から`header.php`を選択
4. `</head>`タグの**直前**に以下のコードを追加:

```html
<!-- Organization Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://gaikoku-jinzai.tcj-education.com/#organization",
  "name": "TCJグローバル",
  "alternateName": "TCJ外国人材Times",
  "url": "https://tcj-education.com/ja/",
  "logo": {
    "@type": "ImageObject",
    "url": "https://gaikoku-jinzai.tcj-education.com/wp-content/themes/tcj-recruitment/assets/img/site-logo.svg",
    "width": 600,
    "height": 60,
    "caption": "TCJグローバル"
  },
  "description": "創業37年、外国人材の採用支援・日本語教育を専門とする総合教育企業",
  "foundingDate": "1987",
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "JP",
    "addressRegion": "東京都",
    "addressLocality": "新宿区"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "url": "https://tcj-education.com/ja/foreign-recruitment/",
    "availableLanguage": ["Japanese", "English"]
  },
  "sameAs": [
    "https://www.facebook.com/tcj.jp/",
    "https://twitter.com/tcj_jp"
  ]
}
</script>
```

5. 「ファイルを更新」をクリック
6. サイトのソースコードを表示して、追加されたことを確認

**⚠️ 注意:**
- `</head>`の前に追加してください（後ではありません）
- コードをコピーする際、引用符が全角になっていないか確認してください

---

### 方法2: Yoast SEO Premiumを使用（プレミアム版のみ）

**手順:**

1. WordPress管理画面 → 「SEO」→「検索の外観」
2. 「一般」タブを選択
3. 「組織情報」セクションに以下を入力:
   - 組織名: `TCJグローバル`
   - ロゴ: サイトロゴを選択
   - URL: `https://tcj-education.com/ja/`

**注:** Yoast SEO無料版では完全なOrganizationスキーマは自動生成されないため、方法1を推奨します。

---

### 方法3: プラグイン「Schema Pro」を使用

**手順:**

1. プラグイン「Schema Pro」をインストール・有効化
2. 「Schema Pro」→「Global Schemas」→「Add New」
3. 「Organization」を選択
4. 必要情報を入力
5. 「Publish」をクリック

**注:** 有料プラグイン（$67/年）のため、予算がある場合のみ推奨。

---

## 3. WebSite descriptionの修正

### 手順

1. WordPress管理画面 → 「SEO」→「検索の外観」
2. 「一般」タブを選択
3. 「サイト説明」フィールドに以下を入力:

```
TCJ外国人材timesは、外国人材の採用を担当されている方、これから外国人材を採用しようと検討している担当者の方に向けて、外国人材採用時のポイントや在留資格、採用後の人材育成や定着に関する内容をお届けします。
```

4. 「変更を保存」をクリック

### 確認方法

1. サイトのトップページを開く
2. ページのソースコードを表示（Ctrl+U または Cmd+U）
3. `"@type":"WebSite"` を検索
4. `"description"` フィールドが空白でないことを確認

---

## 4. BlogPostingへの変更

### 手順

1. WordPress管理画面 → 「SEO」→「検索の外観」
2. 「コンテンツタイプ」タブを選択
3. 「投稿」セクションの「スキーマタイプ」を `Article` から `BlogPosting` に変更
4. 「変更を保存」をクリック

### 確認方法

1. 任意の記事ページを開く
2. ページのソースコードを表示
3. `"@type":"BlogPosting"` が存在することを確認（`Article`ではない）

---

## 5. 著者情報の改善

### 手順

1. WordPress管理画面 → 「ユーザー」→「プロフィール」
2. 「表示名」を `admin` から `TCJ編集部` に変更
3. （オプション）「プロフィール情報」に簡単な自己紹介を追加:

```
TCJグローバルの外国人材採用支援チーム。37年の日本語教育実績を活かし、外国人材の採用・育成・定着に関する実践的な情報を発信しています。
```

4. 「プロフィールを更新」をクリック

### 確認方法

1. 任意の記事ページを開く
2. ページのソースコードを表示
3. `"author"` セクションの `"name"` が `TCJ編集部` になっていることを確認

---

## 6. 実装後の検証方法

### ステップ1: Google Rich Results Test

1. https://search.google.com/test/rich-results を開く
2. サイトのURL（トップページ）を入力
3. 「URLをテスト」をクリック
4. 以下が検出されることを確認:
   - ✅ Organization
   - ✅ WebSite
   - ✅ BreadcrumbList

5. 記事ページのURLでも同様にテスト
6. 以下が検出されることを確認:
   - ✅ BlogPosting（またはArticle）
   - ✅ Organization
   - ✅ BreadcrumbList
   - ✅ ImageObject

**エラーがある場合:**
- 「エラー」タブを確認
- 赤いアイコンは必ず修正
- 黄色いアイコンは推奨事項（必須ではない）

---

### ステップ2: Schema Markup Validator

1. https://validator.schema.org/ を開く
2. 「Code Snippet」タブを選択
3. ページのソースコードから`<script type="application/ld+json">`の中身をコピー
4. 貼り付けて「RUN TEST」をクリック
5. エラーがないことを確認

---

### ステップ3: Google Search Console

1. https://search.google.com/search-console を開く
2. 左メニュー「拡張」→「パンくずリスト」を選択
3. エラーがないことを確認
4. 「拡張」→「記事」を選択（データが表示されるまで数週間かかる場合あり）
5. エラーがないことを確認

**注:** Search Consoleのデータ反映には数日〜数週間かかります。

---

## 7. トラブルシューティング

### Q1: Organizationスキーマが検出されない

**原因:**
- コードが正しく貼り付けられていない
- `</head>`の後に貼り付けてしまった
- キャッシュプラグインが有効

**解決策:**
1. ページのソースコードを表示して、スキーマが存在するか確認
2. キャッシュをクリア（WP Super CacheやW3 Total Cacheなど）
3. ブラウザのキャッシュもクリア（Ctrl+Shift+R）

---

### Q2: 「publisher」が欠落しているとエラーが出る

**原因:**
- Organizationスキーマが実装されていない
- Yoast SEOのArticleスキーマが`publisher`を含めていない

**解決策:**
1. 上記「2. Organizationスキーマの実装」を完了させる
2. Yoast SEOを最新版に更新
3. 記事を再保存

---

### Q3: wordCountが不正確

**原因:**
- Yoast SEOのバグまたは古いバージョン

**解決策:**
1. Yoast SEOを最新版に更新
2. 記事を再保存
3. それでも解決しない場合は、Yoast SEOサポートに問い合わせ

---

### Q4: スキーマが重複している

**原因:**
- 複数のプラグインがスキーマを出力している
- テーマとプラグインの両方がスキーマを出力している

**解決策:**
1. ページのソースコードを表示
2. `<script type="application/ld+json">`が何個あるか確認
3. 同じ`@type`が複数ある場合は、どちらか一方を無効化
4. Yoast SEOを使用している場合、他のSEOプラグインを無効化

---

## 実装チェックリスト

実装完了後、以下をチェックしてください:

### 即時実装（1週間以内）

- [ ] Organizationスキーマを全ページに追加
- [ ] WebSiteのdescriptionを修正
- [ ] wordCount問題を確認・修正
- [ ] Google Rich Results Testで検証
- [ ] Schema Markup Validatorで検証

### 中期実装（1ヶ月以内）

- [ ] Article → BlogPostingへ変更
- [ ] 著者情報を「TCJ編集部」に変更
- [ ] articleSectionプロパティの追加確認
- [ ] Google Search Consoleでエラー確認

### 長期実装（3ヶ月以内）

- [ ] セミナー動画がある記事にVideoObjectを追加
- [ ] 研修プログラムページにCourseスキーマを追加
- [ ] 月次でGoogle Search Consoleのリッチリザルトレポート確認

---

## サポート連絡先

**Yoast SEOサポート:**
- https://yoast.com/help/

**Googleヘルプコミュニティ:**
- https://support.google.com/webmasters/community

**Schema.org公式:**
- https://schema.org/docs/gs.html

---

**次回レビュー推奨日:** 実装完了後1ヶ月（2026年3月中旬）

---

**作成者:** Claude Code (Schema.org専門家)
**最終更新:** 2026年2月17日
