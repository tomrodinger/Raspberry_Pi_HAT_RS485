from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, Paragraph, Spacer, Table

from content import IconLink
from styles import create_heading_style
from utils import get_processed_image


def add_open_source_section(story, normal_style):
    elements = []
    heading = create_heading_style()
    elements.append(Paragraph('Open Source', heading))
    elements.append(Spacer(1, 4))

    elements.append(Paragraph(
        'We share the firmware and KiCAD files so you can modify, remix, or study every part of the RS485 adapter.',
        normal_style
    ))
    elements.append(Spacer(1, 6))

    page_width = 595.27  # A4 width points
    margin = 18 * mm
    content_width = page_width - 2 * margin

    icon_link = IconLink(
        'click_here.png',
        'github.com/tomrodinger/Raspberry_Pi_HAT_RS485',
        'https://github.com/tomrodinger/Raspberry_Pi_HAT_RS485',
        content_width * 0.7
    )
    elements.append(icon_link)
    elements.append(Spacer(1, 6))

    base_width = 170 * mm * 0.3
    hw_logo = get_processed_image('Open-source-hardware-logo.svg.png', base_width * 0.5)
    osi_logo = get_processed_image('Open_Source_Initiative.svg.png', base_width * 0.4)

    logo_table = Table([[hw_logo, osi_logo]], colWidths=[hw_logo.drawWidth + 10, osi_logo.drawWidth + 10])
    logo_table.hAlign = 'CENTER'
    elements.append(logo_table)
    elements.append(Spacer(1, 8))

    story.append(KeepTogether(elements))
