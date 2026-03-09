# -*- coding: utf-8 -*-
"""
Markdown to HTML Converter - Architecture Style (Exact CSS Match)
建築業記事の完全なCSSを使用してHTML変換
"""

import re

def convert_md_to_html_exact_css(md_file, html_file):
    """MarkdownファイルをTCJ建築業スタイル（完全一致CSS）のHTMLに変換"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 建築業記事から抽出した完全なCSS
    css = '''
    <style>
        /* Core Article Container Constraints */
        body {
            font-family: "Noto Sans JP", sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        
        article {
            max-width: 1280px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .entry-content {
            font-family: "Noto Sans JP", sans-serif;
            font-size: 16px;
            line-height: 1.5;
            color: #333333;
        }

        /* H1 Style */
        .entry-content h1 {
            font-size: 28px;
            font-weight: 800;
            color: #102891;
            margin-bottom: 30px;
            line-height: 1.4;
        }

        @media (min-width: 840px) {
            .entry-content h1 {
                font-size: 40px;
            }
        }

        /* H2 Heading Style: Centered with Blue Underline */
        .entry-content h2 {
            margin-top: 4.5rem; /* 72px */
            margin-bottom: 3rem; /* 48px */
            padding-bottom: 15px;
            text-align: center;
            font-size: 28px;
            font-weight: 800;
            color: #102891; /* Primary Blue */
            border-bottom: 2px solid #102891;
        }

        @media (min-width: 840px) {
            .entry-content h2 {
                font-size: 40px;
            }
        }

        /* H3 Heading Style: L-shape Decoration (Left and Bottom Border) */
        .entry-content h3 {
            margin-top: 3rem; /* 48px */
            margin-bottom: 1.125rem; /* 18px */
            padding: 0 0 2px 15px;
            font-size: 22px;
            font-weight: 700;
            color: #424242;
            border-left: 6px solid #102891;
            border-bottom: 2px solid #102891;
            letter-spacing: 1px;
        }

        @media (min-width: 540px) {
            .entry-content h3 {
                font-size: 32px;
            }
        }

        /* Paragraph Style */
        .entry-content p {
            margin: 15px 0;
            line-height: 1.8;
        }

        /* List (UL/OL) Style: Boxed with Blue Border and Rounded Corners */
        .entry-content ul, .entry-content ol {
            margin: 24px 0;
            padding: 16px 24px;
            border: 1px solid #102891;
            border-radius: 8px;
            list-style-type: disc;
            background-color: transparent;
        }

        .entry-content ul li, .entry-content ol li {
            margin-bottom: 1.125rem; /* 18px spacing between items */
        }

        /* Table Style: Clean, Professional with Grey Borders */
        .entry-content figure.wp-block-table {
            overflow-x: auto;
            margin-bottom: 30px;
        }

        .entry-content table {
            width: 100%;
            font-size: 15px;
            border-collapse: collapse;
            border: 1px solid #e1e1e1;
            color: #424242;
            margin: 25px 0;
        }

        .entry-content th, .entry-content td {
            border: 1px solid #f2f2f2;
            padding: 12px;
        }

        .entry-content th {
            background-color: #f5f5f5;
            font-weight: 700;
        }

        /* Links and Strong Text */
        .entry-content a {
            color: #007cff;
            text-decoration: underline;
        }

        .entry-content strong {
            font-weight: 800;
            color: #102891;
        }

        /* Info Box Style */
        .info-box {
            border: 1px solid #102891;
            border-radius: 8px;
            padding: 20px 24px;
            margin: 25px 0;
            background-color: #f8f9ff;
        }

        .info-box p {
            margin: 8px 0;
        }

        /* Stats Infographic */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .stat-card {
            background: linear-gradient(135deg, #102891 0%, #1e3a8a 100%);
            color: white;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .stat-number {
            font-size: 48px;
            font-weight: 800;
            margin: 10px 0;
        }

        .stat-label {
            font-size: 14px;
            opacity: 0.9;
        }

        .stat-description {
            font-size: 12px;
            margin-top: 8px;
            opacity: 0.8;
        }
    </style>
'''
    
    # HTMLヘッダー
    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>【2026年最新】在留資格更新の完全ガイド｜手続き・必要書類・在留期間を伸ばす戦略 - TCJ外国人材Times</title>
    <meta name="description" content="在留資格更新の手続き、必要書類、審査期間を徹底解説。許可率99%の更新を成功させるポイントと、在留期間を3年→5年に伸ばす戦略も紹介。TCJが38年の実績で完全サポート。">
    {css}
</head>
<body>
    <article>
        <div class="entry-content">
'''
    
    # H1を抽出
    h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if h1_match:
        h1_text = h1_match.group(1)
        html += f'            <h1>{h1_text}</h1>\n\n'
        content = content.replace(h1_match.group(0), '', 1)
    
    # 変換処理
    lines = content.split('\n')
    in_table = False
    table_buffer = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 空行または区切り線
        if not line or line == '---':
            i += 1
            continue
        
        # H2
        if line.startswith('## '):
            text = line[3:]
            html += f'            <h2>{text}</h2>\n\n'
            i += 1
            continue
        
        # H3
        if line.startswith('### '):
            text = line[4:]
            html += f'            <h3>{text}</h3>\n\n'
            i += 1
            continue
        
        # 表の開始
        if line.startswith('|') and not in_table:
            in_table = True
            table_buffer = [line]
            i += 1
            continue
        
        # 表の継続
        if line.startswith('|') and in_table:
            table_buffer.append(line)
            i += 1
            continue
        
        # 表の終了
        if in_table and not line.startswith('|'):
            html += convert_table(table_buffer)
            in_table = False
            table_buffer = []
            # 現在の行は次のループで処理
            continue
        
        # リストの検出（ボックス化の判断）
        if line.startswith('- '):
            # 次の数行を先読みしてリストの長さを確認
            list_items = []
            j = i
            while j < len(lines) and lines[j].strip().startswith('- '):
                list_items.append(lines[j].strip()[2:])
                j += 1
            
            # リストが3項目以上ならボックス化
            if len(list_items) >= 3:
                html += '            <div class="info-box">\n'
                for item in list_items:
                    item_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                    html += f'                <p>• {item_html}</p>\n'
                html += '            </div>\n\n'
                i = j
                continue
            else:
                # 短いリストは通常のulとして処理
                html += '            <ul>\n'
                for item in list_items:
                    item_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                    html += f'                <li>{item_html}</li>\n'
                html += '            </ul>\n\n'
                i = j
                continue
        
        # 通常の段落
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        html += f'            <p>{text}</p>\n\n'
        i += 1
    
    # 表が残っている場合
    if in_table:
        html += convert_table(table_buffer)
    
    # HTMLフッター
    html += '''        </div>
    </article>
</body>
</html>'''
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ 変換完了: {html_file}")
    print("✓ 建築業記事の完全なCSSを適用")
    print("✓ 横幅を1280pxに修正")

def convert_table(table_lines):
    """Markdown表をHTMLテーブルに変換"""
    if len(table_lines) < 2:
        return ''
    
    html = '            <table>\n'
    
    # ヘッダー行
    header = table_lines[0].strip('|').split('|')
    html += '                <thead>\n                    <tr>\n'
    for cell in header:
        html += f'                        <th>{cell.strip()}</th>\n'
    html += '                    </tr>\n                </thead>\n'
    
    # データ行（2行目は区切り線なのでスキップ）
    html += '                <tbody>\n'
    for row in table_lines[2:]:
        cells = row.strip('|').split('|')
        html += '                    <tr>\n'
        for cell in cells:
            cell_text = cell.strip()
            cell_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', cell_text)
            html += f'                        <td>{cell_text}</td>\n'
        html += '                    </tr>\n'
    html += '                </tbody>\n'
    
    html += '            </table>\n\n'
    return html

if __name__ == '__main__':
    md_file = r'c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\articles\2026\02\在留資格更新.md'
    html_file = r'c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\output\在留資格更新.html'
    
    convert_md_to_html_exact_css(md_file, html_file)
