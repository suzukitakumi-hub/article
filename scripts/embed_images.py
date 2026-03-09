import base64
import re
import os

images_dir = r"c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\output\images"
html_path = r"c:\Users\suzuki.takumi\Desktop\AI\記事作成_TCJ\output\immigration_control_law_revision.html"

print(f"Reading HTML from: {html_path}")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

def replace_image(match):
    filename = match.group(1) # e.g. residence_status2.jpg
    # Remove query params if any
    if "?" in filename:
        filename = filename.split("?")[0]
        
    filepath = os.path.join(images_dir, filename)
    print(f"Processing image: {filename} -> {filepath}")
    
    if os.path.exists(filepath):
        with open(filepath, "rb") as img_f:
            b64_data = base64.b64encode(img_f.read()).decode("utf-8")
            # Determine mime type
            mime = "image/jpeg"
            if filename.lower().endswith(".png"): mime = "image/png"
            elif filename.lower().endswith(".gif"): mime = "image/gif"
            elif filename.lower().endswith(".webp"): mime = "image/webp"
            
            print(f"  Encoded {len(b64_data)} chars")
            return f'src="data:{mime};base64,{b64_data}"'
    else:
        print(f"  File not found: {filepath}")
        return match.group(0) # No change

# Pattern: src="images/(filename.jpg)"
# We look for src="images/..." and capture the filename
# Regex note: match non-quote chars
new_content = re.sub(r'src="images/([^"]+)"', replace_image, content)

print("Writing updated HTML...")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done.")
