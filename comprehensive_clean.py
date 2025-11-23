#!/usr/bin/env python3
"""
Comprehensive WordPress dependency removal for static sites
"""

import os
import re
from pathlib import Path


def clean_html_file(filepath):
    """Remove WordPress-specific dependencies from HTML file"""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    original = content

    # Remove Elementor Pro frontend config
    content = re.sub(
        r'<script[^>]*id="elementor-pro-frontend-js-before"[^>]*>.*?</script>',
        "",
        content,
        flags=re.DOTALL,
    )

    # Remove Elementor frontend config
    content = re.sub(
        r'<script[^>]*id="elementor-frontend-js-before"[^>]*>.*?</script>',
        "",
        content,
        flags=re.DOTALL,
    )

    # Remove all WordPress plugin references
    patterns_to_remove = [
        r'<link[^>]*href="[^"]*gift-up[^"]*"[^>]*>',
        r'<script[^>]*src="[^"]*gift-up[^"]*"[^>]*></script>',
        r'<script[^>]*src="[^"]*wp-includes[^"]*"[^>]*></script>',
        r'<link[^>]*href="[^"]*wp-includes[^"]*"[^>]*>',
        r'<script[^>]*src="[^"]*elementor-pro[^"]*"[^>]*></script>',
        r'<script[^>]*src="[^"]*elementor[^"]*runtime\.min\.js[^"]*"[^>]*></script>',
        r'<script[^>]*src="[^"]*elementor[^"]*webpack[^"]*"[^>]*></script>',
        r'<script[^>]*src="[^"]*frontend[^"]*handlers[^"]*"[^>]*></script>',
    ]

    for pattern in patterns_to_remove:
        content = re.sub(pattern, "", content, flags=re.IGNORECASE)

    # Remove WordPress JavaScript that causes errors
    content = re.sub(
        r"<script[^>]*>\s*.*?wp\.i18n\.setLocaleData.*?</script>",
        "",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r"<script[^>]*>\s*.*?wp\.apiFetch.*?</script>", "", content, flags=re.DOTALL
    )
    content = re.sub(
        r"<script[^>]*>[^<]*wp-admin[^<]*</script>", "", content, flags=re.IGNORECASE
    )
    content = re.sub(
        r"<script[^>]*>[^<]*wp-json[^<]*</script>", "", content, flags=re.IGNORECASE
    )

    # Remove any remaining scripts that reference wp
    content = re.sub(
        r"<script[^>]*>[^<]*wp\.[^<]*</script>", "", content, flags=re.IGNORECASE
    )

    # Fix font paths - replace local fonts with Google Fonts
    content = re.sub(
        r'<link[^>]*href="[^"]*wp-content/uploads/elementor/google-fonts/[^"]*"[^>]*>',
        "",
        content,
        flags=re.IGNORECASE,
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

    print("Removing WordPress dependencies...")

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
