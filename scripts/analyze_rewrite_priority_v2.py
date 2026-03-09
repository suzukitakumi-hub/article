#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全版リライト優先度分析スクリプト

全MDファイル、GSCデータ、KW順位データ、KWボリュームデータを統合し、
本当にROIが高い記事を特定する。
"""

import os
import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

# 設定
POSTS_DIR = "data/article_archives/posts"
GSC_CSV = "無題のスプレッドシート - SAS_2026-02-01_16-31-32.csv"
KEYWORDS_CSV = "data/keywords/tcj_positions_detailed_2026-01-25.csv"
OUTPUT_FILE = "完全版リライト優先度レポート.md"

# 最近リライトされた記事（手動で管理）
RECENTLY_REWRITTEN = [
    'nursing_care_training.md',  # フィリピン人介護士（2026-02-01リライト）
]

class ComprehensiveArticleAnalyzer:
    def __init__(self):
        self.articles = {}  # {filename: {metadata}}
        self.gsc_data = {}  # {url: {clicks, impressions, queries}}
        self.keyword_data = defaultdict(list)  # {url: [{keyword, volume, rank}]}
        self.keyword_volume_map = {}  # {keyword: volume}
        
    def load_articles(self):
        """全MDファイルのメタデータを読み込む"""
        posts_path = Path(POSTS_DIR)
        
        for md_file in posts_path.glob("*.md"):
            filename = md_file.name
            
            # 内容を読み込み
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                content = ""
            
            # 文字数
            char_count = len(content)
            
            # H2/H3の数
            h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
            h3_count = len(re.findall(r'^### ', content, re.MULTILINE))
            
            # URLを推測
            url_slug = filename.replace('.md', '')
            url = f"https://gaikoku-jinzai.tcj-education.com/posts/{url_slug}"
            
            # 最近リライトされたかチェック
            is_recently_rewritten = filename in RECENTLY_REWRITTEN
            
            self.articles[filename] = {
                'filename': filename,
                'url': url,
                'char_count': char_count,
                'h2_count': h2_count,
                'h3_count': h3_count,
                'is_recently_rewritten': is_recently_rewritten,
                'target_keywords': []  # 後で追加
            }
    
    def load_gsc_data(self):
        """サーチコンソールデータを読み込む"""
        try:
            with open(GSC_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    url = row['Page']
                    
                    if url not in self.gsc_data:
                        self.gsc_data[url] = {
                            'clicks': 0,
                            'impressions': 0,
                            'queries': []
                        }
                    
                    # データを集計
                    self.gsc_data[url]['clicks'] += int(row['Clicks'])
                    self.gsc_data[url]['impressions'] += int(row['Impressions'])
                    
                    ctr = float(row['CTR'].replace('%', ''))
                    position = float(row['Position'])
                    
                    self.gsc_data[url]['queries'].append({
                        'query': row['Query'],
                        'clicks': int(row['Clicks']),
                        'impressions': int(row['Impressions']),
                        'ctr': ctr,
                        'position': position
                    })
        except Exception as e:
            print(f"GSCデータ読み込みエラー: {e}")
    
    def load_keyword_data(self):
        """SE Rankingキーワードデータを完全に読み込む"""
        try:
            with open(KEYWORDS_CSV, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                # ヘッダーをスキップ（最初の2行）
                for i, line in enumerate(lines[2:], start=2):
                    if not line.strip():
                        continue
                    
                    # CSVパース（カンマ区切りだが、ダブルクォートで囲まれている場合を考慮）
                    parts = []
                    current = ""
                    in_quotes = False
                    
                    for char in line:
                        if char == '"':
                            in_quotes = not in_quotes
                        elif char == ',' and not in_quotes:
                            parts.append(current)
                            current = ""
                        else:
                            current += char
                    parts.append(current)  # 最後の要素
                    
                    if len(parts) < 8:
                        continue
                    
                    keyword = parts[0].strip()
                    
                    # 検索ボリューム（3列目、インデックス2）
                    volume_str = parts[2].strip()
                    try:
                        volume = int(volume_str) if volume_str.isdigit() else 0
                    except:
                        volume = 0
                    
                    # 2026-01-25のURL（7列目、インデックス6）
                    url = parts[6].strip() if len(parts) > 6 else ""
                    
                    # 2026-01-25の順位（5列目、インデックス4）
                    rank_str = parts[4].strip() if len(parts) > 4 else "-"
                    try:
                        if rank_str in ["-", "該当無し", "順番待ち", "GSCにデータ無し"]:
                            rank = 999
                        else:
                            rank = float(rank_str)
                    except:
                        rank = 999
                    
                    # キーワードボリュームマップに追加
                    if keyword:
                        self.keyword_volume_map[keyword] = volume
                    
                    # URLがある場合、記事に紐付け
                    if url and keyword and url.startswith("https://gaikoku-jinzai.tcj-education.com"):
                        self.keyword_data[url].append({
                            'keyword': keyword,
                            'volume': volume,
                            'rank': rank
                        })
            
            print(f"   ✓ {len(self.keyword_volume_map)}個のキーワードボリュームを読み込みました")
            print(f"   ✓ {len(self.keyword_data)}URLにキーワードを紐付けました")
            
        except Exception as e:
            print(f"キーワードデータ読み込みエラー: {e}")
            import traceback
            traceback.print_exc()
    
    def calculate_roi_score(self, article: Dict) -> Tuple[float, List[str], Dict]:
        """
        記事のROIスコアを計算
        
        Returns:
            (score, reasons, details): スコア、理由のリスト、詳細情報
        """
        score = 0
        reasons = []
        details = {
            'target_keywords': [],
            'total_volume': 0,
            'avg_rank': 0,
            'improvement_potential': 0
        }
        
        # 最近リライトされた記事は除外
        if article['is_recently_rewritten']:
            return -1000, ["✅ 最近リライト済み（手動除外リスト）"], details
        
        url = article['url']
        
        # キーワードデータがある場合
        if url in self.keyword_data:
            keywords = self.keyword_data[url]
            
            # ボリュームがあるKWのみを対象
            high_volume_kws = [kw for kw in keywords if kw['volume'] > 0]
            
            if high_volume_kws:
                total_volume = sum(kw['volume'] for kw in high_volume_kws)
                avg_rank = sum(kw['rank'] for kw in high_volume_kws) / len(high_volume_kws)
                
                details['target_keywords'] = high_volume_kws
                details['total_volume'] = total_volume
                details['avg_rank'] = avg_rank
                
                # スコアリング
                # 1. 検索ボリュームが高い
                if total_volume >= 300:
                    score += 100
                    reasons.append(f"🔥 超高ボリューム（合計{total_volume}）")
                elif total_volume >= 100:
                    score += 70
                    reasons.append(f"📊 高ボリューム（合計{total_volume}）")
                elif total_volume >= 50:
                    score += 40
                    reasons.append(f"📈 中ボリューム（合計{total_volume}）")
                
                # 2. 順位改善の余地がある
                if avg_rank > 20:
                    improvement = 50
                    score += improvement
                    reasons.append(f"📉 順位改善余地大（平均{avg_rank:.1f}位）")
                    details['improvement_potential'] = improvement
                elif avg_rank > 10:
                    improvement = 30
                    score += improvement
                    reasons.append(f"📊 順位改善余地あり（平均{avg_rank:.1f}位）")
                    details['improvement_potential'] = improvement
                
                # 3. 特定の高ボリュームKWで圏外
                for kw in high_volume_kws:
                    if kw['volume'] >= 300 and kw['rank'] > 20:
                        score += 50
                        reasons.append(f"⚡ Vol {kw['volume']}のKW「{kw['keyword']}」で圏外")
        
        # GSCデータがある場合
        if url in self.gsc_data:
            gsc = self.gsc_data[url]
            impressions = gsc['impressions']
            clicks = gsc['clicks']
            
            # 表示回数が多いのにクリックが少ない（CTR問題）
            if impressions > 100 and clicks == 0:
                score += 30
                reasons.append(f"⚠️ 表示{impressions}回だがクリック0（CTR問題）")
        
        # 記事品質の問題
        if article['h2_count'] == 0:
            score += 40
            reasons.append("❌ H2見出しなし（構造的問題）")
        
        if article['char_count'] < 3000:
            score += 15
            reasons.append(f"📝 文字数不足（{article['char_count']}文字）")
        
        return score, reasons, details
    
    def generate_report(self):
        """分析レポートを生成"""
        # ROIスコアを計算
        priority_list = []
        recent_rewrites = []
        
        for filename, article in self.articles.items():
            score, reasons, details = self.calculate_roi_score(article)
            
            if score < 0:
                recent_rewrites.append({
                    'article': article,
                    'reasons': reasons
                })
            else:
                priority_list.append({
                    'article': article,
                    'score': score,
                    'reasons': reasons,
                    'details': details
                })
        
        # スコア順にソート
        priority_list.sort(key=lambda x: x['score'], reverse=True)
        
        # レポート生成
        report = []
        report.append("# 完全版リライト優先度レポート")
        report.append(f"\n**生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**分析対象**: {len(self.articles)}記事\n")
        report.append(f"**キーワード数**: {len(self.keyword_volume_map)}個\n")
        report.append("---\n")
        
        # 優先度の高い記事
        report.append("## 🔥 リライト優先記事（ROI順）\n")
        
        if priority_list:
            for i, item in enumerate(priority_list[:20], 1):  # 上位20件
                article = item['article']
                score = item['score']
                reasons = item['reasons']
                details = item['details']
                
                report.append(f"### {i}. `{article['filename']}` (ROIスコア: {score})\n")
                report.append(f"- **URL**: {article['url']}")
                report.append(f"- **文字数**: {article['char_count']}文字")
                report.append(f"- **見出し**: H2={article['h2_count']}, H3={article['h3_count']}")
                
                # ターゲットKW
                if details['target_keywords']:
                    report.append(f"\n**ターゲットキーワード**:")
                    for kw in sorted(details['target_keywords'], key=lambda x: x['volume'], reverse=True)[:5]:
                        report.append(f"- 「{kw['keyword']}」: Vol {kw['volume']}, 順位 {kw['rank']:.1f}位")
                    
                    report.append(f"\n**合計検索ボリューム**: {details['total_volume']}")
                    report.append(f"**平均順位**: {details['avg_rank']:.1f}位")
                
                # GSCデータ
                if article['url'] in self.gsc_data:
                    gsc = self.gsc_data[article['url']]
                    report.append(f"\n**GSC実績**: クリック{gsc['clicks']}回, 表示{gsc['impressions']}回")
                
                report.append("\n**リライト理由**:")
                for reason in reasons:
                    report.append(f"- {reason}")
                
                report.append("\n---\n")
        else:
            report.append("リライトが必要な記事はありません。\n")
        
        # 最近リライトされた記事
        report.append(f"\n## ✅ 最近リライト済み（除外: {len(recent_rewrites)}記事）\n")
        
        if recent_rewrites:
            for item in recent_rewrites:
                article = item['article']
                report.append(f"- `{article['filename']}`")
        
        report.append("\n---\n")
        
        # 統計情報
        report.append("## 📊 統計情報\n")
        report.append(f"- **総記事数**: {len(self.articles)}")
        report.append(f"- **リライト候補**: {len(priority_list)}")
        report.append(f"- **最近リライト済み**: {len(recent_rewrites)}")
        report.append(f"- **GSCデータあり**: {len([a for a in self.articles.values() if a['url'] in self.gsc_data])}")
        report.append(f"- **KWデータあり**: {len([a for a in self.articles.values() if a['url'] in self.keyword_data])}")
        
        # ファイルに書き込み
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"\n✅ レポートを生成しました: {OUTPUT_FILE}")
        print(f"📊 リライト候補: {len(priority_list)}記事")
        print(f"✅ 最近リライト済み: {len(recent_rewrites)}記事")
        
        # TOP5を表示
        if priority_list:
            print("\n🔥 TOP5記事:")
            for i, item in enumerate(priority_list[:5], 1):
                article = item['article']
                score = item['score']
                details = item['details']
                print(f"{i}. {article['filename']} (スコア: {score}, Vol: {details['total_volume']})")

def main():
    print("🔍 完全版リライト優先度分析を開始します...\n")
    
    analyzer = ComprehensiveArticleAnalyzer()
    
    print("📁 記事ファイルを読み込み中...")
    analyzer.load_articles()
    print(f"   ✓ {len(analyzer.articles)}記事を読み込みました")
    
    print("\n📊 サーチコンソールデータを読み込み中...")
    analyzer.load_gsc_data()
    print(f"   ✓ {len(analyzer.gsc_data)}URLのデータを読み込みました")
    
    print("\n🔑 キーワードデータを読み込み中...")
    analyzer.load_keyword_data()
    
    print("\n📝 レポートを生成中...")
    analyzer.generate_report()

if __name__ == "__main__":
    main()
