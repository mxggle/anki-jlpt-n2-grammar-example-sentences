import genanki
import csv
import os

import data_tools  # CSV is a generated artifact; notes.json is the source of truth

# ============================================================
# IMPORTANT: These IDs MUST match the original JLPT_N2.apkg
# to ensure cards UPDATE instead of DUPLICATE on re-import.
#
# Original DB analysis:
#   Model ID : 1607392322
#   Model Name: "Japanese Grammar Enhanced Model++"
#   GUID pattern: "n2-line-{LineNumber}" (e.g. "n2-line-1")
#   Fields (20): [FrontSentence, GrammarPattern, LessonInfo,
#                 BackSentence, ReadingFurigana, Translation,
#                 AudioFile, GrammarFormation, RichGrammarFormation,
#                 StyleNotes, ExplanationJapanese, ExplanationChinese,
#                 EnglishMeaning, ChineseMeaning, AdditionalNotes,
#                 AdditionalNotesZh, VocabularyNotes, DetailedExplanation,
#                 Level, LineNumber]
# ============================================================
MODEL_ID = 1607392322  # Must NOT change — Anki uses this to match model

# Load CSS and Templates
TEMPLATE_DIR = 'shin-kanzen-n2-grammar/templates'
CSS_FILE = os.path.join(TEMPLATE_DIR, 'Japanese Grammar Enhanced Model++-styles.css')
HTML_FILE = os.path.join(TEMPLATE_DIR, 'Japanese Grammar Enhanced Model++-Japanese Grammar Card.html')

with open(CSS_FILE, 'r', encoding='utf-8') as f:
    css_content = f.read()

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Split HTML into Front and Back templates
parts = html_content.split('<div class="card-back">')
front_template = parts[0].strip()
back_template = '<div class="card-back">' + parts[1].strip()

# Define the Model — field order MUST match original JLPT_N2.apkg exactly
model = genanki.Model(
    MODEL_ID,
    'Japanese Grammar Enhanced Model++',
    fields=[
        {'name': 'FrontSentence'},       # col[1]
        {'name': 'GrammarPattern'},      # col[2]
        {'name': 'LessonInfo'},          # col[3]
        {'name': 'BackSentence'},        # col[4]
        {'name': 'ReadingFurigana'},     # col[5]
        {'name': 'Translation'},         # col[6]
        {'name': 'AudioFile'},           # col[7]
        {'name': 'GrammarFormation'},    # col[8]
        {'name': 'RichGrammarFormation'},# col[9]
        {'name': 'StyleNotes'},          # col[10]
        {'name': 'ExplanationJapanese'}, # col[11]
        {'name': 'ExplanationChinese'},  # col[12]
        {'name': 'EnglishMeaning'},      # col[13]
        {'name': 'ChineseMeaning'},      # col[14]
        {'name': 'AdditionalNotes'},     # col[15]
        {'name': 'AdditionalNotesZh'},   # col[16]
        {'name': 'VocabularyNotes'},     # col[17]
        {'name': 'DetailedExplanation'}, # col[18]
        {'name': 'Level'},               # col[19]
        {'name': 'LineNumber'},          # col[20]
    ],
    templates=[
        {
            'name': 'Japanese Grammar Card',
            'qfmt': front_template,
            'afmt': back_template,
        },
    ],
    css=css_content
)

# CSV column mapping (0-indexed):
#   col[0]  = Deck name (e.g. "新完全掌握N2语法例句::Lesson 01")
#   col[1]  = FrontSentence
#   col[2]  = GrammarPattern
#   col[3]  = LessonInfo
#   col[4]  = BackSentence
#   col[5]  = ReadingFurigana
#   col[6]  = Translation
#   col[7]  = AudioFile
#   col[8]  = GrammarFormation
#   col[9]  = RichGrammarFormation
#   col[10] = StyleNotes
#   col[11] = ExplanationJapanese
#   col[12] = ExplanationChinese
#   col[13] = EnglishMeaning
#   col[14] = ChineseMeaning
#   col[15] = AdditionalNotes
#   col[16] = AdditionalNotesZh
#   col[17] = VocabularyNotes
#   col[18] = DetailedExplanation
#   col[19] = Level
#   col[20] = LineNumber
#   col[21] = Tags

def safe_get(row, index):
    """Safely get a column value, return '' if index out of range."""
    return row[index].strip() if len(row) > index else ''

# Single source of truth is notes.json. Regenerate notes.csv from it so the
# CSV consumed below is always in sync (never edit notes.csv by hand).
print("Regenerating notes.csv from notes.json (source of truth)...")
data_tools.json_to_csv()

# Read notes.csv
CSV_FILE = 'shin-kanzen-n2-grammar/notes.csv'
media_files = []
decks = {}  # deck_name -> genanki.Deck

with open(CSV_FILE, 'r', encoding='utf-8') as f:
    # Skip lines starting with # (Anki metadata headers)
    reader = csv.reader(line for line in f if not line.startswith('#'))
    for row in reader:
        if not row:
            continue

        try:
            deck_name = safe_get(row, 0)  # e.g. "新完全掌握N2语法例句::Lesson 01"
            line_number = safe_get(row, 20)  # e.g. "1", "2", ...

            # Build fields in exact same order as original model
            fields = [
                safe_get(row, 1),   # FrontSentence
                safe_get(row, 2),   # GrammarPattern
                safe_get(row, 3),   # LessonInfo
                safe_get(row, 4),   # BackSentence
                safe_get(row, 5),   # ReadingFurigana
                safe_get(row, 6),   # Translation
                safe_get(row, 7),   # AudioFile
                safe_get(row, 8),   # GrammarFormation
                safe_get(row, 9),   # RichGrammarFormation
                safe_get(row, 10),  # StyleNotes
                safe_get(row, 11),  # ExplanationJapanese
                safe_get(row, 12),  # ExplanationChinese
                safe_get(row, 13),  # EnglishMeaning
                safe_get(row, 14),  # ChineseMeaning
                safe_get(row, 15),  # AdditionalNotes
                safe_get(row, 16),  # AdditionalNotesZh
                safe_get(row, 17),  # VocabularyNotes
                safe_get(row, 18),  # DetailedExplanation
                safe_get(row, 19),  # Level
                line_number,        # LineNumber
            ]

            # GUID MUST use the same "n2-line-{N}" pattern as the original
            # This ensures Anki matches and updates existing cards instead of creating duplicates
            guid = f'n2-line-{line_number}'

            # Extract and collect audio media files
            audio_field = safe_get(row, 7)
            if audio_field.startswith('[sound:') and audio_field.endswith(']'):
                audio_file = audio_field[7:-1]
                audio_path = os.path.join('shin-kanzen-n2-grammar/medias', audio_file)
                if os.path.exists(audio_path) and audio_path not in media_files:
                    media_files.append(audio_path)

            # Create or reuse a per-lesson sub-deck
            if deck_name not in decks:
                # Use a deterministic deck ID based on the deck name
                deck_id = abs(hash(deck_name)) % (10**10)
                decks[deck_name] = genanki.Deck(deck_id, deck_name)

            note = genanki.Note(
                model=model,
                fields=fields,
                guid=guid,
            )
            decks[deck_name].add_note(note)

        except IndexError as e:
            print(f"Skipping malformed row: {e} — {row[:3]}")
            continue

# Package and Save
all_decks = list(decks.values())
package = genanki.Package(all_decks)
package.media_files = media_files
output_file = 'Shin_Kanzen_Master_Grammar_N2_v1.7.0.apkg'
package.write_to_file(output_file)

total_notes = sum(len(d.notes) for d in all_decks)
print(f"Successfully packaged {total_notes} notes into {output_file}")
print(f"Included {len(media_files)} media files.")
print(f"Decks created: {len(all_decks)}")
