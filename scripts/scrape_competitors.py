#!/usr/bin/env python3
"""
scrape_competitors.py - 競合記事の本文をフル取得するスクリプト

使い方:
  # URLを直接指定（複数可）
  python scripts/scrape_competitors.py https://example.com/article1 https://example.com/article2

  # URLリストファイルから読み込み（1行1URL）
  python scripts/scrape_competitors.py --file data/competitor/urls.txt

  # キーワードでDuckDuckGo検索→上位N件を自動取得
  python scripts/scrape_competitors.py --keyword "外国人採用 課題" --top 5

  # 組み合わせも可
  python scripts/scrape_competitors.py --keyword "外国人採用 課題" --top 5 --output data/competitor/gaijin_adoption

出力:
  data/competitor/YYYYMMDD_HHMM_01_slug.md  ... 各記事の全文
  data/competitor/YYYYMMDD_HHMM_summary.md  ... 全記事の見出し構造サマリー（Claude読み込み用）
"""

import sys
import os
import re
import time
import argparse
import json
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
import trafilatura
from trafilatura.settings import use_config

# デフォルト出力先
DEFAULT_OUTPUT_DIR = Path("data/competitor")

# 自社ドメイン（検索結果から除外）
OWN_DOMAIN = "tcj-education.com"

# リクエストヘッダー
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def fetch_full_content(url: str, timeout: int = 20) -> dict:
    """
    URLから本文・見出し・メタ情報をフル取得する。
    trafilaturaで本文抽出 → 失敗時はBeautifulSoupでフォールバック。
    """
    result = {
        "url": url,
        "title": "",
        "meta_description": "",
        "headings": [],
        "body_text": "",
        "word_count": 0,
        "error": None,
        "method": "trafilatura",
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        html = resp.text

        # --- BeautifulSoupでメタ情報と見出し構造を取得 ---
        soup = BeautifulSoup(html, "lxml")

        # タイトル
        title_tag = soup.find("title")
        result["title"] = title_tag.get_text(strip=True) if title_tag else ""

        # og:title の方が正確な場合があるので優先
        og_title = soup.find("meta", attrs={"property": "og:title"})
        if og_title and og_title.get("content"):
            result["title"] = og_title["content"]

        # メタディスクリプション
        meta_desc = (
            soup.find("meta", attrs={"name": "description"})
            or soup.find("meta", attrs={"property": "og:description"})
        )
        if meta_desc:
            result["meta_description"] = meta_desc.get("content", "")

        # 見出し構造（h1〜h4）
        headings = []
        for tag in soup.find_all(["h1", "h2", "h3", "h4"]):
            text = tag.get_text(separator=" ", strip=True)
            if text and len(text) > 1:
                headings.append({"level": tag.name, "text": text})
        result["headings"] = headings

        # --- trafilaturaで本文抽出（メイン） ---
        config = use_config()
        config.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")
        body = trafilatura.extract(
            html,
            url=url,
            include_tables=True,
            include_links=False,
            include_images=False,
            no_fallback=False,
            favor_recall=True,   # 取りこぼし防止（精度より網羅性優先）
            config=config,
        )

        if body and len(body) > 200:
            result["body_text"] = body
            result["word_count"] = len(body)
        else:
            # フォールバック: BeautifulSoupで main / article タグを探す
            result["method"] = "beautifulsoup_fallback"
            main_content = (
                soup.find("main")
                or soup.find("article")
                or soup.find(id=re.compile(r"(content|main|post|entry)", re.I))
                or soup.find("div", class_=re.compile(r"(content|main|post|entry|article)", re.I))
            )
            if main_content:
                for junk in main_content.find_all(
                    ["script", "style", "nav", "aside", "footer",
                     "header", "form", "iframe", "button"]
                ):
                    junk.decompose()
                body = main_content.get_text(separator="\n", strip=True)
                # 連続空行を1行に圧縮
                body = re.sub(r"\n{3,}", "\n\n", body)
                result["body_text"] = body
                result["word_count"] = len(body)
            else:
                result["error"] = "本文領域を特定できませんでした"

    except requests.exceptions.Timeout:
        result["error"] = f"タイムアウト（{timeout}秒）"
    except requests.exceptions.HTTPError as e:
        result["error"] = f"HTTPエラー: {e.response.status_code}"
    except Exception as e:
        result["error"] = f"取得エラー: {type(e).__name__}: {e}"

    return result


def to_markdown(data: dict) -> str:
    """取得結果をMarkdown形式に変換（Claude読み込み用）"""
    lines = []
    lines.append(f"# {data['title']}\n")
    lines.append(f"**URL:** {data['url']}  ")
    if data["meta_description"]:
        lines.append(f"**メタディスクリプション:** {data['meta_description']}  ")
    lines.append(f"**本文文字数:** {data['word_count']:,}文字  ")
    lines.append(f"**取得方法:** {data['method']}  ")
    if data["error"]:
        lines.append(f"**⚠️ エラー:** {data['error']}  ")

    lines.append("\n---\n")

    # 見出し構造
    lines.append("## 📋 見出し構造\n")
    for h in data["headings"]:
        depth = int(h["level"][1]) - 1
        prefix = "  " * depth + "- "
        tag = f"[{h['level'].upper()}]"
        lines.append(f"{prefix}{tag} {h['text']}")

    lines.append("\n---\n")

    # 本文
    lines.append("## 📄 本文（フル）\n")
    lines.append(data["body_text"] if data["body_text"] else "（本文取得失敗）")

    return "\n".join(lines)


def search_top_urls(keyword: str, top_n: int = 5) -> list[str]:
    """DuckDuckGoでキーワード検索し、上位URLを返す（自社ドメイン除外）"""
    try:
        from duckduckgo_search import DDGS
        print(f"  🔍 DuckDuckGo検索: {keyword}")
        with DDGS() as ddgs:
            results = list(ddgs.text(keyword, region="jp-jp", max_results=top_n + 5))
        urls = [
            r["href"]
            for r in results
            if OWN_DOMAIN not in r.get("href", "")
            and r.get("href", "").startswith("http")
        ]
        urls = list(dict.fromkeys(urls))[:top_n]  # 重複除去＋上位N件
        print(f"  → {len(urls)}件取得")
        for i, u in enumerate(urls, 1):
            print(f"     {i}. {u}")
        return urls
    except ImportError:
        print("⚠️ duckduckgo_search が未インストールです: pip install duckduckgo-search")
        return []
    except Exception as e:
        print(f"⚠️ 検索エラー: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(
        description="競合記事の本文をフル取得するスクリプト",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("urls", nargs="*", help="取得するURL（複数指定可）")
    parser.add_argument("--file", "-f", help="URLリストファイルパス（1行1URL、#でコメント）")
    parser.add_argument("--keyword", "-k", help="検索キーワード（DuckDuckGoで上位URL自動取得）")
    parser.add_argument("--top", "-n", type=int, default=5, help="--keyword使用時の取得件数（デフォルト: 5）")
    parser.add_argument("--output", "-o", help=f"出力ディレクトリ（デフォルト: {DEFAULT_OUTPUT_DIR}）")
    parser.add_argument("--delay", type=float, default=2.0, help="リクエスト間隔（秒、デフォルト: 2.0）")
    parser.add_argument("--timeout", type=int, default=20, help="HTTPタイムアウト（秒、デフォルト: 20）")
    args = parser.parse_args()

    # 出力ディレクトリ
    out_dir = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    # URL収集
    urls = list(args.urls)

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ ファイルが見つかりません: {file_path}")
            sys.exit(1)
        with open(file_path, encoding="utf-8") as f:
            file_urls = [
                line.strip() for line in f
                if line.strip() and not line.startswith("#")
            ]
        print(f"📂 ファイルから {len(file_urls)} 件のURLを読み込み")
        urls += file_urls

    if args.keyword:
        search_urls = search_top_urls(args.keyword, args.top)
        urls += search_urls

    # 重複除去
    urls = list(dict.fromkeys(urls))

    if not urls:
        print("❌ URLが指定されていません。--help でヘルプを確認してください。")
        sys.exit(1)

    print(f"\n🚀 取得開始: {len(urls)}件\n{'='*60}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    all_results = []

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] {url}")
        data = fetch_full_content(url, timeout=args.timeout)
        all_results.append(data)

        status = "✅" if not data["error"] else "⚠️"
        print(f"  {status} 本文: {data['word_count']:,}文字 | {data['method']}")
        print(f"  📌 タイトル: {data['title'][:60]}")
        if data["error"]:
            print(f"  ⚠️ {data['error']}")

        # 個別ファイルに保存
        slug = re.sub(r"[^\w]", "_", urlparse(url).path.strip("/"))[:50] or f"site{i:02d}"
        md_path = out_dir / f"{timestamp}_{i:02d}_{slug}.md"
        md_path.write_text(to_markdown(data), encoding="utf-8")
        print(f"  💾 {md_path}")

        if i < len(urls):
            time.sleep(args.delay)

    # ============================
    # サマリーファイル生成
    # ============================
    summary_lines = [
        f"# 競合記事調査サマリー\n",
        f"**実行日時:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n",
        f"**調査件数:** {len(all_results)}件  \n",
        f"\n---\n\n",
    ]

    for i, data in enumerate(all_results, 1):
        status = "✅" if not data["error"] else "⚠️"
        summary_lines.append(f"## {i}. {status} {data['title']}\n\n")
        summary_lines.append(f"- **URL:** {data['url']}\n")
        summary_lines.append(f"- **本文文字数:** {data['word_count']:,}文字\n")
        if data["meta_description"]:
            summary_lines.append(f"- **メタ:** {data['meta_description'][:100]}\n")
        if data["error"]:
            summary_lines.append(f"- **エラー:** {data['error']}\n")

        summary_lines.append("\n### 見出し構造\n\n")
        for h in data["headings"]:
            depth = int(h["level"][1]) - 1
            prefix = "  " * depth + "- "
            summary_lines.append(f"{prefix}**[{h['level'].upper()}]** {h['text']}\n")

        summary_lines.append("\n### 本文（冒頭500文字）\n\n")
        preview = data["body_text"][:500].replace("\n", " ") if data["body_text"] else "（取得失敗）"
        summary_lines.append(f"> {preview}...\n")

        summary_lines.append("\n---\n\n")

    summary_path = out_dir / f"{timestamp}_summary.md"
    summary_path.write_text("".join(summary_lines), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"✅ 完了！")
    print(f"  個別ファイル: {out_dir}/{timestamp}_01_*.md 〜")
    print(f"  サマリー:     {summary_path}")
    print(f"\n💡 Claudeに読み込ませる場合は以下を使ってください:")
    print(f"  サマリーのみ: {summary_path}")
    print(f"  特定記事の全文: {out_dir}/{timestamp}_XX_*.md")


if __name__ == "__main__":
    main()
