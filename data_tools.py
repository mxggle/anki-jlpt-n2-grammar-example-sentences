#!/usr/bin/env python3
"""
Convert the Anki note data between CSV (notes.csv) and a human-friendly JSON
(notes.json), and verify round-trip fidelity.

Why this exists
---------------
`notes.csv` is the data source consumed by `package_anki.py` to build the .apkg.
Editing raw CSV is painful, so this tool lets you keep a readable JSON as the
working source and regenerate an identical CSV before packaging.

CRITICAL invariants for Anki (do NOT break these)
--------------------------------------------------
Anki matches/updates notes on re-import by their GUID. `package_anki.py` derives
the GUID as  f"n2-line-{LineNumber}"  where LineNumber is column 20 (0-indexed).
Therefore:
  * `lineNumber` is the IDENTITY of each note. Changing it makes Anki treat the
    card as a brand-new note (and orphan the old one). Never renumber existing
    notes. Only append new lineNumbers for genuinely new cards.
  * The model id / model name / field order in package_anki.py must stay fixed.
  * Field *content* (sentences, translations, notes, etc.) may be edited freely;
    that just updates the existing card.

Field/column order is fixed (see FIELDS below) and must match package_anki.py
and the original .apkg exactly.

Usage
-----
  python3 data_tools.py to-json    # notes.csv  -> notes.json
  python3 data_tools.py to-csv     # notes.json -> notes.csv
  python3 data_tools.py verify     # confirm notes.json -> CSV == notes.csv (values)
"""
import csv
import json
import os
import sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shin-kanzen-n2-grammar")
CSV_PATH = os.path.join(BASE, "notes.csv")
JSON_PATH = os.path.join(BASE, "notes.json")

# Anki text-file header (must be reproduced verbatim for direct CSV import).
HEADER_LINES = [
    "#separator:comma",
    "#html:true",
    "#deck column:1",
    "#tags column:22",
]

# Ordered (jsonKey, csv column index). Order == CSV column order == package_anki.py.
FIELDS = [
    ("deck", 0),
    ("frontSentence", 1),
    ("grammarPattern", 2),
    ("lessonInfo", 3),
    ("backSentence", 4),
    ("readingFurigana", 5),
    ("translation", 6),
    ("audioFile", 7),
    ("grammarFormation", 8),
    ("richGrammarFormation", 9),
    ("styleNotes", 10),
    ("explanationJapanese", 11),
    ("explanationChinese", 12),
    ("englishMeaning", 13),
    ("chineseMeaning", 14),
    ("additionalNotes", 15),
    ("additionalNotesZh", 16),
    ("vocabularyNotes", 17),
    ("detailedExplanation", 18),
    ("level", 19),
    ("lineNumber", 20),      # csv col 20 — drives the GUID "n2-line-{lineNumber}"
    ("tags", 21),
]
NUM_COLS = len(FIELDS)  # 22 columns total


def read_csv_rows(path):
    """Return the raw data rows (list of lists), skipping the # header lines."""
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(line for line in f if not line.startswith("#"))
        return [row for row in reader if row]


def csv_to_json():
    rows = read_csv_rows(CSV_PATH)
    notes = []
    for i, row in enumerate(rows, start=1):
        if len(row) != NUM_COLS:
            raise ValueError(f"Row {i} has {len(row)} cols, expected {NUM_COLS}")
        # Omit empty values for readability. to-csv fills any missing key back
        # with "" so the regenerated CSV keeps all columns (structure unchanged).
        note = {key: row[idx] for key, idx in FIELDS if row[idx] != ""}
        notes.append(note)
    payload = {"header": HEADER_LINES, "fieldOrder": [k for k, _ in FIELDS], "notes": notes}
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {len(notes)} notes -> {JSON_PATH}")


def load_notes():
    """Return the list of note dicts from notes.json.

    Accepts either format:
      * {"header": ..., "fieldOrder": ..., "notes": [...]}  (this tool's output)
      * [ {...}, {...} ]                                     (a bare array)
    Any keys outside FIELDS (e.g. `ttsClassification`, used only for TTS audio
    generation) are ignored, so they never reach the CSV / .apkg.
    """
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, dict):
        return payload["notes"]
    if isinstance(payload, list):
        return payload
    raise ValueError(f"Unexpected notes.json top-level type: {type(payload).__name__}")


def json_to_rows():
    rows = []
    for note in load_notes():
        rows.append([note.get(key, "") for key, _ in FIELDS])
    return rows


def json_to_csv():
    rows = json_to_rows()
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        for line in HEADER_LINES:
            f.write(line + "\n")
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)
    print(f"Wrote {len(rows)} notes -> {CSV_PATH}")


def verify():
    """Ensure JSON -> CSV reproduces the same parsed values as the current CSV."""
    original = read_csv_rows(CSV_PATH)
    regenerated = json_to_rows()
    if original == regenerated:
        print(f"OK: round-trip identical ({len(original)} rows, values match).")
        return 0
    print("MISMATCH between notes.csv and notes.json")
    if len(original) != len(regenerated):
        print(f"  row count differs: csv={len(original)} json={len(regenerated)}")
    for i, (a, b) in enumerate(zip(original, regenerated), start=1):
        if a != b:
            print(f"  first diff at row {i}:")
            for j, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    print(f"    col {j}: csv={x!r} json={y!r}")
            break
    return 1


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "to-json":
        csv_to_json()
    elif cmd == "to-csv":
        json_to_csv()
    elif cmd == "verify":
        sys.exit(verify())
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
