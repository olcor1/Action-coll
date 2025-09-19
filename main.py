from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_actions():
    url = "https://www.registredesactionscollectives.quebec/fr/Consulter/RechercherVueAjax"
    payload = {
        "DateDepotDepart": "2025-01-01",
        "DateDepotFin": "2025-09-19"
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.post(url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extraire les titres (exemple à adapter selon la structure réelle)
    actions = []
    for item in soup.select(".nom-de-classe-titre"):  # Ajuster le sélecteur CSS
        actions.append(item.text.strip())

    return actions

@app.route("/test-scrape")
def test_scrape():
    results = scrape_actions()
    return jsonify(results)

if __name__ == "__main__":
    app.run()
