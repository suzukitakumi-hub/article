#!/usr/bin/env python3
"""
SE Ranking Internal API MCP Server
キーワード順位・検索ボリューム・LLM順位を取得するMCPサーバー
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# .envパスを定数として保持（毎リクエストで再読み込みする）
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH)  # 初回読み込み（起動時）

BASE_URL = "https://online.seranking.com"
SITE_ID = os.getenv("SERANKING_SITE_ID", "10028792")
SITE_SE_ID = os.getenv("SERANKING_SITE_SE_ID", "3025525")
COMPETITOR_IDS = [c.strip() for c in os.getenv("SERANKING_COMPETITOR_IDS", "").split(",") if c.strip()]
GROUP_ID = os.getenv("SERANKING_GROUP_ID", "3631156")


def get_session_headers() -> dict:
    """セッションクッキーをヘッダーとして返す"""
    phpsessid   = os.getenv("SERANKING_PHPSESSID", "")
    sesuid      = os.getenv("SERANKING_SESUID", "")
    uid         = os.getenv("SERANKING_UID", "")
    auto_cookie = os.getenv("SERANKING_AUTO_LOGIN_COOKIE", "")
    cookie = f"PHPSESSID={phpsessid}; SESUID={sesuid}; UID={uid}; auto_login_cookie={auto_cookie}"
    return {
        "cookie": cookie,
        "accept": "application/json, text/plain, */*",
        "referer": f"{BASE_URL}/admin.site.rankings.site_id-{SITE_ID}.html",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }


def get_date_range(days: int = 7) -> tuple[str, str]:
    """直近N日の日付範囲を返す"""
    end = datetime.now()
    start = end - timedelta(days=days)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def refresh_session() -> bool:
    """
    auto_login_cookie を使ってセッションを自動更新する。
    成功時は .env の PHPSESSID / SESUID を書き換えて True を返す。
    """
    auto_cookie = os.getenv("SERANKING_AUTO_LOGIN_COOKIE", "")
    uid = os.getenv("SERANKING_UID", "")
    if not auto_cookie:
        return False

    headers = {
        "cookie": f"auto_login_cookie={auto_cookie}; UID={uid}",
        "accept": "text/html,application/json,*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    try:
        resp = requests.get(f"{BASE_URL}/admin.html", headers=headers,
                             timeout=15, allow_redirects=True)
        new_cookies = resp.cookies.get_dict()
        new_phpsessid = new_cookies.get("PHPSESSID", "")
        new_sesuid = new_cookies.get("SESUID", "")

        if not new_phpsessid or not new_sesuid:
            # Set-Cookie ヘッダーから直接パース
            for h in resp.headers.getlist("Set-Cookie") if hasattr(resp.headers, "getlist") else [resp.headers.get("Set-Cookie", "")]:
                if "PHPSESSID=" in h:
                    new_phpsessid = h.split("PHPSESSID=")[1].split(";")[0]
                if "SESUID=" in h:
                    new_sesuid = h.split("SESUID=")[1].split(";")[0]

        if not new_phpsessid or not new_sesuid:
            return False

        # .env を書き換え
        env_path = Path(__file__).parent / ".env"
        text = env_path.read_text(encoding="utf-8")
        import re
        text = re.sub(r"SERANKING_PHPSESSID=.*", f"SERANKING_PHPSESSID={new_phpsessid}", text)
        text = re.sub(r"SERANKING_SESUID=.*", f"SERANKING_SESUID={new_sesuid}", text)
        env_path.write_text(text, encoding="utf-8")

        # プロセス内の環境変数も即時反映
        os.environ["SERANKING_PHPSESSID"] = new_phpsessid
        os.environ["SERANKING_SESUID"] = new_sesuid
        return True

    except Exception:
        return False


def safe_get(url: str, **kwargs) -> requests.Response:
    """GET リクエスト。401時にセッション自動更新してリトライする。"""
    resp = requests.get(url, headers=get_session_headers(), **kwargs)
    if resp.status_code == 401 and refresh_session():
        resp = requests.get(url, headers=get_session_headers(), **kwargs)
    resp.raise_for_status()
    return resp


def safe_post(url: str, **kwargs) -> requests.Response:
    """POST リクエスト。401時にセッション自動更新してリトライする。"""
    resp = requests.post(url, headers=get_session_headers(), **kwargs)
    if resp.status_code == 401 and refresh_session():
        resp = requests.post(url, headers=get_session_headers(), **kwargs)
    resp.raise_for_status()
    return resp


def fetch_keywords_list(days: int = 7, page: int = 1, limit: int = 100) -> dict:
    """キーワード一覧・検索ボリューム・ランディングページを取得"""
    date_from, date_to = get_date_range(days)
    url = (
        f"{BASE_URL}/api.projects.site.positions.html"
        f"?do=keywordsList"
        f"&site_id={SITE_ID}"
        f"&columns[]=landing_page"
        f"&columns[]=volume"
        f"&columns[]=organic_traffic"
        f"&keywords_count_display={limit}"
        f"&page={page}"
        f"&group_by=list"
        f"&is_paid=0"
        f"&columns_group_mode=day"
        f"&site_se_id={SITE_SE_ID}"
        f"&report_period_from={date_from}"
        f"&report_period_to={date_to}"
    )
    resp = safe_get(url, timeout=30)
    return resp.json()


def fetch_positions(k2se_ids: list[str], days: int = 7) -> dict:
    """キーワードIDリストの順位データを取得"""
    date_from, date_to = get_date_range(days)
    ids_str = "%2C".join(k2se_ids)
    url = (
        f"{BASE_URL}/api.projects.site.positions.html"
        f"?do=positions"
        f"&site_id={SITE_ID}"
        f"&site_se_id={SITE_SE_ID}"
        f"&group_by=list"
        f"&is_paid=0"
        f"&k2se_ids={ids_str}"
        f"&columns_group_mode=day"
        f"&report_period_from={date_from}"
        f"&report_period_to={date_to}"
    )
    resp = safe_get(url, timeout=30)
    return resp.json()


def fetch_llm_rankings() -> dict:
    """AI/LLM検索での順位データを取得"""
    url = f"{BASE_URL}/api.llm_rankings.html?site_id={SITE_ID}"
    resp = safe_get(url, timeout=30)
    return resp.json()


def fetch_competitor_keywords(days: int = 30, limit: int = 50, page: int = 1) -> dict:
    """競合サイトとのキーワード比較データを取得"""
    date_from, date_to = get_date_range(days)
    competitor_params = "".join(f"&competitors[]={cid}" for cid in COMPETITOR_IDS)
    url = (
        f"{BASE_URL}/api.competitors.overall.html"
        f"?do=keywords"
        f"&site_id={SITE_ID}"
        f"&site_se_id={SITE_SE_ID}"
        f"{competitor_params}"
        f"&columns[]=volume"
        f"&columns[]=suggested_bid"
        f"&columns[]=competition"
        f"&columns[]=total_in_index"
        f"&report_period_from={date_from}"
        f"&report_period_to={date_to}"
        f"&compare_mode=0"
        f"&single_group={GROUP_ID}"
        f"&tags_all=0"
        f"&list_type=all"
        f"&keywords_count_display={limit}"
        f"&page={page}"
    )
    resp = safe_get(url, timeout=30)
    return resp.json()


def fetch_competitor_avg_positions(period: str = "week", top_range: int = 10) -> dict:
    """競合サイト内の平均順位推移を取得"""
    own_and_competitors = [SITE_ID] + COMPETITOR_IDS[:5]  # 自分+競合最大5位
    ids_params = "".join(f"&competitors_ids[]={cid}" for cid in own_and_competitors)
    url = (
        f"{BASE_URL}/admin.site.competitors.chart.site_id-{SITE_ID}.do-avgpos.html"
        f"?period={period}"
        f"{ids_params}"
        f"&show_site=1"
        f"&top_range={top_range}"
        f"&tags_all=0"
        f"&se={SITE_SE_ID}"
    )
    resp = safe_get(url, timeout=30)
    return resp.json()


def fetch_keyword_research(keyword: str, limit: int = 20, source: str = "jp") -> dict:
    """任意キーワードのボリューム・難易度・サジェストを一括取得"""
    import urllib.parse
    encoded_kw = urllib.parse.quote(keyword)
    headers = get_session_headers()
    headers["referer"] = f"{BASE_URL}/research.keywords.html/?keyword={encoded_kw}&source={source}"
    headers["x-requested-with"] = "XMLHttpRequest"
    headers["content-type"] = "application/x-www-form-urlencoded"
    headers["origin"] = BASE_URL

    # Step1: セッションにキーワードコンテキストをセット（401時に自動リトライ込み）
    sess = requests.Session()
    phpsessid = os.getenv("SERANKING_PHPSESSID", "")
    sesuid = os.getenv("SERANKING_SESUID", "")
    sess.headers.update(headers)
    sess.cookies.set("PHPSESSID", phpsessid)
    sess.cookies.set("SESUID", sesuid)
    init_resp = sess.get(init_url, timeout=30)
    if init_resp.status_code == 401:
        if refresh_session():
            phpsessid = os.getenv("SERANKING_PHPSESSID", "")
            sesuid = os.getenv("SERANKING_SESUID", "")
            sess.cookies.set("PHPSESSID", phpsessid)
            sess.cookies.set("SESUID", sesuid)
            sess.get(init_url, timeout=30)

    # Step2: メインデータ（ボリューム・難易度）
    main_resp = sess.get(
        f"{BASE_URL}/research.keywords.html?json=appWrapData",
        headers=headers, timeout=30
    )
    main_data = main_resp.json() if main_resp.ok else {}

    # Step3: 類似KW・関連KW・疑問文KWを並列取得
    suggestions = {}
    for suggestion_type in ["similar", "related", "questions", "longtail"]:
        url = (
            f"{BASE_URL}/research.api.suggestion.html"
            f"?do={suggestion_type}"
            f"&limit={limit}"
            f"&sort=volume"
            f"&sort_order=desc"
            f"&keyword={encoded_kw}"
            f"&source={source}"
            f"&broad=0"
        )
        s_resp = sess.post(url, headers=headers, timeout=30)
        suggestions[suggestion_type] = s_resp.json() if s_resp.ok else []

    return {
        "keyword": keyword,
        "source": source,
        "main": main_data,
        "suggestions": suggestions,
    }


# MCPサーバー初期化
app = Server("seranking")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_keyword_rankings",
            description=(
                "SERankingからキーワード順位・検索ボリューム・ランディングページを取得します。"
                "直近N日のデータを返します。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "description": "直近何日分のデータを取得するか（デフォルト: 7）",
                        "default": 7,
                    },
                    "page": {
                        "type": "integer",
                        "description": "ページ番号（デフォルト: 1）",
                        "default": 1,
                    },
                    "limit": {
                        "type": "integer",
                        "description": "1ページあたりのキーワード数（デフォルト: 100）",
                        "default": 100,
                    },
                    "top_n": {
                        "type": "integer",
                        "description": "上位N位以内のキーワードのみ返す（例: 10）。省略時は全件。",
                        "default": 0,
                    },
                },
            },
        ),
        Tool(
            name="get_llm_rankings",
            description=(
                "ChatGPT・Gemini・Perplexityなど AI検索でのブランド言及・順位データを取得します。"
            ),
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_competitor_keywords",
            description=(
                "SERランキングの競合調査機能。競合サイトとのキーワード重複状況・検索ボリューム・おすすめ単価を取得します。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "description": "直近30日等、調査期間の日数（デフォルト: 30）",
                        "default": 30,
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返却キーワード数（デフォルト: 50）",
                        "default": 50,
                    },
                    "page": {
                        "type": "integer",
                        "description": "ページ番号（デフォルト: 1）",
                        "default": 1,
                    },
                },
            },
        ),
        Tool(
            name="get_competitor_avg_positions",
            description=(
                "競合サイトとの平均順位推移を取得します。week（週次） / month（月次）を選べます。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "period": {
                        "type": "string",
                        "description": "week または month（デフォルト: week）",
                        "default": "week",
                    },
                    "top_range": {
                        "type": "integer",
                        "description": "上佝N位までのキーワードで計算（デフォルト: 10）",
                        "default": 10,
                    },
                },
            },
        ),
        Tool(
            name="research_keyword",
            description=(
                "任意のキーワードをSERankingのキーワード調査機能で分析します。"
                "検索ボリューム・難易度スコア・類似KW・関連KW・疑問文KW・ロングテールKWを返します。"
                "例: 「外国人採用について調べて」「特定技能のKW難易度を確認して」"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "調査するキーワード（例: 外国人 採用）",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "各サジェストカテゴリの取得件数（デフォルト: 20）",
                        "default": 20,
                    },
                },
                "required": ["keyword"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    # .envをリクエストごとに再読み込み（Cookieや設定変更を再起動不要で反映）
    load_dotenv(ENV_PATH, override=True)
    try:
        if name == "get_keyword_rankings":
            days = arguments.get("days", 7)
            page = arguments.get("page", 1)
            limit = arguments.get("limit", 100)
            top_n = arguments.get("top_n", 0)

            # Step1: キーワード一覧取得
            # 実際のレスポンス: {"data": {"rows": [...]}}
            kw_data = fetch_keywords_list(days=days, page=page, limit=limit)

            raw = kw_data.get("data", {}) if isinstance(kw_data, dict) else {}
            if isinstance(raw, dict):
                keywords = raw.get("rows", [])
            elif isinstance(raw, list):
                keywords = raw
            else:
                keywords = []
            if not keywords and isinstance(kw_data, list):
                keywords = kw_data

            # Step2: k2se_idsを抽出して順位取得
            k2se_ids = []
            kw_map = {}
            for kw in keywords:
                kid = str(kw.get("k2se_id") or kw.get("id", ""))
                if kid:
                    k2se_ids.append(kid)
                    kw_map[kid] = kw

            positions_raw = {}
            if k2se_ids:
                # 100件ずつ分割してリクエスト
                chunk_size = 100
                for i in range(0, len(k2se_ids), chunk_size):
                    chunk = k2se_ids[i:i + chunk_size]
                    pos_data = fetch_positions(chunk, days=days)
                    # レスポンス構造: {"data": {"k2se_id": {"YYYY-MM-DD": {position}, ...}}}
                    data_dict = pos_data.get("data", {}) if isinstance(pos_data, dict) else {}
                    if isinstance(data_dict, dict):
                        for k2se_id, date_entries in data_dict.items():
                            if isinstance(date_entries, dict) and date_entries:
                                latest_date = sorted(date_entries.keys())[-1]
                                positions_raw[str(k2se_id)] = date_entries[latest_date]

            # Step3: 結合して整形
            results = []
            for kw in keywords:
                kid = str(kw.get("k2se_id") or kw.get("id", ""))
                pos = positions_raw.get(kid, {})

                # 実際のフィールド名: site_keyword_keyword, landing_pages[0].url
                keyword_text = (
                    kw.get("site_keyword_keyword")
                    or kw.get("keyword")
                    or kw.get("name", "")
                )
                volume = kw.get("volume") or kw.get("search_volume")

                landing_pages = kw.get("landing_pages", []) or []
                landing_page = (
                    landing_pages[0].get("url") if landing_pages
                    else kw.get("landing_page")
                )

                # 順位: positions_rawから取得（fetch_positionsの最新日付エントリ）
                current_pos = None
                pos_entry = positions_raw.get(kid, {})
                pos_val = pos_entry.get("position") if isinstance(pos_entry, dict) else None
                if pos_val is not None:
                    try:
                        p_int = int(pos_val)
                        current_pos = p_int if 0 < p_int < 200 else None
                    except (ValueError, TypeError):
                        pass

                entry = {
                    "keyword": keyword_text,
                    "position": current_pos,
                    "volume": volume,
                    "landing_page": landing_page,
                    "organic_traffic": kw.get("organic_traffic"),
                }
                results.append(entry)

            # top_nフィルタ
            if top_n > 0:
                results = [
                    r for r in results
                    if r["position"] is not None and r["position"] <= top_n
                ]

            # 順位でソート
            results.sort(key=lambda x: (x["position"] is None, x["position"] or 9999))

            output = {
                "site_id": SITE_ID,
                "period_days": days,
                "total": len(results),
                "keywords": results,
            }
            return [TextContent(type="text", text=json.dumps(output, ensure_ascii=False, indent=2))]

        elif name == "get_llm_rankings":
            data = fetch_llm_rankings()
            return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]

        elif name == "get_competitor_keywords":
            days = arguments.get("days", 30)
            limit = arguments.get("limit", 50)
            page = arguments.get("page", 1)
            data = fetch_competitor_keywords(days=days, limit=limit, page=page)
            output = {
                "site_id": SITE_ID,
                "competitor_ids": COMPETITOR_IDS,
                "period_days": days,
                "data": data,
            }
            return [TextContent(type="text", text=json.dumps(output, ensure_ascii=False, indent=2))]

        elif name == "get_competitor_avg_positions":
            period = arguments.get("period", "week")
            top_range = arguments.get("top_range", 10)
            data = fetch_competitor_avg_positions(period=period, top_range=top_range)
            output = {
                "site_id": SITE_ID,
                "period": period,
                "top_range": top_range,
                "data": data,
            }
            return [TextContent(type="text", text=json.dumps(output, ensure_ascii=False, indent=2))]

        elif name == "research_keyword":
            keyword = arguments.get("keyword", "")
            limit = arguments.get("limit", 20)
            if not keyword:
                return [TextContent(type="text", text="keywordパラメータが必要です。")]
            data = fetch_keyword_research(keyword=keyword, limit=limit)
            return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except requests.HTTPError as e:
        if e.response.status_code == 401:
            msg = (
                "認証エラー（401）: セッションが切れています。\n"
                "SERankingにChromeでログインし直し、DevToolsのcookieから"
                "PHPSESSID と SESUID を取得して .env ファイルを更新してください。"
            )
        else:
            msg = f"HTTPエラー: {e.response.status_code} - {e.response.text[:200]}"
        return [TextContent(type="text", text=msg)]
    except Exception as e:
        return [TextContent(type="text", text=f"エラー: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
