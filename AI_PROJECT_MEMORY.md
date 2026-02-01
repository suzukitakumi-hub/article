# Abitus CFE プロジェクトメモリ

## 🎯 プロジェクト概要

**目的**: Abitus CFE（公認不正検査士）関連記事のSEO最適化とGitHub Pagesでの公開

**サイト**: https://suzukitakumi-hub.github.io/article/

**ブランド要件**: Abitus公式サイトのデザインを完全再現（ピクセルパーフェクト）

---

## 📂 記事一覧

| 記事 | ステータス | URL |
|---|---|---|
| **CFEとは** | ✅ 公開済み | `/CFEとは/` |
| **CFE年収** | ✅ 公開済み | `/CFE年収/` |
| **CFE難易度** | ✅ 公開済み | `/CFE難易度/` |
| **コンプライアンス違反** | ✅ 公開済み | `/コンプライアンス違反/` |
| **不正会計** | ✅ 公開済み | `/不正会計/` |

---

## 🎨 デザイン実装

### CSS設計

**ファイル**: `abitus_style.css`

**実装内容**:
- Abitus公式サイトの完全再現
- 2カラムレイアウト（メインコンテンツ + サイドバー）
- 左側追従ボタン（資料請求、無料説明会）
- ヘッダー構造（白トップバー + 黒ナビゲーション）
- フォント・配色の統一

### 技術的課題と解決

#### 1. GitHub Pages CSS読み込みエラー（2026-01-28）

**問題**: 相対パス（`./css/abitus_style.css`）でCSSが読み込めない

**原因**: GitHub Pagesのリポジトリ名がURLに含まれる構造

**解決策**:
```html
<!-- ❌ 相対パス（動かない） -->
<link rel="stylesheet" href="./css/abitus_style.css">

<!-- ✅ ルート相対パス + キャッシュバスター -->
<link rel="stylesheet" href="/article/コンプライアンス違反/css/abitus_style.css?v=20260128">
```

#### 2. FAQセクションのスタイル不具合（2026-01-28）

**問題**: `.c-faq` クラスが未定義でQ/Aアイコンが表示されない

**解決策**: Abitus公式の `.c-qa` クラスに統一
```css
.c-qa__question::before {
  content: "Q";
  background-color: #024796; /* 青 */
}

.c-qa__answer::before {
  content: "A";
  background-color: #9BAA34; /* 緑 */
}
```

---

## 📝 主要記事の制作経緯

### 「コンプライアンス違反事例20選」

**制作日**: 2026-01-26〜2026-01-28

**内容**:
- ビッグモーター、ホンダ等の2024-2025最新事例
- 不正トライアングル理論の解説
- 業界別事例（金融、製造、小売等）
- FAQ形式のQ&A

**リライトポイント**:
- AI特有の言い回しを排除
- 自然な日本語への修正
- 公式サイトのトーン&マナーに統一

### 「不正会計とは」

**制作日**: 2026-01-26

**リライト内容**:
- AI臭を排除し、人間らしい文章に修正
- 過度な装飾（赤文字、黄色アンダーライン）を削除
- 見出しクラスを公式仕様（`.c-heading-seco`, `.c-heading-tert`）に統一

### CFE合格率の修正（2026-01-28）

**対象記事**: CFE難易度、不正会計

**修正内容**: Abitus合格率を「約80%」→「90%」に変更

**理由**: ユーザー指摘による最新情報への更新

---

## 🛠️ スクリプト修正

### GAS（Google Apps Script）

**対象ファイル**:
- `月次USCPA.txt`
- `月次MBA.txt`

**修正内容**:
- `SyntaxError` の修正
- 配列処理の適正化
- 定型レポート出力機能の改善

---

## ✅ 完了した作業

### デザイン・開発
- [x] Abitus公式デザインの完全再現（CSS実装）
- [x] 2カラムレイアウト + サイドバー
- [x] 左側追従ボタン（資料請求、無料説明会）
- [x] GitHub Pages CSS読み込み問題の解決
- [x] FAQセクションのスタイル修正

### 記事制作
- [x] CFEとは（公開済み）
- [x] CFE年収（公開済み）
- [x] CFE難易度（公開済み）
- [x] コンプライアンス違反（公開済み）
- [x] 不正会計（公開済み）

### データ修正
- [x] CFE合格率の更新（80%→90%）

### ワークスペース整理（2026-01-29）
- [x] Abitus専用ワークスペース作成（`abitus_workspace`）
- [x] 全記事フォルダの移動
- [x] SEOワークフロー複製（`/seo-article-writing`, `/seo-article-rewrite`）
- [x] WordPress→Markdown変換ガイド作成

---

## 🚀 残っている作業

### 記事拡充
- [ ] CFE転職（新規記事）
- [ ] CFE試験対策（新規記事）
- [ ] USCPA vs CFE比較記事

### SEO最適化
- [ ] Search Consoleデータ分析
- [ ] 機会損失キーワードの抽出
- [ ] CTR改善が必要な記事のリライト

### WordPress連携
- [ ] WordPressからXMLエクスポート
- [ ] Markdown変換（`npx wordpress-export-to-markdown`）
- [ ] 既存記事のインポート

---

## 📊 SEO戦略（参考）

### 評価指標（TCJで採用した方針）

| 指標 | 目的 |
|---|---|
| **エンゲージメント率** | コンテンツ品質の測定 |
| **オーガニック流入ページ数** | サイト構造の健全性 |
| **意図別キーワード順位** | 市場シェアの把握 |

**ベンチマーク**: BtoBメディアのエンゲージメント率は55〜70%が標準

---

## 🔗 関連リンク

- [Abitus公式サイト](https://www.abitus.co.jp/)
- [GitHub Pages](https://suzukitakumi-hub.github.io/article/)
- [WordPress→Markdown変換ツール](https://github.com/lonekorean/wordpress-export-to-markdown)

---

## 📌 重要な設計判断

### CSSパス戦略
- GitHub Pagesではルート相対パス（`/article/...`）を使用
- キャッシュバスター（`?v=YYYYMMDD`）で更新を強制

### デザイン方針
- Abitus公式サイトのピクセルパーフェクト再現
- 独自の装飾は追加しない
- 公式CSSクラス名を使用（`.c-heading-seco`, `.c-qa` 等）

### コンテンツ方針
- AI特有の言い回しを排除
- 自然な日本語を優先
- 最新情報（2024-2025年）を積極的に盛り込む

---

## 🗂️ ワークスペース構成

```
abitus_workspace/
├── CFEとは/
├── CFE年収/
├── CFE難易度/
├── コンプライアンス違反/
├── 不正会計/
├── .agent/
│   └── workflows/
│       ├── seo-article-writing.md
│       └── seo-article-rewrite.md
├── AI_PROJECT_MEMORY.md（このファイル）
├── README.md
└── WORDPRESS_TO_MD_GUIDE.md
```

---

**最終更新**: 2026-01-29
