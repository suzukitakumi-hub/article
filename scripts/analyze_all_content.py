import os
import glob
import re
from datetime import datetime

WP_DIR = "wp_markdown_export/posts/**/*.md"
ARCHIVE_DIR = "data/article_archives/posts/*.md"
OUTPUT_DIR = "output/*.html"
REPORT_PATH = "reports/content_audit_2026-02-24.md"

PILLARS = {
    "運送": ["運送", "ドライバー", "運転", "タクシー", "トラック", "バス", "外免切替"],
    "介護": ["介護", "ヘルパー", "施設", "ケア"],
    "特定技能2号": ["特定技能2号", "特定技能 2号", "2号移行"],
    "育成就労": ["育成就労", "育成就労制度"]
}

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def detect_pillars(text):
    found = []
    for pillar, kws in PILLARS.items():
        if any(kw in text for kw in kws):
            found.append(pillar)
    return found if found else ["その他"]

def parse_md(path, is_wp=False):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            title = ""
            if is_wp:
                match = re.search(r'^title:\s+"?(.*?)"?$', content, re.MULTILINE)
                if match:
                    title = match.group(1)
            else:
                match = re.search(r'^#\s+(.*)$', content, re.MULTILINE)
                if match:
                    title = match.group(1)
            if not title:
                title = os.path.basename(path)
            
            # Content length without frontmatter
            text_body = re.sub(r'(?s)^---.*?---', '', content) if is_wp else content
            length = len(text_body.strip())
            return {
                "file": os.path.basename(os.path.dirname(path)) if is_wp else os.path.basename(path),
                "title": title[:40],
                "length": length,
                "pillars": detect_pillars(content),
                "type": "WPエクスポート" if is_wp else "原稿アーカイブ",
                "date": datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y/%m/%d')
            }
    except Exception as e:
        return None

def parse_html(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            title = match.group(1).strip() if match else os.path.basename(path)
            text_body = clean_html(content)
            return {
                "file": os.path.basename(path),
                "title": title[:40],
                "length": len(text_body),
                "pillars": detect_pillars(text_body),
                "type": "HTML出力",
                "date": datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y/%m/%d')
            }
    except Exception as e:
        return None

def main():
    articles = []
    
    # 1. WP Export
    for p in glob.glob(WP_DIR, recursive=True):
        res = parse_md(p, is_wp=True)
        if res: articles.append(res)
            
    # 2. Archive MD
    # for p in glob.glob(ARCHIVE_DIR):
    #     res = parse_md(p)
    #     if res: articles.append(res)
        
    # 3. Output HTML
    for p in glob.glob(OUTPUT_DIR):
        res = parse_html(p)
        if res: articles.append(res)

    print(f"Total articles analyzed: {len(articles)}")
    
    # Identify Thin content in Pillars
    thin_articles = sorted([a for a in articles if a['length'] < 3000 and "その他" not in a['pillars']], key=lambda x: x['length'])
    
    # Pillar coverage count
    pillar_counts = {k: 0 for k in PILLARS.keys()}
    for a in articles:
        for p in a['pillars']:
            if p in pillar_counts: pillar_counts[p] += 1

    report = f"# 全記事オーディットと優先順位再構築レポート\n\n"
    report += f"**分析日時:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    report += f"**総記事数:** {len(articles)}件 (WP: {len([a for a in articles if a['type']=='WPエクスポート'])}, HTML: {len([a for a in articles if a['type']=='HTML出力'])})\n\n"
    
    report += "## メディア3本柱のカバレッジ\n"
    for k, v in pillar_counts.items():
        report += f"- **{k}**: {v}記事\n"
    report += "\n"
    
    report += "## 🚨 スカスカな記事（リライト最優先対象・文字数順）\n"
    report += "| 文字数 | テーマ | タイトル | ファイル |\n"
    report += "|---|---|---|---|\n"
    for a in thin_articles[:20]:  # Top 20 thin
        pillars = ",".join(a['pillars'])
        report += f"| {a['length']} | {pillars} | {a['title']} | {a['file']} |\n"
        
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"Report generated: {REPORT_PATH}")

if __name__ == '__main__':
    main()
