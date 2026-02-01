# WordPress記事をMarkdownに変換する方法

## 必要なもの

1. **Node.js** がインストールされていること
   - [Node.js公式サイト](https://nodejs.org/)からダウンロード
2. **WordPressのエクスポートファイル**（XML形式）
   - WordPress管理画面 → ツール → エクスポート → 「すべてのコンテンツ」を選択

---

## 使い方（簡単3ステップ）

### 1. WordPressからエクスポート

WordPress管理画面で：
1. **ツール** → **エクスポート**
2. **すべてのコンテンツ** を選択
3. **エクスポートファイルをダウンロード** ボタンをクリック
4. XMLファイル（例：`wordpress.2026-01-29.xml`）がダウンロードされる

### 2. ターミナルでコマンド実行

```powershell
# このフォルダに移動
cd C:\Users\suzuki.takumi\Documents\abitus_workspace

# 変換ツールを実行（ウィザード形式）
npx wordpress-export-to-markdown
```

### 3. ウィザードの質問に答える

以下の質問が表示されるので、順番に答えます：

| 質問 | 推奨回答 | 説明 |
|---|---|---|
| Path to WordPress export file? | `wordpress.2026-01-29.xml` | ダウンロードしたXMLファイルのパス |
| Path to output folder? | `./output` | Markdownファイルの出力先 |
| Put each post into its own folder? | `Yes` | 記事ごとにフォルダ分け |
| Add date prefix to posts? | `No` | 日付プレフィックス不要 |
| Save images? | `Yes` | 画像もダウンロード |

---

## コマンドライン引数で一発実行（上級者向け）

ウィザードをスキップして一気に実行する場合：

```powershell
npx wordpress-export-to-markdown `
  --input=wordpress.2026-01-29.xml `
  --output=./output `
  --post-folders=true `
  --prefix-date=false `
  --save-images=true
```

---

## 実行後の確認

```
abitus_workspace/
└── output/
    ├── post-title-1/
    │   ├── index.md        # 記事本文（Markdown）
    │   └── images/         # 記事内の画像
    ├── post-title-2/
    │   ├── index.md
    │   └── images/
    ...
```

各記事のMarkdownファイルには、以下のようなフロントマター（メタデータ）が付きます：

```markdown
---
title: "記事タイトル"
date: "2026-01-29"
categories: ["カテゴリ名"]
tags: ["タグ1", "タグ2"]
---

記事本文がここに...
```

---

## トラブルシューティング

### Node.jsがインストールされていない場合

```powershell
# Node.jsのバージョン確認
node --version

# エラーが出る場合は、Node.jsをインストール
# https://nodejs.org/ からダウンロード
```

### XMLファイルが見つからない場合

- XMLファイルを `abitus_workspace` フォルダに配置してから実行
- またはフルパスで指定：`C:\Users\suzuki.takumi\Downloads\wordpress.xml`

---

## 参考リンク

- [wordpress-export-to-markdown GitHub](https://github.com/lonekorean/wordpress-export-to-markdown)
- [WordPress公式：エクスポート方法](https://wordpress.org/support/article/tools-export-screen/)
