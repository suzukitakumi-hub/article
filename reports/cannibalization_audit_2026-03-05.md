# カニバリゼーション診断レポート

**作成日**: 2026-03-05
**データソース**: GSC（2026-01-19〜2026-02-18）、WordPress記事一覧（86記事）
**凡例**: 順位は加重平均順位（インプレッション×順位の加重）/ 圏外 = GSCデータなし

---

## 🔴 HIGH RISK（GSCで競合確認済み）

### [1] フィリピン人×介護クラスター

| 記事 | タイトル | GSC加重平均順位 | 主要クエリ（位） | 判定 |
|------|----------|----------------|-----------------|------|
| `nursing_care_training` | フィリピン人介護士の教育・研修を解説 | **25.8位** | 「フィリピン人 介護士」18.1位 / 「フィリピン 介護 人材」45.0位 | ✅ 残す（リライト） |
| `filipino_personnel` | フィリピン人介護人材の採用ガイド | **19.4位** | 「フィリピン 介護 人材」9.3位 / 「フィリピン人 介護士」25.7位 | ✅ 残す（リライト） |
| `nursing_care1` | 外国人介護士の適性を見抜く質問集 | **45.6位** | 「介護 採用 難しい 外国人」61.3位 | 🗑️ 統合か削除 |
| `nursing_care_training2` | 外国人介護士のリアル：就労後の教育と課題 | **圏外** | データなし | 🗑️ 削除候補 |
| `nursing_care` | 外国人スタッフ〜介護業編〜 | **圏外** | データなし | 🗑️ 削除候補 |
| `elderly_care_industry1` | 介護業界採用ガイド【前編：EPA・介護】 | **圏外** | データなし | 🗑️ 削除候補 |
| `elderly_care_industry2` | 介護業界採用ガイド【後編：特定技能・技能実習】 | **圏外** | データなし | 🗑️ 削除候補 |
| `介護_外国人_採用.html` | （下書き・未公開） | — | — | ⛔ 公開前に精査 |
| `フィリピン人_介護_採用.html` | （下書き・未公開） | — | — | ⛔ 公開前に精査 |

**推奨アクション**:
- `nursing_care_training` と `filipino_personnel` は両方に順位がある → **意図分離してリライト**
  - `nursing_care_training` → 「フィリピン人介護士の受け入れ後の研修・教育」専用に絞る
  - `filipino_personnel` → 「フィリピン人介護士の採用プロセス・コスト・手続き」専用に絞る
- `nursing_care1` / `nursing_care_training2` / `nursing_care` / `elderly_care_industry1` / `elderly_care_industry2` → **圏外または低順位のため削除 or 上記2記事に統合して301リダイレクト**
- 下書き2本は統合・差別化の方針が固まるまで公開しない

---

### [2] 日本語能力クラスター

| 記事 | タイトル | GSC加重平均順位 | 主要クエリ（位） | 判定 |
|------|----------|----------------|-----------------|------|
| `time_to_learn_japanese` | 外国人社員が「日本語習得のために必要な時間数」とは | **4.6位** | 「日本語レベル」1.0位 / 「日本語習得 時間」1.7位 | ✅ 残す（触らない） |
| `japanese_lang_skills` | 外国人採用の日本語能力ガイド | **16.5位** | 「外国人 日本語レベル 見極め」6.7位 / 「就職先 jlpt level」9.2位 | ✅ 残す（リライト） |
| `jlpt` | JLPTの概要と実際の候補者スキル | **1.2位** | 「jlptとは」1.0位（JLPT固有クエリ） | ✅ 残す（別意図） |
| `japanese_lang_skills3` | JLPTだけでは危険！日本語力の見極め方 | **78.0位** | 「外国人 日本語レベル 見極め」78.0位 | 🗑️ 削除候補 |
| `japanese_lang_skills2` | 人事が知るべき「日本語の検定試験」 | **圏外** | データなし | 🗑️ 削除候補 |
| `application_document` | 応募書類から読み取る外国人材の日本語能力 | **圏外** | データなし | 🗑️ 削除候補 |

**注意**: `time_to_learn_japanese` と `japanese_lang_skills` は競合クエリ（「外国人 日本語レベル 見極め」）で表示されているが、主要クエリの意図が異なる（「時間数」vs「見極め方」）。**強制統合は不要**。ただし `japanese_lang_skills3` は同一意図で78位のため削除が最善。

**推奨アクション**:
- `time_to_learn_japanese`（4.6位）: **触らない**
- `japanese_lang_skills`（16.5位）: **リライトで10位以内を狙う**
- `japanese_lang_skills3`（78位）、`japanese_lang_skills2`（圏外）、`application_document`（圏外）: **削除して`japanese_lang_skills`に301リダイレクト**

---

### [3] 外国人採用 注意点クラスター

| 記事 | タイトル | GSC加重平均順位 | 主要クエリ（位） | 判定 |
|------|----------|----------------|-----------------|------|
| `points_to_note` | 【2025年版】外国人採用の注意点 | **31.7位** | 「外国人 選考 ポイント」15.8位 | ✅ 残す（リライト済み） |
| `precautions_steps-to-adoption` | 外国人雇用の注意点と採用までのステップ | **53.2位** | 「外国人 採用 方法 注意点」53.2位 | 🗑️ 削除 |
| `recruitment_of_foreign_workers` | 初めての外国人材採用ガイド | **圏外** | データなし | 🗑️ 削除候補 |
| `status_and_issues_hiring_foreigner` | 外国人労働者雇用の最新動向と課題 | **53.2位** | 「外国人 採用 課題」85.8位（競合意図は違う） | 🟡 別意図として残す |

**推奨アクション**:
- `precautions_steps-to-adoption`（53位）: **削除 → `points_to_note`に301リダイレクト**（即日実施推奨）
- `recruitment_of_foreign_workers`（圏外）: 内容を`points_to_note`リライト時に吸収して削除

---

## 🟡 MEDIUM RISK（構造的競合）

### [4] 留学生アルバイトクラスター

| 記事 | タイトル | GSC加重平均順位 | 主要クエリ（位） | 判定 |
|------|----------|----------------|-----------------|------|
| `parttimework_for_international_students` | 留学生アルバイト雇用の28時間ルール | **40.1位** | 「外国人 アルバイト採用」33.7位 | ✅ 残す（リライト） |
| `foreign_parttime_worker` | 留学生アルバイトの採用方法 | **圏外** | データなし | 🗑️ 削除 |

**推奨アクション**: `foreign_parttime_worker`を削除し`parttimework_for_international_students`に301リダイレクト。内容をリライト時に吸収。

---

### [5] ビジネスマナークラスター

| 記事 | タイトル | GSC加重平均順位 | 主要クエリ（位） | 判定 |
|------|----------|----------------|-----------------|------|
| `business_manners` | 【国別比較】ビジネスマナーの違いとは？ | **34.8位** ※重複込み | 「外国人 ビジネスマナー 比較」10.2位・7.2位（重複URL） | ✅ 残す |
| `business_etiquette` | 外国人材が困惑する日本のビジネスマナー | **圏外** | データなし | 🗑️ 削除候補 |
| `business_manners2` | ビジネスマナーの教え方（前編） | **圏外** | データなし | 🟡 シリーズとして残すか要判断 |
| `business_manners3` | ビジネスマナーの教え方（後編） | **圏外** | データなし | 🟡 シリーズとして残すか要判断 |

**⚠️ 追加問題**: `Business_manners`（大文字）と`business_manners`（小文字）が別URLとしてGSCに記録されており、同クエリで表示を二分している。301リダイレクトで統一が必要。

**推奨アクション**:
- 大文字URL（`Business_manners`）→ 小文字URL に **301リダイレクト**（即日）
- `business_etiquette`（圏外）: **削除して`business_manners`に統合**
- `business_manners2/3`（前後編・圏外）: 削除 or `business_manners`への統合を検討

---

### [6] 介護業全般クラスター（[1]の周辺）

[1]と重複するが、純粋に介護×外国人採用の全体を狙う記事群。

| 記事 | タイトル | GSC加重平均順位 | 判定 |
|------|----------|----------------|------|
| `nursing_care` | 外国人スタッフ〜介護業編〜 | **圏外** | 🗑️ [1]の整理時に削除 |
| `elderly_care_industry1` | 介護業界採用ガイド前編 | **圏外** | 🗑️ [1]の整理時に削除 |
| `elderly_care_industry2` | 介護業界採用ガイド後編 | **圏外** | 🗑️ [1]の整理時に削除 |

---

### [7] 求人票クラスター

| 記事 | タイトル | GSC加重平均順位 | 主要クエリ（位） | 判定 |
|------|----------|----------------|-----------------|------|
| `job_posting2` | 求人票の作り方＜応用編＞ | **20.3位** | 「外国人 求人票 書き方」15.2位 | ✅ 残す（リライト） |
| `job_posting` | 求人票の作り方＜基礎編＞ | **圏外** | データなし | 🗑️ 削除 or 統合 |

**推奨アクション**: `job_posting`（圏外）を削除し`job_posting2`に統合。`job_posting2`をリライト時に「基礎〜応用まで完全ガイド」の1本にまとめる。

---

### [8] コミュニケーションクラスター

| 記事 | タイトル | GSC加重平均順位 | 判定 |
|------|----------|----------------|------|
| `solving_communication_issues` | 外国人材定着のコミュニケーション課題解決 | **29.6位** | ✅ ハブ記事として残す |
| `communication2` | 外国人社員と円滑に働くために① | **54.5位** | 🟡 様子見 |
| `communication` | やさしい日本語の実践（後編） | **圏外** | 🗑️ 削除候補 |
| `communication3` | 外国人社員と円滑に働くために② | **圏外** | 🗑️ 削除候補 |
| `multinational_team` | 多国籍チームのトラブルと回避策 | **圏外** | 🗑️ 削除候補 |
| `workplace_communication` | 外国人社員の「上司観」「報連相」 | **圏外** | 🗑️ 削除候補 |

---

### [9] 建設業クラスター

| 記事 | タイトル | GSC加重平均順位 | 判定 |
|------|----------|----------------|------|
| `construction_industry1` | 外国人スタッフ〜建設業編〜 | **圏外** | 🗑️ 削除候補 |
| `architecture` | 建築業の外国人材採用、なぜ失敗する？ | **圏外** | 🗑️ 削除候補 |

**推奨アクション**: 両方圏外。どちらか1本にまとめてリライト。建設・建築は同一読者層なので統合が最善。

---

## ⚠️ 技術的重複URL（301リダイレクト要・即日）

| 大文字URL（削除） | 正式URL | 問題 |
|-----------------|---------|------|
| `/posts/Business_manners` | `/posts/business_manners` | 同一クエリ「外国人 ビジネスマナー 比較」に72回表示が分裂 |
| `/posts/Filipino_personnel` | `/posts/filipino_personnel` | 「フィリピン人材 特徴」18回が分裂 |
| `/posts/JLPT` | `/posts/jlpt` | 「jlptとは」15回が分裂 |
| `/posts/precautions_steps-to-Adoption` | `/posts/precautions_steps-to-adoption` | 分裂の可能性あり |

---

## 📋 総合アクションマップ

### 即日実施（工数最小・SEO即効）

| 対象 | アクション |
|------|-----------|
| 重複URL 4件 | 大文字→小文字に301リダイレクト |
| `precautions_steps-to-adoption` | `points_to_note`に301リダイレクト |
| `foreign_parttime_worker` | `parttimework_for_international_students`に301リダイレクト |
| `job_posting` | `job_posting2`に301リダイレクト |

### 次のリライト時に解消（記事をリライトする前に旧記事を削除）

| 削除対象（→統合先） | 統合先リライト記事 |
|--------------------|-------------------|
| `nursing_care1` | `nursing_care_training` or `filipino_personnel` |
| `nursing_care_training2` | `nursing_care_training` |
| `nursing_care` | `elderly_care_industry1/2`を統合した新記事 |
| `elderly_care_industry1` + `elderly_care_industry2` | 介護業採用ピラー記事（新規リライト） |
| `japanese_lang_skills3` | `japanese_lang_skills` |
| `japanese_lang_skills2` | `japanese_lang_skills` |
| `application_document` | `japanese_lang_skills` |
| `business_etiquette` | `business_manners` |
| `recruitment_of_foreign_workers` | `points_to_note` |
| `communication`/`communication3`/`multinational_team`/`workplace_communication` | `solving_communication_issues` |
| `construction_industry1` or `architecture` | 建設業統合リライト |

### 様子見（現状維持）

- `time_to_learn_japanese`（4.6位・安定）: 触らない
- `jlpt`（1.2位・別意図）: 触らない
- `solving_communication_issues`（29.6位）: ハブとして内部リンク強化のみ
- `status_and_issues_hiring_foreigner`（「外国人採用 課題」で別意図）: 競合リスク低

---

## 📊 削除推奨リスト（計14記事）

| 削除順位 | スラッグ | 理由 |
|---------|---------|------|
| 🔴 即日 | `precautions_steps-to-adoption` | 53位・重複意図・301リダイレクト済み |
| 🔴 即日 | `foreign_parttime_worker` | 圏外・重複意図 |
| 🔴 即日 | `job_posting` | 圏外・重複意図 |
| 🟡 次回リライト前 | `nursing_care1` | 45位・意図が曖昧 |
| 🟡 次回リライト前 | `nursing_care_training2` | 圏外 |
| 🟡 次回リライト前 | `nursing_care` | 圏外・1,772文字 |
| 🟡 次回リライト前 | `elderly_care_industry1` | 圏外・2,349文字 |
| 🟡 次回リライト前 | `elderly_care_industry2` | 圏外・2,368文字 |
| 🟡 次回リライト前 | `japanese_lang_skills3` | 78位・重複意図 |
| 🟡 次回リライト前 | `japanese_lang_skills2` | 圏外 |
| 🟡 次回リライト前 | `application_document` | 圏外 |
| 🟡 次回リライト前 | `business_etiquette` | 圏外 |
| 🟡 次回リライト前 | `recruitment_of_foreign_workers` | 圏外 |
| 🟡 次回リライト前 | `communication` / `communication3` / `multinational_team` / `workplace_communication` | 圏外4本 |
