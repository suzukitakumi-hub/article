import os
import re
import glob

target_dir = r"c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\data\article_archives\posts"
output_file = "article_scan_results.txt"

def extract_info(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract Title from Frontmatter
    title_match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
    if not title_match:
        title_match = re.search(r'^title:\s*(.*?)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "No Title Found"

    # Extract H2 Headers
    headers = re.findall(r'^##\s+(.*?)$', content, re.MULTILINE)
    
    # Basic keyword check in content
    keywords = ["注意点", "リスク", "失敗", "トラブル", "デメリット", "課題"]
    found_keywords = [k for k in keywords if k in content]

    return {
        "filename": os.path.basename(filepath),
        "title": title,
        "headers": headers,
        "keywords": found_keywords
    }

results = []
for filepath in glob.glob(os.path.join(target_dir, "*.md")):
    results.append(extract_info(filepath))

# Write results to file
with open(output_file, 'w', encoding='utf-8') as f:
    for r in results:
        f.write(f"File: {r['filename']}\n")
        f.write(f"Title: {r['title']}\n")
        f.write(f"Keywords Found: {', '.join(r['keywords'])}\n")
        f.write("Headers:\n")
        for h in r['headers']:
            f.write(f"  - {h}\n")
        f.write("-" * 40 + "\n")

print(f"Scanned {len(results)} files. Results saved to {output_file}")
