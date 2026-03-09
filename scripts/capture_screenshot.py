from playwright.sync_api import sync_playwright
import sys

def capture(url, output_path, viewport_width=1920, viewport_height=1080):
    """
    指定されたURLのスクリーンショットを取得
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': viewport_width, 'height': viewport_height})
        page.goto(url, wait_until='networkidle', timeout=60000)
        page.screenshot(path=output_path, full_page=False)
        browser.close()
        print(f"Screenshot saved: {output_path}")

if __name__ == "__main__":
    url = "https://gaikoku-jinzai.tcj-education.com/"

    # Desktop viewport (1920x1080)
    print("Capturing desktop viewport...")
    capture(url, "screenshots/desktop_1920x1080.png", 1920, 1080)

    # Laptop viewport (1366x768)
    print("Capturing laptop viewport...")
    capture(url, "screenshots/laptop_1366x768.png", 1366, 768)

    # Tablet viewport (768x1024)
    print("Capturing tablet viewport...")
    capture(url, "screenshots/tablet_768x1024.png", 768, 1024)

    # Mobile viewport (375x812 - iPhone X/11/12)
    print("Capturing mobile viewport...")
    capture(url, "screenshots/mobile_375x812.png", 375, 812)

    print("\nAll screenshots captured successfully!")
