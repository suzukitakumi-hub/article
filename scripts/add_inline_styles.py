import re

with open('output/foreign_license_conversion_v5.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<div class="wrapper">', '<div class="wrapper" style="font-family: \'acumin-pro\', \'Noto Sans JP\', sans-serif; line-height: 1.8; max-width: 900px; margin: 0 auto; color: #333;">')
content = re.sub(r'<h2>', '<h2 style="font-size: 24px; font-weight: bold; border-bottom: 2px solid #0056b3; padding-bottom: 8px; margin-top: 2em; margin-bottom: 1em;">', content)
content = re.sub(r'<h3>', '<h3 style="font-size: 20px; font-weight: bold; padding-left: 10px; border-left: 4px solid #0056b3; margin-top: 1.5em; margin-bottom: 1em;">', content)
content = re.sub(r'<h4>', '<h4 style="font-size: 18px; font-weight: bold; margin-top: 1.5em; margin-bottom: 1em; color: #004085;">', content)

with open('output/foreign_license_conversion_v6.html', 'w', encoding='utf-8') as f:
    f.write(content)
