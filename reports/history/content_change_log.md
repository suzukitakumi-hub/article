# コンテンツ変更ログ

更新日: 2026-03-17

このファイルを、削除記事とリライト記事の単一管理台帳として使います。

- リライト記事: `git log --grep="^rewrite:"` で確認できたコミットを記録
- 削除記事: WordPress管理画面のゴミ箱確認ベースで手動記録
- 削除日時の厳密な時刻は取れていないため、`記録日` は確認日です

## 変更一覧

| 記録日 | 種別 | 記事タイトル | URL | 根拠 | 備考 |
|---|---|---|---|---|---|
| 2026-03-17 | Rewrite | 海外ビジネスマナーの違い5場面 外国人材受け入れの教え方 | https://gaikoku-jinzai.tcj-education.com/posts/business_manners | Git commit `62dc556` / `phase4_output.json` | `【国別比較】ビジネスマナーの違いとは？外国人材と円滑に働くためのポイント` のリライト成果物タイトル |
| 2026-03-17 | Delete | “なぜ”を伝えると変わる！外国人社員に伝わる“日本のビジネスマナー”の教え方（後編） | https://gaikoku-jinzai.tcj-education.com/posts/business_manners3 | WPゴミ箱スクリーンショット確認 | 2026-03-17時点でゴミ箱入りを確認 |
| 2026-03-17 | Delete | 外国人社員とのコミュニケーションの鍵「ワセダ」とは？｜やさしい日本語の実践（後編） | https://gaikoku-jinzai.tcj-education.com/posts/communication | WPゴミ箱スクリーンショット確認 | 2026-03-17時点でゴミ箱入りを確認 |
| 2026-03-17 | Delete | “なぜ”を伝えると変わる！外国人社員に伝わる“日本のビジネスマナー”の教え方（前編） | https://gaikoku-jinzai.tcj-education.com/posts/business_manners2 | WPゴミ箱スクリーンショット確認 | 2026-03-17時点でゴミ箱入りを確認 |
| 2026-03-17 | Delete | 初めての外国人材採用ガイド｜メリット・注意点・手続きの流れを徹底解説 | https://gaikoku-jinzai.tcj-education.com/posts/recruitment_of_foreign_workers | WPゴミ箱スクリーンショット確認 | 2026-03-17時点でゴミ箱入りを確認 |
| 2026-03-17 | Delete | 外国人採用担当者必見！人事が知るべき「日本語の検定試験」 | https://gaikoku-jinzai.tcj-education.com/posts/japanese_lang_skills2 | WPゴミ箱スクリーンショット確認 | 2026-03-17時点でゴミ箱入りを確認 |
| 2026-03-17 | Delete | 応募書類から読み取る外国人材の日本語能力 | https://gaikoku-jinzai.tcj-education.com/posts/application_document | WPゴミ箱スクリーンショット確認 | 2026-03-17時点でゴミ箱入りを確認 |
| 2026-03-17 | Delete | 日本語能力試験（JLPT）の概要と実際の候補者スキル | https://gaikoku-jinzai.tcj-education.com/posts/jlpt | WPゴミ箱スクリーンショット確認 | 2026-03-17時点でゴミ箱入りを確認 |
| 2026-03-17 | Delete | 外国人材が困惑する日本のビジネスマナー | https://gaikoku-jinzai.tcj-education.com/posts/business_etiquette | WPゴミ箱スクリーンショット確認 | 2026-03-17時点でゴミ箱入りを確認 |
| 2026-03-10 | Rewrite | 留学生アルバイト28時間ルールの計算方法と採用確認【2026】 | https://gaikoku-jinzai.tcj-education.com/posts/parttimework_for_international_students | Git commit `4d0f3f5` / 既存履歴ファイル | リライト履歴はGitで確認、タイトルは既存履歴ファイルに合わせて記録 |
| 2026-03-10 | Rewrite | 技能実習生の労災保険適用｜外国人雇用の初動と申請手順【2026】 | https://gaikoku-jinzai.tcj-education.com/posts/work_injury_insurance | Git commit `11e4263` / `phase4_output.json` |  |
| 2026-03-10 | Rewrite | 日本語学習時間の目安｜外国人社員が職場で通じるまでの期間と支援 | https://gaikoku-jinzai.tcj-education.com/posts/time_to_learn_japanese | Git commit `9778f2e` / `phase4_output.json` |  |

## 運用メモ

| 項目 | 管理方法 |
|---|---|
| リライト記事の確認 | `git log --date=short --pretty=format:"%ad|%h|%s" --grep="^rewrite:"` |
| 新規記事の確認 | `git log --date=short --pretty=format:"%ad|%h|%s" --grep="^new:"` |
| 削除記事の確認 | WordPress管理画面のゴミ箱を見て手動追記 |
| 注意点 | Gitで追えるのは、`rewrite:` または `new:` でコミットされた記事だけ |
