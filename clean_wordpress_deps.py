#!/usr/bin/env python3
"""
Remove WordPress-specific dependencies that don't exist in static export
"""

import os
import re
from pathlib import Path


def clean_html_file(filepath):
    """Remove WordPress-specific dependencies from HTML file"""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    original = content

    # Remove WordPress-specific CSS and JS files that don't exist in static export
    patterns_to_remove = [
        # Gift Up checkout
        r'<link[^>]*id="giftup-checkout-external-css"[^>]*>',
        r'<script[^>]*src="[^"]*gift-up[^"]*"[^>]*></script>',
        # Elementor dynamic loading
        r'<script[^>]*src="[^"]*elementor[^"]*runtime\.min\.js[^"]*"[^>]*></script>',
        r'<script[^>]*src="[^"]*elementor[^"]*webpack[^"]*"[^>]*></script>',
        r'<script[^>]*src="[^"]*frontend[^"]*handlers[^"]*"[^>]*></script>',
        # WordPress specific
        r'<script[^>]*src="[^"]*wp-includes[^"]*"[^>]*></script>',
        r'<link[^>]*href="[^"]*wp-includes[^"]*"[^>]*>',
        # Elementor Pro specific files that cause chunk loading errors
        r'<script[^>]*src="[^"]*elementor-pro[^"]*"[^>]*></script>',
    ]

    for pattern in patterns_to_remove:
        content = re.sub(pattern, "", content, flags=re.IGNORECASE)

    # Remove wp hooks and WordPress JavaScript that causes errors
    content = re.sub(
        r"<script[^>]*>\s*.*?wp\.i18n\.setLocaleData.*?</script>",
        "",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r"<script[^>]*>\s*.*?wp\.apiFetch.*?</script>", "", content, flags=re.DOTALL
    )

    # Only write if changed
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    """Clean all HTML files"""
    fixed_count = 0

    print("Removing WordPress-specific dependencies...")

    for filepath in Path(".").rglob("*.html"):
        # Skip hidden files and git directory
        if "/.git/" in str(filepath) or str(filepath).startswith("."):
            continue

        if clean_html_file(filepath):
            fixed_count += 1
            print(f"✓ Cleaned: {filepath}")

    print(f"\n✓ Done! Cleaned {fixed_count} files")


if __name__ == "__main__":
    main()
