#!/usr/bin/env python3
"""
WordPress XML to Static Site Converter
Parses WordPress export XML and creates a static website
"""

import xml.etree.ElementTree as ET
import os
import re
import json
from pathlib import Path
from html import unescape
from urllib.parse import urlparse


class WordPressParser:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        self.channel = self.root.find('channel')

        # Define WordPress namespaces
        self.ns = {
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'wp': 'http://wordpress.org/export/1.2/',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
        }

        self.site_url = ''
        self.site_title = ''
        self.site_description = ''
        self.pages = []
        self.posts = []
        self.attachments = []

    def parse(self):
        """Parse the WordPress XML file"""
        # Get site metadata
        self.site_title = self.channel.find('title').text or 'My Website'
        self.site_url = self.channel.find('link').text or ''
        self.site_description = self.channel.find('description').text or ''

        # Parse all items
        for item in self.channel.findall('item'):
            post_type = item.find('wp:post_type', self.ns)

            if post_type is not None:
                post_type_value = post_type.text

                if post_type_value == 'page':
                    self.pages.append(self._parse_item(item, 'page'))
                elif post_type_value == 'post':
                    self.posts.append(self._parse_item(item, 'post'))
                elif post_type_value == 'attachment':
                    self.attachments.append(self._parse_attachment(item))

        return {
            'site': {
                'title': self.site_title,
                'url': self.site_url,
                'description': self.site_description
            },
            'pages': self.pages,
            'posts': self.posts,
            'attachments': self.attachments
        }

    def _parse_item(self, item, item_type):
        """Parse a page or post item"""
        title = item.find('title').text or 'Untitled'
        link = item.find('link').text or ''
        creator = item.find('dc:creator', self.ns)
        creator_name = creator.text if creator is not None else 'Unknown'

        content = item.find('content:encoded', self.ns)
        content_html = content.text if content is not None else ''

        excerpt = item.find('excerpt:encoded', self.ns)
        excerpt_text = excerpt.text if excerpt is not None else ''

        pub_date = item.find('pubDate')
        pub_date_str = pub_date.text if pub_date is not None else ''

        post_name = item.find('wp:post_name', self.ns)
        slug = post_name.text if post_name is not None else self._slugify(title)

        status = item.find('wp:status', self.ns)
        post_status = status.text if status is not None else 'draft'

        return {
            'title': unescape(title),
            'slug': slug,
            'link': link,
            'author': creator_name,
            'content': content_html or '',
            'excerpt': excerpt_text or '',
            'date': pub_date_str,
            'status': post_status,
            'type': item_type
        }

    def _parse_attachment(self, item):
        """Parse an attachment (media file)"""
        title = item.find('title').text or 'Untitled'
        attachment_url = item.find('wp:attachment_url', self.ns)
        url = attachment_url.text if attachment_url is not None else ''

        return {
            'title': unescape(title),
            'url': url,
            'filename': os.path.basename(urlparse(url).path) if url else ''
        }

    def _slugify(self, text):
        """Convert text to URL-friendly slug"""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s-]', '', text)
        text = re.sub(r'[\s-]+', '-', text)
        return text.strip('-')


def create_static_site(data, output_dir='site'):
    """Create static HTML site from parsed WordPress data"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Create directories
    (output_path / 'pages').mkdir(exist_ok=True)
    (output_path / 'posts').mkdir(exist_ok=True)
    (output_path / 'assets').mkdir(exist_ok=True)
    (output_path / 'css').mkdir(exist_ok=True)

    # Save parsed data as JSON for reference
    with open(output_path / 'site-data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Create CSS
    create_css(output_path / 'css' / 'style.css')

    # Create pages
    for page in data['pages']:
        if page['status'] == 'publish':
            create_html_page(page, output_path / 'pages', data['site'])

    # Create posts
    for post in data['posts']:
        if post['status'] == 'publish':
            create_html_page(post, output_path / 'posts', data['site'])

    # Create index page
    create_index(data, output_path)

    # Create attachments list
    with open(output_path / 'attachments.json', 'w', encoding='utf-8') as f:
        json.dump(data['attachments'], f, indent=2, ensure_ascii=False)

    print(f"✓ Static site created in '{output_dir}/'")
    print(f"  - {len([p for p in data['pages'] if p['status'] == 'publish'])} pages")
    print(f"  - {len([p for p in data['posts'] if p['status'] == 'publish'])} posts")
    print(f"  - {len(data['attachments'])} attachments to download")


def create_css(css_path):
    """Create basic CSS stylesheet"""
    css = """
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --text-color: #333;
    --bg-color: #fff;
    --border-color: #ddd;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--bg-color);
}

header {
    background-color: var(--primary-color);
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

header h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

header p {
    opacity: 0.9;
}

nav {
    background-color: #34495e;
    padding: 0.75rem 0;
}

nav ul {
    list-style: none;
    display: flex;
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

nav a {
    color: white;
    text-decoration: none;
    transition: opacity 0.2s;
}

nav a:hover {
    opacity: 0.8;
}

main {
    padding: 2rem 0;
    min-height: 60vh;
}

article {
    background: white;
    padding: 2rem;
    margin-bottom: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

article h1, article h2 {
    color: var(--primary-color);
    margin-bottom: 1rem;
}

article img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
}

.meta {
    color: #7f8c8d;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

footer {
    background-color: var(--primary-color);
    color: white;
    text-align: center;
    padding: 2rem 0;
    margin-top: 3rem;
}

.page-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.page-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.page-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.page-card h3 {
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.page-card a {
    color: var(--secondary-color);
    text-decoration: none;
}

@media (max-width: 768px) {
    nav ul {
        flex-direction: column;
        gap: 0.5rem;
    }

    .page-list {
        grid-template-columns: 1fr;
    }
}
"""
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css.strip())


def create_html_template(title, content, site_info, nav_links=None):
    """Create HTML page from template"""
    if nav_links is None:
        nav_links = [
            ('/', 'Home'),
            ('/pages/about.html', 'About'),
            ('/pages/contact.html', 'Contact')
        ]

    nav_html = '\n'.join([f'            <li><a href="{link}">{text}</a></li>' for link, text in nav_links])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {site_info['title']}</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>{site_info['title']}</h1>
            <p>{site_info['description']}</p>
        </div>
    </header>

    <nav>
        <ul>
{nav_html}
        </ul>
    </nav>

    <main>
        <div class="container">
{content}
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 {site_info['title']}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""


def create_html_page(page, output_dir, site_info):
    """Create individual HTML page"""
    filename = f"{page['slug']}.html"
    filepath = output_dir / filename

    content = f"""            <article>
                <h1>{page['title']}</h1>
                <div class="meta">Published: {page['date']}</div>
                <div class="content">
{page['content']}
                </div>
            </article>"""

    html = create_html_template(page['title'], content, site_info)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)


def create_index(data, output_path):
    """Create index.html homepage"""
    pages_list = ''
    if data['pages']:
        pages_list = '<h2>Pages</h2>\n<div class="page-list">\n'
        for page in data['pages']:
            if page['status'] == 'publish':
                pages_list += f"""    <div class="page-card">
        <h3><a href="/pages/{page['slug']}.html">{page['title']}</a></h3>
        <p>{page['excerpt'][:150] if page['excerpt'] else 'Read more...'}</p>
    </div>\n"""
        pages_list += '</div>\n'

    posts_list = ''
    if data['posts']:
        posts_list = '<h2>Recent Posts</h2>\n<div class="page-list">\n'
        for post in data['posts']:
            if post['status'] == 'publish':
                posts_list += f"""    <div class="page-card">
        <h3><a href="/posts/{post['slug']}.html">{post['title']}</a></h3>
        <p class="meta">{post['date']}</p>
        <p>{post['excerpt'][:150] if post['excerpt'] else 'Read more...'}</p>
    </div>\n"""
        posts_list += '</div>\n'

    content = f"""            <article>
                <h1>Welcome to {data['site']['title']}</h1>
                {pages_list}
                {posts_list}
            </article>"""

    html = create_html_template('Home', content, data['site'])

    with open(output_path / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    xml_file = '/Users/davidrobbins/Desktop/WordPress.2025-11-22.xml'

    print("Parsing WordPress XML...")
    parser = WordPressParser(xml_file)
    data = parser.parse()

    print(f"\nFound:")
    print(f"  - {len(data['pages'])} pages ({len([p for p in data['pages'] if p['status'] == 'publish'])} published)")
    print(f"  - {len(data['posts'])} posts ({len([p for p in data['posts'] if p['status'] == 'publish'])} published)")
    print(f"  - {len(data['attachments'])} attachments")

    print("\nCreating static site...")
    create_static_site(data)

    print("\n✓ Done! Your static site is ready.")
    print("\nNext steps:")
    print("1. Review the generated site in the 'site/' directory")
    print("2. Download attachments using the attachments.json file")
    print("3. Set up GitHub Pages for free hosting")


if __name__ == '__main__':
    main()
