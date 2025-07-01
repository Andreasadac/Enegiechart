import requests
import csv
from datetime import datetime, timedelta

# Datum berechnen: gestern bis heute
today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)
start = yesterday.isoformat()
end = today.isoformat()

# API-Endpunkt
url = f"https://api.energy-charts.info/power_trend?country=DE&start={start}&end={end}"

# Daten abrufen
response = requests.get(url)
data = response.json()

# Energiequellen definieren
fossil_sources = {'hard_coal', 'lignite', 'natural_gas', 'oil', 'other_fossil'}
renewable_sources = {'solar', 'wind_onshore', 'wind_offshore', 'biomass', 'hydro', 'geothermal'}

# Summen berechnen
fossil_sum = 0
renewable_sum = 0
total_sum = 0

for entry in data['data']:
    source = entry['source']
    values = [v[1] for v in entry['values']]
    avg = sum(values) / len(values) if values else 0
    total_sum += avg
    if source in fossil_sources:
        fossil_sum += avg
    elif source in renewable_sources:
        renewable_sum += avg

# Prozentwerte berechnen
fossil_percent = (fossil_sum / total_sum) * 100 if total_sum else 0
renewable_percent = (renewable_sum / total_sum) * 100 if total_sum else 0

# CSV schreiben
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date', 'Fossil (%)', 'Renewable (%)'])
    writer.writerow([start, f"{fossil_percent:.2f}", f"{renewable_percent:.2f}"])
