import requests
from bs4 import BeautifulSoup
import json

def get_upcoming_matches():
    url = "https://bo3.gg/matches"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find JSON-LD script tag
        script_tag = soup.find('script', type='application/ld+json')
        if not script_tag:
            print("⚠️ Couldn't find match data.")
            return []

        raw_json = json.loads(script_tag.string)

        matches = []
        for match in raw_json:
            if 'name' in match and 'startDate' in match:
                try:
                    team1, team2 = match['name'].split(' vs ')
                except ValueError:
                    continue

                matches.append({
                    "team1": team1.strip(),
                    "team2": team2.strip(),
                    "time": match['startDate'],
                    "match_id": f"{team1.strip()}_vs_{team2.strip()}"
                })

        return matches

    except Exception as e:
        print(f"Error fetching matches from bo3.gg: {e}")
        return []
