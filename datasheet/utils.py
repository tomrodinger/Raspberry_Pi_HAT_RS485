from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List, Sequence, Tuple

from PIL import Image as PILImage
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.platypus import Flowable, Image, Table, TableStyle

from styles import PRIMARY_COLOR

PROJECT_DIR = Path(__file__).resolve().parent
PCB_ROOT = (PROJECT_DIR.parent / 'PCB').resolve()
ASSET_ROOT = PROJECT_DIR
ADAPTER_PHOTO_ROOT = PROJECT_DIR.parent / 'Pictures' / 'adapter'
ADAPTER_PHOTO_PATHS = [
    ADAPTER_PHOTO_ROOT / 'RS485_adapter_20250714153203.jpg',
    ADAPTER_PHOTO_ROOT / 'RS485_adapter_20250714153158.jpg',
]
VERSION_PATTERN = re.compile(r'^\d+\.\d+(?:\.\d+)*$')
SCHEMATIC_SUBDIR = 'schematic'
SCHEMATIC_SUFFIX = '-index-schTop.pdf'


class PDFPageFlowable(Flowable):
    """Embed a PDF page (vector) into the ReportLab story using pdfrw."""
    def __init__(self, pdf_path: Path, target_width: float):
        super().__init__()
        self.pdf_path = pdf_path
        self.xobj = pagexobj(PdfReader(str(pdf_path)).pages[0])
        bbox = self.xobj.BBox
        self.original_width = float(bbox[2]) - float(bbox[0])
        self.original_height = float(bbox[3]) - float(bbox[1])
        self.scale = target_width / self.original_width
        self.target_width = target_width
        self.target_height = self.original_height * self.scale

    def wrap(self, availWidth, availHeight):
        return self.target_width, self.target_height

    def drawOn(self, canvas, x, y, _sW=0):
        canvas.saveState()
        xobj_name = makerl(canvas, self.xobj)
        canvas.translate(x, y)
        canvas.scale(self.scale, self.scale)
        canvas.doForm(xobj_name)
        canvas.restoreState()


def _fatal(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def read_text_file(path: Path, default: str = '') -> str:
    try:
        return path.read_text(encoding='utf-8').strip()
    except FileNotFoundError:
        return default.strip()


def read_lines(path: Path) -> List[str]:
    try:
        return [line.strip() for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    except FileNotFoundError:
        return []


def read_features(filename: str = 'features.txt') -> List[str]:
    return read_lines(ASSET_ROOT / filename)


def get_image_size(image_path: Path, target_width: float) -> Tuple[float, float]:
    with PILImage.open(image_path) as img:
        width, height = img.size
    scale = target_width / float(width)
    return target_width, height * scale


def get_processed_image(image_path: Path, target_width: float) -> Image:
    width, height = get_image_size(image_path, target_width)
    img = Image(str(image_path), width=width, height=height)
    img.hAlign = 'CENTER'
    return img


def get_adapter_photo_paths() -> List[Path]:
    ensure_photo_root()
    missing = [path for path in ADAPTER_PHOTO_PATHS if not path.exists()]
    if missing:
        formatted = '\n  - '.join(str(path) for path in missing)
        _fatal(
            "Adapter hero photo(s) missing. Ensure the files exist at the requested absolute paths:\n"
            f"  - {formatted}"
        )
    return ADAPTER_PHOTO_PATHS


def create_data_table(data: Sequence[Sequence[str]], col_widths: Sequence[float]) -> Table:
    table = Table(data, colWidths=col_widths, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, (0.6, 0.6, 0.6)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return table


def ensure_photo_root():
    if not ADAPTER_PHOTO_ROOT.exists():
        _fatal(f"Adapter photo directory missing: {ADAPTER_PHOTO_ROOT}")
    if not ADAPTER_PHOTO_ROOT.is_dir():
        _fatal(f"Adapter photo path must be a directory: {ADAPTER_PHOTO_ROOT}")


def load_json(path: Path) -> dict:
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def parse_version(version: str) -> Tuple[int, ...]:
    return tuple(int(part) for part in version.split('.'))


def list_version_directories(base_dir: Path = PCB_ROOT) -> List[Tuple[Tuple[int, ...], str, Path]]:
    if not base_dir.exists():
        _fatal(f"PCB directory not found: {base_dir}")
    entries: List[Tuple[Tuple[int, ...], str, Path]] = []
    for candidate in base_dir.iterdir():
        if candidate.is_dir() and VERSION_PATTERN.match(candidate.name):
            entries.append((parse_version(candidate.name), candidate.name, candidate))
    if not entries:
        _fatal(f"No versioned PCB directories found in {base_dir}")
    entries.sort()
    return entries


def find_latest_version_dir(base_dir: Path = PCB_ROOT) -> Tuple[str, Path]:
    version_info = list_version_directories(base_dir)[-1]
    _, version_str, version_path = version_info
    return version_str, version_path


def get_expected_schematic_path(version_dir: Path, version_str: str) -> Path:
    schematic_path = version_dir / SCHEMATIC_SUBDIR / f"{version_str}{SCHEMATIC_SUFFIX}"
    if schematic_path.exists():
        return schematic_path
    available = sorted(map(str, (version_dir / SCHEMATIC_SUBDIR).glob('*index-schTop*.pdf'))) if (version_dir / SCHEMATIC_SUBDIR).exists() else []
    message_lines = [
        f"Missing schematic PDF: {schematic_path}",
        f"The schematic filename must match the directory version ({version_str}).",
        "Please export the schematic from KiCAD with the required name and try again."
    ]
    if available:
        message_lines.insert(1, f"Available candidates were ignored (version mismatch): {available}")
    _fatal('\n'.join(message_lines))
    return schematic_path  # Unreachable


def get_schematic_flowable(content_width: float) -> Tuple[Flowable, str, Path]:
    version_str, version_dir = find_latest_version_dir()
    schematic_path = get_expected_schematic_path(version_dir, version_str)
    flowable = PDFPageFlowable(schematic_path, content_width)
    return flowable, version_str, schematic_path


def ensure_connection_diagram_available(filename: str = 'connection_diagram.jpg') -> Path:
    path = ASSET_ROOT / filename
    if not path.exists():
        _fatal(f"Connection diagram missing: {path}. Please create a symlink to the real asset.")
    if path.is_symlink():
        target = path.resolve()
        if target.is_symlink():
            _fatal(f"Connection diagram symlink must point to a real file, but points to another symlink: {path}")
    return path