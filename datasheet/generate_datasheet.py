#!/usr/bin/env python3
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (Frame, Image, PageTemplate, Paragraph,
                                SimpleDocTemplate, Spacer, Table)

from company_info import add_company_info
from content import add_all_content
from open_source import add_open_source_section
from specs import add_all_specs
from styles import (create_footer_style, create_normal_style,
                    create_slogan_style, create_title_style)
from utils import (ASSET_ROOT, get_adapter_photo_paths, get_image_size,
                   get_processed_image)
from versioning import add_version_info, get_latest_version_info


def first_page(canvas, doc):
    pass  # Title page intentionally has no footer


def later_pages(canvas, doc):
    page_width, _ = A4
    footer_logo = ASSET_ROOT / 'Gearotons_Logo_and_Gearotons_Name.png'
    logo_width = 35 * mm
    logo_height = get_image_size(footer_logo, logo_width)[1] if footer_logo.exists() else logo_width * 0.3
    logo_x = (page_width - logo_width) / 2
    logo_y = 5 * mm
    if footer_logo.exists():
        canvas.drawImage(str(footer_logo), logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')

    canvas.setFont('Helvetica', 10)
    canvas.drawRightString(page_width - 15 * mm, 8 * mm, str(doc.page))


def _build_hero_section(content_width: float):
    slogan_style = create_slogan_style()
    elements = [
        Paragraph('Affordable and Simple All-in-One Motion Control', slogan_style),
        Paragraph('From Education to Innovation', slogan_style),
        Spacer(1, 8),
    ]

    photo_paths = get_adapter_photo_paths()
    photo_count = len(photo_paths)
    if photo_count:
        column_width = max((content_width - (photo_count - 1) * 6) / photo_count, 10)
        photos = [get_processed_image(path, column_width) for path in photo_paths]
        photo_table = Table([photos], colWidths=[column_width] * photo_count)
        photo_table.hAlign = 'CENTER'
        elements.append(photo_table)
        elements.append(Spacer(1, 4))

    return elements


def _output_filenames(version: str, release_date: str):
    sanitized_date = ''.join(ch for ch in release_date.replace(' ', '_') if ch.isalnum() or ch in ('_', '-'))
    dated = f'rs485_adapter_datasheet_v{version}_{sanitized_date}.pdf'
    latest = 'rs485_adapter_datasheet_latest.pdf'
    return dated, latest


def build_story(content_width: float):
    story = []
    title_style = create_title_style()
    normal_style = create_normal_style()

    story.append(Paragraph('RS485 Adapter – DATASHEET', title_style))
    story.append(Spacer(1, 6))

    logo_path = ASSET_ROOT / 'Gearotons_Logo.png'
    if logo_path.exists():
        logo = get_processed_image(logo_path, 90)
        story.append(logo)
        story.append(Spacer(1, 6))

    story.extend(_build_hero_section(content_width))
    story.append(Spacer(1, 10))

    add_all_content(story, normal_style)
    add_all_specs(story, normal_style)
    add_company_info(story, normal_style)
    add_open_source_section(story, normal_style)
    add_version_info(story, normal_style)

    footer_style = create_footer_style()
    story.append(Spacer(1, 12))
    story.append(Paragraph('© {} Gearotons'.format(datetime.now().year), footer_style))
    return story


def generate_pdf():
    version, release_date = get_latest_version_info()
    dated_filename, latest_filename = _output_filenames(version, release_date)

    doc = SimpleDocTemplate(
        dated_filename,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=6 * mm,
        bottomMargin=10 * mm
    )

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 10 * mm, id='normal')
    doc.addPageTemplates([
        PageTemplate(id='First', frames=frame, onPage=first_page),
        PageTemplate(id='Later', frames=frame, onPage=later_pages),
    ])

    story = build_story(doc.width)
    doc.build(story)
    shutil.copyfile(dated_filename, latest_filename)
    print(f"Generated datasheet: {dated_filename}")
    print(f"Copied latest alias: {latest_filename}")


if __name__ == '__main__':
    generate_pdf()
