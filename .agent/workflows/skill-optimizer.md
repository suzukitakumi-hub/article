---
description: Skillsの品質を自動反復改善する。完成記事を正解データとして使い、テキスト勾配でSKILL.mdを改訂する。
---

# Skill Optimizerワークフロー

このワークフローは「既存の完成記事を正解データとして、Skillを自動改善する」ループを実行する。
@Pryzant et al. (2023) のProTeGiアプローチをSEO記事Skillに適用したもの。

## 使い方

```
/skill-optimizer
```

引数なしで起動する。対話の中で対象Skillと正解データを選択する。

---

## 実行原則

- Step2（生成）では正解HTMLを絶対に参照しない。入力コンテキストのみを使う。
- スコアは数値で出力する。感覚評価禁止。
- Skillの改訂は差分（diff形式）で示す。
- 1イテレーション完了後、スコアを `gold-standard/scores.json` に追記する。

---

## Step1：対象Skillと正解データの選択

ユーザーに以下を確認する。

**対象Skill（デフォルト：seo-phase4-writing）**
```
最適化するSkillを選んでください：
1. seo-phase1-intent
2. seo-phase2-competitor
3. seo-phase3-strategy
4. seo-phase4-writing（デフォルト・最も効果大）
5. seo-phase5-validation
```

**正解データの選択**
`.agent/skills/seo-phase4-writing/gold-standard/README.md` を参照し、
利用可能な正解データのリストを表示する。
1〜3件を選択させる。

**入力コンテキストの確認**
各正解データに対応する入力情報を確認する：
- ターゲットKW
- Phase1〜3の出力（存在すれば `data/phase_outputs/` から読む）

---

## Step2：現在のSkillで記事を生成（正解を参照しない）

**⚠️ 絶対ルール：正解HTMLはこのStepで開かない・参照しない。**

現在のSKILL.md（最適化対象）の手順だけに従い、入力コンテキストから記事を生成する。
出力は一時ファイルに保存する：

```
data/skill_optimizer/iteration_{N}/generated_{slug}.html
```

---

## Step3：差分分析（テキスト勾配の計算）

正解HTMLと生成HTMLを比較し、以下の6軸それぞれで0〜100のスコアと差分の理由を記述する。

| 軸 | 評価基準 | スコア | 差分の説明（なぜ差があるのか） |
|---|---|---|---|
| **構成の深さ** | 見出し設計がペルソナの思考フロー（認知→検討→決定）に沿っているか | - | - |
| **1次情報比率** | 公的データ・事例・専門見解が30%以上占めているか | - | - |
| **具体性** | 抽象論で終わらず読者が判断・行動できる情報があるか | - | - |
| **CTA自然さ** | CTAが押し売りでなく、課題解決の流れの中に組み込まれているか | - | - |
| **E-E-A-Tスコア** | Experience/Expertise/Authoritativeness/Trustworthiness | - | - |
| **人間らしさ** | AIっぽさ・定型句・抽象語の空回りがないか | - | - |

**テキスト勾配のまとめ**
「スコアが最も低かった軸」と「なぜSkillに起因する問題なのか」を2〜3文で言語化する。
ここがSKILL.mdの改訂ターゲットになる。

---

## Step4：SKILL.mdの改訂

Step3のテキスト勾配に基づき、SKILL.mdの該当箇所を書き直す。

出力フォーマット：
```diff
### Step X: （改訂対象の手順名）

- 現行:
-（改訂前の記述）

+ 改訂後:
+（改訂後の記述）

改訂理由：（テキスト勾配から特定した問題と解決策）
```

改訂後のSKILL.mdを実際に更新する。

---

## Step5：スコア記録＋ループ判定

`gold-standard/scores.json` に今回のイテレーション結果を追記する：

```json
{
  "iteration": N,
  "date": "YYYY-MM-DD",
  "skill": "seo-phase4-writing",
  "gold_standard_files": ["slug1", "slug2"],
  "scores": {
    "structure_depth": 0,
    "primary_info_ratio": 0,
    "specificity": 0,
    "cta_naturalness": 0,
    "eeat": 0,
    "human_feel": 0,
    "total": 0
  },
  "previous_total": 0,
  "delta": 0,
  "key_improvement": "（今回改訂した箇所の要約）"
}
```

**ループ継続の判断**
- 前回比 +3点以上 → 次のイテレーションを推奨
- 前回比 +1〜2点 → 継続してもよいが効果は限定的
- 前回比 0点以下 → 終了を推奨（過学習の可能性）

ユーザーに結果とループ継続の推奨を伝え、判断を仰ぐ。
