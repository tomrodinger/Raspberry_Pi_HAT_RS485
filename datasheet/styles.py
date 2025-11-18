from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import TableStyle

PRIMARY_COLOR = colors.HexColor('#003049')
SECONDARY_COLOR = colors.HexColor('#669bbc')
LINK_COLOR = colors.HexColor('#34a853')
SERVOMOTOR_SLOGAN_COLOR = colors.HexColor('#34a853')
TEXT_COLOR = colors.HexColor('#222222')


def create_title_style():
    return ParagraphStyle(
        'Title',
        parent=getSampleStyleSheet()['Heading1'],
        fontSize=24,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=18
    )


def create_subtitle_style():
    return ParagraphStyle(
        'Subtitle',
        parent=getSampleStyleSheet()['Heading2'],
        fontSize=16,
        textColor=SECONDARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=6
    )


def create_slogan_style():
    return ParagraphStyle(
        'Slogan',
        parent=getSampleStyleSheet()['Heading2'],
        fontSize=16,
        textColor=SERVOMOTOR_SLOGAN_COLOR,
        alignment=TA_CENTER,
        spaceBefore=2,
        spaceAfter=2,
        leading=18
    )


def create_heading_style():
    return ParagraphStyle(
        'SectionHeading',
        parent=getSampleStyleSheet()['Heading2'],
        fontSize=14,
        textColor=PRIMARY_COLOR,
        spaceBefore=12,
        spaceAfter=6
    )


def create_normal_style():
    return ParagraphStyle(
        'Body',
        parent=getSampleStyleSheet()['Normal'],
        fontSize=10,
        textColor=TEXT_COLOR,
        leading=14
    )


def create_feature_style():
    return ParagraphStyle(
        'Feature',
        parent=getSampleStyleSheet()['Normal'],
        fontSize=10,
        textColor=TEXT_COLOR,
        leading=14,
        bulletText='•',
        bulletFontSize=12,
        leftIndent=18,
        firstLineIndent=0,
        spaceBefore=2,
        spaceAfter=2
    )


def create_link_style():
    return ParagraphStyle(
        'Link',
        parent=getSampleStyleSheet()['Normal'],
        fontSize=13,
        textColor=LINK_COLOR,
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=8
    )


def create_footer_style():
    return ParagraphStyle(
        'Footer',
        parent=getSampleStyleSheet()['Normal'],
        fontSize=9,
        textColor=colors.gray,
        alignment=TA_CENTER
    )


def create_table_style():
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ])
