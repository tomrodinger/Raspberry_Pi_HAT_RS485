from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Tuple

from reportlab.platypus import Paragraph, Spacer

DATA_DIR = Path(__file__).resolve().parent
VERSIONS_FILE = DATA_DIR / 'versions.txt'
DEFAULT_VERSION = ("1.0", "Unknown")


def _parse_line(line: str) -> Tuple[str, str]:
    parts = [segment.strip() for segment in line.split(',', 1)]
    if len(parts) != 2 or not parts[0]:
        return DEFAULT_VERSION
    return parts[0], parts[1]


def get_latest_version_info() -> Tuple[str, str]:
    if not VERSIONS_FILE.exists():
        return DEFAULT_VERSION[0], datetime.now().strftime('%Y-%m-%d')
    lines = [line.strip() for line in VERSIONS_FILE.read_text(encoding='utf-8').splitlines() if line.strip()]
    for line in reversed(lines):
        version, date = _parse_line(line)
        if version != DEFAULT_VERSION[0] or date != DEFAULT_VERSION[1]:
            return version, date if date.lower() != 'unknown' else datetime.now().strftime('%Y-%m-%d')
    return DEFAULT_VERSION[0], datetime.now().strftime('%Y-%m-%d')


def add_version_info(story, style):
    version, release_date = get_latest_version_info()
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Datasheet Version: {version}   Release Date: {release_date}", style))
    story.append(Spacer(1, 12))
