import os
import datetime

target_dirs = [
    r'c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\output',
    r'c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\data\article_archives',
    r'C:\Users\suzuki.takumi\.gemini\antigravity\brain\ecef8f28-4d5b-41e4-8b82-5d4dd73c83a3'
]

files = []

for d in target_dirs:
    if os.path.exists(d):
        for root, dirs, filenames in os.walk(d):
            # Exclude unwanted directories
            if '.agent' in root or 'node_modules' in root or '.git' in root:
                continue
            
            for f in filenames:
                if f.lower().endswith(('.html', '.md')):
                    # Exclude system/config files based on keywords
                    if any(x in f for x in ['TCJ_COMPANY', 'seo_', 'task', 'walkthrough', 'phase', 'guide', 'rule', 'SKILL', 'log', 'readme', 'prompt', 'template']):
                        continue
                    
                    full_path = os.path.join(root, f)
                    
                    # Specific exclusion for the brain directory to avoid clutter, but keep the final article
                    if 'brain' in root and not f.startswith('recruitment_cost_rewrite_final'):
                         continue

                    try:
                        stats = os.stat(full_path)
                        files.append({
                            'path': full_path,
                            'mtime': stats.st_mtime,
                            'name': f
                        })
                    except Exception as e:
                        print(f"Error accessing {f}: {e}")

# Sort by modification time
files.sort(key=lambda x: x['mtime'])

print(f"{'Timestamp':<20} | {'File Name':<40} | {'Path'}")
print("-" * 100)
for f in files:
    dt = datetime.datetime.fromtimestamp(f['mtime']).strftime('%Y-%m-%d %H:%M:%S')
    print(f"{dt:<20} | {f['name']:<40} | {f['path']}")
