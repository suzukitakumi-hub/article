import csv
import sys

csv_file = r"c:\Users\suzuki.takumi\Documents\blog_flows\Keyword Stats 2026-01-19 at 11_24_39.csv"

keywords = []
with open(csv_file, 'r', encoding='utf-16') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        if row.get('Keyword'):
            kw = row['Keyword']
            vol = row.get('Avg. monthly searches', '0')
            comp = row.get('Competition', '')
            try:
                vol_num = float(vol.replace(',', '') if vol else '0')
            except:
                vol_num = 0
            keywords.append({'keyword': kw, 'volume': vol_num, 'competition': comp})

# ボリューム順にソート
sorted_kw = sorted(keywords, key=lambda x: x['volume'], reverse=True)

print("=== TCJ外国人材キーワード 検索ボリューム TOP 30 ===\n")
for i, kw in enumerate(sorted_kw[:30], 1):
    print(f"{i}. {kw['keyword']}: {int(kw['volume'])} (競合: {kw['competition']})")

print(f"\n=== ボリューム1,000以上の最重要キーワード ===\n")
high_vol = [k for k in sorted_kw if k['volume'] >= 1000]
for kw in high_vol:
    print(f"- {kw['keyword']}: {int(kw['volume'])}")
