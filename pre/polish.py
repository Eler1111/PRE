"""Polish-language helpers for user-facing text.

The interface is Polish, so counts have to decline correctly — "1 scena",
"2 sceny", "5 scen". Getting this wrong makes the whole product read as a
translation.
"""

from __future__ import annotations


def plural(count: int, singular: str, few: str, many: str) -> str:
    """Pick the Polish plural form for ``count``.

    >>> plural(1, "scena", "sceny", "scen")
    'scena'
    >>> plural(22, "scena", "sceny", "scen")
    'sceny'
    >>> plural(13, "scena", "sceny", "scen")
    'scen'
    """
    if count == 1:
        return singular
    last_two = abs(count) % 100
    last = abs(count) % 10
    if 2 <= last <= 4 and not 12 <= last_two <= 14:
        return few
    return many


def counted(count: int, singular: str, few: str, many: str) -> str:
    """``"5 scen"`` — the number with its correctly declined noun."""
    return f"{count} {plural(count, singular, few, many)}"
