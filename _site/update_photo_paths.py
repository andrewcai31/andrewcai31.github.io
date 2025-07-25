#!/usr/bin/env python3
import re

def update_photo_paths():
    # Read the photo-wall/index.html file
    with open('photo-wall/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match img tags with /assets/images/photos/ paths
    pattern = r'<img src="/assets/images/photos/([^"]+)" alt="Photo" onclick="openPhotoModal\(this\)">'
    
    # Replacement function
    def replace_img_tag(match):
        filename = match.group(1)
        return f'<img src="/assets/images/thumbs/{filename}" alt="Photo" data-fullsize="/assets/images/photos/{filename}" onclick="openPhotoModal(this)">'
    
    # Replace all matches
    updated_content = re.sub(pattern, replace_img_tag, content)
    
    # Count how many replacements were made
    original_matches = len(re.findall(pattern, content))
    updated_matches = len(re.findall(r'<img src="/assets/images/thumbs/[^"]+".+?data-fullsize="/assets/images/photos/[^"]+".+?onclick="openPhotoModal\(this\)">', updated_content))
    
    # Write the updated content back
    with open('photo-wall/index.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ Updated {original_matches} image paths to use thumbnails")
    print(f"🔍 Found {updated_matches} images with thumbnail paths")
    print("📦 All images now load thumbnails in grid and full-size in modal")

if __name__ == "__main__":
    update_photo_paths() 