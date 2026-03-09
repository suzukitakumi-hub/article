#!/usr/bin/env python3
"""
SE Ranking Cookie 自動更新スクリプト（Playwright版）
.envのPHPSESSID / SESUIDを自動で更新します。

使い方:
  python refresh_cookies.py

実行後、Antigravityを再起動すれば新しいセッションが使われます。
"""

import os
import re
import asyncio
from pathlib import Path
from dotenv import load_dotenv

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwrightが未インストールです。以下を実行してください：")
    print("  pip install playwright")
    print("  playwright install chromium")
    raise SystemExit(1)

ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH)

LOGIN_URL = "https://online.seranking.com/login.html"
DASHBOARD_URL = "https://online.seranking.com/admin.html"
EMAIL = os.getenv("SERANKING_EMAIL", "")
PASS  = os.getenv("SERANKING_PASS", "")


async def refresh_cookies():
    if not EMAIL or not PASS:
        print("ERROR: SERANKING_EMAIL / SERANKING_PASS が .env に未設定です。")
        return False

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print("SERankingにログイン中...")
        await page.goto(LOGIN_URL, wait_until="networkidle")

        # メールアドレス入力
        await page.fill('input[name="aItem[login]"]', EMAIL)
        # パスワード入力
        await page.fill('input[name="aItem[password]"]', PASS)
        # ログインボタンクリック
        await page.click('button[type="submit"].f_btn_blue, input[type="submit"]')

        # ダッシュボードまで待つ
        try:
            await page.wait_for_url(lambda url: "admin" in url or "online.seranking.com" in url,
                                     timeout=15000)
        except Exception:
            print("WARNING: ログイン後のリダイレクト待ちがタイムアウト。クッキーを取得します。")

        # クッキーを取得
        cookies = await context.cookies()
        cookie_map = {c["name"]: c["value"] for c in cookies}

        phpsessid = cookie_map.get("PHPSESSID", "")
        sesuid    = cookie_map.get("SESUID", "")
        auto_login = cookie_map.get("auto_login_cookie", "")
        uid        = cookie_map.get("UID", "")

        await browser.close()

        if not phpsessid:
            print("ERROR: PHPSESSID が取得できませんでした。ログインに失敗した可能性があります。")
            return False

        # .env を書き換え
        text = ENV_PATH.read_text(encoding="utf-8")
        text = re.sub(r"SERANKING_PHPSESSID=.*", f"SERANKING_PHPSESSID={phpsessid}", text)
        if sesuid:
            text = re.sub(r"SERANKING_SESUID=.*", f"SERANKING_SESUID={sesuid}", text)
        if auto_login:
            text = re.sub(r"SERANKING_AUTO_LOGIN_COOKIE=.*",
                          f"SERANKING_AUTO_LOGIN_COOKIE={auto_login}", text)
        if uid:
            text = re.sub(r"SERANKING_UID=.*", f"SERANKING_UID={uid}", text)
        ENV_PATH.write_text(text, encoding="utf-8")

        print("✅ Cookie更新完了！")
        print(f"  PHPSESSID : {phpsessid[:20]}...")
        print(f"  SESUID    : {sesuid[:20]}..." if sesuid else "  SESUID    : (変更なし)")
        print()
        print("Antigravityを再起動するか、MCPサーバーを再起動してください。")
        return True


if __name__ == "__main__":
    asyncio.run(refresh_cookies())
