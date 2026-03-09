import csv
import sys

# UTF-8出力設定
sys.stdout.reconfigure(encoding='utf-8')

csv_file = r"c:\Users\suzuki.takumi\Documents\blog_flows\Keyword Stats 2026-01-19 at 11_24_39.csv"

# CSVを読み込む（タブ区切り）
keywords = []
columns = None

try:
    with open(csv_file, 'r', encoding='utf-16') as f:
        lines = f.readlines()
        
        # ヘッダー行を探す
        header_line = None
        data_start = 0
        for i, line in enumerate(lines):
            if 'Keyword' in line and 'Avg. monthly searches' in line:
                header_line = line.strip()
                data_start = i + 1
                break
        
        if header_line:
            columns = header_line.split('\t')
            print(f"=== CSVカラム ===")
            print(columns)
            print(f"\n=== 総キーワード数 ===")
            
            # データ行を読み込む
            for line in lines[data_start:]:
                values = line.strip().split('\t')
                if len(values) >= len(columns) and values[0]:  # キーワードが存在する行のみ
                    row_dict = dict(zip(columns, values))
                    keywords.append(row_dict)
            
            print(f"{len(keywords)}キーワード\n")
        else:
            print("ヘッダー行が見つかりませんでした")
            sys.exit(1)
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 最初の5行を表示
print("=== データサンプル（最初の5行） ===\n")
for i, kw in enumerate(keywords[:5], 1):
    keyword_name = kw.get('Keyword', '')
    volume = kw.get('Avg. monthly searches', '0')
    print(f"{i}. {keyword_name}: {volume}")

# ボリューム順にソート
try:
    sorted_kw = sorted(keywords, key=lambda x: float(x.get('Avg. monthly searches', '0').replace(',', '').replace('-', '0') or '0'), reverse=True)
    
    print("\n=== 検索ボリューム TOP 50 ===\n")
    for i, kw in enumerate(sorted_kw[:50], 1):
        keyword_name = kw.get('Keyword', '')
        volume = kw.get('Avg. monthly searches', '0')
        competition = kw.get('Competition', '')
        print(f"{i}. {keyword_name}: {volume} (競合: {competition})")
        
    # ボリューム別集計
    print("\n=== ボリューム別集計 ===\n")
    vol_1000_plus = [k for k in keywords if float(k.get('Avg. monthly searches', '0').replace(',', '') or '0') >= 1000]
    vol_500_999 = [k for k in keywords if 500 <= float(k.get('Avg. monthly searches', '0').replace(',', '') or '0') < 1000]
    vol_100_499 = [k for k in keywords if 100 <= float(k.get('Avg. monthly searches', '0').replace(',', '') or '0') < 500]
    vol_under_100 = [k for k in keywords if 0 < float(k.get('Avg. monthly searches', '0').replace(',', '') or '0') < 100]
    
    print(f"1,000以上: {len(vol_1000_plus)}キーワード")
    print(f"500-999: {len(vol_500_999)}キーワード")
    print(f"100-499: {len(vol_100_499)}キーワード")
    print(f"100未満: {len(vol_under_100)}キーワード")
    
except Exception as e:
    print(f"ソートエラー: {e}")
    import traceback
    traceback.print_exc()

