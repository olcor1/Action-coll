from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_actions():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "fr-CA,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.registredesactionscollectives.quebec/fr/Consulter/RecherchePublique",
        "Origin": "https://www.registredesactionscollectives.quebec",
    })

    url_get = "https://www.registredesactionscollectives.quebec/fr/Consulter/RecherchePublique"
    session.get(url_get)

    url_post = "https://www.registredesactionscollectives.quebec/fr/Consulter/RechercherVueAjax"
    payload = {
        "DateDepotDepart": "2025-01-01",
        "DateDepotFin": "2025-09-19",
    }
    response = session.post(url_post, data=payload)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    table = soup.find("table", id="tableau-resultats")
    if not table:
        return results

    tbody = table.find("tbody")
    if not tbody:
        return results

    for row in tbody.find_all("tr", role="row"):
        cols = row.find_all("td")
        if len(cols) < 4:
            continue
        nom_parties = cols[0].get_text(strip=True)
        date_depot = cols[1].get_text(strip=True)
        cause_concerne = cols[2].get_text(strip=True)
        sujet = cols[3].get_text(strip=True)

        lien_tag = cols[0].find("a")
        lien = lien_tag["href"] if lien_tag else ""

        results.append({
            "NomParties": nom_parties,
            "DateDepot": date_depot,
            "CauseConcerne": cause_concerne,
            "Sujet": sujet,
            "Lien": lien
        })

    return results

@app.route("/test-scrape")
def test_scrape():
    results = scrape_actions()
    return jsonify(results)

if __name__ == "__main__":
    app.run()
