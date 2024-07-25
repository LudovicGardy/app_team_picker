import requests
from bs4 import BeautifulSoup

from modules.config import load_configurations


def get_medals():
    env_variables = load_configurations()
    medals_url = str(env_variables.get("MEDALS_URL"))

    response = requests.get(medals_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        gold_medals = silver_medals = bronze_medals = total_medals = "0"

        gold_element = soup.find("abbr", class_="gold")
        silver_element = soup.find("abbr", class_="silver")
        bronze_element = soup.find("abbr", class_="bronze")
        total_element = soup.find("abbr", class_="total")

        if gold_element:
            gold_medals = gold_element.get("title").split(" ")[0]
        if silver_element:
            silver_medals = silver_element.get("title").split(" ")[0]
        if bronze_element:
            bronze_medals = bronze_element.get("title").split(" ")[0]
        if total_element:
            total_medals = total_element.get("title").split(" ")[0]

        medals = {
            "gold_medals": gold_medals,
            "silver_medals": silver_medals,
            "bronze_medals": bronze_medals,
            "total_medals": total_medals,
        }

    else:
        print(f"Échec de la requête GET. Statut de la réponse: {response.status_code}")

    return medals
