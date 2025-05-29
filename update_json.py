import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# URL der Energy-Charts-Seite
url = "https://www.energy-charts.info/charts/energy_pie/chart.htm?l=de&c=DE&interval=year&source=total&year=2025"

# Selenium WebDriver einrichten
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Seite laden
driver.get(url)
time.sleep(5)  # Wartezeit für vollständiges Laden

# Werte extrahieren
erneuerbare = driver.find_element(By.XPATH, '//*[contains(text(), "Erneuerbare Energien")]/following-sibling::td').text
fossile = driver.find_element(By.XPATH, '//*[contains(text(), "Fossile Energien")]/following-sibling::td').text
driver.quit()

# JSON-Daten erstellen
heute = time.strftime("%d.%m.%Y")
json_data = [
    [
        ["", f"Stand: {heute}"],
        ["Erneuerbare Energien", float(erneuerbare.replace(",", "."))],
        ["Fossile Energien", float(fossile.replace(",", "."))]
    ]
]

# JSON-Datei speichern
with open("strommix_2025.json", "w") as json_file:
    json.dump(json_data, json_file, indent=2)
