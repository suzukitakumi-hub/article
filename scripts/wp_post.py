#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wp_post.py  -  HTMLファイルをWordPressに【下書き保存】するスクリプト

■ 安全設計
  - DELETE は一切呼ばない（コードレベルで存在しない）
  - status は "draft" 固定。--publish フラグを明示しない限り公開しない
  - 1回の実行で投稿できるのは 1記事のみ
  - 本文が 200KB を超える場合は異常とみなして中断
  - 実行前に内容をサマリー表示し、"y" 入力がないと送信しない（--yes で省略可）
  - すべての操作を data/wp_post_log.csv に記録
  - --dry-run モードで実際の送信なしに動作確認できる

■ 使い方
  # 下書き作成（確認プロンプトあり）
  python scripts/wp_post.py articles/points_to_note_rewrite.html

  # 既存記事を更新（投稿IDを指定）
  python scripts/wp_post.py articles/points_to_note_rewrite.html --post-id 456

  # 確認なしで即時実行（自動化スクリプトから呼ぶとき用）
  python scripts/wp_post.py articles/driver_exam_v1.html --yes

  # 実際には送信せず動作確認
  python scripts/wp_post.py articles/driver_exam_v1.html --dry-run

■ 必要な設定（.env ファイル）
  WP_URL=https://gaikoku-jinzai.tcj-education.com
  WP_USER=あなたのWP管理者ユーザー名
  WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth

# ---------------------------------------------------------------------------
# 定数
# ---------------------------------------------------------------------------
CONTENT_SIZE_LIMIT_BYTES = 200 * 1024  # 200KB: これを超えたら異常として中断
LOG_FILE = "data/wp_post_log.csv"
LOG_HEADERS = ["timestamp", "action", "html_file", "post_id", "title", "slug", "status", "wp_url", "dry_run", "result", "note"]

# ---------------------------------------------------------------------------
# .env 読み込み（python-dotenv 不要の軽量版）
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
# HTML パーサー
# ---------------------------------------------------------------------------
def extract_title_from_phase_output(html_path: Path) -> str:
    """data/phase_outputs/phase4_output.json の title を補完フォールバックとして返す"""
    json_path = Path("data/phase_outputs/phase4_output.json")
    if not json_path.exists():
        return ""
    try:
        import json
        data = json.loads(json_path.read_text(encoding="utf-8"))
        # html_path が phase4_output の html_path と一致するか確認
        stored = data.get("html_path", "")
        if stored and Path(stored).name == html_path.name:
            return data.get("title", "")
    except Exception:
        pass
    return ""


def extract_title(content: str, html_path: Path | None = None) -> str:
    """TITLE: コメント → <title> → <h1> → phase4_output.json の順で抽出"""
    m = re.search(r"^TITLE:\s*(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    m = re.search(r"<title>(.*?)</title>", content, re.DOTALL | re.IGNORECASE)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL | re.IGNORECASE)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    # 最後のフォールバック: phase4_output.json
    if html_path:
        t = extract_title_from_phase_output(html_path)
        if t:
            return t
    return ""


def extract_meta_description(content: str) -> str:
    """DESCRIPTION: コメント行 → meta description タグの順で抽出"""
    m = re.search(r"^DESCRIPTION:\s*(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    m = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']',
        content, re.IGNORECASE
    )
    if m:
        return m.group(1).strip()
    return ""


def extract_body_html(content: str) -> str:
    """記事本文HTMLを返す。TITLE:/DESCRIPTION: 行と <html>/<head> は除去する。"""
    # <body> タグがあればその中身のみを使う
    m = re.search(r"<body[^>]*>(.*?)</body>", content, re.DOTALL | re.IGNORECASE)
    if m:
        body = m.group(1)
    else:
        body = content

    # 先頭のコメント行 (TITLE: / DESCRIPTION:) を除去
    body = re.sub(r"^(TITLE|DESCRIPTION):[^\n]*\n?", "", body, flags=re.MULTILINE)
    return body.strip()


def slug_from_path(html_path: str) -> str:
    """ファイル名からWPスラッグを推定: points_to_note_rewrite.html → points-to-note"""
    stem = Path(html_path).stem
    # _rewrite / _v数字 の末尾サフィックスを除去
    stem = re.sub(r"_(rewrite|v\d+)$", "", stem, flags=re.IGNORECASE)
    return stem.replace("_", "-")


# ---------------------------------------------------------------------------
# ログ記録
# ---------------------------------------------------------------------------
def write_log(entry: dict) -> None:
    log_path = Path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not log_path.exists()
    with open(log_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_HEADERS)
        if write_header:
            writer.writeheader()
        writer.writerow(entry)


# ---------------------------------------------------------------------------
# WordPress REST API クライアント（DELETE は存在しない）
# ---------------------------------------------------------------------------
class SafeWPClient:
    ALLOWED_METHODS = {"GET", "POST", "PUT"}  # DELETE は許可しない

    def __init__(self, wp_url: str, username: str, app_password: str):
        self.base = wp_url.rstrip("/")
        self.auth = HTTPBasicAuth(username, app_password.replace(" ", " "))
        self.headers = {"Content-Type": "application/json"}

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        method = method.upper()
        if method not in self.ALLOWED_METHODS:
            raise ValueError(f"[SAFETY] メソッド '{method}' は許可されていません。GET/POST/PUT のみ使用可能です。")
        url = f"{self.base}/wp-json/wp/v2/{endpoint}"
        resp = requests.request(method, url, auth=self.auth, headers=self.headers, timeout=30, **kwargs)
        if not resp.ok:
            raise RuntimeError(f"WP API エラー [{resp.status_code}]: {resp.text[:400]}")
        return resp.json()

    def get_post_by_slug(self, slug: str) -> dict | None:
        """スラッグで既存記事を検索（読み取り専用）"""
        results = self._request("GET", f"posts?slug={slug}&status=any&per_page=1")
        return results[0] if results else None

    def create_draft(self, title: str, content: str, slug: str, meta_desc: str = "") -> dict:
        """新規投稿を下書きで作成（status は draft 固定）"""
        payload: dict = {
            "title":   title,
            "content": content,
            "slug":    slug,
            "status":  "draft",  # ← 固定。外部から変更不可
        }
        if meta_desc:
            payload["meta"] = {"_yoast_wpseo_metadesc": meta_desc}
        return self._request("POST", "posts", json=payload)

    def update_to_draft(self, post_id: int, title: str, content: str, meta_desc: str = "") -> dict:
        """既存記事を更新し、ステータスを draft に戻す（公開済み記事を非公開にはしない）"""
        payload: dict = {
            "title":   title,
            "content": content,
            "status":  "draft",  # ← 固定
        }
        if meta_desc:
            payload["meta"] = {"_yoast_wpseo_metadesc": meta_desc}
        return self._request("PUT", f"posts/{post_id}", json=payload)


# ---------------------------------------------------------------------------
# メイン処理
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="HTMLファイルをWordPressに下書き保存します")
    parser.add_argument("html_file", help="投稿するHTMLファイルのパス")
    parser.add_argument("--post-id", type=int, default=None,
                        help="更新する既存投稿のID（省略時はスラッグで自動検索）")
    parser.add_argument("--slug",    default=None,
                        help="WPスラッグ（省略時はファイル名から自動推定）")
    parser.add_argument("--title",   default=None,
                        help="記事タイトル（省略時はHTML内から自動抽出）")
    parser.add_argument("--yes",     action="store_true",
                        help="確認プロンプトをスキップして実行")
    parser.add_argument("--dry-run", action="store_true",
                        help="送信内容を表示するだけで実際には送信しない")
    args = parser.parse_args()

    # .env 読み込み
    load_dotenv(".env")
    wp_url  = os.environ.get("WP_URL", "").strip()
    wp_user = os.environ.get("WP_USER", "").strip()
    wp_pass = os.environ.get("WP_APP_PASSWORD", "").strip()

    if not all([wp_url, wp_user, wp_pass]) and not args.dry_run:
        print("[ERROR] .env に WP_URL / WP_USER / WP_APP_PASSWORD を設定してください。")
        print("        .env.example を参考にしてください。")
        sys.exit(1)

    # ファイル読み込み
    html_path = Path(args.html_file)
    if not html_path.exists():
        print(f"[ERROR] ファイルが見つかりません: {html_path}")
        sys.exit(1)

    raw = html_path.read_text(encoding="utf-8")

    # サイズ安全チェック（200KB 超は異常とみなして中断）
    raw_bytes = len(raw.encode("utf-8"))
    if raw_bytes > CONTENT_SIZE_LIMIT_BYTES:
        print(f"[ERROR] ファイルサイズが {raw_bytes // 1024}KB と大きすぎます（上限 200KB）。")
        print("        正しいファイルを指定しているか確認してください。")
        sys.exit(1)

    # メタデータ抽出
    title     = args.title or extract_title(raw, html_path)
    meta_desc = extract_meta_description(raw)
    body_html = extract_body_html(raw)
    slug      = args.slug or slug_from_path(str(html_path))

    if not title:
        print("[WARN] タイトルを自動抽出できませんでした。--title オプションで指定してください。")
        title = html_path.stem

    # 送信前サマリー表示
    print("=" * 55)
    print("  WordPress 下書き保存 - 送信内容確認")
    print("=" * 55)
    print(f"  ファイル     : {html_path}")
    print(f"  タイトル     : {title}")
    print(f"  スラッグ     : {slug}")
    print(f"  本文サイズ   : {len(body_html):,} 文字 / {raw_bytes // 1024} KB")
    if meta_desc:
        print(f"  メタディスク : {meta_desc[:70]}...")
    print(f"  ステータス   : draft（下書き固定）")
    if args.post_id:
        print(f"  投稿ID       : {args.post_id}（既存記事を更新）")
    print(f"  投稿先       : {wp_url or '（dry-run）'}")
    if args.dry_run:
        print("\n  [DRY-RUN] 実際の送信は行いません。")
    print("=" * 55)

    if args.dry_run:
        write_log({
            "timestamp": datetime.now().isoformat(),
            "action":    "dry-run",
            "html_file": str(html_path),
            "post_id":   args.post_id or "",
            "title":     title,
            "slug":      slug,
            "status":    "draft",
            "wp_url":    wp_url,
            "dry_run":   True,
            "result":    "skipped",
            "note":      "dry-run モード",
        })
        print("\n✅ dry-run 完了。実際の送信はありませんでした。")
        return

    # 確認プロンプト
    if not args.yes:
        answer = input("\n  上記の内容でWordPressに下書き保存しますか？ [y/N]: ").strip().lower()
        if answer != "y":
            print("  キャンセルしました。")
            write_log({
                "timestamp": datetime.now().isoformat(),
                "action":    "cancelled",
                "html_file": str(html_path),
                "post_id":   "",
                "title":     title,
                "slug":      slug,
                "status":    "draft",
                "wp_url":    wp_url,
                "dry_run":   False,
                "result":    "cancelled",
                "note":      "ユーザーがキャンセル",
            })
            sys.exit(0)

    # WP クライアント初期化
    client = SafeWPClient(wp_url, wp_user, wp_pass)

    try:
        if args.post_id:
            # 投稿ID 指定で更新
            print(f"\n  投稿ID={args.post_id} を更新中...")
            result = client.update_to_draft(args.post_id, title, body_html, meta_desc)
            post_id = result["id"]
            action_label = "更新"
        else:
            # スラッグで既存記事を検索
            print(f"\n  スラッグ '{slug}' の既存記事を検索中...")
            existing = client.get_post_by_slug(slug)
            if existing:
                post_id_existing = existing["id"]
                existing_title_raw = existing.get("title", {})
                existing_title = existing_title_raw.get("rendered", "") if isinstance(existing_title_raw, dict) else str(existing_title_raw)

                # ⚠️ 既存記事が見つかった場合は --yes でも必ず確認する
                # （slug推定は不完全なため、誤った記事を上書きするリスクがある）
                print(f"\n  ⚠️  既存記事が見つかりました。上書き更新します。")
                print(f"     投稿ID    : {post_id_existing}")
                print(f"     既存タイトル: {existing_title}")
                print(f"     新タイトル : {title}")
                answer = input("\n  この記事を上書きしますか？ [y/N]: ").strip().lower()
                if answer != "y":
                    print("  キャンセルしました。--post-id で投稿IDを明示的に指定して再実行してください。")
                    write_log({
                        "timestamp": datetime.now().isoformat(),
                        "action":    "cancelled",
                        "html_file": str(html_path),
                        "post_id":   post_id_existing,
                        "title":     title,
                        "slug":      slug,
                        "status":    "draft",
                        "wp_url":    wp_url,
                        "dry_run":   False,
                        "result":    "cancelled",
                        "note":      "slug一致による既存記事更新をユーザーがキャンセル",
                    })
                    sys.exit(0)

                result = client.update_to_draft(post_id_existing, title, body_html, meta_desc)
                post_id = result["id"]
                action_label = "更新"
            else:
                print("  既存記事なし。新規投稿を作成中...")
                result = client.create_draft(title, body_html, slug, meta_desc)
                post_id = result["id"]
                action_label = "新規作成"

    except Exception as e:
        print(f"\n[ERROR] WP API 呼び出しに失敗しました: {e}")
        write_log({
            "timestamp": datetime.now().isoformat(),
            "action":    "error",
            "html_file": str(html_path),
            "post_id":   args.post_id or "",
            "title":     title,
            "slug":      slug,
            "status":    "draft",
            "wp_url":    wp_url,
            "dry_run":   False,
            "result":    "error",
            "note":      str(e),
        })
        sys.exit(1)

    # 成功ログ
    edit_url = f"{wp_url}/wp-admin/post.php?post={post_id}&action=edit"
    write_log({
        "timestamp": datetime.now().isoformat(),
        "action":    action_label,
        "html_file": str(html_path),
        "post_id":   post_id,
        "title":     title,
        "slug":      slug,
        "status":    "draft",
        "wp_url":    wp_url,
        "dry_run":   False,
        "result":    "success",
        "note":      "",
    })

    print(f"\n✅ {action_label}完了！")
    print(f"   投稿ID   : {post_id}")
    print(f"   編集URL  : {edit_url}")
    print(f"   ※ 下書き保存済み。WP管理画面で内容を確認してから公開してください。")


if __name__ == "__main__":
    main()
