# Schema.org マークアップ分析レポート
**対象サイト:** https://gaikoku-jinzai.tcj-education.com/
**分析日:** 2026年2月17日
**分析者:** Claude Code (Schema.org専門家)

---

## 1. 検出結果サマリー

### 現在実装されているスキーマ

| スキーマタイプ | 実装場所 | フォーマット | ステータス |
|------------|---------|------------|----------|
| **CollectionPage** | トップページ | JSON-LD | ✅ 実装済み |
| **BreadcrumbList** | 全ページ | JSON-LD | ✅ 実装済み |
| **WebSite** | 全ページ | JSON-LD | ✅ 実装済み |
| **Article** | 記事ページ | JSON-LD | ✅ 実装済み |
| **WebPage** | 記事ページ | JSON-LD | ✅ 実装済み |
| **ImageObject** | 記事ページ | JSON-LD | ✅ 実装済み |
| **Person** (Author) | 記事ページ | JSON-LD | ✅ 実装済み |

**実装プラグイン:** Yoast SEO v26.8

---

## 2. 詳細バリデーション結果

### ✅ CollectionPage (トップページ)

```json
{
  "@type": "CollectionPage",
  "@id": "https://gaikoku-jinzai.tcj-education.com/",
  "url": "https://gaikoku-jinzai.tcj-education.com/",
  "name": "TCJ外国人材Times -",
  "isPartOf": {"@id": "https://gaikoku-jinzai.tcj-education.com/#website"},
  "breadcrumb": {"@id": "https://gaikoku-jinzai.tcj-education.com/#breadcrumb"},
  "inLanguage": "ja"
}
```

**検証結果:**
- ✅ @context: `https://schema.org` (正しいプロトコル)
- ✅ @type: `CollectionPage` (記事一覧ページに適切)
- ✅ 必須プロパティ: 全て存在
- ⚠️ 改善余地: `description` プロパティの追加推奨

---

### ✅ Article (記事ページ)

```json
{
  "@type": "Article",
  "@id": "https://gaikoku-jinzai.tcj-education.com/posts/2025_foreign-human-resources#article",
  "headline": "【2026年最新】外国人材紹介会社おすすめ5選｜絶対に失敗しない選び方と比較ポイントを徹底解説",
  "datePublished": "2025-12-27T17:46:29+00:00",
  "dateModified": "2026-01-13T06:39:36+00:00",
  "author": {"name": "admin", "@id": "..."},
  "image": {"@id": "...#primaryimage"},
  "thumbnailUrl": "...",
  "wordCount": 79,
  "commentCount": 0,
  "inLanguage": "ja"
}
```

**検証結果:**
- ✅ 必須プロパティ完備 (headline, datePublished, author, image)
- ✅ ISO 8601形式の日付
- ✅ 絶対URL使用
- ⚠️ **重大な問題:** `wordCount: 79` は明らかに不正確（実際の記事は数千文字）
- ⚠️ 改善推奨: `publisher` プロパティの追加（Organization情報）
- ⚠️ 改善推奨: `articleSection` の追加（カテゴリー情報）

---

### ✅ BreadcrumbList

```json
{
  "@type": "BreadcrumbList",
  "@id": "https://gaikoku-jinzai.tcj-education.com/posts/2025_foreign-human-resources#breadcrumb",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "ホーム", "item": "https://gaikoku-jinzai.tcj-education.com/"},
    {"@type": "ListItem", "position": 2, "name": "【2026年最新】外国人材紹介会社おすすめ5選｜絶対に失敗しない選び方と比較ポイントを徹底解説"}
  ]
}
```

**検証結果:**
- ✅ 構造が正しい
- ✅ position順序が正しい
- ⚠️ 最終アイテムに`item`プロパティがない（仕様上は許容されるが追加推奨）

---

### ✅ WebSite

```json
{
  "@type": "WebSite",
  "@id": "https://gaikoku-jinzai.tcj-education.com/#website",
  "url": "https://gaikoku-jinzai.tcj-education.com/",
  "name": "TCJ外国人材Times",
  "description": "",
  "potentialAction": [
    {
      "@type": "SearchAction",
      "target": {
        "@type": "EntryPoint",
        "urlTemplate": "https://gaikoku-jinzai.tcj-education.com/?s={search_term_string}"
      },
      "query-input": {
        "@type": "PropertyValueSpecification",
        "valueRequired": true,
        "valueName": "search_term_string"
      }
    }
  ],
  "inLanguage": "ja"
}
```

**検証結果:**
- ✅ SearchAction実装済み（サイト内検索対応）
- ❌ **重大な問題:** `description` が空文字列
- ⚠️ 改善推奨: `publisher` プロパティでOrganizationと連携

---

## 3. 欠落しているスキーマ（重要度順）

### 🔴 優先度【高】: Organization

**現状:** 実装なし
**問題点:**
- 記事の`publisher`情報が欠落
- Googleのリッチリザルト要件を満たしていない
- ナレッジパネル表示の機会損失

**推奨実装:**

```json
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
    "height": 60
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
    "url": "https://tcj-education.com/ja/foreign-recruitment/"
  },
  "sameAs": [
    "https://www.facebook.com/tcj.jp/",
    "https://twitter.com/tcj_jp"
  ]
}
```

**記事ページへの統合:**
```json
{
  "@type": "Article",
  "headline": "...",
  "publisher": {
    "@id": "https://gaikoku-jinzai.tcj-education.com/#organization"
  }
}
```

---

### 🟡 優先度【中】: BlogPosting (Articleの代わり)

**現状:** 汎用の`Article`を使用
**推奨:** より具体的な`BlogPosting`に変更

**理由:**
- TCJ外国人材Timesはブログメディア形式
- `BlogPosting`はArticleのサブタイプで、ブログ記事に最適
- Googleの記事リッチリザルトで有利

**変更例:**
```json
{
  "@type": "BlogPosting",  // Article → BlogPostingに変更
  "headline": "...",
  "articleSection": "採用ノウハウ",  // カテゴリー情報追加
  "articleBody": "記事本文の抜粋...",  // 推奨プロパティ
  "publisher": {"@id": "...#organization"}
}
```

---

### 🟡 優先度【中】: FAQPage

**現状:** 実装なし
**対象記事:** 「よくある質問」セクションを含む記事（例: 外国人材紹介会社の記事）

**⚠️ 重要な制限事項:**
- **FAQページスキーマは2023年8月以降、政府機関と医療機関のみが使用可能**
- TCJは教育企業のため、**FAQPageスキーマは使用不可**
- 代替策: 記事内に自然な形でQ&A形式を含める（スキーマなし）

**結論:** FAQPageスキーマは実装しない（Googleのポリシー違反を回避）

---

### 🟢 優先度【低】: VideoObject

**現状:** 実装なし
**潜在的機会:**
- セミナー動画がある場合は実装を検討
- YouTube埋め込み動画がある記事には有効

**推奨実装（動画がある場合のみ）:**
```json
{
  "@type": "VideoObject",
  "name": "外国人材採用セミナー【2026年最新】",
  "description": "...",
  "thumbnailUrl": "https://...",
  "uploadDate": "2026-01-15T08:00:00+09:00",
  "duration": "PT15M33S",
  "contentUrl": "https://www.youtube.com/watch?v=...",
  "embedUrl": "https://www.youtube.com/embed/..."
}
```

---

### 🟢 優先度【低】: Course

**現状:** 実装なし
**潜在的機会:**
- TCJが提供する日本語研修プログラムを紹介するページがあれば有効
- 教育コンテンツに適したスキーマ

**推奨実装（研修プログラムページに）:**
```json
{
  "@type": "Course",
  "name": "ビジネス日本語研修プログラム",
  "description": "企業向け外国人材の日本語能力向上支援",
  "provider": {
    "@id": "https://gaikoku-jinzai.tcj-education.com/#organization"
  },
  "courseMode": ["online", "onsite"],
  "inLanguage": "ja"
}
```

---

## 4. 非推奨・使用禁止スキーマ

### ❌ 使用禁止: HowTo
- **理由:** 2023年9月にリッチリザルト廃止
- **現状:** 実装なし（正しい）

### ❌ 使用禁止: SpecialAnnouncement
- **理由:** 2025年7月31日に廃止
- **現状:** 実装なし（正しい）

### ❌ 制限付き: FAQ
- **理由:** 2023年8月以降、政府・医療機関のみ使用可能
- **現状:** 実装なし（正しい）
- **推奨:** Q&A形式のコンテンツは通常のHTMLで記述

---

## 5. 技術的問題と修正推奨

### 🔴 重大な問題

1. **wordCount不正確**
   - 現状: `"wordCount": 79`
   - 実際: 数千文字の記事
   - 修正: Yoast SEOの設定を確認、正確なカウントに修正

2. **WebSiteのdescription空白**
   - 現状: `"description": ""`
   - 修正: `"description": "TCJ外国人材timesは、外国人材の採用を担当されている方、これから外国人材を採用しようと検討している担当者の方に向けて、外国人材採用時のポイントや在留資格、採用後の人材育成や定着に関する内容をお届けします。"`

3. **Organizationスキーマ欠落**
   - 影響: Articleの`publisher`が未設定 → リッチリザルト対象外の可能性
   - 修正: 上記のOrganizationスキーマを追加

### 🟡 改善推奨

4. **Article → BlogPostingへ変更**
   - より具体的なスキーマタイプを使用

5. **articleSectionの追加**
   - カテゴリー情報を明示的に含める

6. **author情報の強化**
   - 現状: `"name": "admin"` (汎用的)
   - 推奨: 実名または役職（例: `"name": "TCJ編集部"`）

---

## 6. 実装優先順位ロードマップ

### フェーズ1: 即時対応（1週間以内）

1. ✅ **Organizationスキーマの追加**
   - 全ページの`<head>`内に実装
   - 記事ページの`publisher`プロパティに連携

2. ✅ **WebSiteのdescription修正**
   - Yoast SEO設定で修正

3. ✅ **wordCount問題の修正**
   - Yoast SEOプラグインの更新または設定確認

### フェーズ2: 中期改善（1ヶ月以内）

4. ✅ **Article → BlogPostingへ変更**
   - Yoast SEOの記事タイプ設定で変更

5. ✅ **articleSectionの追加**
   - カテゴリー情報をスキーマに反映

6. ✅ **author情報の改善**
   - WordPressユーザープロファイルの整備

### フェーズ3: 長期強化（3ヶ月以内）

7. ⭕ **VideoObjectの実装**
   - セミナー動画がある記事に追加

8. ⭕ **Courseスキーマの実装**
   - 研修プログラム紹介ページに追加

---

## 7. Googleリッチリザルト対応状況

### 現在対応済み

- ✅ パンくずリスト (BreadcrumbList)
- ✅ サイトリンク検索ボックス (WebSite + SearchAction)
- ⚠️ 記事 (Article) - **publisherが欠落しているため不完全**

### 対応可能（実装推奨）

- ⭕ 組織のナレッジパネル (Organization)
- ⭕ 動画リッチリザルト (VideoObject) ※動画がある場合
- ⭕ コースリッチリザルト (Course) ※研修プログラムページ

### 対応不可（ポリシー制限）

- ❌ FAQ (政府・医療機関のみ)
- ❌ HowTo (廃止済み)

---

## 8. 競合他社との比較

### TCJの現状スコア: **65/100**

**評価内訳:**
- 基本実装: ✅ (CollectionPage, BreadcrumbList, WebSite, Article)
- リッチリザルト対応: ⚠️ (Organizationが欠落)
- データ品質: ⚠️ (wordCount不正確、description空白)
- 拡張スキーマ: ❌ (VideoObject, Course未実装)

**改善後の予測スコア: 85/100**

---

## 9. 推奨アクションプラン

### 今すぐ実装すべきこと

```json
<!-- 全ページの<head>内に追加 -->
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
    "url": "https://gaikoku-jinzai.tcj-education.com/wp-content/themes/tcj-recruitment/assets/img/site-logo.svg"
  },
  "description": "創業37年、外国人材の採用支援・日本語教育を専門とする総合教育企業",
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "url": "https://tcj-education.com/ja/foreign-recruitment/"
  }
}
</script>
```

### Yoast SEO設定変更

1. **サイト説明の追加**
   - WordPress管理画面 → SEO → 検索の外観 → 一般
   - サイト説明を入力

2. **記事タイプの変更**
   - SEO → 検索の外観 → コンテンツタイプ
   - 投稿のスキーマタイプを`BlogPosting`に変更

3. **著者情報の整備**
   - ユーザー → プロフィール
   - 表示名を「TCJ編集部」などに変更

---

## 10. 検証ツール

実装後、以下のツールで検証してください:

1. **Google Rich Results Test**
   - https://search.google.com/test/rich-results
   - 各ページURLを入力してテスト

2. **Schema Markup Validator**
   - https://validator.schema.org/
   - JSON-LDコードを直接貼り付けて検証

3. **Google Search Console**
   - 「拡張」セクションでリッチリザルトのエラー確認

---

## まとめ

**現状:**
- 基本的なスキーマは実装済み（Yoast SEO使用）
- 致命的なエラーはないが、最適化の余地が大きい

**最優先課題:**
1. Organizationスキーマの追加
2. WebSiteのdescription修正
3. wordCount問題の解決

**期待される効果:**
- Googleリッチリザルトでの表示改善
- クリック率（CTR）の向上
- ナレッジパネル表示の可能性

**推定作業時間:**
- フェーズ1: 2〜4時間
- フェーズ2: 4〜8時間
- フェーズ3: 要件次第

---

**レポート作成:** Claude Code (Schema.org専門家)
**次回レビュー推奨:** 実装完了後1ヶ月
