import urllib.request
import urllib.parse
import re

url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote('外免切替 とは')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')
urls = re.findall(r'class="result__url" href="(.*?)"', html)

for u in urls[:10]:
    original_url = urllib.parse.unquote(u)
    if not 'ad_domain' in original_url and original_url.startswith('//duckduckgo.com/l/?uddg='):
        actual = urllib.parse.unquote(original_url.split('uddg=')[1].split('&')[0])
        print(actual)
