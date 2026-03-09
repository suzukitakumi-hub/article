#!/usr/bin/env python3
"""
TCJ 文体（ですます調）バリデーション v1.0
だ・である調の文末を検出する。全チェックPASSするまで記事を完成とみなさない。

使い方:
  python3 validate_tone.py <HTMLまたはテキストファイル>
"""

import re
import sys
from pathlib import Path


SCRIPT_VERSION = "1.0.0"

# (文末パターン, 除外パターンリスト, 修正ヒント)
# 文を「。」で分割後、各文の末尾をチェックする
DAIDEARU_CHECKS = [
    ("だ",       [],                      "だ → です"),
    ("である",   [],                      "である → です"),
    ("なのだ",   [],                      "なのだ → なのです"),
    ("だった",   [],                      "だった → でした"),
    ("であった", [],                      "であった → でした"),
    ("ない",     [],                      "ない → ません/ありません"),
    ("いる",     [],                      "いる → います"),
    ("いた",     [],                      "いた → いました"),
    ("した",     ["ました", "でした"],    "した → しました"),
]

MIN_SENTENCE_LEN = 8  # これ未満の文（短すぎる断片）はスキップ


def strip_html(html: str) -> str:
    """HTMLタグを除去してプレーンテキストを返す。"""
    text = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&[a-zA-Z]+;", "", text)
    return text


def check_tone(text: str) -> list[dict]:
    """だ・である調の文末を検出して違反リストを返す。"""
    violations = []
    sentences = re.split(r"[。！？]", text)

    for s in sentences:
        s = s.strip()
        if len(s) < MIN_SENTENCE_LEN:
            continue

        for ending, exclusions, hint in DAIDEARU_CHECKS:
            if s.endswith(ending):
                # 除外パターンに該当する場合はスキップ（ですます調の正常形）
                if any(s.endswith(exc) for exc in exclusions):
                    break
                violations.append({
                    "hint": hint,
                    "sentence": ("…" + s[-60:]) if len(s) > 60 else s,
                })
                break  # 1文につき1件のみ報告

    return violations


def main():
    if len(sys.argv) < 2:
        print("使い方: python3 validate_tone.py <ファイル>")
        sys.exit(1)

    filepath = sys.argv[1]
    raw = Path(filepath).read_text(encoding="utf-8")

    is_html = bool(re.search(r"<(p|div|h[1-6]|table|section)\b", raw, re.IGNORECASE))
    text = strip_html(raw) if is_html else raw

    violations = check_tone(text)

    print("=" * 60)
    print(f"TCJ 文体バリデーション v{SCRIPT_VERSION}")
    print("=" * 60)
    print(f"\n[INFO] 入力ファイル: {filepath}")
    print(f"[INFO] HTML検出: {'あり（タグ除去済み）' if is_html else 'なし（プレーンテキスト）'}")

    if not violations:
        print("\n" + "=" * 60)
        print("[PASS] 文体チェック全項目PASS - ですます調が守られています")
        print("=" * 60)
        sys.exit(0)
    else:
        print(f"\n[FAIL] {len(violations)}件のだ・である調を検出\n")
        for i, v in enumerate(violations, 1):
            print(f"  [{i:02d}] {v['hint']}")
            print(f"       → {v['sentence']}")
            print()
        print("=" * 60)
        print(f"違反合計: {len(violations)}件")
        print("すべてですます調に修正してから再実行してください。")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
