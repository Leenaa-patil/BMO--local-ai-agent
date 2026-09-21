import json
import os
from datetime import datetime


BMO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NOTES_FILE = os.path.join(
    BMO_ROOT,
    "memory",
    "notes.json"
)


def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []

    with open(NOTES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as file:
        json.dump(notes, file, indent=4)


def save_note(note):
    notes = load_notes()

    notes.append({
        "task": note,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "done": False
    })

    save_notes(notes)

    return f"I'll remember that: {note}"


def get_notes():
    notes = load_notes()

    pending = [
        note["task"]
        for note in notes
        if not note["done"]
    ]

    if not pending:
        return "You don't have any pending notes."

    return "\n".join(
        f"- {note}"
        for note in pending
    )