import json
from datetime import datetime

# Beispielwerte für Erneuerbar und Fossil (in Prozent)
erneuerbar_prozent = 62.5
fossil_prozent = 37.5

# Aktuelles Datum im gewünschten Format
heute = datetime.today().strftime("%d.%m.%Y")
stand_text = f"Stand: {heute}"

# Infogram-kompatible Datenstruktur
infogram_data = {
    "sheet1": {
        "columns": ["Kategorie", "Wert"],
        "rows": [
            [stand_text, ""],
            ["Erneuerbar", erneuerbar_prozent],
            ["Fossil", fossil_prozent]
        ]
    }
}

# JSON-Datei speichern
with open("infogram_ready_data.json", "w", encoding="utf-8") as f:
    json.dump(infogram_data, f, ensure_ascii=False, indent=2)

print("Die Datei 'infogram_ready_data.json' wurde erfolgreich erstellt.")
