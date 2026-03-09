#!/usr/bin/env python3
"""
gate_check.py - SEO記事ワークフローのフェーズゲートチェッカー

各PhaseのJSONアウトプットを検証し、必須キーが揃っているか確認する。
EXIT 0 = ゲート通過 / EXIT 1 = ゲート失敗（次のPhaseに進めない）

使い方:
  python .agent/scripts/gate_check.py --phase 1 --file data/phase_outputs/phase1_output.json
  python .agent/scripts/gate_check.py --phase 2 --file data/phase_outputs/phase2_output.json
"""

import argparse
import json
import os
import sys
from datetime import datetime

# 各Phaseの必須キー定義
REQUIRED_KEYS = {
    1: {
        "keys": ["intent_4elements", "article_axis", "goal_scenario"],
        "description": "Phase1: 検索意図分析・本軸・ゴールシナリオ",
        "rewrite_extra": ["existing_article_diagnosis"],
    },
    2: {
        "keys": [
            "paa",
            "related_keywords",
            "competitor_analysis",
            "intent_score",
            "common_topics",
            "differentiation_topics",
            "gap_analysis",
            "differentiation",
        ],
        "description": "Phase2: PAA・競合分析・ギャップ分析",
        "rewrite_extra": [],
    },
    3: {
        "keys": [
            "persona",
            "structure",
            "usp_plan",
            "primary_info_plan",
            "target_chars",
            "internal_link_plan",
            "claim_evidence_map",
        ],
        "description": "Phase3: ペルソナ・構成・USP・CEM",
        "rewrite_extra": [],
    },
    4: {
        "keys": [
            "html_path",
            "title",
            "meta_description",
            "self_check_passed",
            "char_count_check",
            "cta_count",
            "faq_count",
        ],
        "description": "Phase4: HTML出力・自己チェック結果",
        "rewrite_extra": [],
    },
}


def load_json(filepath):
    if not os.path.exists(filepath):
        return None, f"ファイルが存在しません: {filepath}"
    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"JSONパースエラー: {e}"


def check_keys(data, required_keys):
    missing = []
    empty = []
    for key in required_keys:
        if key not in data:
            missing.append(key)
        elif data[key] is None or data[key] == "" or data[key] == [] or data[key] == {}:
            empty.append(key)
    return missing, empty


def main():
    parser = argparse.ArgumentParser(description="SEOワークフロー フェーズゲートチェッカー")
    parser.add_argument("--phase", type=int, required=True, choices=[1, 2, 3, 4],
                        help="チェック対象のPhase番号 (1-4)")
    parser.add_argument("--file", type=str, required=True,
                        help="チェックするJSONファイルのパス")
    parser.add_argument("--mode", type=str, default="new", choices=["new", "rewrite"],
                        help="実行モード (new/rewrite, デフォルト: new)")
    args = parser.parse_args()

    phase = args.phase
    if phase not in REQUIRED_KEYS:
        print(f"[GATE ERROR] Phase {phase} はゲートチェック対象外です。")
        sys.exit(1)

    spec = REQUIRED_KEYS[phase]
    required = list(spec["keys"])

    # rewriteモードの場合は追加キーを要求
    if args.mode == "rewrite" and spec.get("rewrite_extra"):
        required += spec["rewrite_extra"]

    print(f"\n{'='*55}")
    print(f"  SEO WF ゲートチェック - Phase {phase}")
    print(f"  {spec['description']}")
    print(f"  ファイル: {args.file}")
    print(f"  モード: {args.mode}")
    print(f"{'='*55}")

    # ファイル読み込み
    data, err = load_json(args.file)
    if data is None:
        print(f"\n[GATE FAIL] {err}")
        print("\n⛔ Phase {next_phase} には進めません。".format(next_phase=phase + 1))
        print(f"   → Phase {phase} を完了させ、以下のファイルを生成してください:")
        print(f"   → {args.file}")
        print(f"\n   必須キー: {required}\n")
        sys.exit(1)

    # 必須キーチェック
    missing, empty = check_keys(data, required)

    passed = True
    for key in required:
        if key in missing:
            print(f"  [FAIL] {key} : キーが存在しない")
            passed = False
        elif key in empty:
            print(f"  [FAIL] {key} : 値が空")
            passed = False
        else:
            print(f"  [PASS] {key}")

    print(f"\n{'='*55}")

    if passed:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"  ✅ Phase {phase} ゲート通過 [{ts}]")
        print(f"  → Phase {phase + 1} を開始してください。")
        print(f"{'='*55}\n")
        sys.exit(0)
    else:
        print(f"  ⛔ Phase {phase} ゲート失敗")
        print(f"  → 上記の [FAIL] 項目を解消し、{args.file} を更新してから再実行してください。")
        print(f"  → Phase {phase + 1} の開始は禁止です。")
        print(f"{'='*55}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
