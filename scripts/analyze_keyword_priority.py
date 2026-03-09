"""
キーワード優先度分析スクリプト

SE Rankingデータ、競合KWリスト、既存記事を総合分析し、
次に書くべきキーワードの優先度リストを生成する。

使用方法:
    python scripts/analyze_keyword_priority.py
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import re
from pathlib import Path

# 設定
BASE_DIR = Path(__file__).parent.parent
SERANKING_DIR = BASE_DIR / "SERanking"
KEYWORD_DATA_DIR = BASE_DIR / "data" / "keyword_data"
EXISTING_ARTICLES_DIR = BASE_DIR / "data" / "existing_articles"
ARTICLE_ARCHIVES_DIR = BASE_DIR / "data" / "article_archives" / "posts"
OUTPUT_DIR = BASE_DIR / "output"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# 日付
TODAY = datetime.now().strftime("%Y-%m-%d")
RECENT_DAYS = 30  # 最近30日以内の記事を除外

def load_seranking_positions():
    """SE Ranking順位データを読み込み"""
    positions_file = SERANKING_DIR / "tcj_positions_detailed_2026-02-12.csv"
    if not positions_file.exists():
        print(f"警告: {positions_file} が見つかりません")
        return pd.DataFrame()
    
    # エンコーディングを試行
    for encoding in ['utf-8', 'shift-jis', 'cp932']:
        try:
            df = pd.read_csv(positions_file, encoding=encoding)
            print(f"SE Ranking順位データ読み込み成功: {len(df)}件")
            return df
        except:
            continue
    
    print(f"エラー: {positions_file} の読み込みに失敗")
    return pd.DataFrame()

def load_competitor_keywords():
    """競合KWリストを読み込み"""
    competitor_file = SERANKING_DIR / "tcj_competitors_overall_2026-02-16.csv"
    if not competitor_file.exists():
        print(f"警告: {competitor_file} が見つかりません")
        return pd.DataFrame()
    
    df = pd.read_csv(competitor_file, skiprows=1, encoding='utf-8')
    print(f"競合KWリスト読み込み成功: {len(df)}件")
    return df

def load_existing_articles():
    """既存記事リストを読み込み"""
    existing_keywords = set()
    recent_keywords = set()
    cutoff_date = datetime.now() - timedelta(days=RECENT_DAYS)
    
    # ARTICLE_HISTORY.mdから読み込み
    article_history = EXISTING_ARTICLES_DIR / "ARTICLE_HISTORY.md"
    if article_history.exists():
        with open(article_history, 'r', encoding='utf-8') as f:
            content = f.read()
            # ファイル名とタイトルからKWを抽出
            for line in content.split('\n'):
                # HTMLファイル名
                if '.html' in line:
                    # 日本語ファイル名を抽出
                    match = re.search(r'([^\\/]+)\.html', line)
                    if match:
                        filename = match.group(1)
                        existing_keywords.add(filename.lower())
                        # スペース区切りも追加
                        existing_keywords.add(filename.replace('_', ' ').lower())
    
    # outputフォルダのHTMLファイルから読み込み
    if OUTPUT_DIR.exists():
        for html_file in OUTPUT_DIR.glob("*.html"):
            file_date = datetime.fromtimestamp(html_file.stat().st_mtime)
            filename_kw = html_file.stem.lower()
            existing_keywords.add(filename_kw)
            existing_keywords.add(filename_kw.replace('_', ' '))
            
            # HTMLファイルの中身からタイトルを抽出
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    # <title>タグから抽出
                    title_match = re.search(r'<title>([^<]+)</title>', html_content)
                    if title_match:
                        title = title_match.group(1)
                        # タイトルから主要KWを抽出
                        for kw in ['在留資格', '更新', '特定技能', '介護', '外国人', '採用', '注意点', '手続き']:
                            if kw in title:
                                existing_keywords.add(kw.lower())
            except:
                pass
            
            if file_date > cutoff_date:
                recent_keywords.add(filename_kw)
                recent_keywords.add(filename_kw.replace('_', ' '))
    
    # article_archivesフォルダのMDファイルから読み込み
    if ARTICLE_ARCHIVES_DIR.exists():
        for md_file in ARTICLE_ARCHIVES_DIR.glob("*.md"):
            filename_kw = md_file.stem.lower()
            existing_keywords.add(filename_kw)
            existing_keywords.add(filename_kw.replace('_', ' '))
    
    print(f"既存記事: {len(existing_keywords)}件, 最近30日: {len(recent_keywords)}件")
    return existing_keywords, recent_keywords

def extract_keyword_from_text(text):
    """テキストからキーワードを抽出（簡易版）"""
    # スペース区切りのKWを正規化
    normalized = text.lower().replace(' ', '_').replace('　', '_')
    return normalized

def analyze_keyword_priority(competitor_df, existing_kw, recent_kw):
    """キーワード優先度を分析"""
    priority_list = []
    
    for _, row in competitor_df.iterrows():
        keyword = row['キーワード']
        volume = row['検索ボリューム']
        competition = row['競合性']
        tcj_rank = row['tcj']
        
        # 競合がTop10に入っているか確認
        competitors = ['https://onodera-user-run.co.jp/', 'https://www.glory-of-bridge.com/',
                      'https://www.gtn.co.jp/tokuteiginou_support', 'https://willof-work.co.jp/corp/service/',
                      'https://persol-gw.co.jp/service/', 'https://www.orj.co.jp/business', 'https://kjtimes.jp/']
        
        comp_in_top10 = []
        for comp in competitors:
            if comp in row.index:
                rank = row[comp]
                if rank not in ['-', 'ND'] and not pd.isna(rank):
                    try:
                        if int(rank) <= 10:
                            comp_in_top10.append(comp)
                    except:
                        pass
        
        if len(comp_in_top10) > 0:
            is_tcj_unranked = tcj_rank in ['-', 'ND'] or pd.isna(tcj_rank)
            try:
                tcj_rank_val = 999 if is_tcj_unranked else int(tcj_rank)
            except:
                tcj_rank_val = 999

            # 既存記事チェック（改善版）
            kw_normalized = keyword.lower().replace(' ', '').replace('　', '')
            is_existing = False
            is_recent = False
            
            # キーワードの各部分が既存記事に含まれているかチェック
            kw_parts = keyword.split()
            for existing in existing_kw:
                existing_normalized = existing.lower().replace(' ', '').replace('　', '')
                if kw_normalized in existing_normalized or existing_normalized in kw_normalized:
                    is_existing = True
                    break
                if len(kw_parts) >= 2:
                    if all(part in existing for part in kw_parts):
                        is_existing = True
                        break
            
            for recent in recent_kw:
                recent_normalized = recent.lower().replace(' ', '').replace('　', '')
                if kw_normalized in recent_normalized or recent_normalized in kw_normalized:
                    is_recent = True
                    break

            # 区分判定
            if is_recent:
                category = "最近作成"
                reason_prefix = "直近30日以内に作成済"
            elif is_existing or (not is_tcj_unranked and tcj_rank_val > 10):
                category = "リライト"
                reason_prefix = "既存記事あり/順位改善"
            elif not is_existing and is_tcj_unranked:
                category = "新規作成"
                reason_prefix = "未作成"
            else:
                category = "上位ランクイン"
                reason_prefix = "既に上位"

            if category == "上位ランクイン":
                continue

            # スコアリング
            volume_score = volume if volume > 0 else 0
            competition_score = (1 - competition) * 100 if competition > 0 else 50
            gap_score = len(comp_in_top10) * 10
            
            # リライトや最近作成の場合のスコア調整
            if category == "最近作成":
                total_score = (volume_score + competition_score + gap_score) * 0.1
            elif category == "リライト":
                total_score = (volume_score + competition_score + gap_score) * 0.8
            else:
                total_score = volume_score + competition_score + gap_score
                
            priority_list.append({
                '区分': category,
                'キーワード': keyword,
                'ボリューム': volume,
                '競合性': competition,
                '競合Top10数': len(comp_in_top10),
                'スコア': total_score,
                '理由': f"{reason_prefix} (競合{len(comp_in_top10)}社Top10入)"
            })
    
    # スコア順にソート
    priority_df = pd.DataFrame(priority_list).sort_values('スコア', ascending=False)
    return priority_df

def generate_priority_report(priority_df, output_file):
    """優先度レポートを生成"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# キーワード優先度リスト\n\n")
        f.write(f"**生成日**: {TODAY}\n")
        f.write(f"**分析対象**: SE Ranking競合KWリスト\n")
        f.write(f"**分析条件**: 新規作成・リライト・最近作成（抽出してカテゴリ分け）\n\n")
        f.write("---\n\n")
        f.write("## 優先度Top20\n\n")
        
        if len(priority_df) == 0:
            f.write("該当するキーワードがありません。\n")
            return
        
        f.write("| 区分 | 順位 | キーワード | ボリューム | 競合性 | 競合Top10 | スコア | 理由 |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        
        for idx, row in priority_df.head(20).iterrows():
            f.write(f"| {row['区分']} | {idx+1} | {row['キーワード']} | {row['ボリューム']} | {row['競合性']:.2f} | {row['競合Top10数']}社 | {row['スコア']:.0f} | {row['理由']} |\n")
        
        f.write("\n---\n\n")
        f.write("## 推奨アクション\n\n")
        f.write("新規作成およびリライトの上位3〜5件のキーワードから記事作成・改善を開始してください。\n\n")
        
        if len(priority_df) > 0:
            top3 = priority_df.head(3)
            f.write("### 今すぐ着手すべきKW（Top3）\n\n")
            for idx, row in top3.iterrows():
                f.write(f"**{idx+1}. [{row['区分']}] {row['キーワード']}** (ボリューム: {row['ボリューム']})\n")
                f.write(f"- 競合性: {row['競合性']:.2f}\n")
                f.write(f"- {row['理由']}\n\n")

def main():
    print("=" * 80)
    print("キーワード優先度分析スクリプト")
    print("=" * 80)
    
    # データ読み込み
    print("\n[1/4] データ読み込み中...")
    competitor_df = load_competitor_keywords()
    existing_kw, recent_kw = load_existing_articles()
    
    if competitor_df.empty:
        print("エラー: 競合KWリストが読み込めませんでした")
        return
    
    # 優先度分析
    print("\n[2/4] 優先度分析中...")
    priority_df = analyze_keyword_priority(competitor_df, existing_kw, recent_kw)
    
    # レポート生成
    print("\n[3/4] レポート生成中...")
    output_file = REPORTS_DIR / f"keyword_priority_{TODAY}.md"
    generate_priority_report(priority_df, output_file)
    
    # ログ出力
    print("\n[4/4] ログ出力中...")
    log_file = REPORTS_DIR / "keyword_priority_analysis_log.txt"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 分析完了: {len(priority_df)}件のKW候補\n")
    
    print("\n" + "=" * 80)
    print(f"✅ 完了: {output_file}")
    print(f"📊 候補KW数: {len(priority_df)}件")
    if len(priority_df) > 0:
        print(f"🎯 Top1: {priority_df.iloc[0]['キーワード']} (ボリューム: {priority_df.iloc[0]['ボリューム']})")
    print("=" * 80)

if __name__ == "__main__":
    main()
