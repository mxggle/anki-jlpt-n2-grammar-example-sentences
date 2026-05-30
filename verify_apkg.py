#!/usr/bin/env python3
"""
Verify a packaged .apkg preserves the invariants Anki relies on to UPDATE
(not duplicate) existing cards on re-import.

Checks
------
  * Model ID   == 1607392322            (Anki matches the model by id)
  * Model name == "Japanese Grammar Enhanced Model++"
  * Field count == 20                   (field order/count must stay fixed)
  * Every note GUID matches  n2-line-{N} (the identity used for updates)
  * Reports note count and any duplicate / malformed GUIDs

Usage
-----
  python3 verify_apkg.py                  # checks the default output .apkg
  python3 verify_apkg.py path/to/file.apkg
"""
import glob
import json
import os
import re
import sqlite3
import sys
import tempfile
import zipfile

EXPECTED_MODEL_ID = 1607392322
EXPECTED_MODEL_NAME = "Japanese Grammar Enhanced Model++"
EXPECTED_FIELD_COUNT = 20
GUID_RE = re.compile(r"^n2-line-(\d+)$")


def default_apkg():
    candidates = sorted(glob.glob("Shin_Kanzen_Master_Grammar_N2_v*.apkg"))
    if candidates:
        return candidates[-1]
    others = sorted(glob.glob("*.apkg"))
    return others[0] if others else None


def load_collection(apkg_path):
    """Extract the collection sqlite db from the .apkg to a temp file."""
    with zipfile.ZipFile(apkg_path) as z:
        names = z.namelist()
        db_name = "collection.anki21" if "collection.anki21" in names else "collection.anki2"
        if db_name not in names:
            raise ValueError(f"{apkg_path} contains no collection db (members: {names})")
        tmp = tempfile.mktemp(suffix=".anki2")
        with open(tmp, "wb") as f:
            f.write(z.read(db_name))
    return tmp


def verify(apkg_path):
    print(f"Verifying: {apkg_path}")
    tmp = load_collection(apkg_path)
    errors = []
    try:
        con = sqlite3.connect(tmp)
        cur = con.cursor()

        # --- Model checks ---
        models = json.loads(cur.execute("select models from col").fetchone()[0])
        if str(EXPECTED_MODEL_ID) not in models:
            errors.append(
                f"Model ID {EXPECTED_MODEL_ID} not found (present: {list(models)})"
            )
        else:
            m = models[str(EXPECTED_MODEL_ID)]
            if m["name"] != EXPECTED_MODEL_NAME:
                errors.append(
                    f"Model name mismatch: {m['name']!r} != {EXPECTED_MODEL_NAME!r}"
                )
            n_fields = len(m["flds"])
            if n_fields != EXPECTED_FIELD_COUNT:
                errors.append(
                    f"Field count {n_fields} != expected {EXPECTED_FIELD_COUNT}"
                )
            print(f"  Model ID    : {EXPECTED_MODEL_ID} ({m['name']})")
            print(f"  Field count : {n_fields}")

        # --- GUID checks ---
        guids = [row[0] for row in cur.execute("select guid from notes").fetchall()]
        print(f"  Note count  : {len(guids)}")
        bad = [g for g in guids if not GUID_RE.match(g)]
        if bad:
            errors.append(f"{len(bad)} notes have non n2-line-N guids, e.g. {bad[:5]}")
        dups = {g for g in guids if guids.count(g) > 1}
        if dups:
            errors.append(f"duplicate guids: {sorted(dups)[:5]}")
    finally:
        con.close()
        os.remove(tmp)

    if errors:
        print("\nFAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nOK: all invariants hold (Model ID / field count / GUID pattern).")
    return 0


def main():
    apkg = sys.argv[1] if len(sys.argv) > 1 else default_apkg()
    if not apkg or not os.path.exists(apkg):
        print(f"apkg not found: {apkg!r}")
        sys.exit(2)
    sys.exit(verify(apkg))


if __name__ == "__main__":
    main()
