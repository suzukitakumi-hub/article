# -*- coding: utf-8 -*-
"""
Markdown to HTML Converter for TCJ Articles (WordPress Style)
建築業記事のWordPressスタイルを適用
- H1は含めない（リード文から開始）
- インラインCSSを使用
- タイトルは個別に案内
"""

import re
import sys
import os

def convert_md_to_html_wordpress_style(md_file, html_file):
    """MarkdownファイルをTCJ WordPressスタイルのHTMLに変換"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # フロントマターを削除
    content = re.sub(r'^---[\s\S]*?---\s*', '', content)
    
    # H1(タイトル)を抽出して個別に案内
    h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1)
        content = content.replace(h1_match.group(0), '', 1)
        print(f"\n📌 タイトルはこれで設定してください: {title}\n")
    
    # HTML開始（WordPressスタイル - インラインCSS）
    html = '''<div
    style="font-family: 'acumin-pro', 'Noto Sans JP', sans-serif; font-size: 16px; line-height: 1.8; color: #424242; letter-spacing: 0.05em; background: #fff; padding: 20px; max-width: 900px; margin: 0 auto;">
'''
    
    # 変換処理
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # 空行・区切り線をスキップ
        if not line or line == '---':
            i += 1
            continue
        
        # H2
        if line.startswith('## '):
            text = line[3:]
            html += f'''    <h2
        style="font-size: 28px; font-weight: bold; line-height: 1.3; color: #424242; margin-top: 60px; margin-bottom: 24px; padding-bottom: 15px; border-bottom: 2px solid #102891;">
        {text}</h2>

'''
            i += 1
            continue
        
        # H3
        if line.startswith('### '):
            text = line[4:]
            html += f'''    <h3
        style="font-size: 22px; font-weight: bold; line-height: 1.3; color: #424242; margin-top: 46px; margin-bottom: 18px; border-left: 6px solid #102891; padding-left: 15px; background-color: transparent;">
        {text}</h3>
'''
            i += 1
            continue
        
        # H4
        if line.startswith('#### '):
            text = line[5:]
            html += f'''    <h4
        style="font-size: 18px; font-weight: bold; color: #102891; margin-bottom: 15px; border-left: 4px solid #102891; padding-left: 10px;">
        {text}</h4>
'''
            i += 1
            continue
        
        # 表の開始
        if line.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            html += convert_table(table_lines)
            continue
        
        # 引用ブロック (> で始まる行) - CTAボックスとして処理
        if line.startswith('> '):
            quote_lines = []
            while i < len(lines) and (lines[i].strip().startswith('> ') or lines[i].strip() == '>'):
                line_content = lines[i].strip()
                if line_content == '>':
                    # 空の引用行は改行として扱う
                    quote_lines.append('')
                else:
                    quote_lines.append(line_content[2:])
                i += 1
            
            # 空行を除去
            quote_lines = [line for line in quote_lines if line]
            
            # リンクを変換（ボタン化と通常リンクの区別）
            processed_lines = []
            for line in quote_lines:
                # リンクテキストから>>を削除
                line = re.sub(r'\[>>', r'[', line)
                
                # 行全体がリンクの場合はボタン化
                link_match = re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', line.strip())
                if link_match:
                    text = link_match.group(1)
                    url = link_match.group(2)
                    # 建築業記事のボタンスタイルを適用
                    button_html = f'<a href="{url}" style="display: inline-block; background-color: #102891; color: #fff; padding: 15px 40px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 18px; margin: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: all 0.3s ease;">{text}</a>'
                    processed_lines.append(button_html)
                else:
                    # 文中のリンクは通常のスタイル
                    line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #102891; text-decoration: underline;">\1</a>', line)
                    processed_lines.append(line)
            
            quote_text = '<br>'.join(processed_lines)
            # <br>タグがボタンの間に入るとレイアウトが崩れる可能性があるため、ボタンの前の<br>は削除などの調整が必要だが、
            # シンプルに段落分けするか、divで囲む手もある。
            # ここではシンプルに、全ての行をpタグやdivで処理せず、改行で繋ぐ既存ロジックを維持しつつ、ボタン自体にmarginを持たせる。
            # ただし、テキストとボタンの間隔を確保するため、<br>は有効。
            
            html += f'''    <div style="background-color: #f0f4f8; padding: 40px; border-radius: 10px; margin: 40px 0; text-align: center; border: 1px solid #e1e1e1;">
        <p style="margin-bottom: 24px; font-size: 18px; font-weight: bold; color: #102891;">外国人材採用でお悩みの方へ</p>
        <p style="margin-bottom: 24px;">{quote_text}</p>
    </div>

'''
            continue
        
        # 画像
        if line.startswith('!['):
            img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
            if img_match:
                alt_text = img_match.group(1)
                img_src = img_match.group(2)
                html += f'''    <img class="alignnone size-medium" src="{img_src}" alt="{alt_text}" style="max-width: 100%; height: auto; margin: 24px 0;" />

'''
            i += 1
            continue
        
        # リストの検出（ボックス化の判断）
        if line.startswith('- '):
            list_items = []
            j = i
            while j < len(lines) and lines[j].strip().startswith('- '):
                list_items.append(lines[j].strip()[2:])
                j += 1
            
            # リストが3項目以上ならボックス化
            if len(list_items) >= 3:
                html += '    <ul style="list-style: none; padding: 1em 1.5em; margin: 24px 0; border: 1px solid #102891;">\n'
                for item in list_items:
                    item_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                    html += f'        <li style="margin-bottom: 10px;">{item_html}</li>\n'
                html += '    </ul>\n\n'
                i = j
                continue
            else:
                # 短いリストは通常の段落として処理
                for item in list_items:
                    item_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                    html += f'    <p style="margin-bottom: 15px;">• {item_html}</p>\n'
                i = j
                continue
        
        # 通常の段落
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        # リンクを変換
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #102891; text-decoration: underline;">\1</a>', text)
        html += f'    <p style="margin-bottom: 24px;">{text}</p>\n'
        i += 1
    
    # HTML終了
    html += '</div>'
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"変換完了: {html_file}")
    print("✓ WordPressスタイル（インラインCSS）を適用")
    print("✓ H1は含めず、リード文から開始")
    print("✓ リストの乱用を改善（ボックス化）")
    print("✓ H2/H3/H4に装飾を追加")

def convert_table(table_lines):
    """Markdown表をHTMLテーブルに変換"""
    if len(table_lines) < 2:
        return ''
    
    html = '''    <table
        style="width: 100%; border-collapse: collapse; margin-bottom: 30px; border: 1px solid #e1e1e1; font-size: 15px;">
        <thead>
            <tr style="background-color: #f0f4f8;">
'''
    
    # ヘッダー行
    header = table_lines[0].strip('|').split('|')
    for cell in header:
        cell_text = cell.strip()
        cell_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', cell_text)
        html += f'                <th style="padding: 12px; border: 1px solid #e1e1e1; text-align: left;">{cell_text}</th>\n'
    html += '''            </tr>
        </thead>
        <tbody>
'''
    
    # データ行（2行目は区切り線なのでスキップ）
    for row in table_lines[2:]:
        cells = row.strip('|').split('|')
        html += '            <tr>\n'
        for cell in cells:
            cell_text = cell.strip()
            cell_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', cell_text)
            html += f'                <td style="padding: 12px; border: 1px solid #e1e1e1;">{cell_text}</td>\n'
        html += '            </tr>\n'
    
    html += '''        </tbody>
    </table>

'''
    return html

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法: python convert_md_to_html_wordpress.py <Markdownファイルパス>")
        sys.exit(1)
    
    md_file = sys.argv[1]
    
    # 出力ファイル名を生成
    base_name = os.path.splitext(os.path.basename(md_file))[0]
    html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', f'{base_name}.html')
    
    convert_md_to_html_wordpress_style(md_file, html_file)
