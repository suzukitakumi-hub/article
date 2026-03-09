import requests
import json
import re
from pathlib import Path

def get_featured_image_url(post_slug, base_url="https://gaikoku-jinzai.tcj-education.com"):
    """記事のスラグからアイキャッチ画像URLを取得"""

    # 記事情報を取得
    api_url = f"{base_url}/wp-json/wp/v2/posts?slug={post_slug}"

    try:
        print(f"[INFO] 記事情報を取得中: {post_slug}")
        response = requests.get(api_url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                # アイキャッチ画像のIDを取得
                featured_media_id = data[0].get('featured_media')

                if featured_media_id and featured_media_id > 0:
                    # 画像情報を取得
                    media_url = f"{base_url}/wp-json/wp/v2/media/{featured_media_id}"
                    print(f"  [IMAGE] 画像情報を取得中: ID {featured_media_id}")

                    media_response = requests.get(media_url, timeout=10)
                    if media_response.status_code == 200:
                        media_data = media_response.json()
                        image_url = media_data.get('source_url')
                        print(f"  [OK] 取得成功: {image_url}")
                        return image_url
                    else:
                        print(f"  [ERROR] 画像取得失敗: HTTP {media_response.status_code}")
                else:
                    print(f"  [WARN] アイキャッチ画像が設定されていません")
            else:
                print(f"  [ERROR] 記事が見つかりませんでした")
        else:
            print(f"  [ERROR] 記事取得失敗: HTTP {response.status_code}")

    except Exception as e:
        print(f"  [ERROR] エラー: {e}")

    return None


def extract_related_posts_from_html(html_content):
    """HTMLから関連記事のスラグと画像パスを抽出"""

    # 関連記事リンクのパターン（href属性からスラグを抽出）
    pattern = r'href="https://gaikoku-jinzai\.tcj-education\.com/posts/([^"]+)"[^>]*>.*?<img src="([^"]+)"'

    matches = re.findall(pattern, html_content, re.DOTALL)

    results = []
    for slug, old_img_path in matches:
        results.append({
            'slug': slug,
            'old_path': old_img_path
        })

    return results


def update_html_with_images(html_path, image_mapping):
    """HTMLファイルの画像パスを更新"""

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    updated_content = content

    for old_path, new_url in image_mapping.items():
        if new_url:
            updated_content = updated_content.replace(f'src="{old_path}"', f'src="{new_url}"')
            print(f"[UPDATE] 置換: {old_path} -> {new_url}")

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"\n[OK] HTMLファイルを更新しました: {html_path}")


def main():
    html_file = Path(r"c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\output\nursing_care1.html")

    if not html_file.exists():
        print(f"❌ ファイルが見つかりません: {html_file}")
        return

    # HTMLから関連記事を抽出
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    related_posts = extract_related_posts_from_html(html_content)

    print(f"\n[INFO] 関連記事を {len(related_posts)} 件検出しました\n")
    print("="*60)

    # 各記事の画像URLを取得
    image_mapping = {}

    for post in related_posts:
        slug = post['slug']
        old_path = post['old_path']

        print(f"\n[PROCESSING] 処理中: {slug}")
        image_url = get_featured_image_url(slug)

        if image_url:
            image_mapping[old_path] = image_url
        else:
            print(f"  [WARN] デフォルト画像を使用します")
            # プレースホルダー画像（TCJのロゴなど）
            image_mapping[old_path] = "https://gaikoku-jinzai.tcj-education.com/wp-content/themes/tcj-recruitment/assets/img/site-logo.svg"

    print("\n" + "="*60)
    print(f"\n[SUMMARY] 取得結果サマリー:")
    print(f"  成功: {sum(1 for url in image_mapping.values() if url and 'svg' not in url)} 件")
    print(f"  失敗: {sum(1 for url in image_mapping.values() if url and 'svg' in url)} 件")

    # HTMLを更新
    if image_mapping:
        print(f"\n[UPDATE] HTMLファイルを更新中...\n")
        update_html_with_images(html_file, image_mapping)
    else:
        print(f"\n[WARN] 更新する画像がありませんでした")


if __name__ == "__main__":
    main()
