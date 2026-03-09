# -*- coding: utf-8 -*-
"""
Markdown to HTML Converter - Architecture Article Style
建築業記事のインラインスタイルを使用してHTML変換
"""

import os
import re
import sys
from html import escape


def extract_frontmatter(content):
    """YAML frontmatter を抽出して本文とメタ情報を返す。"""
    meta = {}
    if not content.startswith("---\n"):
        return meta, content

    end = content.find("\n---", 4)
    if end == -1:
        return meta, content

    fm = content[4:end].splitlines()
    body = content[end + 4 :].lstrip("\n")

    current_key = None
    for line in fm:
        if not line.strip():
            continue
        if re.match(r"^\s*-\s+", line) and current_key:
            meta.setdefault(current_key, []).append(line.strip()[2:].strip('"'))
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            current_key = key.strip()
            val = val.strip().strip('"')
            if val:
                meta[current_key] = val
            else:
                meta[current_key] = []
    return meta, body


def strip_markdown_links(text):
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    return text


def to_inline(text):
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[(.+?)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', text)
    return text


def build_description(content, fallback):
    for raw in content.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("|") or line.startswith("- ") or line.startswith("```"):
            continue
        clean = strip_markdown_links(re.sub(r"\*\*(.+?)\*\*", r"\1", line))
        if clean:
            return clean[:150]
    return fallback[:150]


def convert_md_to_html(md_file, html_file):
    """MarkdownファイルをTCJ建築業スタイル（インラインCSS）のHTMLに変換"""
    with open(md_file, "r", encoding="utf-8") as f:
        raw = f.read()

    meta, content = extract_frontmatter(raw)

    # H1抽出（なければ frontmatter title を使用）
    h1_match = re.search(r"^# (.+)$", content, re.MULTILINE)
    h1_title = h1_match.group(1).strip() if h1_match else ""
    if h1_match:
        content = content.replace(h1_match.group(0), "", 1)

    page_title = meta.get("title") or h1_title or "TCJ外国人材Times"
    meta_desc = build_description(content, page_title)

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(page_title)} - TCJ外国人材Times</title>
    <meta name="description" content="{escape(meta_desc)}">
</head>
<body>
    <article class="rounded-[10px] bg-white shadow-xl overflow-hidden">
        <div class="entry-content">
            <div style="font-family: 'acumin-pro', 'Noto Sans JP', sans-serif; font-size: 16px; line-height: 1.8; color: #424242; letter-spacing: 0.05em; background: #fff; padding: 20px; max-width: 900px; margin: 0 auto;">
"""

    lines = content.split("\n")
    in_table = False
    table_buffer = []
    in_list = False
    list_buffer = []
    list_type = None
    in_code = False
    code_buffer = []

    i = 0
    while i < len(lines):
        line_raw = lines[i]
        line = line_raw.strip()

        if line.startswith("```"):
            if not in_code:
                in_code = True
                code_buffer = []
            else:
                html += '<pre style="margin: 24px 0; padding: 16px; border: 1px solid #e1e1e1; background: #fafafa; overflow-x: auto;"><code>'
                html += escape("\n".join(code_buffer))
                html += "</code></pre>\n"
                in_code = False
                code_buffer = []
            i += 1
            continue

        if in_code:
            code_buffer.append(line_raw)
            i += 1
            continue

        if not line:
            i += 1
            continue

        if line == "---":
            i += 1
            continue

        if line.startswith("#### "):
            html += f'<h4 style="font-size: 18px; font-weight: bold; color: #102891; margin-top: 32px; margin-bottom: 15px; border-left: 4px solid #102891; padding-left: 10px;">{to_inline(line[5:])}</h4>\n'
            i += 1
            continue

        if line.startswith("### "):
            html += f'<h3 style="font-size: 22px; font-weight: bold; line-height: 1.3; color: #424242; margin-top: 46px; margin-bottom: 18px; border-left: 6px solid #102891; padding-left: 15px; background-color: transparent;">{to_inline(line[4:])}</h3>\n'
            i += 1
            continue

        if line.startswith("## "):
            html += f'<h2 style="font-size: 28px; font-weight: bold; line-height: 1.3; color: #424242; margin-top: 60px; margin-bottom: 24px; padding-bottom: 15px; border-bottom: 2px solid #102891;">{to_inline(line[3:])}</h2>\n'
            i += 1
            continue

        image_match = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", line)
        if image_match:
            alt, src = image_match.groups()
            html += f'<p style="margin-bottom: 24px;"><img src="{escape(src)}" alt="{escape(alt or "記事画像")}" style="width: 100%; height: auto; border-radius: 8px;"></p>\n'
            i += 1
            continue

        if line.startswith("|") and not in_table:
            in_table = True
            table_buffer = [line]
            i += 1
            continue

        if line.startswith("|") and in_table:
            table_buffer.append(line)
            i += 1
            continue

        if in_table and not line.startswith("|"):
            html += convert_table(table_buffer)
            in_table = False
            table_buffer = []
            continue

        if (line.startswith("- ") or re.match(r"^\d+\.\s", line)) and not in_list:
            in_list = True
            list_type = "ul" if line.startswith("- ") else "ol"
            list_buffer = [line]
            i += 1
            continue

        if in_list:
            if (list_type == "ul" and line.startswith("- ")) or (list_type == "ol" and re.match(r"^\d+\.\s", line)):
                list_buffer.append(line)
                i += 1
                continue
            html += convert_list(list_buffer, list_type)
            in_list = False
            list_buffer = []
            list_type = None
            continue

        html += f'<p style="margin-bottom: 24px;">{to_inline(line)}</p>\n'
        i += 1

    if in_table:
        html += convert_table(table_buffer)
    if in_list:
        html += convert_list(list_buffer, list_type)
    if in_code and code_buffer:
        html += '<pre style="margin: 24px 0; padding: 16px; border: 1px solid #e1e1e1; background: #fafafa; overflow-x: auto;"><code>'
        html += escape("\n".join(code_buffer))
        html += "</code></pre>\n"

    html += """            </div>
        </div>
    </article>
</body>
</html>"""

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] 変換完了: {html_file}")
    print("[OK] タイトル・メタ・画像・frontmatter対応済み")


def convert_table(table_lines):
    """Markdown表をHTMLテーブルに変換（建築業スタイル）"""
    if len(table_lines) < 2:
        return ""

    html = '<table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e1e1e1; font-size: 15px;">\n'
    header = table_lines[0].strip("|").split("|")
    html += '<thead>\n<tr style="background-color: #f0f4f8;">\n'
    for cell in header:
        html += f'<th style="padding: 12px; border: 1px solid #e1e1e1; text-align: left;">{to_inline(cell.strip())}</th>\n'
    html += "</tr>\n</thead>\n"

    html += "<tbody>\n"
    for row in table_lines[2:]:
        cells = row.strip("|").split("|")
        html += "<tr>\n"
        for cell in cells:
            html += f'<td style="padding: 12px; border: 1px solid #e1e1e1;">{to_inline(cell.strip())}</td>\n'
        html += "</tr>\n"
    html += "</tbody>\n</table>\n"
    return html


def convert_list(list_lines, list_type):
    """リストをHTMLに変換（建築業スタイル）"""
    html = f'<{list_type} style="list-style: none; padding: 1em 1.5em; margin: 24px 0; border: 1px solid #102891;">\n'
    for line in list_lines:
        if list_type == "ul":
            text = line[2:].strip()
        else:
            text = re.sub(r"^\d+\.\s+", "", line).strip()
        html += f'<li style="margin-bottom: 10px;">{to_inline(text)}</li>\n'
    html += f"</{list_type}>\n"
    return html


if __name__ == "__main__":
    if len(sys.argv) > 1:
        md_file = sys.argv[1]
        if len(sys.argv) > 2:
            html_file = sys.argv[2]
        else:
            base_name = os.path.basename(md_file).replace(".md", "")
            html_file = os.path.join(os.path.dirname(md_file), "..", "output", f"{base_name}.html")
            os.makedirs(os.path.dirname(html_file), exist_ok=True)
    else:
        md_file = r"c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\data\article_archives\posts\job_posting.md"
        html_file = r"c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\output\job_posting.html"

    print(f"Converting: {md_file} -> {html_file}")
    convert_md_to_html(md_file, html_file)
