# -*- coding: utf-8 -*-
"""
Markdown to HTML Converter for TCJ Articles
在留資格更新記事をHTML形式に変換
"""

import re

def convert_md_to_html(md_file, html_file):
    """MarkdownファイルをTCJスタイルのHTMLに変換"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # HTMLヘッダー
    html = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>【2026年最新】在留資格更新の完全ガイド｜手続き・必要書類・在留期間を伸ばす戦略 - TCJ外国人材Times</title>
    <meta name="description" content="在留資格更新の手続き、必要書類、審査期間を徹底解説。許可率99%の更新を成功させるポイントと、在留期間を3年→5年に伸ばす戦略も紹介。TCJが38年の実績で完全サポート。">
</head>
<body>
    <article class="rounded-[10px] bg-white shadow-xl overflow-hidden">
        <div class="entry-content">
'''
    
    # H1を抽出してタイトルに
    h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if h1_match:
        h1_text = h1_match.group(1)
        html += f'            <h1 class="font-notosansjp text-[28px] font-extrabold sm:text-4xl/normal md:text-[46px]">{h1_text}</h1>\n\n'
        content = content.replace(h1_match.group(0), '', 1)
    
    # 変換処理
    lines = content.split('\n')
    in_list = False
    in_table = False
    table_buffer = []
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if in_list:
                html += '            </ul>\n\n'
                in_list = False
            continue
        
        # H2
        if line.startswith('## '):
            if in_list:
                html += '            </ul>\n\n'
                in_list = False
            text = line[3:]
            html += f'            <h2 class="wp-block-heading">{text}</h2>\n\n'
        
        # H3
        elif line.startswith('### '):
            if in_list:
                html += '            </ul>\n\n'
                in_list = False
            text = line[4:]
            html += f'            <h3 class="wp-block-heading">{text}</h3>\n\n'
        
        # リスト
        elif line.startswith('- '):
            if not in_list:
                html += '            <ul class="list-disc space-y-3 pl-5">\n'
                in_list = True
            text = line[2:]
            # **bold**を<strong>に変換
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            html += f'                <li>{text}</li>\n'
        
        # 表の開始
        elif line.startswith('|') and not in_table:
            in_table = True
            table_buffer = [line]
        
        # 表の継続
        elif line.startswith('|') and in_table:
            table_buffer.append(line)
        
        # 表の終了
        elif in_table and not line.startswith('|'):
            html += convert_table(table_buffer)
            in_table = False
            table_buffer = []
            # 現在の行を処理
            if line.startswith('**'):
                text = line.replace('**', '')
                html += f'            <p><strong>{text}</strong></p>\n\n'
            else:
                html += f'            <p>{line}</p>\n\n'
        
        # 通常の段落
        else:
            if in_list:
                html += '            </ul>\n\n'
                in_list = False
            
            # **bold**を<strong>に変換
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            html += f'            <p>{text}</p>\n\n'
    
    # リストが開いたままの場合
    if in_list:
        html += '            </ul>\n\n'
    
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
    
    print(f"変換完了: {html_file}")

def convert_table(table_lines):
    """Markdown表をHTMLテーブルに変換"""
    if len(table_lines) < 2:
        return ''
    
    html = '            <table class="w-full border-collapse">\n'
    
    # ヘッダー行
    header = table_lines[0].strip('|').split('|')
    html += '                <thead>\n                    <tr>\n'
    for cell in header:
        html += f'                        <th class="border border-gray-300 bg-blue-100 px-4 py-2 text-left">{cell.strip()}</th>\n'
    html += '                    </tr>\n                </thead>\n'
    
    # データ行（2行目は区切り線なのでスキップ）
    html += '                <tbody>\n'
    for row in table_lines[2:]:
        cells = row.strip('|').split('|')
        html += '                    <tr>\n'
        for cell in cells:
            cell_text = cell.strip()
            # **bold**を<strong>に変換
            cell_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', cell_text)
            html += f'                        <td class="border border-gray-300 px-4 py-2">{cell_text}</td>\n'
        html += '                    </tr>\n'
    html += '                </tbody>\n'
    
    html += '            </table>\n\n'
    return html

if __name__ == '__main__':
    md_file = r'c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\articles\2026\02\在留資格更新.md'
    html_file = r'c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\output\在留資格更新.html'
    
    convert_md_to_html(md_file, html_file)
