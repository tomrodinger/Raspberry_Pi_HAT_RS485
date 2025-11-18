from __future__ import annotations

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Spacer, Table

from styles import create_heading_style, create_table_style, create_normal_style

CONTENT_MARGIN = 18 * mm


def _content_width() -> float:
    page_width, _ = A4
    return page_width - 2 * CONTENT_MARGIN


def _simple_table(data):
    widths = [_content_width() * 0.3, _content_width() * 0.7]
    table = Table(data, colWidths=widths, hAlign='LEFT')
    table.setStyle(create_table_style())
    return table


def add_electrical_specs(story, normal_style):
    heading = create_heading_style()
    normal = create_normal_style()
    story.append(PageBreak())
    elements = [
        Paragraph('Electrical Specifications', heading),
        Spacer(1, 4)
    ]

    data = [
        ['Parameter', 'Specification'],
        ['Supply Voltage', Paragraph('5V nominal when powered via USB (up to 6V max) or can be powered with 3.3V or 5V from your project\'s power supply rail.', normal)],
        ['Typical Current Draw', Paragraph('To be determined', normal)],
        ['Supported Baud Rates', Paragraph('Up to 1 Mbps is tested and supported', normal)],
        ['ESD Protection', Paragraph('±8 kV (air or contact) on USB and headers. Components on the PCB are not protected, so use ESD straps or place the board into an enclosure.', normal)],
    ]

    elements.append(_simple_table(data))
    elements.append(Spacer(1, 8))
    story.append(KeepTogether(elements))


def add_interface_specs(story, normal_style):
    heading = create_heading_style()
    normal = create_normal_style()
    elements = [
        Paragraph('Interface & Connectivity', heading),
        Spacer(1, 4)
    ]

    data = [
        ['Connector', 'Details'],
        ['Bus Terminals', Paragraph('Two sets of A, B, GND on a 2.54 mm header for field wiring', normal)],
        ['Host Interface', Paragraph('USB, Raspberry Pi header stacking, and jumper wire area (GND/TX/RX) for boards like Arduino or ESP32', normal)],
        ['Status Indicators', Paragraph('Power LED (yellow), transmit LED (red) and receive LED (green)', normal)],
    ]

    elements.append(_simple_table(data))
    elements.append(Spacer(1, 8))
    story.append(KeepTogether(elements))


def add_mechanical_specs(story, normal_style):
    heading = create_heading_style()
    normal = create_normal_style()
    elements = [
        Paragraph('Mechanical Details', heading),
        Spacer(1, 4)
    ]

    data = [
        ['Parameter', 'Value'],
        ['Physical Dimensions', Paragraph('46.2 mm x 30.9 mm. Thickness at thickest point is 11 mm.', normal)],
        ['PCB Thickness', Paragraph('1.6 mm.', normal)],
        ['Weight', Paragraph('To be determined', normal)],
        ['Environmental Rating', Paragraph('0 °C to 60 °C, non-condensing', normal)],
    ]

    elements.append(_simple_table(data))
    elements.append(Spacer(1, 8))
    story.append(KeepTogether(elements))


def add_all_specs(story, normal_style):
    add_electrical_specs(story, normal_style)
    add_interface_specs(story, normal_style)
    add_mechanical_specs(story, normal_style)
