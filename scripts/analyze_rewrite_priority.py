#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
リライト優先記事の分析スクリプト

サーチコンソールデータ、SE Rankingキーワードデータを中心に分析し、
本当にテコ入れが必要な記事を特定する。
"""

import os
import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# 設定
POSTS_DIR = "data/article_archives/posts"
GSC_CSV = "無題のスプレッドシート - SAS_2026-02-01_16-31-32.csv"
OUTPUT_FILE = "リライト優先記事レポート.md"

# 最近リライトされた記事（手動で管理）
RECENTLY_REWRITTEN = [
    'nursing_care_training.md',  # フィリピン人介護士（2026-02-01リライト）
]

class ArticleAnalyzer:
    def __init__(self):
        self.articles = {}  # {filename: {metadata}}
        self.gsc_data = {}  # {url: {clicks, impressions, queries}}
        
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
            
            # URLを推測（filename.md -> /posts/filename）
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
                'is_recently_rewritten': is_recently_rewritten
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
                    
                    # CTRとPositionは平均を取る（簡易的）
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
    

    
    def calculate_priority_score(self, article: Dict) -> Tuple[float, List[str]]:
        """
        記事の優先度スコアを計算
        
        Returns:
            (score, reasons): スコアと理由のリスト
        """
        score = 0
        reasons = []
        
        # 最近リライトされた記事は除外
        if article['is_recently_rewritten']:
            return -1000, [f"✅ 最近リライト済み（手動除外リスト）"]
        
        # GSCデータがある場合
        url = article['url']
        if url in self.gsc_data:
            gsc = self.gsc_data[url]
            impressions = gsc['impressions']
            clicks = gsc['clicks']
            
            # 表示回数が多いのにクリックが少ない（CTR問題）
            if impressions > 50 and clicks == 0:
                score += 50
                reasons.append(f"⚠️ 表示{impressions}回だがクリック0（CTR問題）")
            
            # 表示回数が多い（需要がある）
            if impressions > 100:
                score += 30
                reasons.append(f"📊 高需要（表示{impressions}回）")
            
            # 平均順位が低い
            if gsc['queries']:
                avg_position = sum(q['position'] for q in gsc['queries']) / len(gsc['queries'])
                if avg_position > 20:
                    score += 20
                    reasons.append(f"📉 平均順位が低い（{avg_position:.1f}位）")
        
        # 記事品質の問題
        if article['h2_count'] == 0:
            score += 40
            reasons.append("❌ H2見出しなし（構造的問題）")
        
        if article['char_count'] < 3000:
            score += 15
            reasons.append(f"📝 文字数不足（{article['char_count']}文字）")
        

        
        return score, reasons
    
    def generate_report(self):
        """分析レポートを生成"""
        # 優先度を計算
        priority_list = []
        recent_rewrites = []
        
        for filename, article in self.articles.items():
            score, reasons = self.calculate_priority_score(article)
            
            if score < 0:
                recent_rewrites.append({
                    'article': article,
                    'reasons': reasons
                })
            else:
                priority_list.append({
                    'article': article,
                    'score': score,
                    'reasons': reasons
                })
        
        # スコア順にソート
        priority_list.sort(key=lambda x: x['score'], reverse=True)
        
        # レポート生成
        report = []
        report.append("# リライト優先記事レポート")
        report.append(f"\n**生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**分析対象**: {len(self.articles)}記事\n")
        report.append("---\n")
        
        # 優先度の高い記事
        report.append("## 🔥 リライト優先記事（優先度順）\n")
        
        if priority_list:
            for i, item in enumerate(priority_list[:20], 1):  # 上位20件
                article = item['article']
                score = item['score']
                reasons = item['reasons']
                
                report.append(f"### {i}. `{article['filename']}` (スコア: {score})\n")
                report.append(f"- **URL**: {article['url']}")
                report.append(f"- **文字数**: {article['char_count']}文字")
                report.append(f"- **見出し**: H2={article['h2_count']}, H3={article['h3_count']}")
                
                # GSCデータ
                if article['url'] in self.gsc_data:
                    gsc = self.gsc_data[article['url']]
                    report.append(f"- **GSC**: クリック{gsc['clicks']}回, 表示{gsc['impressions']}回")
                    
                    # 主要クエリ（表示回数上位3件）
                    if gsc['queries']:
                        top_queries = sorted(gsc['queries'], key=lambda x: x['impressions'], reverse=True)[:3]
                        report.append(f"- **主要クエリ**:")
                        for q in top_queries:
                            report.append(f"  - 「{q['query']}」: {q['impressions']}回表示, {q['position']:.1f}位")
                
                report.append("\n**テコ入れ理由**:")
                for reason in reasons:
                    report.append(f"- {reason}")
                
                report.append("\n---\n")
        else:
            report.append("リライトが必要な記事はありません。\n")
        
        # 最近リライトされた記事（除外リスト）
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
        
        # ファイルに書き込み
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"\n✅ レポートを生成しました: {OUTPUT_FILE}")
        print(f"📊 リライト候補: {len(priority_list)}記事")
        print(f"✅ 最近リライト済み: {len(recent_rewrites)}記事")

def main():
    print("🔍 リライト優先記事の分析を開始します...\n")
    
    analyzer = ArticleAnalyzer()
    
    print("📁 記事ファイルを読み込み中...")
    analyzer.load_articles()
    print(f"   ✓ {len(analyzer.articles)}記事を読み込みました")
    
    print("\n📊 サーチコンソールデータを読み込み中...")
    analyzer.load_gsc_data()
    print(f"   ✓ {len(analyzer.gsc_data)}URLのデータを読み込みました")
    
    print("\n📝 レポートを生成中...")
    analyzer.generate_report()

if __name__ == "__main__":
    main()
