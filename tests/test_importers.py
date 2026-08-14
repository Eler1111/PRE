"""Import adapters.

The same screenplay is written into every supported container format, and
each one has to produce the same film model — that is the whole point of
having adapters rather than one parser per format.
"""

from __future__ import annotations

import pytest

from pre.analysis import import_screenplay
from pre.importers import importer_for, supported_extensions
from pre.importers.pdf import restore_paragraph_breaks, strip_page_furniture
from pre.queries import find_entity, list_scenes, scenes_with_entity

from . import builders


@pytest.fixture(params=["fountain", "fdx", "celtx", "docx_styled", "docx_plain"])
def screenplay_file(request, tmp_path):
    """The same two-scene screenplay in each structured format."""
    builder = {
        "fountain": lambda p: builders.write_fountain(p / "scenariusz.fountain"),
        "fdx": lambda p: builders.write_fdx(p / "scenariusz.fdx"),
        "celtx": lambda p: builders.write_celtx(p / "scenariusz.celtx"),
        "docx_styled": lambda p: builders.write_docx(p / "scenariusz.docx", styled=True),
        "docx_plain": lambda p: builders.write_docx(p / "scenariusz.docx", styled=False),
    }[request.param]
    return builder(tmp_path)


def test_every_format_produces_the_same_model(project, screenplay_file):
    import_screenplay(project, screenplay_file)

    scenes = list_scenes(project)
    assert [scene["heading_raw"] for scene in scenes] == [
        "WN. MAGAZYN_01 - DZIEŃ",
        "PL. NABRZEŻE_01 - NOC",
    ]
    assert [scene["time_of_day"] for scene in scenes] == ["DAY", "NIGHT"]
    assert [scene["int_ext"] for scene in scenes] == ["INT", "EXT"]

    character = find_entity(project, "POSTAĆ_01", "CHARACTER")
    assert character is not None
    speaking = [
        row for row in scenes_with_entity(project, character["id"]) if row["speaks"]
    ]
    assert len(speaking) == 2


def test_every_format_keeps_the_original_file(project, screenplay_file):
    import_screenplay(project, screenplay_file)
    copies = list(project.script_dir.iterdir())
    assert len(copies) == 1
    assert copies[0].read_bytes() == screenplay_file.read_bytes()


@pytest.mark.parametrize(
    "name,expected",
    [
        ("a.fountain", "FOUNTAIN"),
        ("a.txt", "TXT"),
        ("a.fdx", "FDX"),
        ("a.celtx", "CELTX"),
        ("a.docx", "DOCX"),
        ("a.pdf", "PDF"),
    ],
)
def test_routes_each_extension_to_its_importer(tmp_path, name, expected):
    assert importer_for(tmp_path / name).format_name == expected


def test_supported_extensions_are_listed_for_the_user():
    assert set(supported_extensions()) == {
        ".celtx", ".docx", ".fdx", ".fountain", ".pdf", ".spmd", ".txt"
    }


@pytest.mark.parametrize(
    "name,hint",
    [
        ("scenariusz.doc", "zapisz dokument jako .docx"),
        ("scenariusz.rtf", "wyeksportuj scenariusz"),
    ],
)
def test_refuses_near_miss_formats_with_a_usable_hint(tmp_path, name, hint):
    with pytest.raises(ValueError) as exc:
        importer_for(tmp_path / name)
    assert hint in str(exc.value).lower()


# ---------------------------------------------------------------- Final Draft


def test_fdx_reads_the_title_page(project, tmp_path):
    result = import_screenplay(project, builders.write_fdx(tmp_path / "s.fdx"))
    row = project.connection.execute(
        "SELECT title FROM script WHERE id = ?", (result.script_id,)
    ).fetchone()
    assert row["title"] == builders.TITLE


def test_fdx_page_break_markers_do_not_become_dialogue(project, tmp_path):
    import_screenplay(project, builders.write_fdx(tmp_path / "s.fdx"))
    lines = project.connection.execute("SELECT text FROM dialogue_line").fetchall()
    assert "(MORE)" not in {row["text"] for row in lines}


def test_fdx_rejects_a_file_it_cannot_parse(project, tmp_path):
    broken = tmp_path / "broken.fdx"
    broken.write_text("<FinalDraft><Content>", encoding="utf-8")
    with pytest.raises(ValueError, match="Final Draft"):
        import_screenplay(project, broken)


# ---------------------------------------------------------------------- Celtx


def test_celtx_picks_the_script_not_the_notes(project, tmp_path):
    import_screenplay(project, builders.write_celtx(tmp_path / "s.celtx"))
    # The container also holds a notes document, which is not the screenplay.
    assert len(list_scenes(project)) == 2


def test_celtx_reads_exported_html_saved_with_the_celtx_extension(project, tmp_path):
    exported = tmp_path / "eksport.celtx"
    exported.write_text(
        '<html><body><p class="sceneheading">WN. MAGAZYN_01 - DZIEŃ</p>'
        '<p class="action">Wchodzi.</p>'
        '<p class="character">POSTAĆ_01</p>'
        '<p class="dialog">Mam to.</p></body></html>',
        encoding="utf-8",
    )
    import_screenplay(project, exported)
    assert len(list_scenes(project)) == 1


def test_celtx_rejects_a_container_without_a_script(project, tmp_path):
    import zipfile

    empty = tmp_path / "pusty.celtx"
    with zipfile.ZipFile(empty, "w") as archive:
        archive.writestr("project.rdf", "<rdf:RDF/>")
    with pytest.raises(ValueError, match="Celtx"):
        import_screenplay(project, empty)


# ----------------------------------------------------------------------- Word


def test_docx_rejects_the_legacy_doc_format(project, tmp_path):
    legacy = tmp_path / "stary.docx"
    legacy.write_bytes(b"\xd0\xcf\x11\xe0not a zip")
    with pytest.raises(ValueError, match="Word"):
        import_screenplay(project, legacy)


# ------------------------------------------------------------------------ PDF


def test_pdf_import_end_to_end(project, tmp_path):
    pdf = builders.write_pdf(
        tmp_path / "scenariusz.pdf",
        [
            "WN. MAGAZYN_01 - DZIEN",
            "POSTAC_01 wchodzi miedzy regaly. " + "Tekst wypelniajacy strone. " * 12,
            "                    POSTAC_01",
            "               Mam to.",
            "Odchodzi do drzwi.",
            "12.",
            "PL. NABRZEZE_01 - NOC",
            "POSTAC_01 biegnie. " + "Dalszy opis sceny. " * 12,
        ],
    )
    import_screenplay(project, pdf)

    scenes = list_scenes(project)
    assert [scene["time_of_day"] for scene in scenes] == ["DAY", "NIGHT"]

    character = find_entity(project, "POSTAC_01", "CHARACTER")
    assert character is not None
    line = project.connection.execute("SELECT text FROM dialogue_line").fetchone()
    # Without rebuilt paragraph breaks the speech would swallow the action
    # that follows it.
    assert line["text"] == "Mam to."


def test_pdf_without_a_text_layer_is_refused(project, tmp_path):
    scanned = builders.write_pdf(tmp_path / "skan.pdf", ["Strona 1"])
    with pytest.raises(ValueError, match="warstwy tekstowej"):
        import_screenplay(project, scanned)


@pytest.mark.parametrize(
    "line",
    ["12.", "  7  ", "(23)", "CONTINUED:", "(CONTINUED)", "CIĄG DALSZY:", "(MORE)"],
)
def test_strips_page_furniture(line):
    assert strip_page_furniture(f"Akcja.\n{line}\nDalej.") == "Akcja.\nDalej."


@pytest.mark.parametrize("line", ["POSTAĆ_01", "Rok 1987 zmienił wszystko.", "WN. A - DZIEŃ"])
def test_keeps_real_screenplay_lines(line):
    assert line in strip_page_furniture(f"Akcja.\n{line}\nDalej.")


def test_paragraph_rebuild_binds_dialogue_to_its_cue():
    rebuilt = restore_paragraph_breaks(
        "WN. MAGAZYN - DZIEN\n"
        "Wchodzi.\n"
        "                    POSTAC_01\n"
        "               (cicho)\n"
        "               Mam to.\n"
        "Odchodzi.\n"
    )
    blocks = [block for block in rebuilt.split("\n\n") if block.strip()]
    # Cue, parenthetical and speech are one block; action stands apart.
    assert len(blocks) == 4
    assert "POSTAC_01" in blocks[2] and "Mam to." in blocks[2]
    assert blocks[3].strip() == "Odchodzi."


def test_paragraph_rebuild_leaves_well_extracted_text_alone():
    text = "WN. A - DZIEN\n\nWchodzi.\n\n    POSTAC_01\n\n  Mam to.\n"
    assert restore_paragraph_breaks(text) == text


def test_paragraph_rebuild_does_nothing_without_indentation():
    # Nothing to reason from, so the text is left exactly as extracted.
    text = "WN. A - DZIEN\nWchodzi.\nPOSTAC_01\nMam to.\n"
    assert restore_paragraph_breaks(text) == text
