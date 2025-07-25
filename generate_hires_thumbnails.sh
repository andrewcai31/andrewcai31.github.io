#!/bin/bash

echo "🖼️ Generating higher-resolution thumbnails for photo wall..."

# Counter for progress
count=0
total=$(ls assets/images/photos/*.{jpeg,jpg,JPEG,JPG,png,PNG} 2>/dev/null | wc -l)

echo "📸 Processing $total images with higher resolution..."

# Process each image in the photos directory
for img in assets/images/photos/*.{jpeg,jpg,JPEG,JPG,png,PNG}; do
    # Skip if no files match the pattern
    [ ! -f "$img" ] && continue
    
    # Get filename without path
    filename=$(basename "$img")
    
    # Create thumbnail path
    thumb_path="assets/images/thumbs/$filename"
    
    # Generate higher-res thumbnail: 600px width, maintain aspect ratio, 85% quality
    sips -Z 600 -s format jpeg -s formatOptions 85 "$img" --out "$thumb_path" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        ((count++))
        echo "✅ [$count/$total] Updated thumbnail: $filename"
    else
        echo "❌ Failed to update thumbnail: $filename"
    fi
done

echo ""
echo "🎉 Higher-resolution thumbnail generation complete!"
echo "📊 Updated $count thumbnails"

# Show size comparison
original_size=$(du -sh assets/images/photos/ | cut -f1)
thumb_size=$(du -sh assets/images/thumbs/ | cut -f1)
echo "📈 Original photos: $original_size"
echo "📉 Higher-res thumbnails: $thumb_size" 