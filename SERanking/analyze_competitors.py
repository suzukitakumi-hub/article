import pandas as pd

def df_to_markdown(df):
    """Convert DataFrame to Markdown table without tabulate dependency"""
    lines = []
    # Header
    lines.append('| ' + ' | '.join(str(col) for col in df.columns) + ' |')
    # Separator
    lines.append('|' + '|'.join(['---' for _ in df.columns]) + '|')
    # Rows
    for _, row in df.iterrows():
        lines.append('| ' + ' | '.join(str(val) for val in row) + ' |')
    return '\n'.join(lines)

# Load CSV
df = pd.read_csv('tcj_competitors_overall_2026-02-16.csv', skiprows=1)

# Competitor mapping
competitors = {
    'https://onodera-user-run.co.jp/': '小野寺',
    'https://www.glory-of-bridge.com/': 'グローリーブリッジ',
    'https://www.gtn.co.jp/tokuteiginou_support': 'GTN',
    'https://willof-work.co.jp/corp/service/': 'ウィルオブ',
    'https://persol-gw.co.jp/service/': 'パーソル',
    'https://www.orj.co.jp/business': 'ORJ',
    'https://kjtimes.jp/': 'KJタイムス'
}

output = []
output.append("# SE Ranking 競合分析レポート")
output.append(f"\n**分析日**: 2026-02-16")
output.append(f"**総KW数**: {len(df)}件")
output.append(f"**競合サイト数**: {len(competitors)}サイト\n")

output.append("---\n")
output.append("## 1. 競合サイト別ランクイン状況\n")

comp_stats = []
for comp_url, comp_name in competitors.items():
    ranked = df[df[comp_url].notna() & (df[comp_url] != '-') & (df[comp_url] != 'ND')]
    ranked_numeric = pd.to_numeric(ranked[comp_url], errors='coerce')
    
    total = len(ranked)
    top10 = len(ranked_numeric[ranked_numeric <= 10])
    top3 = len(ranked_numeric[ranked_numeric <= 3])
    
    comp_stats.append({
        '競合サイト': comp_name,
        '総ランクイン': total,
        'Top10入り': top10,
        'Top3入り': top3
    })

comp_df = pd.DataFrame(comp_stats).sort_values('総ランクイン', ascending=False)
output.append(df_to_markdown(comp_df))

output.append("\n---\n")
output.append("## 2. TCJ ランクイン状況\n")

tcj_ranked = df[df['tcj'].notna() & (df['tcj'] != '-') & (df['tcj'] != 'ND')]
tcj_numeric = pd.to_numeric(tcj_ranked['tcj'], errors='coerce')

output.append(f"- **総ランクイン数**: {len(tcj_ranked)}件")
output.append(f"- **Top10入り**: {len(tcj_numeric[tcj_numeric <= 10])}件")
output.append(f"- **Top3入り**: {len(tcj_numeric[tcj_numeric <= 3])}件\n")

output.append("### TCJがTop10に入っているKW\n")
top10 = tcj_ranked[tcj_numeric <= 10].copy()
top10['順位'] = pd.to_numeric(top10['tcj'], errors='coerce')
top10 = top10.sort_values('検索ボリューム', ascending=False)
output.append(df_to_markdown(top10[['キーワード', '検索ボリューム', '順位']]))

output.append("\n---\n")
output.append("## 3. キーワードギャップ分析\n")
output.append("**競合がTop10に入っているがTCJがランク外のKW**\n")

gap_keywords = []
for _, row in df.iterrows():
    tcj_rank = row['tcj']
    if tcj_rank == '-' or tcj_rank == 'ND' or pd.isna(tcj_rank):
        comp_ranks = []
        for comp_url, comp_name in competitors.items():
            rank = row[comp_url]
            if rank not in ['-', 'ND'] and not pd.isna(rank):
                try:
                    rank_num = int(rank)
                    if rank_num <= 10:
                        comp_ranks.append((comp_name, rank_num))
                except:
                    pass
        
        if comp_ranks:
            gap_keywords.append({
                'キーワード': row['キーワード'],
                '検索ボリューム': row['検索ボリューム'],
                '競合性': row['競合性'],
                '競合Top10': ', '.join([f"{name}({rank}位)" for name, rank in sorted(comp_ranks, key=lambda x: x[1])])
            })

gap_df = pd.DataFrame(gap_keywords)
if len(gap_df) > 0:
    gap_df = gap_df.sort_values('検索ボリューム', ascending=False)
    
    output.append("### ボリューム100以上のギャップKW\n")
    high_vol_gap = gap_df[gap_df['検索ボリューム'] >= 100]
    if len(high_vol_gap) > 0:
        output.append(df_to_markdown(high_vol_gap.head(30)))
    else:
        output.append("該当なし")
    
    output.append("\n### ボリューム10-99のギャップKW（上位30件）\n")
    mid_vol_gap = gap_df[(gap_df['検索ボリューム'] >= 10) & (gap_df['検索ボリューム'] < 100)]
    if len(mid_vol_gap) > 0:
        output.append(df_to_markdown(mid_vol_gap.head(30)))
    else:
        output.append("該当なし")

output.append("\n---\n")
output.append("## 4. 推奨アクション\n")
output.append("### 優先的に狙うべきKW（ギャップKWから抽出）\n")

if len(gap_df) > 0:
    priority = gap_df[
        (gap_df['検索ボリューム'] >= 100) & 
        (gap_df['競合性'] < 0.5)
    ].head(15)
    
    if len(priority) > 0:
        output.append("**条件**: ボリューム100以上 & 競合性0.5未満\n")
        output.append(df_to_markdown(priority[['キーワード', '検索ボリューム', '競合性', '競合Top10']]))
    else:
        output.append("該当なし（条件を緩和して再検討）")

# Write to file
with open('competitor_analysis_report.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("レポート作成完了: competitor_analysis_report.md")
