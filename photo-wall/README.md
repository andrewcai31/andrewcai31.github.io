# How to Add Photos to Your Photo Wall

## Step 1: Add Your Images
1. Put your image files in `assets/images/photos/`
2. Use common formats: `.jpg`, `.jpeg`, `.png`, `.webp`
3. Recommended size: 800-1200px wide for best quality

## Step 2: Update the Photo Wall Page
Edit `photo-wall/index.html` and replace the placeholder with your photos:

```html
<div class="photo-grid">
    <div class="photo-item">
        <img src="/assets/images/photos/your-photo.jpg" alt="Description of photo" onclick="openPhotoModal(this)">
        <div class="photo-caption">Your caption here</div>
    </div>
    
    <div class="photo-item">
        <img src="/assets/images/photos/another-photo.jpg" alt="Description" onclick="openPhotoModal(this)">
        <div class="photo-caption">Another caption</div>
    </div>
    
    <!-- Add more photos here -->
</div>
```

## Step 3: Build and View
Run `bundle exec jekyll build` to update your site!

## Features
- **Responsive grid**: Automatically adjusts to screen size
- **Click to enlarge**: Photos open in a modal for full-size viewing
- **Captions**: Add descriptions to your photos
- **Mobile-friendly**: Looks great on all devices

## Tips
- Keep captions short and meaningful
- For better performance, optimize your images before uploading
- The grid will automatically arrange photos in a masonry-like layout 