from playwright.sync_api import sync_playwright

def capture_fullpage(url, output_path, viewport_width=1920, viewport_height=1080):
    """
    フルページスクリーンショットを取得
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': viewport_width, 'height': viewport_height})
        page.goto(url, wait_until='networkidle', timeout=60000)
        page.screenshot(path=output_path, full_page=True)
        browser.close()
        print(f"Full page screenshot saved: {output_path}")

if __name__ == "__main__":
    url = "https://gaikoku-jinzai.tcj-education.com/"

    # Desktop full page
    print("Capturing desktop full page...")
    capture_fullpage(url, "screenshots/desktop_fullpage.png", 1920, 1080)

    # Mobile full page
    print("Capturing mobile full page...")
    capture_fullpage(url, "screenshots/mobile_fullpage.png", 375, 812)

    print("\nFull page screenshots captured successfully!")
