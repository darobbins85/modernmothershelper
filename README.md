# Modern Mother's Helper Static Website

This is a free, static version of the Modern Mother's Helper website, converted from WordPress and hosted on GitHub Pages.

## Original Site
- **Original WordPress Site**: https://modernmothershelper.com
- **Business**: Mother's Helper service in Austin, TX

## Technology Stack
- **Hosting**: GitHub Pages (free)
- **Content**: Static HTML/CSS
- **Source**: Converted from WordPress XML export

## Project Structure
```
├── site/                    # Static website files
│   ├── index.html          # Homepage
│   ├── pages/              # Individual pages
│   ├── posts/              # Blog posts
│   ├── css/                # Stylesheets
│   └── assets/             # Media files (images, etc.)
├── parse_wordpress.py      # WordPress XML parser
├── download_media.py       # Media downloader
└── README.md
```

## Local Development

To view the site locally:

```bash
cd site
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Deployment

This site is automatically deployed via GitHub Pages from the `site/` directory.

## Next Steps

1. ✅ Parse WordPress content to HTML
2. ✅ Create static site structure
3. ⏳ Download media files (currently blocked by WordPress host)
4. ⏳ Set up custom domain (modernmothershelper.com)
5. ⏳ Configure GitHub Pages

## Notes

- All content extracted from WordPress export (Nov 22, 2025)
- 8 published pages
- 1 blog post
- 156 media attachments
- Zero hosting costs!
