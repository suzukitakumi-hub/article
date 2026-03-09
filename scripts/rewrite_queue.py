#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rewrite_queue.py  -  リライト対象記事の自動優先度調査スクリプト

■ 安全設計
  - 完全読み取り専用。WordPressへの書き込みは一切行わない
  - WP REST API は GET のみ使用
  - ローカルファイルへの書き込みはレポート出力のみ

■ データソース（優先順）
  1. WordPress REST API     → 公開記事一覧・最終更新日を取得（WP_URL が設定済みの場合）
  2. data/published_urls/  → WP API 未設定時のフォールバック
  3. data/gsc/             → GSCパフォーマンスデータ（最新ファイルを自動選択）
  4. articles/*.html       → ローカルリライト済みファイルの更新日で「最近リライト済み」を判定
  5. data/article_archives/posts/ → 原稿MD（文字数・見出し数の品質判定）

■ 使い方
  # 通常実行（reports/ にレポートを出力）
  python scripts/rewrite_queue.py

  # 上位N件だけ表示
  python scripts/rewrite_queue.py --top 10

  # WP API をスキップしてローカルデータのみで実行
  python scripts/rewrite_queue.py --no-wp-api

  # JSON形式で出力（Claude Code からの読み込み用）
  python scripts/rewrite_queue.py --json
"""

import argparse
import csv
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth

JST = timezone(timedelta(hours=9))

# ---------------------------------------------------------------------------
# 設定
# ---------------------------------------------------------------------------
BASE_URL       = "https://gaikoku-jinzai.tcj-education.com"
GSC_DIR        = "data/gsc"
PUBLISHED_CSV  = "data/published_urls/export-all-urls-392852.CSV"
ARCHIVES_DIR   = "data/article_archives/posts"
ARTICLES_DIR   = "articles"
REPORTS_DIR    = "reports"

# 「最近リライト済み」とみなす日数（この日数以内に articles/*.html が更新されていたら除外）
RECENTLY_REWRITTEN_DAYS = 30

# ---------------------------------------------------------------------------
# .env 読み込み
# ---------------------------------------------------------------------------
def load_dotenv(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


# ---------------------------------------------------------------------------
# データ取得：WP REST API（GET のみ・読み取り専用）
# ---------------------------------------------------------------------------
def fetch_wp_posts(wp_url: str, wp_user: str, wp_pass: str) -> list[dict]:
    """
    WP REST API から公開記事一覧を取得する。
    返り値: [{"id": int, "slug": str, "title": str, "modified": "YYYY-MM-DDT..."}]
    """
    posts = []
    auth  = HTTPBasicAuth(wp_user, wp_pass)
    page  = 1
    while True:
        url  = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
        params = {
            "status":   "publish",
            "per_page": 100,
            "page":     page,
            "_fields":  "id,slug,title,modified,link",
        }
        try:
            resp = requests.get(url, auth=auth, params=params, timeout=20)
        except requests.RequestException as e:
            print(f"  [WARN] WP API 接続エラー: {e}")
            break

        if resp.status_code == 400:  # ページ超過
            break
        if not resp.ok:
            print(f"  [WARN] WP API エラー [{resp.status_code}]: {resp.text[:200]}")
            break

        batch = resp.json()
        if not batch:
            break
        posts.extend(batch)
        total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1

    return posts


# ---------------------------------------------------------------------------
# データ取得：ローカルフォールバック（WP API が使えない場合）
# ---------------------------------------------------------------------------
def load_published_urls_csv() -> list[dict]:
    """data/published_urls/ のCSVから記事一覧を読み込む"""
    csv_path = Path(PUBLISHED_CSV)
    if not csv_path.exists():
        return []
    posts = []
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get("URL", "").strip()
            title = row.get("Title", "").strip()
            if not url or "/posts/" not in url:
                continue
            slug = url.rstrip("/").split("/")[-1]
            posts.append({"id": None, "slug": slug, "title": title, "modified": None, "link": url})
    return posts


# ---------------------------------------------------------------------------
# データ取得：GSC CSV（最新ファイルを自動選択）
# ---------------------------------------------------------------------------
def load_gsc_data() -> dict[str, dict]:
    """
    data/gsc/ の最新CSVを読み込む。
    返り値: {slug: {"clicks": int, "impressions": int, "avg_position": float, "queries": [...]}}
    """
    gsc_dir = Path(GSC_DIR)
    if not gsc_dir.exists():
        return {}

    csv_files = sorted(gsc_dir.glob("gsc_*.csv"))
    if not csv_files:
        return {}

    latest = csv_files[-1]  # ファイル名でソートすると日付順になる
    print(f"  GSCデータ: {latest.name} を使用")

    data: dict[str, dict] = {}
    with open(latest, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            page = row.get("Page", "").strip()
            if "/posts/" not in page:
                continue
            slug = page.rstrip("/").split("/")[-1]
            clicks      = int(row.get("Clicks", 0) or 0)
            impressions = int(row.get("Impressions", 0) or 0)
            try:
                position = float(row.get("Position", 99).replace("%", "") if isinstance(row.get("Position"), str) else row.get("Position", 99))
            except (ValueError, TypeError):
                position = 99.0

            if slug not in data:
                data[slug] = {"clicks": 0, "impressions": 0, "positions": [], "queries": []}
            data[slug]["clicks"]      += clicks
            data[slug]["impressions"] += impressions
            data[slug]["positions"].append(position)
            data[slug]["queries"].append({
                "query":       row.get("Query", ""),
                "clicks":      clicks,
                "impressions": impressions,
                "position":    position,
            })

    # 平均順位を計算
    for slug, d in data.items():
        if d["positions"]:
            d["avg_position"] = sum(d["positions"]) / len(d["positions"])
        else:
            d["avg_position"] = 99.0

    return data


# ---------------------------------------------------------------------------
# データ取得：ローカル articles/ の更新日（最近リライト済み判定）
# ---------------------------------------------------------------------------
def load_recently_rewritten_slugs(days: int = RECENTLY_REWRITTEN_DAYS) -> set[str]:
    """
    articles/ 以下の HTML ファイルの更新日時を見て、
    直近 N 日以内に更新されたスラッグのセットを返す。
    """
    cutoff = datetime.now().timestamp() - days * 86400
    slugs: set[str] = set()
    articles_dir = Path(ARTICLES_DIR)
    if not articles_dir.exists():
        return slugs

    for html_file in articles_dir.rglob("*.html"):
        mtime = html_file.stat().st_mtime
        if mtime >= cutoff:
            stem = html_file.stem
            # _rewrite / _v数字 のサフィックスを除去してスラッグ推定
            stem = re.sub(r"_(rewrite|v\d+)$", "", stem, flags=re.IGNORECASE)
            slug = stem.replace("_", "-")
            slugs.add(slug)
            # アンダースコア版も追加（一致精度向上）
            slugs.add(stem)

    return slugs


# ---------------------------------------------------------------------------
# データ取得：記事アーカイブ（品質判定用）
# ---------------------------------------------------------------------------
def load_archive_quality() -> dict[str, dict]:
    """
    data/article_archives/posts/*.md から文字数・H2数を読み込む。
    返り値: {slug: {"char_count": int, "h2_count": int}}
    """
    quality: dict[str, dict] = {}
    archive_dir = Path(ARCHIVES_DIR)
    if not archive_dir.exists():
        return quality

    for md_file in archive_dir.glob("*.md"):
        slug = md_file.stem.replace("_", "-")
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        quality[slug] = {
            "char_count": len(content),
            "h2_count":   len(re.findall(r"^## ", content, re.MULTILINE)),
        }
    return quality


# ---------------------------------------------------------------------------
# スコアリング
# ---------------------------------------------------------------------------
def score_article(slug: str, title: str, gsc: Optional[dict], quality: Optional[dict],
                  modified_str: Optional[str], recently_rewritten: bool) -> tuple[int, list[str]]:
    """
    記事のリライト優先度スコアと理由を返す。
    スコアが高いほどリライト優先度が高い。
    """
    if recently_rewritten:
        return -1, ["✅ 直近30日以内にリライト済み（除外）"]

    score   = 0
    reasons = []

    # ---- GSCデータによるスコアリング ----
    if gsc:
        impressions  = gsc["impressions"]
        clicks       = gsc["clicks"]
        avg_position = gsc["avg_position"]

        # 表示回数が多い → 露出はある
        if impressions >= 500:
            score += 40
            reasons.append(f"📊 表示回数 {impressions:,}（高露出）")
        elif impressions >= 100:
            score += 20
            reasons.append(f"📈 表示回数 {impressions:,}（中程度の露出）")

        # 表示回数が多いのにクリックが少ない → CTR改善でインパクト大
        if impressions >= 100 and clicks == 0:
            score += 40
            reasons.append(f"⚠️  表示{impressions:,}回だがクリック0（タイトル/メタ改善で即効性あり）")
        elif impressions > 0 and clicks / impressions < 0.01 and impressions >= 50:
            score += 25
            reasons.append(f"⚠️  CTR {clicks/impressions*100:.1f}%（低CTR）")

        # 順位が 11〜30 位 → リライトで1ページ目に押し上げ可能
        if 10 < avg_position <= 30:
            score += 35
            reasons.append(f"🎯 平均順位 {avg_position:.1f}位（2〜3ページ目。リライトで1ページ目狙い）")
        elif 30 < avg_position <= 50:
            score += 20
            reasons.append(f"📉 平均順位 {avg_position:.1f}位（改善余地大）")

        # Top クエリを追記
        top_queries = sorted(gsc["queries"], key=lambda x: x["impressions"], reverse=True)[:3]
        for q in top_queries:
            if q["impressions"] >= 10:
                reasons.append(f"   └ 「{q['query']}」 表示{q['impressions']}回 / {q['position']:.1f}位")
    else:
        # GSCデータなし → 表示圏外か計測漏れ
        score += 5
        reasons.append("❓ GSCデータなし（圏外 or 未計測）")

    # ---- 記事品質によるスコアリング ----
    if quality:
        if quality["h2_count"] == 0:
            score += 30
            reasons.append("❌ H2見出しなし（構造的問題）")
        if quality["char_count"] < 3000:
            score += 20
            reasons.append(f"📝 文字数 {quality['char_count']:,}（短すぎる）")

    # ---- WP最終更新日によるスコアリング ----
    if modified_str:
        try:
            modified_dt = datetime.fromisoformat(modified_str.replace("Z", "+00:00"))
            age_days    = (datetime.now(timezone.utc) - modified_dt).days
            if age_days >= 365:
                score += 25
                reasons.append(f"🕐 最終更新から {age_days}日（情報が古い可能性）")
            elif age_days >= 180:
                score += 10
                reasons.append(f"🕐 最終更新から {age_days}日（半年以上経過）")
        except (ValueError, TypeError):
            pass

    return score, reasons


# ---------------------------------------------------------------------------
# レポート生成
# ---------------------------------------------------------------------------
def build_report(ranked: list[dict], top_n: int, gsc_available: bool, wp_api_used: bool) -> str:
    now_str = datetime.now(JST).strftime("%Y-%m-%d %H:%M")
    lines   = []
    lines.append(f"# リライト優先度レポート（{now_str}）\n")
    lines.append(f"- GSCデータ: {'あり' if gsc_available else 'なし'}")
    lines.append(f"- WP API:   {'使用' if wp_api_used else '未使用（ローカルCSVを使用）'}")
    lines.append(f"- 除外:     直近{RECENTLY_REWRITTEN_DAYS}日以内にリライト済みの記事")
    lines.append("")
    lines.append("---\n")

    active = [r for r in ranked if r["score"] >= 0]
    excluded = [r for r in ranked if r["score"] < 0]

    lines.append(f"## 🔥 リライト候補（上位{min(top_n, len(active))}件）\n")
    for i, item in enumerate(active[:top_n], 1):
        lines.append(f"### {i}. {item['title']}")
        lines.append(f"- **スコア**: {item['score']}")
        lines.append(f"- **URL**: {BASE_URL}/posts/{item['slug']}")
        if item.get("wp_id"):
            lines.append(f"- **WP投稿ID**: {item['wp_id']}")
        for reason in item["reasons"]:
            lines.append(f"- {reason}")
        lines.append("")

    lines.append(f"\n## ✅ 直近リライト済み（除外: {len(excluded)}件）\n")
    for item in excluded:
        lines.append(f"- {item['title']} (`{item['slug']}`)")

    lines.append(f"\n---\n*このレポートは自動生成されました。WPへの書き込みは一切行っていません。*")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# メイン処理
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="リライト対象記事の優先度を調査します（読み取り専用）")
    parser.add_argument("--top",       type=int, default=15,  help="表示する上位N件（デフォルト15）")
    parser.add_argument("--no-wp-api", action="store_true",   help="WP APIをスキップしてローカルデータのみで実行")
    parser.add_argument("--json",      action="store_true",   help="JSON形式で出力（Claudeが読みやすい形式）")
    args = parser.parse_args()

    load_dotenv(".env")
    wp_url  = os.environ.get("WP_URL",          "").strip()
    wp_user = os.environ.get("WP_USER",          "").strip()
    wp_pass = os.environ.get("WP_APP_PASSWORD",  "").strip()

    print("=" * 55)
    print("  リライト優先度調査（読み取り専用）")
    print("=" * 55)

    # ---- Step1: 記事一覧を取得 ----
    wp_api_used = False
    posts: list[dict] = []

    if not args.no_wp_api and all([wp_url, wp_user, wp_pass]):
        print("\n[1/4] WordPress から公開記事一覧を取得中...")
        posts = fetch_wp_posts(wp_url, wp_user, wp_pass)
        if posts:
            print(f"  → {len(posts)} 記事を取得しました")
            wp_api_used = True
        else:
            print("  → WP API から取得できませんでした。ローカルCSVを使用します。")

    if not posts:
        print("\n[1/4] ローカルCSVから記事一覧を読み込み中...")
        posts = load_published_urls_csv()
        print(f"  → {len(posts)} 記事を読み込みました")

    if not posts:
        print("[ERROR] 記事一覧を取得できませんでした。")
        return

    # ---- Step2: GSCデータ読み込み ----
    print("\n[2/4] GSCデータを読み込み中...")
    gsc_data  = load_gsc_data()
    gsc_available = bool(gsc_data)
    print(f"  → {len(gsc_data)} ページのGSCデータを読み込みました")

    # ---- Step3: 補助データ読み込み ----
    print("\n[3/4] 補助データ（リライト済み判定・品質）を読み込み中...")
    recently_rewritten = load_recently_rewritten_slugs()
    archive_quality    = load_archive_quality()
    print(f"  → 直近リライト済み: {len(recently_rewritten)} スラッグ")
    print(f"  → 記事アーカイブ: {len(archive_quality)} 件")

    # ---- Step4: スコアリング ----
    print("\n[4/4] スコアリング中...")
    ranked: list[dict] = []

    for post in posts:
        slug     = post.get("slug", "")
        title_raw = post.get("title", "")
        # WP API だと title が {"rendered": "..."} の場合がある
        if isinstance(title_raw, dict):
            title = title_raw.get("rendered", slug)
        else:
            title = title_raw or slug
        # HTMLエンティティを簡易デコード
        title = title.replace("&#8211;", "–").replace("&amp;", "&").replace("&#038;", "&")

        modified_str = post.get("modified")
        wp_id        = post.get("id")
        is_recent    = slug in recently_rewritten or slug.replace("-", "_") in recently_rewritten

        gsc   = gsc_data.get(slug)
        qual  = archive_quality.get(slug) or archive_quality.get(slug.replace("-", "_"))

        score, reasons = score_article(slug, title, gsc, qual, modified_str, is_recent)
        ranked.append({
            "score":    score,
            "slug":     slug,
            "title":    title,
            "wp_id":    wp_id,
            "reasons":  reasons,
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)

    # ---- 出力 ----
    active   = [r for r in ranked if r["score"] >= 0]
    excluded = [r for r in ranked if r["score"] < 0]
    top_n    = args.top

    if args.json:
        output = {
            "generated_at": datetime.now(JST).isoformat(),
            "wp_api_used":  wp_api_used,
            "top_candidates": [
                {"rank": i+1, "slug": r["slug"], "title": r["title"],
                 "score": r["score"], "wp_id": r["wp_id"], "reasons": r["reasons"]}
                for i, r in enumerate(active[:top_n])
            ],
            "excluded_recently_rewritten": [
                {"slug": r["slug"], "title": r["title"]} for r in excluded
            ],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # ターミナル表示
        print(f"\n{'='*55}")
        print(f"  リライト候補 TOP {min(top_n, len(active))}件")
        print(f"{'='*55}")
        for i, item in enumerate(active[:top_n], 1):
            print(f"\n{i}. 【スコア {item['score']}】 {item['title']}")
            print(f"   URL: {BASE_URL}/posts/{item['slug']}")
            if item["wp_id"]:
                print(f"   WP投稿ID: {item['wp_id']}")
            for r in item["reasons"]:
                if not r.startswith("   └"):
                    print(f"   {r}")
                else:
                    print(f"  {r}")

        print(f"\n✅ 直近リライト済みとして除外: {len(excluded)}件")

        # レポートファイルに保存
        reports_dir = Path(REPORTS_DIR)
        reports_dir.mkdir(exist_ok=True)
        report_path = reports_dir / f"rewrite_queue_{datetime.now().strftime('%Y%m%d')}.md"
        report_text = build_report(ranked, top_n, gsc_available, wp_api_used)
        report_path.write_text(report_text, encoding="utf-8")
        print(f"\n📄 レポートを保存しました: {report_path}")


if __name__ == "__main__":
    main()
