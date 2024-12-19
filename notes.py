import json
import os
from config import NOTES_FILE

def load_notes():
    """Загружает заметки из файла."""
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_notes(notes):
    """Сохраняет заметки в файл."""
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)

notes = load_notes()

def get_user_notes(user_id):
    """Получить заметки пользователя."""
    return notes.get(str(user_id), [])

def add_note(user_id, note_text):
    """Добавить заметку для пользователя."""
    user_id = str(user_id)
    user_notes = notes.get(user_id, [])
    note_id = len(user_notes) + 1
    user_notes.append({"id": note_id, "text": note_text})
    notes[user_id] = user_notes
    save_notes(notes)

def edit_note(user_id, note_id, new_text):
    """Редактировать заметку пользователя."""
    user_id = str(user_id)
    user_notes = notes.get(user_id, [])
    for note in user_notes:
        if note["id"] == note_id:
            note["text"] = new_text
            save_notes(notes)
            return True
    return False

def delete_note(user_id, note_id):
    """Удалить заметку пользователя."""
    user_id = str(user_id)
    user_notes = notes.get(user_id, [])
    updated_notes = [note for note in user_notes if note["id"] != note_id]
    if len(updated_notes) < len(user_notes):
        notes[user_id] = updated_notes
        save_notes(notes)
        return True
    return False
