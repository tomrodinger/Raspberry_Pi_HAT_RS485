from __future__ import annotations

from pathlib import Path

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Flowable, KeepTogether, PageBreak, Paragraph, Spacer

from styles import create_feature_style, create_heading_style
from utils import (
    ASSET_ROOT,
    ensure_connection_diagram_available,
    get_processed_image,
    get_schematic_flowable,
    read_features,
    read_text_file,
)

CONTENT_MARGIN = 18 * mm


def _content_width() -> float:
    page_width, _ = A4
    return page_width - 2 * CONTENT_MARGIN


class IconLink(Flowable):
    LINK_COLOR = (
        52 / 255,
        168 / 255,
        83 / 255,
    )

    def __init__(self, icon_path: str, text: str, url: str, width: float):
        super().__init__()
        self.icon_path = icon_path
        self.text = text
        self.url = url
        self.width = width
        self.height = 32

    def wrap(self, *args):
        return self.width, self.height

    def draw(self):
        icon_size = 24
        text_x = (self.width - icon_size) / 2 + icon_size + 6

        self.canv.drawImage(self.icon_path, (self.width - icon_size) / 2 - 6, 4, icon_size, icon_size, mask='auto')

        self.canv.setFont('Helvetica', 13)
        self.canv.setFillColorRGB(*self.LINK_COLOR)
        text_width = self.canv.stringWidth(self.text, 'Helvetica', 13)
        self.canv.drawString(text_x, 10, self.text)

        self.canv.linkURL(self.url, (text_x, 4, text_x + text_width, 24), relative=1)


def add_introduction(story, normal_style):
    text = read_text_file(ASSET_ROOT / 'introduction.txt', default='(Add RS485 overview in introduction.txt)')
    story.append(Paragraph('RS485 Adapter Overview', create_heading_style()))
    story.append(Paragraph(text, normal_style))
    story.append(Spacer(1, 8))


def add_features(story, normal_style):
    story.append(PageBreak())
    story.append(Paragraph('Key Features', create_heading_style()))
    feature_style = create_feature_style()
    features = read_features()
    if not features:
        features = ['Add feature lines inside features.txt']
    for feature in features:
        story.append(Paragraph(feature, feature_style))
    story.append(Spacer(1, 8))


def add_connection_diagram(story, normal_style):
    story.append(PageBreak())
    story.append(Paragraph('Connection Diagram', create_heading_style()))
    diagram_path = ensure_connection_diagram_available()
    diagram = get_processed_image(diagram_path, _content_width())
    story.append(KeepTogether([diagram]))
    story.append(Spacer(1, 8))


def add_schematic_section(story, normal_style):
    story.append(PageBreak())
    story.append(Paragraph('Schematic Diagram', create_heading_style()))
    schematic_img, version_str, schematic_path = get_schematic_flowable(_content_width())
    story.append(KeepTogether([schematic_img]))
    story.append(Spacer(1, 8))


def add_getting_started(story, normal_style):
    story.append(Paragraph('Getting Started', create_heading_style()))
    story.append(Paragraph(
        'Follow our online quickstart to wire the adapter and use it with Gearotons servomotors.',
        normal_style
    ))
    story.append(Spacer(1, 4))
    icon_link = IconLink(
        'click_here.png',
        'tutorial.gearotons.com',
        'https://tutorial.gearotons.com',
        _content_width()
    )
    story.append(icon_link)
    story.append(Spacer(1, 8))


def add_feedback(story, normal_style):
    story.append(Paragraph('Feedback and Support', create_heading_style()))
    story.append(Paragraph(
        'Spotted an error or need help? Send feedback through our portal so we can keep the datasheet accurate for every class.',
        normal_style
    ))
    story.append(Spacer(1, 4))
    icon_link = IconLink(
        'click_here.png',
        'tutorial.gearotons.com/feedback',
        'https://tutorial.gearotons.com/feedback',
        _content_width()
    )
    story.append(icon_link)
    story.append(Spacer(1, 8))


def add_all_content(story, normal_style):
    add_introduction(story, normal_style)
    add_features(story, normal_style)
    add_connection_diagram(story, normal_style)
    add_schematic_section(story, normal_style)
    add_getting_started(story, normal_style)
    add_feedback(story, normal_style)
