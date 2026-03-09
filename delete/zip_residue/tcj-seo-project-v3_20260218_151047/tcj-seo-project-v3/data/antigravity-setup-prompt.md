# TCJ SEO記事作成プロジェクト v3 — Antigravity構築指示

## あなたへの指示

このプロジェクト内のファイルを元に、Antigravityの `.agent/` 構造を確認・補完してください。
**すでに配置済みのファイルの内容は変更しないこと。** 特にバリデーションスクリプトは改変禁止です。

---

## すでに配置済みのファイル（変更禁止）

```
.agent/rules/writing-rules.md                    ← 常時適用ガードレール
.agent/workflows/seo-article.md                   ← 5 Phase全体フロー
.agent/skills/seo-phase1-intent/SKILL.md          ← Phase1: 検索意図分析
.agent/skills/seo-phase2-competitor/SKILL.md       ← Phase2: 競合調査
.agent/skills/seo-phase3-strategy/SKILL.md         ← Phase3: 構成設計
.agent/skills/seo-phase4-writing/SKILL.md          ← Phase4: 執筆
.agent/skills/seo-phase5-validation/SKILL.md       ← Phase5: 検証
.agent/skills/seo-phase5-validation/scripts/validate_article.py ← 機械バリデーション【改変禁止】
```

## 確認・補完が必要なファイル

以下のファイルが空またはプレースホルダーの場合、その旨を報告してください：
- `.agent/skills/seo-phase4-writing/references/html-template.html` ← HTMLテンプレート
- `data/tcj-company-profile.md` ← 自社情報

以下のファイルが不足している場合は作成してください（既存があれば変更不要）：
- `.agent/skills/seo-phase4-writing/references/html-parts-guide.md` ← パーツ使い分けガイド
- `.agent/skills/seo-phase4-writing/references/llmo-rules.md` ← LLMO対策ルール

---

## バリデーションスクリプト使用ルール（厳守）

### 引数形式（この形式以外は使用禁止）
```bash
python3 .agent/skills/seo-phase5-validation/scripts/validate_article.py \
  article.html \
  --title "タイトル文字列" \
  --target-chars 5000
```

### 禁止事項
1. **スクリプトの内容を書き換えてはならない。** 引数パーサー、チェックロジック、出力形式の改変は一切禁止。
2. **スクリプトを別の場所にコピーして改変版を作ってはならない。**
3. **スクリプトの出力をパースして加工してはならない。** 出力はそのまま表示すること。
4. **文字数報告はスクリプトの「本文文字数（プレーンテキスト、空白除く）」を使用すること。** HTMLソースの文字数を報告してはならない。

---

## 自己チェック（構築完了後に実行すること）

### チェック1：ファイル存在確認
```bash
find .agent/ -type f | sort
```

### チェック2：バリデーションスクリプトのバージョン確認
```bash
grep "SCRIPT_VERSION" .agent/skills/seo-phase5-validation/scripts/validate_article.py
```
→ `SCRIPT_VERSION = "3.0.0"` と表示されること。

### チェック3：スクリプトの動作テスト
```bash
echo "これはテスト記事です。向上します。存在します。本稿では、テストです。Q1.テスト" > /tmp/test.txt
python3 .agent/skills/seo-phase5-validation/scripts/validate_article.py \
  /tmp/test.txt \
  --title "テストタイトルこれは三十七文字以上になるように書いています" \
  --target-chars 3000
```
→ 複数の違反（禁止ワード「向上」「存在」、メタ表現「本稿では」、タイトル超過、文字数不足等）が検出されればOK。

### チェック4：html-template.html の確認
→ 空またはプレースホルダーなら報告。

### チェック5：tcj-company-profile.md の確認
→ 空または不在なら報告。

---

## v2→v3の変更点

| 項目 | v2 | v3 |
|---|---|---|
| 文字数カウント | HTMLソース込みの文字数を報告していた | プレーンテキスト（タグ除去・空白除く）の文字数をスクリプトが正確にカウント |
| 年号チェック | タイトルと本文の整合性のみ | 現在年（datetime.now().year）との一致もチェック |
| メタ表現 | 「本記事では」「この記事では」のみ | 「本稿では」も追加 |
| スクリプト改変 | 保護なし（Antigravityが勝手に書き換えた） | 改変禁止を明記＋バージョン番号で検証 |
| 目標文字数チェック | なし | --target-chars引数で±20%チェック |
| 引数パーサー | --titleフラグ式 | 同じだがargparseではなく明示的パース（シェル分割問題を回避） |
