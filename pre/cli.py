"""A minimal Polish command line for Module 01.

The real interface is the chat (D-003). This exists so the analysis can be
run and inspected before the chat surface is built, and so the module is
testable by hand against a real screenplay.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analysis import import_screenplay
from .project import Project, ProjectLockedError, detect_sync_folder
from .queries import (
    entity_states,
    find_entity,
    list_scenes,
    open_review_flags,
    scenes_with_entity,
)
from .summary import analysis_summary


def _open(path: str) -> Project:
    project = Project.open(Path(path))
    warning = project.sync_warning()
    if warning:
        print(f"\n{warning.message}\n", file=sys.stderr)
    return project


def cmd_nowy(args: argparse.Namespace) -> int:
    warning = detect_sync_folder(Path(args.sciezka).parent)
    project = Project.create(Path(args.sciezka), name=args.nazwa or Path(args.sciezka).stem)
    try:
        print(f"Utworzono projekt: {project.path}")
        if warning:
            print(f"\n{warning.message}")
    finally:
        project.close()
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    project = _open(args.projekt)
    try:
        result = import_screenplay(project, Path(args.scenariusz))
        print(analysis_summary(project))
        if result.review_flag_count:
            print("\nDo rozstrzygnięcia:")
            for flag in open_review_flags(project):
                print(f"  • {flag['question']}")
    finally:
        project.close()
    return 0


def cmd_sceny(args: argparse.Namespace) -> int:
    project = _open(args.projekt)
    try:
        for scene in list_scenes(project):
            marker = "" if scene["chronology_status"] == "UNKNOWN" else f"  [{scene['chronology_status']}]"
            print(f"{scene['script_order']:>3}. {scene['heading_raw']}{marker}")
    finally:
        project.close()
    return 0


def cmd_postac(args: argparse.Namespace) -> int:
    project = _open(args.projekt)
    try:
        entity = find_entity(project, args.nazwa)
        if entity is None:
            print(f"Nie znaleziono: {args.nazwa}", file=sys.stderr)
            return 1

        print(f"{entity['display_name']}  [{entity['entity_type']}, {entity['information_status']}]")
        print("\nWystępuje w scenach:")
        for row in scenes_with_entity(project, entity["id"]):
            speaks = ", mówi" if row["speaks"] else ""
            certainty = "" if row["information_status"] == "FACT" else "  (wnioskowane)"
            print(f"  {row['script_order']:>3}. {row['appearance_type']}{speaks}{certainty}")

        states = entity_states(project, entity["id"])
        if states:
            print("\nStany:")
            for state in states:
                scenes = ", ".join(str(s["script_order"]) for s in state["scenes"])
                print(f"  {state['name']}  →  sceny: {scenes or 'brak'}")
    finally:
        project.close()
    return 0


def cmd_niejasnosci(args: argparse.Namespace) -> int:
    project = _open(args.projekt)
    try:
        flags = open_review_flags(project)
        if not flags:
            print("Brak niejasności do rozstrzygnięcia.")
        for flag in flags:
            print(f"• {flag['question']}")
            if flag["evidence"]:
                print(f"  podstawa: {flag['evidence']}")
    finally:
        project.close()
    return 0


def cmd_podsumowanie(args: argparse.Namespace) -> int:
    project = _open(args.projekt)
    try:
        print(analysis_summary(project))
    finally:
        project.close()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pre", description="PRE — Moduł 01")
    sub = parser.add_subparsers(dest="polecenie", required=True)

    new = sub.add_parser("nowy", help="utwórz nowy projekt")
    new.add_argument("sciezka")
    new.add_argument("--nazwa")
    new.set_defaults(func=cmd_nowy)

    imp = sub.add_parser("import", help="wczytaj i przeanalizuj scenariusz")
    imp.add_argument("projekt")
    imp.add_argument("scenariusz")
    imp.set_defaults(func=cmd_import)

    for name, help_text, func in (
        ("sceny", "pokaż wszystkie sceny", cmd_sceny),
        ("niejasnosci", "pokaż niejasności do rozstrzygnięcia", cmd_niejasnosci),
        ("podsumowanie", "pokaż podsumowanie projektu", cmd_podsumowanie),
    ):
        cmd = sub.add_parser(name, help=help_text)
        cmd.add_argument("projekt")
        cmd.set_defaults(func=func)

    who = sub.add_parser("postac", help="pokaż postać lub lokację")
    who.add_argument("projekt")
    who.add_argument("nazwa")
    who.set_defaults(func=cmd_postac)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except ProjectLockedError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (FileNotFoundError, FileExistsError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
