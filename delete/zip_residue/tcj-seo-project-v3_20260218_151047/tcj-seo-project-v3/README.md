# TCJ SEO記事作成プロジェクト — Antigravity設定ガイド

## このフォルダの構成

```
tcj-seo-project/
├── .agent/
│   ├── rules/
│   │   └── writing-rules.md          ← 常時適用（禁止ワード、文体ルール等）
│   ├── workflows/
│   │   └── seo-article.md            ← /seo-article で呼び出す全体フロー
│   └── skills/
│       ├── seo-phase1-intent/
│       │   └── SKILL.md              ← 検索意図分析（自動読み込み）
│       ├── seo-phase2-competitor/
│       │   └── SKILL.md              ← 競合調査+ギャップ分析（自動読み込み）
│       ├── seo-phase3-strategy/
│       │   └── SKILL.md              ← ペルソナ+構成案+USP計画（自動読み込み）
│       ├── seo-phase4-writing/
│       │   ├── SKILL.md              ← 執筆ルール（自動読み込み）
│       │   └── references/
│       │       ├── html-template.html ← HTMLパーツ定義【要貼り付け】
│       │       ├── html-parts-guide.md← パーツ使い分けガイド
│       │       └── llmo-rules.md     ← LLMO対策ルール
│       └── seo-phase5-validation/
│           └── SKILL.md              ← 検証+最終出力（自動読み込み）
└── data/
    └── tcj-company-profile.md         ← 自社情報【要貼り付け】
```

## セットアップ手順

### Step1：Antigravityをインストール
1. https://antigravity.google/download からダウンロード
2. インストーラーを実行
3. 初回起動時の設定で「Agent-assisted development」を選択（推奨）
4. Googleアカウントでサインイン
5. モデルはGemini 3 Proを選択

### Step2：このフォルダをAntigravityで開く
1. Antigravityを起動
2. 「Open Folder」でこのtcj-seo-projectフォルダを選択
3. .agent/ フォルダが自動認識される

### Step3：自社ファイルを貼り付ける（2箇所）
以下の2ファイルに、既存の内容をそのまま貼り付ける。

1. `data/tcj-company-profile.md`
   → 既存のTCJ_COMPANY_PROFILE.mdの内容をペースト

2. `.agent/skills/seo-phase4-writing/references/html-template.html`
   → 既存のseo_article_html_template.htmlの内容をペースト

### Step4：動作確認
1. Agent Managerのチャット欄に `/seo-article` と入力
2. ワークフローが呼び出されることを確認
3. キーワードと目的を伝えてPhase1が始まることを確認

## 使い方

チャット欄で以下のように入力する：

```
/seo-article
ターゲットキーワード：特定技能 人材紹介
記事の目的：リード獲得
```

エージェントがPhase1→2→3→4→5の順に実行する。
各Phaseで対応するSkillが自動的に読み込まれ、
そのPhaseに必要なルールと手順だけがコンテキストに入る。

## なぜこの構成にしたのか（元のプロンプトとの違い）

| 元のプロンプト | この構成 |
|---|---|
| 1ファイルに全Phase+全ルール | Phase別に5つのSkillに分割 |
| 常に全ルールがコンテキストに入る | 必要なPhaseのルールだけ読み込み |
| Writing Rulesが後半で忘れられがち | Rulesとして常時適用を保証 |
| HTMLテンプレートが常にコンテキスト消費 | Phase4実行時だけ読み込み |

この分割により、コンテキストウィンドウの圧迫が解消され、
各Phaseのゲート条件が飛ばされにくくなる。

## 営業資料（サービス概要v14）について

現状、PDF形式の営業資料はAntigravityのSkillsのreferencesに
直接置けない（テキストファイルのみ）。

対応方法：
1. PDFの主要な訴求ポイントをMarkdownに書き起こす
2. .agent/skills/seo-phase3-strategy/references/service-v14-summary.md として配置
3. Phase3のUSP配置計画で自動参照される
