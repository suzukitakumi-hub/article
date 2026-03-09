#!/usr/bin/env python3
"""
TCJ SEO記事バリデーションスクリプト v3
Phase5で実行し、全項目PASSするまで記事を完成とみなさない。

【重要】このスクリプトの内容を変更してはならない。
引数形式、チェックロジック、出力形式を一切改変しないこと。

使い方:
  python3 validate_article.py <HTMLまたはテキストファイル> --title "タイトル文字列" --target-chars 5000

引数:
  --title          記事タイトル（必須）
  --target-chars   Phase3で計画した想定文字数（任意、指定時は±20%チェック）
"""

import re
import sys
import hashlib
from datetime import datetime
from pathlib import Path


# ============================================================
# 改変検出用ハッシュ（このコメント行より下のCONFIGセクションのみ変更可）
# ============================================================
SCRIPT_VERSION = "3.0.0"


# ============================================================
# 設定値（writing-rules.md と同期させること）
# ============================================================

BANNED_WORDS = [
    "ニーズ", "セクション", "示します", "示す", "提供", "考慮",
    "活用", "存在", "特定", "向上", "慎重", "アプローチ", "スムーズ",
]

BANNED_WORD_EXCEPTIONS = {
    "特定": ["特定技能", "特定活動", "特定産業分野"],
}

BANNED_METAPHORS = [
    "羅針盤", "コンパス", "潤滑油", "車の両輪", "スパイス",
    "レシピ", "DNA", "土台", "柱", "地図", "設計書",
]

SAFETY_CUSHIONS = [
    "一般的に", "多くの場合", "状況によって異なります",
    "一概には言えませんが", "ケースバイケースです",
]

CLOSING_CLICHES = [
    "参考になれば幸いです", "まずは小さく始めましょう",
    "いかがでしたか", "結論から言うと",
]

META_EXPRESSIONS = [
    "本記事では", "以下で解説します", "この記事では", "本稿では",
]

MAX_EXCLAMATION = 2
MAX_TITLE_LENGTH = 36
MIN_TITLE_LENGTH = 28
MAX_CONSECUTIVE_ENDINGS = 2


# ============================================================
# ユーティリティ
# ============================================================

def strip_html(html: str) -> str:
    """HTMLタグを除去してプレーンテキストを返す。"""
    text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&[a-zA-Z]+;', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def count_content_chars(text: str) -> int:
    """プレーンテキストの文字数をカウント（空白を除く）。"""
    return len(re.sub(r'\s', '', text))


def parse_args():
    """引数をパース。--title と --target-chars をサポート。"""
    args = sys.argv[1:]
    filepath = None
    title = ""
    target_chars = None

    i = 0
    while i < len(args):
        if args[i] == "--title" and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        elif args[i] == "--target-chars" and i + 1 < len(args):
            target_chars = int(args[i + 1])
            i += 2
        elif not args[i].startswith("--"):
            filepath = args[i]
            i += 1
        else:
            i += 1

    return filepath, title, target_chars


# ============================================================
# チェック関数群（各関数は violations リストを返す）
# ============================================================

def check_banned_words(text: str) -> list[dict]:
    violations = []
    lines = text.split("\n")
    for word in BANNED_WORDS:
        exceptions = BANNED_WORD_EXCEPTIONS.get(word, [])
        for i, line in enumerate(lines, 1):
            if word in line:
                clean_line = line
                for exc in exceptions:
                    clean_line = clean_line.replace(exc, "")
                if word in clean_line:
                    violations.append({
                        "rule": "禁止ワード",
                        "detail": f"「{word}」L{i}",
                        "context": line.strip()[:80],
                    })
    return violations


def check_banned_metaphors(text: str) -> list[dict]:
    violations = []
    lines = text.split("\n")
    for m in BANNED_METAPHORS:
        for i, line in enumerate(lines, 1):
            if m in line:
                violations.append({
                    "rule": "禁止比喩",
                    "detail": f"「{m}」L{i}",
                    "context": line.strip()[:80],
                })
    return violations


def check_safety_cushions(text: str) -> list[dict]:
    violations = []
    lines = text.split("\n")
    for c in SAFETY_CUSHIONS:
        for i, line in enumerate(lines, 1):
            if c in line:
                violations.append({
                    "rule": "安全クッション語",
                    "detail": f"「{c}」L{i}",
                    "context": line.strip()[:80],
                })
    return violations


def check_closing_cliches(text: str) -> list[dict]:
    violations = []
    lines = text.split("\n")
    for cl in CLOSING_CLICHES:
        for i, line in enumerate(lines, 1):
            if cl in line:
                violations.append({
                    "rule": "締め定型句",
                    "detail": f"「{cl}」L{i}",
                    "context": line.strip()[:80],
                })
    return violations


def check_meta_expressions(text: str) -> list[dict]:
    violations = []
    lines = text.split("\n")
    for me in META_EXPRESSIONS:
        for i, line in enumerate(lines, 1):
            if me in line:
                violations.append({
                    "rule": "メタ表現",
                    "detail": f"「{me}」L{i}",
                    "context": line.strip()[:80],
                })
    return violations


def check_consecutive_endings(text: str) -> list[dict]:
    violations = []
    sentences = re.split(r"。", text)
    history = []

    for s in sentences:
        s = s.strip()
        if not s or len(s) < 10:
            history = []
            continue

        if s.endswith("です"):
            ending = "です"
        elif s.endswith("ます"):
            ending = "ます"
        elif s.endswith("ました"):
            ending = "ました"
        elif s.endswith("ません"):
            ending = "ません"
        elif s.endswith("でした"):
            ending = "でした"
        else:
            ending = s[-3:] if len(s) >= 3 else s

        history.append({"ending": ending, "text": s[:40]})

        if len(history) >= 3:
            last3 = [e["ending"] for e in history[-3:]]
            if last3[0] == last3[1] == last3[2]:
                violations.append({
                    "rule": "語尾3連続",
                    "detail": f"「{last3[0]}」",
                    "context": " / ".join(e["text"] + "…" for e in history[-3:]),
                })

    return violations


def check_exclamation(text: str) -> list[dict]:
    count = text.count("！")
    if count > MAX_EXCLAMATION:
        return [{"rule": "感嘆符超過", "detail": f"！×{count}回（上限{MAX_EXCLAMATION}）", "context": ""}]
    return []


def check_colon_space(text: str) -> list[dict]:
    violations = []
    lines = text.split("\n")
    for i, line in enumerate(lines, 1):
        if "： " in line:
            violations.append({
                "rule": "コロン＋半角スペース",
                "detail": f"L{i}",
                "context": line.strip()[:80],
            })
    return violations


def check_title(title: str) -> list[dict]:
    violations = []
    if not title:
        violations.append({"rule": "タイトル未指定", "detail": "--title引数が空", "context": ""})
        return violations
    n = len(title)
    if n > MAX_TITLE_LENGTH:
        violations.append({
            "rule": "タイトル文字数超過",
            "detail": f"{n}文字（上限{MAX_TITLE_LENGTH}文字）",
            "context": title,
        })
    elif n < MIN_TITLE_LENGTH:
        violations.append({
            "rule": "タイトル文字数不足",
            "detail": f"{n}文字（下限{MIN_TITLE_LENGTH}文字）",
            "context": title,
        })
    return violations


def check_year_consistency(text: str, title: str) -> list[dict]:
    """タイトルと本文の年号整合性 + 現在年チェック。"""
    violations = []
    current_year = str(datetime.now().year)

    # タイトル内の年号が現在年か
    title_years = re.findall(r"(20\d{2})年", title) if title else []
    for y in title_years:
        if y != current_year:
            violations.append({
                "rule": "年号：現在年と不一致（タイトル）",
                "detail": f"タイトルに{y}年あり（現在年={current_year}年）",
                "context": title,
            })

    # 本文内の「20XX年最新」「20XX年版」が現在年か
    for pattern, label in [
        (r"(20\d{2})年最新", "○○年最新"),
        (r"(20\d{2})年版", "○○年版"),
    ]:
        for match in re.finditer(pattern, text):
            y = match.group(1)
            if y != current_year:
                violations.append({
                    "rule": f"年号：現在年と不一致（本文「{label}」）",
                    "detail": f"本文に{y}年{label[2:]}あり（現在年={current_year}年）",
                    "context": text[max(0, match.start()-20):match.end()+20],
                })

    # タイトルと本文の不整合
    if title_years:
        title_year = title_years[0]
        body_latest = re.findall(r"(20\d{2})年最新", text)
        for y in body_latest:
            if y != title_year:
                violations.append({
                    "rule": "年号：タイトルと本文の不整合",
                    "detail": f"タイトル={title_year}年 vs 本文={y}年最新",
                    "context": "",
                })

    return violations


def check_faq_count(text: str) -> list[dict]:
    faq_count = len(re.findall(r"Q\d+[\.\．]", text))
    if faq_count < 5:
        return [{"rule": "FAQ不足", "detail": f"{faq_count}問（最低5問）", "context": ""}]
    return []


def check_char_count(text: str, target: int | None) -> list[dict]:
    """プレーンテキスト文字数を報告。target指定時は±20%チェック。"""
    char_count = count_content_chars(text)
    violations = []

    if target:
        lower = int(target * 0.8)
        upper = int(target * 1.2)
        if char_count < lower:
            violations.append({
                "rule": "文字数不足",
                "detail": f"本文{char_count}文字（目標{target}文字の80%={lower}文字を下回る）",
                "context": "",
            })
        elif char_count > upper:
            violations.append({
                "rule": "文字数超過",
                "detail": f"本文{char_count}文字（目標{target}文字の120%={upper}文字を上回る）",
                "context": "",
            })

    return violations, char_count


def check_forbidden_tags(text: str) -> list[dict]:
    """禁止タグ（style, head）が含まれていないかチェック。"""
    violations = []
    # 大文字小文字を区別せずチェックするために小文字化
    lower_text = text.lower()
    
    if "<style" in lower_text:
        violations.append({
            "rule": "禁止タグ",
            "detail": "本文に<style>タグが含まれています。CSSは外部ファイル（テーマCSS等）で管理してください。",
            "context": re.search(r'<style[^>]*>', text, re.IGNORECASE).group(0) if re.search(r'<style[^>]*>', text, re.IGNORECASE) else "<style>"
        })
        
    if "<head" in lower_text:
        violations.append({
            "rule": "禁止タグ",
            "detail": "本文に<head>タグが含まれています。",
            "context": re.search(r'<head[^>]*>', text, re.IGNORECASE).group(0) if re.search(r'<head[^>]*>', text, re.IGNORECASE) else "<head>"
        })
        
    return violations


# ============================================================
# メイン実行
# ============================================================

def main():
    filepath, title, target_chars = parse_args()

    if not filepath:
        print("使い方: python3 validate_article.py <ファイル> --title \"タイトル\" [--target-chars 5000]")
        sys.exit(1)

    raw = Path(filepath).read_text(encoding="utf-8")

    # HTML判定：タグが含まれていればHTMLとして処理
    is_html = bool(re.search(r'<(p|div|h[1-6]|table|section)\b', raw, re.IGNORECASE))
    if is_html:
        text = strip_html(raw)
    else:
        text = raw

    # 全チェック実行
    all_violations = []
    all_violations.extend(check_banned_words(text))
    all_violations.extend(check_banned_metaphors(text))
    all_violations.extend(check_safety_cushions(text))
    all_violations.extend(check_closing_cliches(text))
    all_violations.extend(check_meta_expressions(text))
    all_violations.extend(check_consecutive_endings(text))
    all_violations.extend(check_exclamation(text))
    all_violations.extend(check_colon_space(text))
    all_violations.extend(check_faq_count(text))
    all_violations.extend(check_title(title))
    all_violations.extend(check_year_consistency(text, title))
    all_violations.extend(check_forbidden_tags(raw))

    char_violations, char_count = check_char_count(text, target_chars)
    all_violations.extend(char_violations)

    # === 結果出力 ===
    print("=" * 60)
    print(f"TCJ SEO記事バリデーション v{SCRIPT_VERSION}")
    print("=" * 60)

    # 入力情報
    print(f"\n[INFO] 入力ファイル: {filepath}")
    print(f"[INFO] HTML検出: {'あり（タグ除去済み）' if is_html else 'なし（プレーンテキスト）'}")
    print(f"[INFO] タイトル: {title if title else '（未指定）'}")
    if title:
        print(f"[INFO] タイトル文字数: {len(title)}文字")
    print(f"[INFO] 本文文字数（プレーンテキスト、空白除く）: {char_count}文字")
    if target_chars:
        print(f"[INFO] 目標文字数: {target_chars}文字（許容範囲: {int(target_chars*0.8)}〜{int(target_chars*1.2)}文字）")
    print(f"[INFO] 現在年: {datetime.now().year}年")

    if not all_violations:
        print("\n" + "=" * 60)
        print("[PASS] 全チェック項目PASS - Phase5完了可能")
        print("=" * 60)
        sys.exit(0)
    else:
        by_rule = {}
        for v in all_violations:
            rule = v["rule"]
            if rule not in by_rule:
                by_rule[rule] = []
            by_rule[rule].append(v)

        print(f"\n[FAIL] {len(all_violations)}件の違反を検出\n")

        for rule, items in by_rule.items():
            print(f"--- {rule} ({len(items)}件) ---")
            for item in items:
                print(f"  [x] {item['detail']}")
                if item.get("context"):
                    print(f"     -> {item['context']}")
            print()

        print("=" * 60)
        print(f"違反合計: {len(all_violations)}件")
        print("全件修正してから再実行してください。")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
