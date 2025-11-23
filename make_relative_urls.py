#!/usr/bin/env python3
"""
Convert absolute URLs to relative URLs for GitHub Pages compatibility
This makes the site work on both local (localhost:8000) and GitHub Pages (username.github.io/repo/)
"""

import os
import re
from pathlib import Path


def get_relative_depth(filepath):
    """Calculate how many levels deep a file is from root"""
    # Count the number of directory separators
    parts = Path(filepath).parts
    # Exclude the filename itself
    return len(parts) - 1


def fix_html_file(filepath):
    """Convert absolute URLs to relative URLs in HTML file"""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    original = content
    depth = get_relative_depth(filepath)

    # Create the relative path prefix (../ for each level deep)
    if depth == 0:
        prefix = "."  # Root level - no prefix needed for GitHub Pages
    else:
        prefix = "../" * depth
        prefix = prefix.rstrip("/")

    # For root level files, use empty prefix to avoid ./
    if depth == 0:
        url_prefix = ""
    else:
        url_prefix = prefix + "/"

    # Fix href and src attributes that start with /
    # But don't change external URLs (http://, https://, mailto:, tel:, etc.)
    content = re.sub(
        r'(href|src)="/((?!http|https|mailto|tel|#))', rf'\1="{url_prefix}\2', content
    )

    # Fix CSS url() functions that start with /
    content = re.sub(
        r'url\("/((?!http|https|mailto|tel|#))', rf'url("{url_prefix}\1', content
    )

    # Fix CSS url() functions that start with /
    content = re.sub(
        r'url\("/((?!http|https|mailto|tel|#))', rf'url("{prefix}/\1', content
    )

    # Only write if changed
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    """Fix all HTML files"""
    fixed_count = 0

    print("Converting absolute URLs to relative URLs...")
    print("This makes the site work on both localhost and GitHub Pages!\n")

    for filepath in Path(".").rglob("*.html"):
        # Skip hidden files and git directory
        if "/.git/" in str(filepath) or str(filepath).startswith("."):
            continue

        if fix_html_file(filepath):
            fixed_count += 1
            print(f"✓ Fixed: {filepath}")

    print(f"\n✓ Done! Fixed {fixed_count} files")
    print("\nThe site will now work at:")
    print("  - http://localhost:8000 (local testing)")
    print("  - https://darobbins85.github.io/modernmothershelper/ (GitHub Pages)")


if __name__ == "__main__":
    main()
