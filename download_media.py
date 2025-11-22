#!/usr/bin/env python3
"""
Download WordPress Media Files
Downloads all attachments from the WordPress export
"""

import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse
import urllib.request
import urllib.error


def download_attachments(attachments_file='site/attachments.json', output_dir='site/assets/images'):
    """Download all attachments from the WordPress export"""

    # Load attachments
    with open(attachments_file, 'r', encoding='utf-8') as f:
        attachments = json.load(f)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {len(attachments)} attachments...")

    downloaded = 0
    failed = []

    for i, attachment in enumerate(attachments, 1):
        url = attachment.get('url', '')
        filename = attachment.get('filename', '')

        if not url or not filename:
            continue

        # Create output file path
        output_file = output_path / filename

        # Skip if already exists
        if output_file.exists():
            print(f"[{i}/{len(attachments)}] ✓ Already exists: {filename}")
            downloaded += 1
            continue

        # Download file
        try:
            print(f"[{i}/{len(attachments)}] Downloading: {filename}...", end=' ')

            # Add headers to mimic browser request
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                }
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()

            with open(output_file, 'wb') as f:
                f.write(data)

            print(f"✓ ({len(data)} bytes)")
            downloaded += 1

        except Exception as e:
            print(f"✗ Failed: {e}")
            failed.append({'filename': filename, 'url': url, 'error': str(e)})

    print(f"\n{'='*60}")
    print(f"Downloaded: {downloaded}/{len(attachments)}")

    if failed:
        print(f"Failed: {len(failed)}")
        print("\nFailed downloads:")
        for item in failed[:10]:  # Show first 10 failures
            print(f"  - {item['filename']}: {item['error']}")

        # Save failed list
        with open('site/failed-downloads.json', 'w', encoding='utf-8') as f:
            json.dump(failed, f, indent=2, ensure_ascii=False)
        print(f"\nFull list of failures saved to: site/failed-downloads.json")

    return downloaded, failed


def main():
    print("WordPress Media Downloader")
    print("="*60)

    if not os.path.exists('site/attachments.json'):
        print("Error: site/attachments.json not found!")
        print("Please run parse_wordpress.py first.")
        sys.exit(1)

    downloaded, failed = download_attachments()

    if downloaded > 0:
        print("\n✓ Download complete!")
        print(f"\nMedia files saved to: site/assets/images/")
        print("\nNext steps:")
        print("1. Update image references in HTML files")
        print("2. Test the site locally")
        print("3. Deploy to GitHub Pages")


if __name__ == '__main__':
    main()
