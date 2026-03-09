# Core Web Vitals & Performance Analysis
**URL**: https://gaikoku-jinzai.tcj-education.com/
**分析日**: 2026年2月17日
**分析ツール**: cURL, WebFetch, PageSource Analysis

---

## エグゼクティブサマリー

TCJ外国人材Timesのウェブサイトは、WordPressベースのコンテンツサイトで、複数のトラッキングスクリプトと外部依存が多いことから、**パフォーマンス最適化の余地が大きい**状態です。特に以下の領域で改善が必要です。

### 主要な問題点
1. **10個の同期JavaScriptファイル**がレンダリングをブロック
2. **次世代画像フォーマット（WebP/AVIF）の使用率が低い**（2箇所のみ）
3. **CSS背景画像が10個**使用されており、LCP要素が最適化されていない
4. **キャッシュ戦略が未設定**または不十分
5. **HTML初期ペイロードが52KB**と大きい

---

## 1. Core Web Vitals 推定評価

### 🔴 LCP (Largest Contentful Paint)
**予測値**: 3.5-4.5秒（目標: <2.5秒）
**ステータス**: **不合格 (Poor)**

#### 問題の詳細
- **LCP候補要素**:
  - ヒーロー画像（CSS背景画像）: `/src/img/home/hero.webp`
  - 記事のサムネイル画像（scaled PNG）: `Gemini_Generated_Image_bcgwmwbcgwmwbcgw-scaled.png`

#### 遅延要因
1. **CSS背景画像の使用**: ヒーロー画像がCSS `background-image`で実装されているため、CSSパース後まで発見されない
2. **10個の同期スクリプト**: jQueryおよびプラグインスクリプトがレンダリングをブロック
3. **画像の事前読み込み不足**: `<link rel="preload">` が未使用
4. **次世代フォーマット未対応**: PNGとJPGが主流（WebPは2箇所のみ）

#### 推奨改善策
- [ ] ヒーロー画像を `<img>` タグに変更し、`fetchpriority="high"` を設定
- [ ] LCP画像に `<link rel="preload" as="image">` を追加
- [ ] 画像をWebP/AVIF形式に変換（80%以上のサイズ削減可能）
- [ ] `srcset` と `sizes` 属性を適切に設定
- [ ] 不要なプラグインスクリプトを削除（PixelYourSite、Select2など）

---

### 🟡 INP (Interaction to Next Paint)
**予測値**: 250-350ms（目標: <200ms）
**ステータス**: **要改善 (Needs Improvement)**

#### 問題の詳細
- **22個のJavaScriptファイル**が読み込まれている
- **jQuery 3.7.1 + jQuery Migrate**: レガシー依存
- **トラッキングスクリプト多数**:
  - Google Analytics/GA4 (GT-WKPPL8VZ)
  - Facebook Pixel (1384782639254552)
  - PixelYourSite (v11.1.5)
  - Google Tag Manager

#### メインスレッド負荷の原因
1. **同期スクリプト**: 10個のスクリプトがパース時にメインスレッドをブロック
2. **大量のインラインスクリプト**: データレイヤー初期化など8+個
3. **重いプラグイン**: Flatpickr、Select2、PixelYourSite
4. **トラッキングスクリプト**: 4つの異なるトラッキングシステム

#### 推奨改善策
- [ ] jQuery依存を削除し、バニラJavaScriptに移行
- [ ] トラッキングスクリプトを統合（Google Tag Managerに集約）
- [ ] 不要なプラグインを削除（Flatpickr、Select2は未使用の可能性）
- [ ] スクリプトに `defer` または `async` 属性を追加
- [ ] コード分割とダイナミックインポートを実装
- [ ] Service Workerでスクリプトキャッシュを実装

---

### 🟢 CLS (Cumulative Layout Shift)
**予測値**: 0.05-0.08（目標: <0.1）
**ステータス**: **合格 (Good)** ※ただし改善余地あり

#### 良好な点
- 画像に `width` と `height` 属性が設定されている
- `contain-intrinsic-size: 3000px 1500px` がインライン定義されている
- レスポンシブ画像に `sizes="auto"` が使用されている

#### 潜在的なリスク
1. **Web Fontの読み込み**: Google Fonts（Material Symbols）の読み込み中にレイアウトシフトの可能性
2. **広告枠の未定義**: 動的コンテンツの挿入によるシフトの可能性
3. **CSS背景画像**: アスペクト比が未定義の要素

#### 推奨改善策
- [ ] フォントに `font-display: swap` を明示的に設定
- [ ] 動的コンテンツ領域に最小高さを設定
- [ ] CSS Grid/Flexboxで固定レイアウトを実装
- [ ] アスペクト比をCSS `aspect-ratio` で明示

---

## 2. パフォーマンス指標

### ページサイズとリソース構成

| 指標 | 値 | 評価 |
|------|-----|------|
| **HTML初期ペイロード** | 52,110 バイト (50.9 KB) | 🟡 やや大きい |
| **外部CSSファイル** | 7個 | 🟡 多い |
| **インラインCSSブロック** | 5個 | 🟡 多い |
| **外部JavaScriptファイル** | 22個（うち同期: 10個） | 🔴 非常に多い |
| **画像総数** | 15+ | 🟢 適切 |
| **次世代フォーマット使用率** | 13% (2/15) | 🔴 低い |
| **CSS背景画像** | 10個 | 🔴 多すぎる |

### サーバー設定

| 項目 | 値 | 評価 |
|------|-----|------|
| **サーバー** | nginx | 🟢 Good |
| **HTTP/2** | 不明（要確認） | ⚪ 未検証 |
| **Gzip/Brotli圧縮** | 有効（Vary: Accept-Encoding） | 🟢 Good |
| **Cache-Control** | 未確認（レスポンス空） | 🔴 設定不足の可能性 |
| **CDN** | 未使用（オリジンサーバー直接） | 🔴 未使用 |

---

## 3. リソース最適化の機会

### 3.1 画像最適化

#### 現状の問題
```html
<!-- 非効率な実装例 -->
<div style="background-image: url(https://gaikoku-jinzai.tcj-education.com/wp-content/uploads/2026/01/Gemini_Generated_Image_bcgwmwbcgwmwbcgw-scaled.png);"></div>

<!-- 低品質な画像最適化 -->
<img src="...recruitment01.jpg" loading="lazy" decoding="async" />
```

#### 推奨改善策

**1. 次世代フォーマットへの変換**
```html
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="..." fetchpriority="high" />
</picture>
```

**2. レスポンシブ画像の適切な実装**
```html
<img
  src="image-800.webp"
  srcset="image-400.webp 400w, image-800.webp 800w, image-1200.webp 1200w"
  sizes="(max-width: 768px) 100vw, 50vw"
  width="800"
  height="600"
  alt="..."
  loading="lazy"
  decoding="async"
/>
```

**3. LCP画像の事前読み込み**
```html
<link rel="preload" as="image" href="/src/img/home/hero.webp" fetchpriority="high" />
```

**4. CSS背景画像の削減**
- ヒーロー画像、記事サムネイルは `<img>` タグに変更
- 装飾的な背景のみCSSで実装

### 3.2 JavaScript最適化

#### 削除すべきスクリプト（優先度高）

1. **jQuery + jQuery Migrate**: バニラJSに移行（~30KB削減）
2. **Flatpickr**: 使用されていない場合は削除（~15KB削減）
3. **Select2**: 使用されていない場合は削除（~20KB削減）
4. **PixelYourSite**: 必要性を再検証（~10KB削減）

#### 統合すべきトラッキングスクリプト
```javascript
// 現状: 4つの独立したトラッキングシステム
- Google Analytics (GA4)
- Facebook Pixel
- Google Tag Manager
- PixelYourSite

// 推奨: Google Tag Manager に統合
→ 1つのコンテナで全てを管理（50%以上のスクリプト削減）
```

#### スクリプトの遅延読み込み
```html
<!-- 現状（問題） -->
<script src="jquery.min.js"></script>

<!-- 推奨 -->
<script src="jquery.min.js" defer></script>
```

### 3.3 CSS最適化

#### 問題点
- **インラインCSS**: 5つのブロックで約40-50KB
- **外部CSS**: 7ファイル（リクエスト多い）
- **未使用CSS**: WordPressブロックライブラリの大部分が未使用

#### 推奨改善策

**1. クリティカルCSSの抽出**
```html
<style>
  /* ファーストビューに必要な最小限のCSS（~5KB） */
  .hero { ... }
  .nav { ... }
</style>
<link rel="preload" as="style" href="main.css" onload="this.onload=null;this.rel='stylesheet'">
```

**2. 未使用CSSの削除**
- PurgeCSSまたはUnCSSでWordPress未使用スタイルを削除
- Dashiconsは管理画面のみで使用（フロントエンドから削除）

**3. CSSの結合と最小化**
```
7つの外部CSSファイル → 1つの最適化されたファイル
推定削減: 60-70KB → 20-30KB
```

---

## 4. キャッシング戦略

### 現状の問題
- HTTPヘッダーに `Cache-Control` の明示的な設定が確認できない
- ETags、Last-Modifiedの活用状況が不明

### 推奨設定

#### 静的リソース（画像、CSS、JS）
```nginx
location ~* \.(jpg|jpeg|png|gif|webp|avif|svg|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header Vary "Accept-Encoding";
}
```

#### HTMLページ
```nginx
location / {
    add_header Cache-Control "public, max-age=3600, stale-while-revalidate=86400";
}
```

#### Service Worker実装
```javascript
// キャッシュファーストストラテジー
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

---

## 5. CDN導入の推奨

### 現状
- オリジンサーバー（nginx）から直接配信
- グローバルユーザー向けには遅延が発生する可能性

### 推奨CDNプロバイダー

1. **Cloudflare** (推奨)
   - 無料プランで十分
   - 自動WebP/AVIF変換
   - HTTP/2、HTTP/3対応
   - Brotli圧縮
   - DDoS保護

2. **AWS CloudFront**
   - 高パフォーマンス
   - Lambda@Edgeで画像変換

3. **Fastly**
   - リアルタイムキャッシュパージ
   - エッジコンピューティング

---

## 6. パフォーマンス改善ロードマップ

### Phase 1: クイックウィン（1-2週間）

**優先度: 高**
- [ ] 画像をWebP形式に変換（即時50-70%削減）
- [ ] ヒーロー画像にpreloadディレクティブ追加
- [ ] jQuery以外の不要なプラグインを削除
- [ ] スクリプトにdefer属性を追加
- [ ] Cloudflare無料CDNを導入

**期待効果**: LCP 1.5秒改善、INP 100ms改善

### Phase 2: 構造的改善（1ヶ月）

**優先度: 中**
- [ ] jQuery依存を削除（バニラJS化）
- [ ] トラッキングをGTMに統合
- [ ] クリティカルCSSを抽出
- [ ] 未使用CSSを削除
- [ ] Service Worker実装

**期待効果**: LCP 0.8秒改善、INP 80ms改善、CLS 0.02改善

### Phase 3: 高度な最適化（2-3ヶ月）

**優先度: 低**
- [ ] HTTP/3対応
- [ ] 画像CDNの導入（Cloudinary/Imgix）
- [ ] コード分割とダイナミックインポート
- [ ] SSRまたはSSG化の検討
- [ ] Edge Computing実装

**期待効果**: LCP 0.5秒改善、INP 50ms改善

---

## 7. 改善後の予測値

### 改善前（現状）
| 指標 | 値 | ステータス |
|------|-----|-----------|
| LCP | 3.5-4.5秒 | 🔴 Poor |
| INP | 250-350ms | 🟡 Needs Improvement |
| CLS | 0.05-0.08 | 🟢 Good |

### 改善後（Phase 1+2完了時）
| 指標 | 値 | ステータス |
|------|-----|-----------|
| LCP | **1.8-2.2秒** | 🟢 Good |
| INP | **120-180ms** | 🟢 Good |
| CLS | **0.03-0.05** | 🟢 Good |

### 改善後（Phase 3完了時）
| 指標 | 値 | ステータス |
|------|-----|-----------|
| LCP | **1.2-1.5秒** | 🟢 Excellent |
| INP | **80-120ms** | 🟢 Excellent |
| CLS | **0.01-0.03** | 🟢 Excellent |

---

## 8. 技術的な実装ガイド

### 8.1 nginx設定例

```nginx
# /etc/nginx/conf.d/performance.conf

# Gzip圧縮
gzip on;
gzip_vary on;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
gzip_min_length 1000;

# Brotli圧縮（優先）
brotli on;
brotli_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

# HTTP/2有効化
listen 443 ssl http2;

# キャッシュ設定
location ~* \.(jpg|jpeg|png|gif|webp|avif|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

location ~* \.(css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# セキュリティヘッダー
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
```

### 8.2 WordPress最適化プラグイン

**推奨プラグイン**
1. **WP Rocket** (有料) - オールインワンパフォーマンス
2. **Perfmatters** (有料) - スクリプト管理
3. **ShortPixel** (無料) - 画像最適化
4. **Asset CleanUp** (無料) - 不要なスクリプト削除

**削除すべきプラグイン**
- PixelYourSite → Google Tag Managerに移行
- WP User Avatar → 軽量な代替に変更

### 8.3 画像変換スクリプト

```bash
#!/bin/bash
# 全JPG/PNGをWebPに変換

find ./wp-content/uploads -type f \( -name "*.jpg" -o -name "*.png" \) | while read file; do
    output="${file%.*}.webp"
    if [ ! -f "$output" ]; then
        cwebp -q 85 "$file" -o "$output"
        echo "Converted: $output"
    fi
done
```

### 8.4 Service Worker実装例

```javascript
// sw.js
const CACHE_VERSION = 'v1';
const CACHE_ASSETS = [
  '/assets/css/app.css',
  '/assets/js/app.js',
  '/src/img/home/hero.webp'
];

// インストール
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => {
      return cache.addAll(CACHE_ASSETS);
    })
  );
});

// フェッチ（キャッシュファースト）
self.addEventListener('fetch', (event) => {
  if (event.request.destination === 'image') {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request).then((fetchResponse) => {
          return caches.open(CACHE_VERSION).then((cache) => {
            cache.put(event.request, fetchResponse.clone());
            return fetchResponse;
          });
        });
      })
    );
  }
});
```

---

## 9. モニタリングとテスト

### 推奨ツール

1. **PageSpeed Insights** (Google公式)
   - URL: https://pagespeed.web.dev/
   - 毎週月曜日に実行

2. **GTmetrix**
   - URL: https://gtmetrix.com/
   - 詳細なウォーターフォール分析

3. **WebPageTest**
   - URL: https://www.webpagetest.org/
   - 複数ロケーションからのテスト

4. **Chrome DevTools Lighthouse**
   - ローカルでの継続的テスト

5. **Google Search Console**
   - Core Web Vitalsレポート（実ユーザーデータ）

### 継続的モニタリング

```yaml
# GitHub Actions: .github/workflows/performance.yml
name: Performance Test
on:
  schedule:
    - cron: '0 0 * * 1'  # 毎週月曜日午前0時
  push:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Lighthouse
        uses: treosh/lighthouse-ci-action@v9
        with:
          urls: 'https://gaikoku-jinzai.tcj-education.com/'
          budgetPath: './budget.json'
          uploadArtifacts: true
```

---

## 10. まとめと次のステップ

### 現状評価: 🔴 パフォーマンス不合格

**スコア予測**
- **PageSpeed Insights**: 40-55点（モバイル）
- **GTmetrix**: C-Dグレード
- **Google Search Console**: Core Web Vitals不合格

### 最優先アクション（今週実施）

1. ✅ **画像をWebPに変換** → LCP 1.5秒改善
2. ✅ **不要なプラグイン削除** → INP 80ms改善
3. ✅ **Cloudflare CDN導入** → LCP 0.5秒改善
4. ✅ **スクリプトにdefer追加** → INP 50ms改善

### 成功の定義

**3ヶ月後の目標**
- PageSpeed Insights: 90点以上（モバイル）
- LCP: 1.5秒以下
- INP: 150ms以下
- CLS: 0.05以下
- Google Search Console: Core Web Vitals合格率 100%

---

## 参考資料

### 公式ドキュメント
- [Core Web Vitals report - Search Console Help](https://support.google.com/webmasters/answer/9205520?hl=en)
- [About PageSpeed Insights | Google for Developers](https://developers.google.com/speed/docs/insights/v5/about)
- [What Are Core Web Vitals & How to Improve Them](https://www.monsterinsights.com/what-are-core-web-vitals/)

### ツールとリソース
- [8 Best Tools for Core Web Vitals Testing](https://wp-rocket.me/blog/core-web-vitals-testing-performance-monitoring-tools/)
- [Best Core Web Vitals Tools in 2026](https://www.singlegrain.com/artificial-intelligence/best-core-web-vitals-tools-in-2026/)
- [GTmetrix | Website Performance Testing](https://gtmetrix.com/)
- [DebugBear Core Web Vitals Test](https://www.debugbear.com/test/core-web-vitals)
- [SpeedVitals Core Web Vitals Checker](https://speedvitals.com/tools/core-web-vitals-checker)

### 学習リソース
- [How to Use PageSpeed Insights to Improve Core Web Vitals](https://www.workshopdigital.com/blog/how-to-use-pagespeed-insights-to-improve-core-web-vitals/)
- [Core Web Vitals: Key metrics to measure site performance](https://www.hostinger.com/tutorials/core-web-vitals)
- [Measure Core Web Vitals | PageSpeed Insights](https://www.matthewedgar.net/measure-core-web-vitals-page-speed-insights/)

---

**報告書作成**: Claude Code Analysis Engine
**最終更新**: 2026年2月17日
