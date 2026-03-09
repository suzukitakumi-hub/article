# Gold Standard — 正解データ一覧

このディレクトリは `/skill-optimizer` ワークフローで使用する正解データ（完成記事HTML）の参照リストを管理する。

## 正解データの選定基準

- ユーザーが最終的にOKを出した完成版HTML
- Phase1〜5を通しており、writing-rulesへの準拠が確認されたもの
- 直近6ヶ月以内に作成されたもの（古い記事は仕様が変わっている可能性があるため）

---

## 利用可能な正解データ

| # | スラッグ | キーワード | 文字数 | 作成日 | HTMLパス |
|---|---|---|---|---|---|
| 1 | `points_to_note_rewrite` | 外国人 採用 注意点 | 7,382文字 | 2026-02-26 | `articles/points_to_note_rewrite.html` |
| 2 | `foreign_license_conversion_v9` | 外国人 運転免許 切替 | - | 2026-02 | `output/foreign_license_conversion_v9.html` |
| 3 | `transportation_driver_v1` | 外国人 トラック運転手 採用 | - | 2026-02 | `output/transportation_driver_v1.html` |
| 4 | `immigration_control_law_revision` | 出入国管理法 改正 | - | 2026-02 | `output/immigration_control_law_revision.html` |
| 5 | `留学生アルバイト_28時間ルール` | 留学生 アルバイト 28時間 | - | 2026-02 | `output/留学生アルバイト_28時間ルール.html` |

---

## 追加方法

記事が完成したら以下の手順でこのリストに追加する：

1. 上のテーブルに行を追加（スラッグ・KW・文字数・作成日・HTMLパス）
2. 必要であれば対応するPhase1〜3の出力を `data/phase_outputs/` の履歴として保存する

---

## 入力コンテキストの用意方法

`/skill-optimizer` 実行時、正解データに対応する「入力コンテキスト」が必要になる。
以下に記録しておくこと。

| スラッグ | ターゲットKW | Phase1〜3出力の有無 |
|---|---|---|
| `points_to_note_rewrite` | 外国人 採用 注意点 | なし（手動でKWのみ提供） |
| `foreign_license_conversion_v9` | 外国人 運転免許 切替 | なし |
| `transportation_driver_v1` | 外国人 トラック運転手 採用 | なし |
