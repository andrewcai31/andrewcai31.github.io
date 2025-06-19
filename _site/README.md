# Simple Jekyll Website

A minimalist website built with Jekyll and the "no style, please" theme. Features fast loading, clean design, and support for markdown and LaTeX.

## Features

- **Minimalist Design**: Under 1kb of CSS for fast loading
- **Responsive Layout**: Works on all devices
- **Markdown Support**: Write content in markdown
- **LaTeX Integration**: Mathematical expressions with KaTeX
- **Collections**: Organized content with Things and Writing sections
- **SEO Optimized**: Built-in SEO tags and sitemap
- **GitHub Pages Ready**: Easy deployment

## Sections

### Info
Static page with information about the site and author.

### Things
A collection of interesting links and resources. Each thing can have:
- Title
- Description
- External link
- Date
- Custom content

### Writing
Blog posts and articles with full markdown and LaTeX support.

## Getting Started

### Prerequisites

- Ruby (2.4 or higher)
- RubyGems
- Bundler

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

2. Install dependencies:
```bash
bundle install
```

3. Start the development server:
```bash
bundle exec jekyll serve
```

4. Open your browser and visit `http://localhost:4000`

## Customization

### Site Configuration

Edit `_config.yml` to customize:
- Site title and description
- Author information
- URL settings
- Collections configuration

### Adding Content

#### New Thing
Create a file in `_things/` with front matter:
```yaml
---
title: "Your Thing Title"
description: "Brief description"
link: "https://example.com"
date: 2024-01-01
---
```

#### New Writing Post
Create a file in `_writing/` with front matter:
```yaml
---
title: "Your Post Title"
description: "Brief description"
date: 2024-01-01
---
```

### Styling

The CSS is in `assets/css/style.css`. The design follows the "no style, please" philosophy with minimal styling for maximum readability.

## LaTeX Support

The site supports LaTeX math expressions using KaTeX:

- Inline math: `$x^2 + y^2 = z^2$`
- Block math: `$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$`

## Deployment

### GitHub Pages

1. Push your code to GitHub
2. Go to repository settings
3. Enable GitHub Pages
4. Select source branch (usually `main` or `master`)

### Other Platforms

The site can be deployed to any static hosting service:
- Netlify
- Vercel
- Cloudflare Pages
- AWS S3

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- Theme inspired by [no style, please](http://jekyllthemes.org/themes/no-style-please/)
- Built with [Jekyll](https://jekyllrb.com/)
- LaTeX rendering with [KaTeX](https://katex.org/) 