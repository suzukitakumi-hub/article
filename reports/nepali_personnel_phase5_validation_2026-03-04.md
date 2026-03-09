# Phase5: 検証・最終出力

- 対象HTML: `output/nepali_personnel_rewrite_v1.html`
- タイトル: `ネパール人材の特徴5選と採用実務 失敗回避のチェック項目`
- 検証日: 2026-03-04

## 1) 機械バリデーション結果

実行コマンド:

```bash
python3 .agent/skills/seo-phase5-validation/scripts/validate_article.py   output/nepali_personnel_rewrite_v1.html   --title "ネパール人材の特徴5選と採用実務 失敗回避のチェック項目"   --target-chars 6200
```

結果:
- PASS
- 本文文字数（プレーンテキスト、空白除く）: **4967文字**
- FAQ数: 5
- タイトル文字数: 28
- 年号整合: PASS

## 1.5) デザインテンプレ準拠チェック

実行コマンド:

```bash
python3 .agent/skills/seo-phase5-validation/scripts/validate_design_template.py   output/nepali_personnel_rewrite_v1.html
```

結果:
- PASS

## 1.6) 文体（ですます調）チェック

実行コマンド:

```bash
python3 .agent/skills/seo-phase5-validation/scripts/validate_tone.py   output/nepali_personnel_rewrite_v1.html
```

結果:
- PASS

## 2) LLMO対策チェック

- [x] H2/H3直下で結論先出し
- [x] 定義文を冒頭配置
- [x] 比較・手順・要件を表/箇条書きで構造化
- [x] 公的データに出典名と時点を付記
- [x] Q&A見出しあり
- [x] FAQ 5問以上

## 3) E-E-A-Tスコアカード

- Experience: 4
- Expertise: 4
- Authoritativeness: 4
- Trustworthiness: 5
- 合計: **17点**（合格）

## 4) コンテンツ品質チェック

- [x] 網羅性
- [x] 深度
- [x] 独自性
- [x] 最新性
- [x] ペルソナ適合
- [x] 文字数（Phase3目標±20%）
- [x] 1次情報比率
- [x] BtoB最適化
- [x] 内部リンク妥当性（3件、許可URLのみ）
- [x] クラスター整合（C5固定）
- [x] 空虚長文排除
- [x] 根拠トレーサビリティ

## 5) 画像プレースホルダー一覧

- なし（最終版ではプレースホルダー画像を残していません）

## 6) 公開後改善タスク

- 14日後チェック:
  - 指標: `ネパール人材 特徴` を含むクエリのCTR、表示回数、平均掲載順位
  - 判定: 表示回数20以上かつCTR2.5%未満のクエリが2件以上
  - 実施: タイトル語順の微修正、導入2段落の意図一致調整、FAQ質問文の語句差し替え

- 30日後チェック:
  - 指標: 平均掲載順位11〜20位帯クエリの件数
  - 判定: 11〜20位帯クエリが3件以上
  - 実施: H3を1本追加、比較表の列を1つ追加、内部リンクカードの配置位置見直し

## 7) 進捗管理更新

- `reports/history/article_history.txt` に完了行を追記済み
- `reports/history/ARTICLE_HISTORY.md` に `nepali_personnel_rewrite_v1.html` を追記済み
- `data/existing_articles/ARTICLE_HISTORY.md` に `nepali_personnel_rewrite_v1.html` を追記済み
