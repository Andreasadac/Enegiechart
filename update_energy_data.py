name: Tägliches Update der Energiedaten

on:
  schedule:
    - cron: '0 6 * * *'  # Täglich um 6:00 UTC (8:00 Uhr München-Zeit)
  workflow_dispatch:     # Manuelles Auslösen möglich

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Repository klonen
        uses: actions/checkout@v3

      - name: Python einrichten
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Abhängigkeiten installieren (falls nötig)
        run: |
          pip install -r requirements.txt || true

      - name: Skript ausführen
        run: python update_energy_data.py

      - name: Änderungen committen
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          git add infogram_ready_data.json
          git commit -m "Automatisches Update: $(date +'%Y-%m-%d')" || echo "Keine Änderungen"
          git push
