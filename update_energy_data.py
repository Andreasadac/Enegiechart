import json
import requests
from datetime import datetime

# Aktuelles Datum im Format YYYY-MM-DD
heute = datetime.today().strftime("%Y-%m-%d")

# Energy-Charts API-Endpunkt
api_url = f"https://www.energy-charts.info/charts/power/chart_data/de/{heute}/{heute}.json"

try:
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # Quellen zuordnen
    erneuerbare_quellen = {"Wind", "Solar", "Biomass", "Hydro", "Other renewables"}
    fossile_quellen = {"Lignite", "Hard coal", "Natural gas", "Oil", "Other fossil"}

    erneuerbar_summe = 0.0
    fossil_summe = 0.0

    for serie in data.get("data", []):
        name = serie.get("name", "")
        werte = serie.get("values", [])
        mittelwert = sum(v for _, v in werte if v is not None) / len(werte) if werte else 0

        if name in erneuerbare_quellen:
            erneuerbar_summe += mittelwert
        elif name in fossile_quellen:
            fossil_summe += mittelwert

    gesamt = erneuerbar_summe + fossil_summe
    erneuerbar_prozent = round((erneuerbar_summe / gesamt) * 100, 1) if gesamt > 0 else 0
    fossil_prozent = round((fossil_summe / gesamt) * 100, 1) if gesamt > 0 else 0

except Exception as e:
    print("Fehler beim Abrufen der Daten:", e)
    erneuerbar_prozent = 0
    fossil_prozent = 0

# Infogram-kompatible JSON-Datei
stand_text = f"Stand: {datetime.today().strftime('%d.%m.%Y')}"
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

with open("infogram_ready_data.json", "w", encoding="utf-8") as f:
    json.dump(infogram_data, f, ensure_ascii=False, indent=2)

print("infogram_ready_data.json wurde erfolgreich erstellt.")
