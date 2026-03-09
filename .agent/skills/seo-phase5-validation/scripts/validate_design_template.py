#!/usr/bin/env python3
"""
Design template validator for TCJ SEO workflow.
Checks strict template compliance beyond text quality rules.
"""

import re
import sys
from pathlib import Path


DISALLOWED_THEME_CLASSES = [
    "p-column-detail",
    "p-column-detail__body",
    "scroll-box",
    "table-default",
    "step-process",
    "p-faq-part",
    "c-cta-part",
]


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python validate_design_template.py <html_file>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"[ERROR] File not found: {path}")
        return 2

    html = path.read_text(encoding="utf-8", errors="ignore")
    errors = []

    # 1) Wrapper style compliance (template baseline)
    wrapper_ok = False
    for m in re.finditer(r"<div[^>]*style=\"([^\"]+)\"[^>]*>", html, flags=re.IGNORECASE):
        style = m.group(1)
        if (
            "'acumin-pro'" in style
            and "'Noto Sans JP'" in style
            and "line-height: 1.8" in style
            and "max-width: 900px" in style
        ):
            wrapper_ok = True
            break
    if not wrapper_ok:
        errors.append("WRAPPERのテンプレスタイル（acumin-pro / line-height 1.8 / max-width 900px）が見つかりません。")

    # 2) Disallow theme-dependent classes in article HTML
    for cls in DISALLOWED_THEME_CLASSES:
        if re.search(rf'class=\"[^\"]*\b{re.escape(cls)}\b', html):
            errors.append(f"テーマ依存クラス禁止違反: {cls}")

    # 3) Require inline styles on section headings
    for tag in ("h2", "h3", "h4"):
        if re.search(rf"<{tag}(?![^>]*\bstyle=)[^>]*>", html, flags=re.IGNORECASE):
            errors.append(f"{tag.upper()}にインラインstyleがない要素があります。")

    # 4) Internal link card structure must match template shape
    card_pattern = re.compile(
        r"<div\s+class=\"tcj-blogcard\">\s*"
        r"<span\s+class=\"tcj-blogcard-label\">.*?</span>\s*"
        r"<a\s+href=\"[^\"]+\"\s+class=\"tcj-blogcard-link\"[^>]*>\s*"
        r"<img\s+[^>]*>\s*"
        r"<span\s+class=\"tcj-blogcard-title\">.*?</span>\s*"
        r"</a>\s*</div>",
        flags=re.IGNORECASE | re.DOTALL,
    )
    if "tcj-blogcard" in html and not card_pattern.search(html):
        errors.append("内部リンクカードがテンプレ構造と一致しません。")

    # 5) Disallow generated variant class names
    if re.search(r"\btcj-blogcard__", html):
        errors.append("`tcj-blogcard__*` の派生クラスは使用禁止です。")

    # 6) Internal link image placeholders are not allowed
    for bad in ("placehold.jp", "placeholder"):
        if re.search(rf'<div\s+class="tcj-blogcard">[\s\S]*?src="[^"]*{re.escape(bad)}[^"]*"', html, flags=re.IGNORECASE):
            errors.append(f"内部リンクカード画像にプレースホルダーURL（{bad}）が残っています。")

    print("============================================================")
    print("TCJ Design Template Validation")
    print("============================================================")

    if errors:
        for e in errors:
            fail(e)
        print("============================================================")
        print(f"[RESULT] FAIL ({len(errors)} issues)")
        print("============================================================")
        return 1

    print("[PASS] デザインテンプレ準拠")
    print("============================================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())
