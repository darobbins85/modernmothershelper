#!/usr/bin/env python3
"""
Fix hardcoded WordPress domain links
"""

import re
from pathlib import Path

def fix_file(filepath):
    """Fix hardcoded domain in a single file"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original = content

    # Calculate depth for relative path
    depth = len(Path(filepath).parts) - 1
    if depth == 0:
        home_link = "."
    else:
        home_link = "../" * depth
        home_link = home_link.rstrip('/')

    # Replace hardcoded WordPress URLs with relative home link
    content = re.sub(
        r'href="https?://(www\.)?modernmothershelper\.com/"',
        f'href="{home_link}/"',
        content
    )

    # Only write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    fixed = 0
    print("Fixing hardcoded WordPress domain links...")

    for filepath in Path('.').rglob('*.html'):
        if '/.git/' in str(filepath):
            continue
        if fix_file(filepath):
            fixed += 1
            print(f"✓ {filepath}")

    print(f"\n✓ Fixed {fixed} files")

if __name__ == '__main__':
    main()
