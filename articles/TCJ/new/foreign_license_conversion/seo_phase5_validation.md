# Phase5: 検証・最終出力

- 対象HTML: `output/foreign_license_conversion_v9.html`
- タイトル: `外免切替とは？2026年版 採用前チェックと配属設計の実務ガイド`
- 検証日: 2026-02-24

## 1) 機械バリデーション結果

実行コマンド:

```bash
python3 .agent/skills/seo-phase5-validation/scripts/validate_article.py \
  output/foreign_license_conversion_v9.html \
  --title "外免切替とは？2026年版 採用前チェックと配属設計の実務ガイド" \
  --target-chars 6000
```

結果:
- PASS
- 本文文字数（プレーンテキスト、空白除く）: **4869文字**
- FAQ数: 6
- タイトル文字数: 32
- 年号整合: PASS

## 1.5) デザインテンプレ準拠チェック

実行コマンド:

```bash
python3 .agent/skills/seo-phase5-validation/scripts/validate_design_template.py \
  output/foreign_license_conversion_v9.html
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
- Expertise: 5
- Authoritativeness: 5
- Trustworthiness: 5
- 合計: **19点**（合格）

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
- [x] クラスター整合（C1中心 + C5隣接）
- [x] 空虚長文排除
- [x] 根拠トレーサビリティ

## 5) 公開後改善タスク

- 14日後チェック:
  - 指標: 対策KWと関連クエリのCTR（GSC）
  - 判定: 表示が多いのにCTRが低いクエリが2件以上
  - 実施: タイトルと導入文、FAQの質問文をクエリ語に合わせて微修正

- 30日後チェック:
  - 指標: 平均掲載順位11〜20位のクエリ
  - 判定: 11〜20位帯クエリが3件以上
  - 実施: 該当クエリに対応するH3追記、比較表の項目追加、内部リンクアンカー調整

## 6) 進捗管理更新

- `reports/history/article_history.txt` に完了行を追記済み
- `reports/history/ARTICLE_HISTORY.md` に `foreign_license_conversion_v9.html` を追記済み

