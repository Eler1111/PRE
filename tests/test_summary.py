"""The Polish summary and its grammar.

The interface is Polish, so a count that does not decline correctly is a
visible defect, not a cosmetic one.
"""

from __future__ import annotations

import pytest

from pre.polish import counted, plural
from pre.summary import analysis_summary


@pytest.mark.parametrize(
    "count,expected",
    [
        (1, "scena"),
        (2, "sceny"),
        (4, "sceny"),
        (5, "scen"),
        (11, "scen"),
        (12, "scen"),
        (14, "scen"),
        (22, "sceny"),
        (25, "scen"),
        (0, "scen"),
        (101, "scen"),
        (102, "sceny"),
    ],
)
def test_polish_plural_forms(count, expected):
    assert plural(count, "scena", "sceny", "scen") == expected


def test_counted_joins_number_and_noun():
    assert counted(5, "scena", "sceny", "scen") == "5 scen"


def test_summary_reports_the_stored_counts(analysed):
    project, result = analysed
    text = analysis_summary(project)
    assert text.startswith("Scenariusz przeanalizowany.")
    assert f"{result.scene_count} scen" in text


def test_summary_states_that_no_assets_exist(analysed):
    project, _ = analysed
    # The whole point of global analysis is to understand the film without
    # producing anything, so the summary says so out loud.
    assert "Nie utworzono jeszcze żadnych assetów." in analysis_summary(project)


def test_summary_surfaces_open_questions(analysed):
    project, _ = analysed
    assert "do rozstrzygnięcia" in analysis_summary(project)


def test_summary_has_no_broken_declensions(analysed):
    project, _ = analysed
    text = analysis_summary(project)
    for wrong in ("1 sceny", "1 postacie", "1 lokacje", "2 scen\n", "5 sceny"):
        assert wrong not in text
