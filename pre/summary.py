"""The Polish summary shown after a screenplay is analysed."""

from __future__ import annotations

from .polish import counted
from .project import Project
from .queries import ProjectCounts, project_counts


def analysis_summary(project: Project) -> str:
    """A short Polish report, built only from what is actually stored.

    It states outright that no assets exist yet, because the whole point of
    global analysis is to understand the film without producing anything.
    """
    counts = project_counts(project)
    lines = ["Scenariusz przeanalizowany.", ""]
    lines.extend(_count_lines(counts))
    lines.append("")

    if counts.open_review_flags:
        lines.append(
            f"{counted(counts.open_review_flags, 'niejasność', 'niejasności', 'niejasności')} "
            "do rozstrzygnięcia."
        )
    lines.append("Nie utworzono jeszcze żadnych assetów.")
    return "\n".join(lines)


def _count_lines(counts: ProjectCounts) -> list[str]:
    lines = [
        counted(counts.scenes, "scena", "sceny", "scen"),
        counted(counts.characters, "postać", "postacie", "postaci"),
    ]
    if counts.speaking_characters:
        lines.append(
            counted(
                counts.speaking_characters,
                "postać mówiąca",
                "postacie mówiące",
                "postaci mówiących",
            )
        )
    lines.append(counted(counts.locations, "lokacja", "lokacje", "lokacji"))

    if counts.props:
        lines.append(counted(counts.props, "rekwizyt", "rekwizyty", "rekwizytów"))
    for count, noun in (
        (counts.character_state_events, "zmiana stanu postaci"),
        (counts.location_state_events, "zmiana stanu lokacji"),
        (counts.prop_state_events, "zmiana stanu rekwizytu"),
    ):
        if count:
            lines.append(f"{count} × {noun}")

    if counts.voice_requirements:
        lines.append(f"Wymagane profile głosowe: {counts.voice_requirements}")
    if counts.acting_requirements:
        lines.append(f"Wymagane profile aktorskie: {counts.acting_requirements}")
    return lines
