import csv, re
from collections import defaultdict

# Meta広告データ
with open('TCJ_-_-_2023_02_05-_-2026_03_05.csv', 'r', encoding='utf-8-sig') as f:
    ads = list(csv.DictReader(f))

with open('オンラインセミナー企画 - テーマ予定.csv', 'r', encoding='utf-8-sig') as f:
    sem_raw = list(csv.reader(f))

with open('オンラインセミナー企画 - セミナー実績集計結果.csv', 'r', encoding='utf-8-sig') as f:
    res_raw = list(csv.reader(f))

# セミナーテーマ整理
seminars = []
for row in sem_raw[3:]:
    if len(row) < 11: continue
    m = re.search(r'(\d{2})/(\d{2})', row[1])
    if not m: continue
    seminars.append({
        'no': row[0], 'date': row[1],
        'date_code': m.group(1)+m.group(2),
        'status': row[3], 'theme': row[10],
        'category': row[4], 'sub_category': row[5]
    })
sem_by_no = {s['no']: s for s in seminars}
sem_by_code = {s['date_code']: s for s in seminars}

# 実績集計 Semカラム位置
sem_row = None
for row in res_raw:
    if 'Sem01' in row:
        sem_row = row
        break
sem_col_idx = {val: i for i, val in enumerate(sem_row) if re.match(r'Sem\d+', val)}

申込者数_row = None
有効リード_row = None
有効リード割合_row = None
for row in res_raw:
    if len(row) > 3 and row[3] == '申込者数':
        申込者数_row = row
    if len(row) > 7 and row[5] == '有効' and row[7] == '「zoho_企業リード管理」シート':
        有効リード_row = row
    if len(row) > 5 and row[5] == '有効リード割合':
        有効リード割合_row = row

def get_val(data_row, sem_no):
    if data_row is None: return None
    idx = sem_col_idx.get(sem_no)
    if idx is None or idx >= len(data_row): return None
    v = data_row[idx].strip()
    return v if v not in ('n/a', '-', '') else None

# 広告データ グループ化
ad_groups = defaultdict(list)
for ad in ads:
    name = ad['広告の名前']
    m = re.search(r'_(\d{4})_([AB])', name)
    if m:
        ad_groups[m.group(1)].append(ad)

def aggregate_ads(items):
    total_r=0; total_s=0.0; total_i=0; total_c=0
    ab = defaultdict(lambda: {'results':0,'spend':0.0,'impressions':0,'clicks':0})
    for item in items:
        name = item['広告の名前']
        r = int(item['結果']) if item['結果'] else 0
        s = float(item['消化金額 (JPY)']) if item['消化金額 (JPY)'] else 0.0
        imp = int(item['インプレッション']) if item['インプレッション'] else 0
        c = int(item['リンクのクリック']) if item['リンクのクリック'] else 0
        m = re.search(r'_([AB])$', name)
        if m:
            v = m.group(1)
            ab[v]['results'] += r
            ab[v]['spend'] += s
            ab[v]['impressions'] += imp
            ab[v]['clicks'] += c
        total_r += r; total_s += s; total_i += imp; total_c += c
    return {
        'total_results': total_r, 'total_spend': total_s,
        'cpa': total_s/total_r if total_r > 0 else None,
        'impressions': total_i,
        'ctr': (total_c/total_i*100) if total_i > 0 else 0,
        'ab': dict(ab)
    }

ad_to_sem = {
    '0522': '0522', '0625': '0626', '0709': '0710', '0806': '0807',
    '0910': '0911', '1002': '1002', '1015': '1016', '1023': '1023',
    '1028': '1028', '1106': '1106', '1111': '1111', '1113': '1113',
    '1118': '1118', '1120': '1120', '1125': '1125', '1127': '1127',
    '1202': '1202', '1204': '1204', '1211': '1211', '1216': '1216',
    '1219': '1219', '1223': '1223', '0106': '0106', '0108': '0108',
    '0113': '0113', '0115': '0115', '0120': '0120', '0122': '0122',
    '0127': '0127', '0212': '0212', '0217': '0217', '0219': '0219',
    '0224': '0224', '0226': '0226', '0310': '0310',
}
sem_no_to_adcode = {}
for ad_code, sem_code in ad_to_sem.items():
    sem = sem_by_code.get(sem_code)
    if sem:
        sem_no_to_adcode[sem['no']] = ad_code

sem_order = [f'Sem{i:02d}' for i in range(1, 39)]

# ============================
# 【3】A/Bテスト結果比較
# ============================
print("="*110)
print("【3】A/Bテスト結果の比較")
print("="*110)
print(f"{'No.':<7}{'日付':<12}{'A申込':>6}{'A消化':>10}{'A_CPA':>9}{'B申込':>6}{'B消化':>10}{'B_CPA':>9}{'結果':>8}  メモ")
print("-"*110)

a_win=0; b_win=0; tie=0
for sem_no in sem_order:
    sem = sem_by_no.get(sem_no)
    if not sem: continue
    ad_code = sem_no_to_adcode.get(sem_no)
    if not ad_code: continue
    stat = aggregate_ads(ad_groups[ad_code])
    ab = stat['ab']
    if 'A' not in ab or 'B' not in ab: continue

    a = ab['A']; b = ab['B']
    a_cpa = a['spend']/a['results'] if a['results'] > 0 else None
    b_cpa = b['spend']/b['results'] if b['results'] > 0 else None

    if a_cpa and b_cpa:
        if a_cpa < b_cpa: result = 'A優勢'; a_win += 1
        elif b_cpa < a_cpa: result = 'B優勢'; b_win += 1
        else: result = '引分'; tie += 1
    elif a['results'] > b['results']: result = 'A優勢'; a_win += 1
    elif b['results'] > a['results']: result = 'B優勢'; b_win += 1
    else: result = '引分'; tie += 1

    a_cpa_str = "{:,.0f}".format(a_cpa) if a_cpa else "N/A"
    b_cpa_str = "{:,.0f}".format(b_cpa) if b_cpa else "N/A"
    diff = ""
    if a_cpa and b_cpa:
        diff_pct = (b_cpa - a_cpa)/a_cpa * 100
        if result == 'A優勢':
            diff = "B比{:.0f}%高コスト".format(abs(diff_pct))
        else:
            diff = "A比{:.0f}%高コスト".format(abs(diff_pct))

    print(f"{sem_no:<7}{sem['date']:<12}{a['results']:>6}{a['spend']:>9,.0f}円 {a_cpa_str:>9}{b['results']:>6}{b['spend']:>9,.0f}円 {b_cpa_str:>9}{result:>8}  {diff}")

print("-"*110)
total_ab = a_win + b_win + tie
print(f"A勝利: {a_win}回 / B勝利: {b_win}回 / 引分: {tie}回（計{total_ab}回のA/Bテスト）")

# ============================
# 【4】総合突合表
# ============================
print()
print("="*150)
print("【4】総合突合表：テーマ × 広告実績 × 有効リード（開催済みのみ）")
print("="*150)
print(f"{'No.':<7}{'日付':<11}{'カテゴリ':<18}{'テーマ（短縮）':<40}{'Zoho申込':>8}{'広告申込':>8}{'消化金額':>10}{'CPA':>9}{'有効リード':>9}{'有効率':>7}")
print("-"*150)

total_zoho = 0; total_ad = 0; total_spend = 0.0; total_valid = 0
for sem_no in sem_order:
    sem = sem_by_no.get(sem_no)
    if not sem: continue
    if sem['status'] != '開催済み': continue

    ad_code = sem_no_to_adcode.get(sem_no)
    stat = aggregate_ads(ad_groups[ad_code]) if ad_code else None

    zoho = get_val(申込者数_row, sem_no)
    valid = get_val(有効リード_row, sem_no)
    valid_rate = get_val(有効リード割合_row, sem_no)

    zoho_n = int(zoho) if zoho and zoho.isdigit() else 0
    valid_n = int(valid) if valid and valid.isdigit() else 0
    valid_rate_s = valid_rate if valid_rate else '-'

    ad_r = stat['total_results'] if stat else 0
    ad_s = stat['total_spend'] if stat else 0.0
    cpa = stat['cpa'] if stat else None
    cpa_str = "{:,.0f}円".format(cpa) if cpa else "N/A"

    cat = (sem['category'] + ('/' + sem['sub_category'] if sem['sub_category'] else ''))[:18]
    theme_short = sem['theme'][:38] + '..' if len(sem['theme']) > 38 else sem['theme']

    print(f"{sem_no:<7}{sem['date']:<11}{cat:<19}{theme_short:<40}{zoho_n:>8}{ad_r:>8}{ad_s:>10,.0f}円 {cpa_str:>10}{valid_n:>9}{valid_rate_s:>7}")

    total_zoho += zoho_n
    total_ad += ad_r
    total_spend += ad_s
    total_valid += valid_n

print("-"*150)
total_cpa = total_spend / total_ad if total_ad > 0 else 0
total_valid_rate = (total_valid / total_zoho * 100) if total_zoho > 0 else 0
print(f"{'合計':<7}{'':11}{'':19}{'':40}{total_zoho:>8}{total_ad:>8}{total_spend:>10,.0f}円 {total_cpa:>9,.0f}円{total_valid:>9}{total_valid_rate:>6.1f}%")
