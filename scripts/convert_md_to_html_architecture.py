# -*- coding: utf-8 -*-
"""
Markdown to HTML Converter for TCJ Articles (Architecture Style)
在留資格更新記事を建築業記事のデザインで変換
"""

import re

def convert_md_to_html_architecture_style(md_file, html_file):
    """MarkdownファイルをTCJ建築業スタイルのHTMLに変換"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CSS（建築業記事のスタイルを再現）
    css = '''
    <style>
        body {
            font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.8;
            color: #424242;
            background-color: #f9f9f9;
            padding: 20px;
        }
        article {
            max-width: 900px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            font-size: 32px;
            font-weight: 800;
            color: #102891;
            margin-bottom: 30px;
            line-height: 1.4;
        }
        h2 {
            font-size: 28px;
            font-weight: 700;
            color: #424242;
            text-align: center;
            border-bottom: 2px solid #102891;
            padding-bottom: 15px;
            margin: 50px 0 30px 0;
        }
        h3 {
            font-size: 22px;
            font-weight: 700;
            color: #424242;
            border-left: 6px solid #102891;
            border-bottom: 2px solid #102891;
            padding-left: 15px;
            padding-bottom: 10px;
            margin: 35px 0 20px 0;
        }
        p {
            font-size: 16px;
            margin: 15px 0;
        }
        strong {
            color: #102891;
            font-weight: 700;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
        }
        th {
            background-color: #f0f4f8;
            padding: 12px;
            text-align: left;
            border: 1px solid #e1e1e1;
            font-weight: 700;
        }
        td {
            padding: 12px;
            border: 1px solid #e1e1e1;
        }
        .info-box {
            border: 0.67px solid #102891;
            border-radius: 8px;
            padding: 20px 24px;
            margin: 25px 0;
            background-color: #f8f9ff;
        }
        .info-box p {
            margin: 8px 0;
        }
        .info-box p:first-child {
            margin-top: 0;
        }
        .info-box p:last-child {
            margin-bottom: 0;
        }
        .step-number {
            display: inline-block;
            background-color: #102891;
            color: white;
            padding: 2px 10px;
            border-radius: 4px;
            margin-right: 8px;
            font-weight: 700;
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
'''
    
    # H1を抽出
    h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if h1_match:
        h1_text = h1_match.group(1)
        html += f'        <h1>{h1_text}</h1>\n\n'
        content = content.replace(h1_match.group(0), '', 1)
    
    # 変換処理
    lines = content.split('\n')
    in_table = False
    table_buffer = []
    in_info_box = False
    info_box_buffer = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 空行
        if not line or line == '---':
            i += 1
            continue
        
        # H2
        if line.startswith('## '):
            text = line[3:]
            html += f'        <h2>{text}</h2>\n\n'
            i += 1
            continue
        
        # H3
        if line.startswith('### '):
            text = line[4:]
            html += f'        <h3>{text}</h3>\n\n'
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
                html += '        <div class="info-box">\n'
                for item in list_items:
                    item_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                    html += f'            <p>• {item_html}</p>\n'
                html += '        </div>\n\n'
                i = j
                continue
            else:
                # 短いリストは通常の段落として処理
                for item in list_items:
                    item_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                    html += f'        <p>• {item_html}</p>\n'
                i = j
                continue
        
        # 通常の段落
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        html += f'        <p>{text}</p>\n\n'
        i += 1
    
    # 表が残っている場合
    if in_table:
        html += convert_table(table_buffer)
    
    # HTMLフッター
    html += '''    </article>
</body>
</html>'''
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"変換完了: {html_file}")
    print("✓ 建築業記事のデザインを適用")
    print("✓ リストの乱用を改善（ボックス化）")
    print("✓ H2/H3に装飾を追加")

def convert_table(table_lines):
    """Markdown表をHTMLテーブルに変換"""
    if len(table_lines) < 2:
        return ''
    
    html = '        <table>\n'
    
    # ヘッダー行
    header = table_lines[0].strip('|').split('|')
    html += '            <thead>\n                <tr>\n'
    for cell in header:
        html += f'                    <th>{cell.strip()}</th>\n'
    html += '                </tr>\n            </thead>\n'
    
    # データ行（2行目は区切り線なのでスキップ）
    html += '            <tbody>\n'
    for row in table_lines[2:]:
        cells = row.strip('|').split('|')
        html += '                <tr>\n'
        for cell in cells:
            cell_text = cell.strip()
            cell_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', cell_text)
            html += f'                    <td>{cell_text}</td>\n'
        html += '                </tr>\n'
    html += '            </tbody>\n'
    
    html += '        </table>\n\n'
    return html

if __name__ == '__main__':
    md_file = r'c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\articles\2026\02\在留資格更新.md'
    html_file = r'c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\output\在留資格更新.html'
    
    convert_md_to_html_architecture_style(md_file, html_file)
