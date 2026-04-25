#!/usr/bin/env python3
"""Emit a JSON snapshot of the Python numerology + zodiac output for
the parity check. Reads input from argv to stay deterministic across
runs.

Usage:
    python3 scripts/python-snapshot.py "Budi Santoso" 1990-05-17 2026-04-25
"""

import json
import sys
from datetime import date

# Python source lives one level up from web/.
sys.path.insert(0, "/home/user/chatbuddy")
from numerology import build_profile  # noqa: E402
from zodiac import chinese_zodiac, sun_sign, weton  # noqa: E402


def parse_iso(s: str) -> date:
    y, m, d = (int(x) for x in s.split("-"))
    return date(y, m, d)


def main() -> None:
    if len(sys.argv) != 4:
        print("usage: python3 python-snapshot.py <fullName> <dob> <today>", file=sys.stderr)
        sys.exit(2)
    full_name = sys.argv[1]
    dob = parse_iso(sys.argv[2])
    today = parse_iso(sys.argv[3])

    profile = build_profile(full_name, dob, today=today)
    shio = chinese_zodiac(dob)
    wet = weton(dob)

    print(
        json.dumps(
            {
                "life_path": profile["life_path"],
                "expression": profile["expression"],
                "soul_urge": profile["soul_urge"],
                "personality": profile["personality"],
                "birthday": profile["birthday"],
                "personal_year": profile["personal_year"],
                "personal_month": profile["personal_month"],
                "personal_day": profile["personal_day"],
                "maturity": profile["maturity"],
                "subconscious_self": profile["subconscious_self"],
                "cornerstone": profile["cornerstone"],
                "capstone": profile["capstone"],
                "first_vowel": profile["first_vowel"],
                "karmic_lessons": profile["karmic_lessons"],
                "hidden_passion": profile["hidden_passion"],
                "planes_dominant": profile["planes"]["dominant"],
                "bridges_lp_ex": profile["bridges"]["life_path_expression"],
                "bridges_su_pe": profile["bridges"]["soul_urge_personality"],
                "sun_sign": sun_sign(dob),
                "shio_animal": shio["animal"],
                "shio_element": shio["element"],
                "weton_dina": wet["dina"],
                "weton_pasaran": wet["pasaran"],
                "weton_neptu": wet["neptu"],
            }
        )
    )


if __name__ == "__main__":
    main()
