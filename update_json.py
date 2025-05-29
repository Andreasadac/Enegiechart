import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# URL der Energy-Charts-Seite
url = "https://www.energy-charts.info/charts/energy_pie/chart.htm?l=de&c=DE&interval=year&source=total&year=2025"

# Selenium WebDriver einrichten
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Seite laden
driver.get(url)

# Warte auf die Sichtbarkeit der Texte
wait = WebDriverWait(driver, 15)
erneuerbare_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Erneuerbare Energien")]/following-sibling::td')))
fossile_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Fossile Energien")]/following-sibling::td')))

# Werte extrahieren
erneuerbare = erneuerbare_element.text
fossile = fossile_element.text

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
