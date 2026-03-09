import re

with open('output/foreign_license_conversion_v6.html', 'r', encoding='utf-8') as f:
    content = f.read()

# リード文の置換 (243字程度へ短縮)
old_lead_pattern = r"    <p>「海外でトラック運転手として十分な経験を持つ外国人を採用したいが.*?明確になるはずです。\n    </p>"
new_lead = """    <p>「海外で優秀な外国人ドライバーを採用しても、日本の免許に切り替えられず現場で使えないのでは…？」<br>
深刻なドライバー不足に悩む運送・物流企業において、即戦力となる「外免切替」での外国人材採用は不可欠です。しかし、2025年10月以降の厳格化ルールや複雑な条件を知らずに採用すると、来日後に配属できず大きな損失を生むリスクがあります。<br>
この記事では、人事担当者が知るべき外免切替の最新3大条件から、現場で安全に実務をこなせる実践的な日本語教育の手法まで完全網羅。採用前のミスマッチを防ぎ、最速で戦力化する具体策を200文字以下で解説します。</p>"""

content = re.sub(old_lead_pattern, new_lead, content, flags=re.DOTALL)

# FAQ部分のデザインをシンプルなdl/dt/ddから背景色・ボーダー等の枠線の改善を行う（v6のものを置換）
old_faq_pattern = r'<div class="faq-section"[\s\n]*style="margin-top:3em; padding:1.5em; background-color:white; border:2px solid #ddd; border-radius:8px;">'
new_faq = '<div class="faq-section" style="margin-top:3em; padding:2em; background-color:#f8f9fa; border-top:4px solid #0056b3; border-radius:4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'

content = re.sub(old_faq_pattern, new_faq, content)

with open('output/foreign_license_conversion_v7.html', 'w', encoding='utf-8') as f:
    f.write(content)
