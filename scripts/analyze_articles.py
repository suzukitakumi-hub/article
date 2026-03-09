import os
import re
import csv
import glob
from datetime import datetime

# Configuration
SOURCE_DIR = r"data/article_archives/posts"
OUTPUT_FILE = "article_quality_report.csv"

def parse_frontmatter(content):
    """
    Simple regex-based frontmatter parser.
    Returns a dict of metadata and the remaining body content.
    """
    meta = {}
    body = content
    # Regex for YAML frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    
    if match:
        yaml_text = match.group(1)
        body = match.group(2)
        
        # Simple line-by-line parsing for key: value
        for line in yaml_text.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                meta[key.strip()] = val.strip().strip('"').strip("'")
    
    return meta, body

def analyze_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    meta, body = parse_frontmatter(content)
    
    # Metrics
    char_count = len(body.replace(" ", "").replace("\n", ""))
    
    # Heading counts
    h1_count = len(re.findall(r'^#\s', body, re.MULTILINE))
    h2_count = len(re.findall(r'^##\s', body, re.MULTILINE))
    h3_count = len(re.findall(r'^###\s', body, re.MULTILINE))
    
    # Date parsing
    date_str = meta.get('date', '')
    is_outdated = False
    try:
        if date_str:
            # Try parsing typical formats like '2023-01-01' or '2023-01-01 12:00:00'
            dt = datetime.fromisoformat(date_str.replace(" ", "T"))
            if dt.year < 2024:
                is_outdated = True
    except ValueError:
        pass # Keep false if parse fails

    # Quality Flags
    issues = []
    
    # Exclusions
    if 'sem' in os.path.basename(filepath) and char_count < 1000:
       return None # Skip webinar LPs from quality check if they are short (expected)

    if char_count < 1000:
        issues.append("Thin Content (<1000 chars)")
    if h2_count == 0:
        issues.append("No H2 Headings")
    if is_outdated:
        issues.append("Outdated (<2024)")
    if not meta.get('description'): # Assuming 'description' key exists in frontmatter
        pass # Description is often missing in WP exports unless Yoast was used, checking anyway
        # issues.append("No Meta Description") 

    return {
        'filename': os.path.basename(filepath),
        'title': meta.get('title', 'No Title'),
        'date': date_str,
        'char_count': char_count,
        'h2_count': h2_count,
        'h3_count': h3_count,
        'issues': "; ".join(issues),
        'issue_count': len(issues)
    }

def main():
    files = glob.glob(os.path.join(SOURCE_DIR, "*.md"))
    results = []
    
    print(f"Analyzing {len(files)} files in {SOURCE_DIR}...")
    
    for file in files:
        data = analyze_file(file)
        if data:
            results.append(data)
            
    # Sort by issue count (descending), then character count (ascending)
    results.sort(key=lambda x: (x['issue_count'], -x['char_count']), reverse=True)
    
    # Write CSV
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['filename', 'title', 'date', 'char_count', 'h2_count', 'h3_count', 'issue_count', 'issues']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in results:
            writer.writerow(row)
            
    print(f"Analysis complete. Report saved to {OUTPUT_FILE}")

    # Print top 5 worst articles to stdout for quick view
    print("\n--- Top 5 Candidates for Improvement ---")
    for row in results[:5]:
        print(f"[{row['issue_count']} Issues] {row['filename']} ({row['char_count']} chars) - {row['issues']}")

if __name__ == "__main__":
    main()
