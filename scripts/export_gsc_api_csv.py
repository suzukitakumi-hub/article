#!/usr/bin/env python3
"""
Export Google Search Console Search Analytics data to CSV.

Output CSV columns are compatible with existing local scripts:
Query, Page, Clicks, Impressions, CTR, Position

Example:
  python scripts/export_gsc_api_csv.py ^
    --property "https://gaikoku-jinzai.tcj-education.com/" ^
    --start-date 2026-01-01 ^
    --end-date 2026-01-31 ^
    --service-account-json "C:\\keys\\gsc-sa.json" ^
    --output "data/gsc/gsc_2026-01.csv"
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from typing import Any


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--property", required=True, help='URL-prefix or domain property, e.g. "https://example.com/" or "sc-domain:example.com"')
    p.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    p.add_argument("--end-date", required=True, help="YYYY-MM-DD")
    p.add_argument("--service-account-json", default=os.getenv("GSC_SERVICE_ACCOUNT_JSON", ""), help="Path to service account JSON")
    p.add_argument("--output", default="gsc_export.csv", help="Output CSV path")
    p.add_argument("--dimensions", default="query,page", help="Comma-separated dimensions (default: query,page)")
    p.add_argument("--search-type", default="web", choices=["web", "image", "video", "news", "discover", "googleNews"], help="Search type")
    p.add_argument("--max-rows", type=int, default=50000, help="Maximum rows to export")
    p.add_argument("--page-size", type=int, default=25000, help="Rows per API call (max 25000)")
    p.add_argument("--country", default="", help="Optional country code filter, e.g. jpn")
    p.add_argument("--device", default="", help="Optional device filter: DESKTOP, MOBILE, TABLET")
    p.add_argument("--query-contains", default="", help="Optional query contains filter")
    p.add_argument("--page-contains", default="", help="Optional page contains filter")
    return p.parse_args()


def build_filter_groups(args: argparse.Namespace) -> list[dict[str, Any]]:
    filters: list[dict[str, Any]] = []
    if args.country:
        filters.append({"dimension": "country", "operator": "equals", "expression": args.country.lower()})
    if args.device:
        filters.append({"dimension": "device", "operator": "equals", "expression": args.device.upper()})
    if args.query_contains:
        filters.append({"dimension": "query", "operator": "contains", "expression": args.query_contains})
    if args.page_contains:
        filters.append({"dimension": "page", "operator": "contains", "expression": args.page_contains})
    if not filters:
        return []
    return [{"filters": filters}]


def main() -> int:
    args = parse_args()
    if not args.service_account_json:
        print("[ERROR] --service-account-json is required (or set GSC_SERVICE_ACCOUNT_JSON).")
        return 2

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("[ERROR] Missing dependencies. Install:")
        print("  pip install google-api-python-client google-auth google-auth-httplib2")
        return 2

    scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
    credentials = service_account.Credentials.from_service_account_file(args.service_account_json, scopes=scopes)
    service = build("searchconsole", "v1", credentials=credentials, cache_discovery=False)

    dimensions = [d.strip() for d in args.dimensions.split(",") if d.strip()]
    page_size = max(1, min(args.page_size, 25000))
    max_rows = max(1, args.max_rows)

    all_rows: list[dict[str, Any]] = []
    start_row = 0
    while len(all_rows) < max_rows:
        current_size = min(page_size, max_rows - len(all_rows))
        body: dict[str, Any] = {
            "startDate": args.start_date,
            "endDate": args.end_date,
            "dimensions": dimensions,
            "rowLimit": current_size,
            "startRow": start_row,
            "type": args.search_type,
        }
        filter_groups = build_filter_groups(args)
        if filter_groups:
            body["dimensionFilterGroups"] = filter_groups

        response = service.searchanalytics().query(siteUrl=args.property, body=body).execute()
        rows = response.get("rows", [])
        if not rows:
            break

        all_rows.extend(rows)
        if len(rows) < current_size:
            break
        start_row += len(rows)

    with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["Query", "Page", "Clicks", "Impressions", "CTR", "Position"])
        writer.writeheader()
        for row in all_rows:
            keys = row.get("keys", [])
            key_map = dict(zip(dimensions, keys))
            ctr = float(row.get("ctr", 0.0)) * 100.0
            writer.writerow(
                {
                    "Query": key_map.get("query", ""),
                    "Page": key_map.get("page", ""),
                    "Clicks": int(row.get("clicks", 0)),
                    "Impressions": int(row.get("impressions", 0)),
                    "CTR": f"{ctr:.2f}%",
                    "Position": f"{float(row.get('position', 0.0)):.2f}",
                }
            )

    print(f"[OK] Exported {len(all_rows)} rows -> {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

