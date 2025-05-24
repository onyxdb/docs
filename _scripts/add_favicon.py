#!/usr/bin/env python3
# Copied from https://gist.github.com/Deimvis/75b49330c6a9b9fb66c998ed8118d1fb
import os
import shutil
import sys
from pathlib import Path

from bs4 import BeautifulSoup


def add_favicon(html_file: Path, favicon_file: Path):
    with html_file.open('r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    if soup.find("link", rel="icon"):
        return
    
    new_favicon_tag = soup.new_tag("link", rel="icon", href='/'+favicon_file.name, type=f"image/{favicon_file.suffix[1:]}")
    
    head_tag = soup.head
    if head_tag:
        head_tag.append(new_favicon_tag)
    else:
        head_tag = soup.new_tag("head")
        soup.html.insert(0, head_tag)
        head_tag.append(new_favicon_tag)
    
    with html_file.open('w') as f:
        f.write(str(soup))


def process_html(html_dir: Path, favicon_file: Path):
    for root, _, files in os.walk(html_dir.absolute()):
        for f in files:
            if f.endswith(".html"):
                html_file = Path(os.path.join(root, f))
                add_favicon(html_file, favicon_file)


def main():
    assert len(sys.argv) == 3, f'Incorrect number of arguments: {len(sys.argv)-1}, expected: 2'
    html_dir = Path(sys.argv[1])
    favicon_file  = Path(sys.argv[2])
    assert html_dir.is_dir()
    assert favicon_file.is_file()
    assert favicon_file.suffix != ''
    
    shutil.copy(favicon_file, html_dir / favicon_file.name)
    process_html(html_dir, favicon_file)


if __name__ == '__main__':
    main()
