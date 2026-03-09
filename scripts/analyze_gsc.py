import pandas as pd
import os

# Configuration
GSC_FILE = "無題のスプレッドシート - SAS_2026-02-01_16-31-32.csv"
QUALITY_REPORT = "article_quality_report.csv"
OUTPUT_REPORT = "geo_seo_analysis_jan2026.txt"

def main():
    # 1. Load Data
    try:
        df_gsc = pd.read_csv(GSC_FILE)
        print(f"Loaded GSC Data: {len(df_gsc)} rows")
    except Exception as e:
        print(f"Error loading GSC data: {e}")
        return

    try:
        df_quality = pd.read_csv(QUALITY_REPORT)
        # Create a mapping from slug to filename/issues
        # Assumption: GSC URL '.../posts/slug' maps to 'slug.md'
        df_quality['slug'] = df_quality['filename'].str.replace('.md', '', regex=False)
        quality_map = df_quality.set_index('slug')[['filename', 'issue_count', 'issues']].to_dict('index')
        print(f"Loaded Quality Report: {len(df_quality)} rows")
    except Exception as e:
        print(f"Error loading Quality report: {e}")
        quality_map = {}

    # 2. Extract Slug from GSC URL for matching
    # URL format: .../posts/slug or just .../
    def extract_slug(url):
        if pd.isna(url): return ""
        parts = url.rstrip('/').split('/')
        if 'posts' in parts:
            return parts[-1]
        if 'download' in parts:
            return "download/" + parts[-1] 
        return "TOP_HOME" # homepage

    df_gsc['slug'] = df_gsc['Page'].apply(extract_slug)

    # 3. Aggregation by Page
    page_stats = df_gsc.groupby('slug').agg({
        'Clicks': 'sum',
        'Impressions': 'sum',
        'Position': 'mean',
        'Page': 'first' # keep one full url
    }).sort_values('Impressions', ascending=False)

    # 4. Aggregation by Query
    query_stats = df_gsc.groupby('Query').agg({
        'Clicks': 'sum',
        'Impressions': 'sum',
        'Position': 'mean'
    }).sort_values('Impressions', ascending=False)

    # 5. Analysis Logic
    
    report_lines = []
    report_lines.append(f"SEO Analysis Report (Jan 2026)\n{'='*30}\n")

    # Insight A: High Potential Queries (Imp > 50, Pos > 10)
    high_potential = query_stats[
        (query_stats['Impressions'] > 50) & 
        (query_stats['Position'] > 10)
    ]
    report_lines.append(f"## 🚀 High Potential Queries (High Imp, Low Rank)")
    report_lines.append(f"  Criteria: >50 Impressions, Rank >10.0\n")
    if not high_potential.empty:
        for q, row in high_potential.head(10).iterrows():
            report_lines.append(f"  - [{q}] Imp: {row['Impressions']}, Rank: {row['Position']:.1f}")
    else:
        report_lines.append("  (None found)")

    # Insight B: Top Performing Pages
    report_lines.append(f"\n## 🏆 Top Pages by Clicks")
    for slug, row in page_stats.head(5).iterrows():
        report_lines.append(f"  - {slug}: {row['Clicks']} Clicks, {row['Impressions']} Imp")

    # Insight C: Cross-Reference with Low Quality
    report_lines.append(f"\n## ⚠️ Low Quality Articles with Traffic")
    report_lines.append(f"  Checking articles flagged in quality report against GSC data...\n")
    
    matches_found = False
    for slug, row in page_stats.iterrows():
        if slug in quality_map:
            q_data = quality_map[slug]
            if q_data['issue_count'] > 0:
                matches_found = True
                report_lines.append(f"  - [Warning] {slug}")
                report_lines.append(f"    Issues: {q_data['issues']}")
                report_lines.append(f"    Performance: {row['Clicks']} Clicks, {row['Impressions']} Imp, Rank {row['Position']:.1f}")

    if not matches_found:
        report_lines.append("  No low quality articles found with significant traffic (Good news?).")

    # Insight D: Zero Traffic Low Quality Pages (The "Dead Weight")
    report_lines.append(f"\n## 🗑️ Dead Weight Candidates (Low Quality & No GSC Data)")
    report_lines.append(f"  These files exist locally, have quality issues, and appear in 0 GSC rows (Jan).\n")
    
    gsc_slugs = set(page_stats.index)
    dead_weight_count = 0
    for slug, q_data in quality_map.items():
        if slug not in gsc_slugs and q_data['issue_count'] > 0:
            if dead_weight_count < 10: # Limit output
                report_lines.append(f"  - {slug} ({q_data['issues']})")
            dead_weight_count += 1
            
    if dead_weight_count > 10:
        report_lines.append(f"  ... and {dead_weight_count - 10} more.")

    # Write Report
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"Report generated: {OUTPUT_REPORT}")
    print('\n'.join(report_lines)) # Print to stdout for agent to read

if __name__ == "__main__":
    main()
