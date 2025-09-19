from flask import Flask
import requests

app = Flask(__name__)



url = "https://www.registredesactionscollectives.quebec/fr/Consulter/RechercherVueAjax"
payload = {
    "DateDepotDepart": "2025-01-01",   # Exemple date de début
    "DateDepotFin": "2025-09-19",      # Exemple date de fin
    # Ajouter d’autres champs de formulaire si nécessaire, ex: "NumeroDossier": "", etc.
}
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.post(url, data=payload, headers=headers)
print(response.text)  # Le HTML des résultats
@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run()

