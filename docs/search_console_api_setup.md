# Search Console API setup (service account)

This project can already analyze GSC CSV files.
Use this guide to export those CSV files directly from Search Console API.

## 1) Create Google Cloud project

1. Open Google Cloud Console.
2. Create/select a project.
3. Enable API:
   - `APIs & Services` -> `Library` -> enable `Google Search Console API`.

## 2) Create service account key

1. `APIs & Services` -> `Credentials` -> `Create Credentials` -> `Service account`.
2. Create the account.
3. Open the service account -> `Keys` -> `Add key` -> `Create new key` -> JSON.
4. Save JSON securely (do not commit).

## 3) Grant Search Console access to service account

1. Open Search Console.
2. Open target property.
3. `Settings` -> `Users and permissions` -> `Add user`.
4. Add service account email (looks like `name@project.iam.gserviceaccount.com`).
5. Role: `Owner` (or Full, but Owner is safer for API visibility).

## 4) Install Python dependencies

```bash
pip install google-api-python-client google-auth google-auth-httplib2
```

## 5) Export CSV (same format your scripts already use)

```bash
python scripts/export_gsc_api_csv.py ^
  --property "https://gaikoku-jinzai.tcj-education.com/" ^
  --start-date 2026-01-01 ^
  --end-date 2026-01-31 ^
  --service-account-json "C:\keys\gsc-sa.json" ^
  --output "data/gsc/gsc_2026-01.csv"
```

Output columns:
- `Query, Page, Clicks, Impressions, CTR, Position`

This output can be consumed by existing scripts such as:
- `scripts/analyze_gsc.py`
- `scripts/analyze_rewrite_priority.py`
- `scripts/analyze_rewrite_priority_v2.py`

## Notes

- URL-prefix property example: `https://example.com/`
- Domain property example: `sc-domain:example.com`
- If you get empty rows:
  - confirm property type is correct
  - confirm service account is added to that property
  - confirm date range has data

## Workflow integration inputs

When running this project's SEO workflow, you can pass either:

1. `gsc_csv_path` directly (already exported), or
2. Let Phase0 auto-export by passing:
   - `gsc_property`
   - `gsc_service_account_json`
   - `gsc_start_date`
   - `gsc_end_date`

Example:

```text
gsc_property=https://gaikoku-jinzai.tcj-education.com/
gsc_service_account_json=prime-elf-487804-u7-0b20b3309ec8.json
gsc_start_date=2026-01-19
gsc_end_date=2026-02-18
```
