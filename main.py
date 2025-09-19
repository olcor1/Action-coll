from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

def scrape_actions_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.binary_location = "/usr/bin/chromium"  # Adapte selon install Docker

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.registredesactionscollectives.quebec/fr/Consulter/RecherchePublique")

    wait = WebDriverWait(driver, 30)

    input_debut = wait.until(EC.presence_of_element_located((By.ID, "DateDepotDepart")))
    input_debut.clear()
    input_debut.send_keys("2025-01-01")

    input_fin = driver.find_element(By.ID, "DateDepotFin")
    input_fin.clear()
    input_fin.send_keys("2025-09-19")

    bouton_rechercher = driver.find_element(By.ID, "rechercher")
    bouton_rechercher.click()

    wait.until(EC.presence_of_element_located((By.ID, "tableau-resultats")))
    time.sleep(5)

    tableau = driver.find_element(By.ID, "tableau-resultats")
    lignes = tableau.find_elements(By.CSS_SELECTOR, "tbody tr[role='row']")

    results = []
    for ligne in lignes:
        colonnes = ligne.find_elements(By.TAG_NAME, "td")
        if len(colonnes) < 4:
            continue
        nom_parties = colonnes[0].text.strip()
        date_depot = colonnes[1].text.strip()
        cause_concerne = colonnes[2].text.strip()
        sujet = colonnes[3].text.strip()
        lien = ""
        try:
            lien = colonnes[0].find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            pass

        results.append({
            "NomParties": nom_parties,
            "DateDepot": date_depot,
            "CauseConcerne": cause_concerne,
            "Sujet": sujet,
            "Lien": lien
        })

    driver.quit()
    return results

@app.route("/test-scrape")
def test_scrape():
    results = scrape_actions_selenium()
    return jsonify(results)

if __name__ == "__main__":
    app.run()
