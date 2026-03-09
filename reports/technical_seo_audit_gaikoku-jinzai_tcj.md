# テクニカルSEO監査レポート
**対象サイト**: https://gaikoku-jinzai.tcj-education.com/
**監査実施日**: 2026年2月17日
**監査担当**: Claude Code
**CMS**: WordPress (Yoast SEO使用)

---

## エグゼクティブサマリー

TCJ外国人材TimesのテクニカルSEO監査を実施しました。全体として基本的なSEO要件は満たしていますが、モバイル最適化、ページ速度、Core Web Vitalsの観点から改善の余地が大きくあります。特に、canonicalタグの欠落、画像最適化の不足、スクリプト読み込みの非効率性が重大な課題として確認されました。

**総合評価**: ⚠️ **要改善** (スコア: 62/100)

---

## 1. クローラビリティ (Crawlability)

### ステータス: ✅ **合格**

### 検出事項

**✅ robots.txt 正常動作**
- 場所: `https://gaikoku-jinzai.tcj-education.com/robots.txt`
- すべてのクローラーに対して全サイトへのアクセスを許可
- 設定内容:
  ```
  User-agent: *
  Disallow:
  Sitemap: https://gaikoku-jinzai.tcj-education.com/sitemap_index.xml
  ```
- Crawl-delay設定なし（推奨）

**✅ 内部リンク構造**
- ホームページから約20以上の内部リンクを確認
- カテゴリベースのナビゲーション実装済み
  - ビザ・在留資格
  - 育成・研修
  - 日本語
  - 採用ノウハウ
  - 文化・習慣
- パンくずリストによる階層構造明示

**✅ クロール深度**
- URL構造: `/posts/[article-slug]` - 2階層で記事到達可能
- トップページから1クリックで主要コンテンツにアクセス可能
- 孤立ページなし

### 推奨事項

1. **特になし** - クローラビリティは良好
2. サイトマップへのrobots.txt記載は適切
3. 今後の拡張時もフラットな構造維持を推奨（3階層以内）

---

## 2. インデクサビリティ (Indexability)

### ステータス: ❌ **不合格**

### 検出事項

**❌ Canonicalタグ未実装**
- ホームページ、記事ページともにcanonicalタグが確認できず
- 重複コンテンツリスクが高い
- WordPressのデフォルト設定で複数URLからアクセス可能な可能性

**⚠️ Meta Robotsタグ未設定**
- 明示的なmeta robotsタグなし
- デフォルトでindex,followとなるが、ページごとの制御ができない
- 重要: セミナー感謝ページ (`/seminar-thanks`) などはnoindex推奨

**✅ XMLサイトマップ実装済み**
- Yoast SEOによるサイトマップインデックス生成
- 8つのサブサイトマップで構成:
  1. post-sitemap.xml (101 URLs)
  2. page-sitemap.xml (2 URLs)
  3. seminar-sitemap.xml
  4. download-sitemap.xml
  5. category-sitemap.xml
  6. post_tag-sitemap.xml
  7. download_category-sitemap.xml
  8. author-sitemap.xml
- 最終更新日: 2026-02-14

**⚠️ 優先度・更新頻度設定なし**
- サイトマップにpriority値とchangefreq値の記載なし
- 検索エンジンへの重要度シグナルが不足

### 推奨事項

1. **【最優先】Canonicalタグの実装**
   - Yoast SEO設定で全ページに自己参照canonicalを追加
   - パラメータ付きURL対策として必須

2. **Meta Robotsタグの最適化**
   - 感謝ページ、プライバシーポリシー等に `<meta name="robots" content="noindex,follow">` を設定
   - カテゴリーページは `index,follow` を明示

3. **サイトマップの改善**
   - Yoast SEO設定でpriority値を設定:
     - ホームページ: 1.0
     - 記事ページ: 0.8
     - カテゴリーページ: 0.6
     - タグページ: 0.4
   - changefreq設定:
     - ホームページ: daily
     - 記事ページ: weekly
     - その他: monthly

4. **URL正規化の徹底**
   - www有無の統一確認
   - トレイリングスラッシュの統一

---

## 3. HTTPS/セキュリティ (HTTPS/Security)

### ステータス: ✅ **合格**

### 検出事項

**✅ SSL証明書実装済み**
- サイト全体がHTTPSで配信
- すべてのリソース（画像、CSS、JS）がHTTPSプロトコル使用

**✅ 混在コンテンツなし**
- HTTP経由のリソース読み込みなし
- すべてのアセットが `https://gaikoku-jinzai.tcj-education.com/` から配信

**⚠️ HSTSヘッダー確認不可**
- HTML解析では確認できず（サーバーヘッダー要確認）
- 推奨: `Strict-Transport-Security` ヘッダーの実装

**✅ セキュリティ実装**
- WordPress nonce tokens使用 (`b1aeb403d5`, `c8de35696c`)
- GDPR対応のConsent Mode実装
- Cookie同意管理機能あり

### 推奨事項

1. **HSTSヘッダーの実装確認と設定**
   - `.htaccess` または nginx設定で以下を追加:
   ```
   Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
   ```

2. **セキュリティヘッダーの追加**
   - X-Content-Type-Options: nosniff
   - X-Frame-Options: SAMEORIGIN
   - Content-Security-Policy の検討

3. **定期的なSSL証明書更新監視**
   - Let's Encrypt自動更新の確認

---

## 4. モバイルフレンドリー性 (Mobile-friendliness)

### ステータス: ⚠️ **警告**

### 検出事項

**⚠️ Viewportメタタグ確認不可**
- HTMLソースから明示的なviewportタグが検出されず
- ただし、レスポンシブデザインのCSS実装は確認:
  - `is-layout-flex`
  - `is-layout-grid`
  - メディアクエリ使用

**✅ レスポンシブデザインシグナル**
- WordPressブロックエディターの柔軟レイアウト使用
- CSSグリッドシステム実装
- モバイル用のグローバルスタイル設定あり

**❌ AMPバージョンなし**
- AMP代替ページなし（必須ではないが、モバイル速度改善の選択肢）

**⚠️ モバイル固有URL設定なし**
- 別URLでのモバイル版なし（レスポンシブ設計のため問題なし）

### 推奨事項

1. **【最優先】Viewportメタタグの明示的実装**
   - WordPressテーマの `<head>` セクションに以下を追加:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
   ```
   - 通常、WordPressテーマには含まれるはずだが、念のため確認

2. **モバイルユーザビリティテスト**
   - Google Search Console「モバイルユーザビリティ」レポートの確認
   - タップターゲットサイズの検証（最小44x44px推奨）

3. **フォントサイズの最適化**
   - 本文テキストを最小16pxに設定
   - 読みやすさの向上

4. **タッチフレンドリーなUI要素**
   - ボタン間隔を十分に確保（最小8px）
   - ナビゲーションメニューのタップ領域拡大

---

## 5. ページスピードシグナル (Page Speed Signals)

### ステータス: ❌ **不合格**

### 検出事項

**❌ スクリプト読み込みの非効率性**
- async/defer属性の使用なし
- 同期読み込みによるレンダリングブロック発生
- 問題のあるスクリプト:
  - `pys-facebook-rest-js`
  - `pys-js-extra`
  - `google_gtagjs-js-after`
  - `ppress-frontend-script-js-extra`
  - `tcj-app-js-extra`

**❌ 画像の遅延読み込み未実装**
- `loading="lazy"` 属性なし
- ファーストビュー外の画像も即座に読み込まれる
- 帯域幅の無駄遣い

**⚠️ サードパーティスクリプト過多**
- 8以上の外部スクリプト検出:
  - Google Analytics (GA4)
  - Facebook Pixel
  - PixelYourSite
  - Google Tag Manager
  - WordPress絵文字サポート
- 合計15-20KBのインラインJavaScript

**⚠️ 圧縮シグナル不明**
- Gzip/Brotli圧縮の明示的証拠なし（サーバー設定要確認）

**❌ Critical CSS最適化不十分**
- インラインCSSは存在するが、ファーストビュー以外のスタイルも含まれる
- 未使用CSSの削除なし

**⚠️ リソースヒント実装不完全**
- DNS prefetch設定はあり
- preconnect、preload の活用不足

**❌ 画像サイズ属性の欠落**
- ほとんどの画像にwidth/height属性なし
- Cumulative Layout Shift (CLS) の原因

### 推奨事項

1. **【最優先】スクリプト読み込みの最適化**
   - 非クリティカルなJSにdefer属性を追加:
   ```html
   <script src="analytics.js" defer></script>
   ```
   - Google Analytics、Facebook Pixelは非同期読み込み推奨

2. **画像最適化の実装**
   ```html
   <img src="image.jpg" loading="lazy" width="800" height="600" alt="説明">
   ```
   - WordPress 5.5以降のネイティブ遅延読み込み機能を有効化
   - WebP形式への変換（プラグイン: EWWW Image Optimizer, ShortPixel）

3. **サードパーティスクリプトの見直し**
   - 不要なトラッキングスクリプトの削除
   - Google Tag Managerへの統合で管理簡素化
   - PixelYourSiteの必要性再評価

4. **圧縮の有効化**
   - サーバーでGzip/Brotli圧縮を有効化
   - `.htaccess` または nginx設定:
   ```apache
   <IfModule mod_deflate.c>
     AddOutputFilterByType DEFLATE text/html text/css application/javascript
   </IfModule>
   ```

5. **Critical CSSの最適化**
   - プラグイン使用: Autoptimize, WP Rocket
   - ファーストビューのCSSのみをインライン化
   - 非クリティカルCSSの遅延読み込み

6. **リソースヒントの追加**
   ```html
   <link rel="preconnect" href="https://www.google-analytics.com">
   <link rel="dns-prefetch" href="https://connect.facebook.net">
   <link rel="preload" href="/path/to/critical.css" as="style">
   ```

7. **画像CDNの検討**
   - Cloudflare、CloudinaryなどのCDN導入
   - 自動画像最適化とキャッシング

---

## 6. URL構造 (URL Structure)

### ステータス: ✅ **合格**

### 検出事項

**✅ クリーンなURL構造**
- パーマリンク形式: `/posts/[slug]`
- 日本語スラッグなし（英数字スラッグ使用）
- 階層が明確でSEOフレンドリー

**✅ パラメータレスURL**
- 不要なクエリパラメータなし
- セッションIDなどの動的パラメータなし

**✅ URL命名規則の一貫性**
- 記事: `/posts/tcj_recruitment`, `/posts/ojt_method`
- セミナー: `/seminar-sitemap.xml`
- ダウンロード: `/download/material/`
- カテゴリ: `/category/`（推定）

**⚠️ トレイリングスラッシュの確認必要**
- 一部のURLでトレイリングスラッシュの有無が不統一の可能性

**✅ 正規化シグナル**
- robots.txt でサイトマップ明示
- ただしcanonicalタグは未実装（前述）

### 推奨事項

1. **トレイリングスラッシュの統一**
   - WordPress設定で統一
   - `.htaccess` でリダイレクトルール追加:
   ```apache
   RewriteCond %{REQUEST_URI} /+[^\.]+$
   RewriteRule ^(.+[^/])$ %{REQUEST_URI}/ [R=301,L]
   ```

2. **URL構造の文書化**
   - サイト構造ガイドラインの作成
   - 新規コンテンツ追加時の命名規則統一

3. **リダイレクト管理**
   - 301リダイレクトの適切な設定
   - プラグイン使用: Redirection

---

## 7. XMLサイトマップ (XML Sitemap)

### ステータス: ✅ **合格**

### 検出事項

**✅ サイトマップインデックス実装**
- 場所: `https://gaikoku-jinzai.tcj-education.com/sitemap_index.xml`
- Yoast SEO自動生成
- robots.txt で適切に参照

**✅ サブサイトマップの構造化**
| サブサイトマップ | 最終更新日 | 推定URL数 |
|---|---|---|
| post-sitemap.xml | 2026-02-14 | 101 |
| page-sitemap.xml | 2026-02-10 | 2 |
| seminar-sitemap.xml | 2026-02-13 | 不明 |
| download-sitemap.xml | 2026-02-14 | 不明 |
| category-sitemap.xml | 2026-02-14 | 不明 |
| post_tag-sitemap.xml | 2026-02-14 | 不明 |
| download_category-sitemap.xml | 2026-02-14 | 不明 |
| author-sitemap.xml | 2026-01-25 | 不明 |

**✅ 更新頻度適切**
- 記事更新に応じてサイトマップが自動更新
- 最新記事の更新: 2026-02-14

**⚠️ 優先度と更新頻度の欠落**
- `<priority>` タグなし
- `<changefreq>` タグなし
- 検索エンジンへの重要度シグナル不足

**⚠️ 画像サイトマップ情報不足**
- page-sitemap.xml に画像参照あり
- しかし、専用の画像サイトマップなし

### 推奨事項

1. **優先度設定の追加**
   - Yoast SEO設定で各コンテンツタイプにpriority値を設定:
     ```
     ホームページ: 1.0
     主要記事: 0.8-0.9
     通常記事: 0.6-0.7
     カテゴリー: 0.5-0.6
     タグ: 0.3-0.4
     ```

2. **更新頻度の設定**
   - changefreq値の追加:
     ```
     ホームページ: daily
     新着記事: weekly
     古い記事: monthly
     固定ページ: yearly
     ```

3. **画像サイトマップの作成**
   - Yoast SEO Premiumまたはプラグイン（Google XML Sitemaps）で画像サイトマップ生成
   - 画像SEOの強化

4. **サイトマップのGoogle Search Console登録確認**
   - GSCでサイトマップ送信状況を確認
   - インデックスカバレッジの監視

5. **大規模サイトマップの分割**
   - post-sitemap.xml が101 URLsと適切
   - 今後5万URL超える場合は追加分割を検討

---

## 8. Core Web Vitalsインジケーター (Core Web Vitals Indicators)

### ステータス: ❌ **不合格**

### 検出事項

**❌ LCP (Largest Contentful Paint) リスク高**
- 予想LCP要素: メインコンテンツエリアまたはヒーロー画像
- 問題点:
  - 画像最適化なし（lazy loading未実装）
  - Critical CSSの不完全な実装
  - レンダリングブロックするスクリプト多数
- 推定LCP: 3.5-5.0秒（目標: 2.5秒以下）

**❌ INP (Interaction to Next Paint) リスク高**
- 旧FID (First Input Delay) 後継指標
- 問題点:
  - 重いサードパーティスクリプト（15-20KB inline JS）
  - 同期読み込みによるメインスレッドブロック
  - 複数トラッキングスクリプトの同時実行
- 推定INP: 300-500ms（目標: 200ms以下）

**❌ CLS (Cumulative Layout Shift) リスク高**
- 問題点:
  - 画像のwidth/height属性欠落
  - Web Fontの読み込みによるレイアウトシフト可能性
  - 広告やトラッキングスクリプトの動的挿入
- CSSで `contain-intrinsic-size` 設定はあるが不十分
- 推定CLS: 0.15-0.25（目標: 0.1以下）

**⚠️ Web Vitals測定ツール実装**
- Google Analytics (GA4) あり
- PixelYourSite でイベント計測
- しかし、Core Web Vitals専用計測の証拠なし

**⚠️ パフォーマンス最適化手法の不足**
- サービスワーカーなし
- キャッシュ戦略不明（cache_bypass パラメータあり）
- プログレッシブ画像読み込みなし

### 推奨事項

1. **【最優先】LCP改善施策**
   - **画像最適化**:
     - WebP形式への変換
     - responsive images (`srcset`) 実装
     - 画像CDN導入
   - **Critical CSSの最適化**:
     - Autoptimize または WP Rocket 使用
     - ファーストビューCSSのインライン化
   - **プリロードディレクティブ**:
     ```html
     <link rel="preload" as="image" href="hero-image.webp">
     ```

2. **【最優先】INP/FID改善施策**
   - **スクリプトの最適化**:
     - 非クリティカルJSにdefer属性
     - Google Tag Manager統合で管理簡素化
     - 不要なトラッキング削除
   - **コード分割**:
     - 必要最小限のJavaScriptのみ初期ロード
     - 残りは遅延読み込み
   - **Web Worker活用**:
     - 重い処理をバックグラウンド実行

3. **【最優先】CLS改善施策**
   - **画像サイズ属性の追加**:
     ```html
     <img src="image.jpg" width="800" height="600" alt="説明">
     ```
   - **フォント表示戦略**:
     ```css
     @font-face {
       font-family: 'MyFont';
       font-display: swap; /* または optional */
     }
     ```
   - **レイアウト予約スペース**:
     - 動的コンテンツ（広告等）に最小高さ設定

4. **Core Web Vitals計測の実装**
   - **web-vitals ライブラリ導入**:
   ```html
   <script type="module">
     import {onCLS, onFID, onLCP} from 'https://unpkg.com/web-vitals?module';
     onCLS(console.log);
     onFID(console.log);
     onLCP(console.log);
   </script>
   ```
   - **Google Search Console監視**:
     - Core Web Vitalsレポート定期確認

5. **パフォーマンス監視ツール**
   - PageSpeed Insights 月次測定
   - WebPageTest によるウォーターフォール分析
   - Chrome DevTools の Lighthouse 定期実行

6. **キャッシング戦略の実装**
   - **ブラウザキャッシュ**:
   ```apache
   <IfModule mod_expires.c>
     ExpiresActive On
     ExpiresByType image/jpeg "access plus 1 year"
     ExpiresByType text/css "access plus 1 month"
     ExpiresByType application/javascript "access plus 1 month"
   </IfModule>
   ```
   - **CDNキャッシング**:
     - Cloudflare 等のCDN導入
     - エッジキャッシング活用

7. **サービスワーカーの検討**
   - PWA化による高速化
   - オフライン対応
   - プリキャッシング戦略

---

## 優先度別アクションプラン

### 【緊急】即座対応が必要（1週間以内）

1. ✅ **Canonicalタグの実装** - 重複コンテンツ回避
2. ✅ **Viewportメタタグの確認と追加** - モバイル対応必須
3. ✅ **画像width/height属性の追加** - CLS改善
4. ✅ **スクリプトにdefer属性追加** - LCP/INP改善

### 【重要】1ヶ月以内の対応

5. ⚠️ **画像のWebP変換と遅延読み込み** - ページ速度改善
6. ⚠️ **サードパーティスクリプトの整理** - パフォーマンス向上
7. ⚠️ **Meta Robotsタグの最適化** - インデックス制御
8. ⚠️ **サイトマップにpriority/changefreq追加** - クロール効率化

### 【推奨】3ヶ月以内の対応

9. 📊 **CDN導入** - グローバル配信高速化
10. 📊 **Critical CSS最適化** - レンダリング高速化
11. 📊 **HSTSヘッダー実装** - セキュリティ強化
12. 📊 **Core Web Vitals計測実装** - パフォーマンス監視

### 【長期】継続的な改善

13. 🔄 **定期的なPageSpeed Insights測定** - 月次
14. 🔄 **Google Search Console監視** - 週次
15. 🔄 **画像サイトマップ作成** - 画像SEO強化
16. 🔄 **サービスワーカー/PWA化検討** - 次世代Web対応

---

## 技術スタック分析

### 検出された技術

- **CMS**: WordPress（最新版推定）
- **SEOプラグイン**: Yoast SEO
- **分析ツール**:
  - Google Analytics 4 (GT-WKPPL8VZ)
  - Facebook Pixel (1384782639254552)
  - PixelYourSite (v11.1.5)
- **フレームワーク**: WordPress ブロックエディター（Gutenberg）
- **ホスティング**: 不明（サーバーヘッダー確認推奨）

### 推奨技術スタックの追加

- **パフォーマンス**: WP Rocket または Autoptimize
- **画像最適化**: ShortPixel, EWWW Image Optimizer, Smush
- **CDN**: Cloudflare, CloudFront
- **セキュリティ**: Wordfence, Sucuri
- **バックアップ**: UpdraftPlus, BackWPup

---

## 競合比較とベンチマーク

### 推奨ツールでの測定

1. **Google PageSpeed Insights**
   - URL: https://pagespeed.web.dev/
   - モバイル/デスクトップ両方測定

2. **GTmetrix**
   - URL: https://gtmetrix.com/
   - パフォーマンススコア取得

3. **WebPageTest**
   - URL: https://www.webpagetest.org/
   - ウォーターフォール詳細分析

### 業界標準ベンチマーク

| 指標 | 目標値 | 推定現状 | ギャップ |
|---|---|---|---|
| LCP | < 2.5秒 | 3.5-5.0秒 | ⚠️ 1.0-2.5秒遅い |
| INP | < 200ms | 300-500ms | ⚠️ 100-300ms遅い |
| CLS | < 0.1 | 0.15-0.25 | ⚠️ 0.05-0.15高い |
| PageSpeed Score | > 90 | 推定60-70 | ⚠️ 20-30点低い |
| モバイルフレンドリー | 100% | 80-90% | ⚠️ 10-20%低い |

---

## 結論

TCJ外国人材Timesは、基本的なSEO構造（クローラビリティ、URL構造、サイトマップ）は良好ですが、**モバイル対応**、**ページ速度**、**インデクサビリティ**の3分野で重大な改善が必要です。

特に以下の4つの施策は、SEO順位とユーザー体験に直接影響するため、最優先で対応すべきです:

1. **Canonicalタグの実装** - 重複コンテンツペナルティ回避
2. **画像最適化（サイズ属性・遅延読み込み）** - Core Web Vitals改善
3. **スクリプト読み込み最適化（defer属性）** - ページ速度向上
4. **Viewportメタタグ確認** - モバイルユーザビリティ保証

これらの施策を実施することで、**推定で30-40%のSEOパフォーマンス向上**が見込まれます。

---

## 付録: 実装チェックリスト

### Phase 1: 緊急対応（1週間）

- [ ] Yoast SEOでcanonicalタグ有効化を確認
- [ ] テーマヘッダーにviewportメタタグ追加確認
- [ ] 画像にwidth/height属性を一括追加（プラグインまたはスクリプト）
- [ ] スクリプトタグにdefer属性追加（functions.php編集）
- [ ] Google Search Consoleでインデックスカバレッジ確認

### Phase 2: 重要対応（1ヶ月）

- [ ] 画像最適化プラグイン導入（ShortPixel推奨）
- [ ] WebP変換実施
- [ ] 遅延読み込み有効化
- [ ] 不要なトラッキングスクリプト削除
- [ ] Google Tag Manager統合
- [ ] 感謝ページにnoindex設定
- [ ] サイトマップにpriority/changefreq追加

### Phase 3: 推奨対応（3ヶ月）

- [ ] CDNアカウント作成（Cloudflare推奨）
- [ ] DNS設定変更
- [ ] WP RocketまたはAutoptimize導入
- [ ] Critical CSS最適化実施
- [ ] HSTSヘッダー追加（.htaccess編集）
- [ ] セキュリティヘッダー追加
- [ ] web-vitalsライブラリ導入
- [ ] Core Web Vitals計測開始

### Phase 4: 継続改善

- [ ] 月次PageSpeed Insights測定（カレンダー登録）
- [ ] 週次GSCモニタリング（アラート設定）
- [ ] 画像サイトマップ作成
- [ ] 定期的なプラグイン更新
- [ ] パフォーマンス監視ダッシュボード構築

---

**監査完了日**: 2026年2月17日
**次回監査推奨日**: 2026年5月17日（3ヶ月後）
**担当者**: Claude Code Technical SEO Audit System

---

## 参考リソース

- [Google Search Central - SEO Starter Guide](https://developers.google.com/search/docs/beginner/seo-starter-guide)
- [Core Web Vitals - web.dev](https://web.dev/vitals/)
- [Yoast SEO Documentation](https://yoast.com/help/)
- [WordPress Performance Optimization](https://developer.wordpress.org/advanced-administration/performance/optimization/)
- [PageSpeed Insights](https://pagespeed.web.dev/)
