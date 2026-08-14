"""Builders for screenplay files in each supported container format.

The same two-scene screenplay is produced in every format, so the importer
tests can assert that all roads lead to the same film model.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

# One screenplay, expressed once, rendered into every format below.
SCENES = [
    (
        "WN. MAGAZYN_01 - DZIEŃ",
        "POSTAĆ_01 wchodzi między regały.",
        [("POSTAĆ_01", "(cicho)", "Mam to.")],
    ),
    (
        "PL. NABRZEŻE_01 - NOC",
        "POSTAĆ_01 biegnie wzdłuż nabrzeża.",
        [("POSTAĆ_01", None, "Nic jej nie będzie."), ("POSTAĆ_02", None, "Zobaczymy.")],
    ),
]

TITLE = "SCENARIUSZ TESTOWY"


def write_fountain(path: Path) -> Path:
    lines = [f"Title: {TITLE}", ""]
    for heading, action, dialogue in SCENES:
        lines += [heading, "", action, ""]
        for speaker, parenthetical, text in dialogue:
            lines.append(speaker)
            if parenthetical:
                lines.append(parenthetical)
            lines += [text, ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_fdx(path: Path) -> Path:
    def paragraph(kind: str, text: str) -> str:
        escaped = text.replace("&", "&amp;").replace("<", "&lt;")
        return f'<Paragraph Type="{kind}"><Text>{escaped}</Text></Paragraph>'

    body = [
        "<?xml version='1.0' encoding='UTF-8'?>",
        '<FinalDraft DocumentType="Script" Version="5">',
        "<Content>",
    ]
    for heading, action, dialogue in SCENES:
        body.append(paragraph("Scene Heading", heading))
        body.append(paragraph("Action", action))
        for speaker, parenthetical, text in dialogue:
            body.append(paragraph("Character", speaker))
            if parenthetical:
                body.append(paragraph("Parenthetical", parenthetical))
            body.append(paragraph("Dialogue", text))
        # Final Draft writes this at page breaks; it must not reach the model.
        body.append(paragraph("Dialogue", "(MORE)"))
    body += [
        "</Content>",
        f"<TitlePage><Content>{paragraph('General', TITLE)}</Content></TitlePage>",
        "</FinalDraft>",
    ]
    path.write_text("\n".join(body), encoding="utf-8")
    return path


def write_celtx(path: Path) -> Path:
    html = ["<html><body>"]
    for heading, action, dialogue in SCENES:
        html.append(f'<p class="sceneheading">{heading}</p>')
        html.append(f'<p class="action">{action}</p>')
        for speaker, parenthetical, text in dialogue:
            html.append(f'<p class="character">{speaker}</p>')
            if parenthetical:
                html.append(f'<p class="parenthetical">{parenthetical}</p>')
            html.append(f'<p class="dialog">{text}</p>')
    html.append("</body></html>")
    document = "\n".join(html)

    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("project.rdf", "<rdf:RDF/>")
        archive.writestr("notes.html", "<html><body><p>Notatki</p></body></html>")
        archive.writestr("script-01.html", document)
    return path


def write_docx(path: Path, *, styled: bool) -> Path:
    """Write a .docx, either with screenplay styles or as plain paragraphs."""
    w = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

    def paragraph(style: str | None, text: str) -> str:
        escaped = text.replace("&", "&amp;").replace("<", "&lt;")
        properties = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
        return f"<w:p>{properties}<w:r><w:t>{escaped}</w:t></w:r></w:p>"

    parts = [f'<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="{w}"><w:body>']
    for heading, action, dialogue in SCENES:
        parts.append(paragraph("SceneHeading" if styled else None, heading))
        parts.append(paragraph("Action" if styled else None, action))
        for speaker, parenthetical, text in dialogue:
            parts.append(paragraph("Character" if styled else None, speaker))
            if parenthetical:
                parts.append(paragraph("Parenthetical" if styled else None, parenthetical))
            parts.append(paragraph("Dialogue" if styled else None, text))
    parts.append("</w:body></w:document>")

    content_types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="xml" ContentType="application/xml"/>'
        "</Types>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("word/document.xml", "".join(parts))
    return path


def write_pdf(path: Path, lines: list[str]) -> Path:
    """Write a minimal single-page PDF containing ``lines`` as text.

    Hand-built rather than generated, so the test suite needs no PDF
    writer. Courier and WinAnsi keep it to characters the encoding covers.
    """
    escaped = [line.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)") for line in lines]
    body = "\n".join(f"({line}) Tj T*" for line in escaped)
    stream = f"BT /F1 12 Tf 72 720 Td 14 TL\n{body}\nET"

    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>",
    ]

    out = "%PDF-1.4\n"
    offsets = []
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n{obj}\nendobj\n"

    xref_offset = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n"
    out += "".join(f"{offset:010d} 00000 n \n" for offset in offsets)
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n"
    )

    path.write_bytes(out.encode("latin-1"))
    return path
