import requests
import os
from dotenv import load_dotenv

# Load environment variables (needed for local testing or .env in Render)
load_dotenv()

def get_upcoming_matches():
    api_key = os.getenv("PANDASCORE_API_KEY")
    if not api_key:
        print("❌ PANDASCORE_API_KEY is missing in environment.")
        return []

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    url = "https://api.pandascore.co/cs2/matches/upcoming?per_page=5&sort=begin_at"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        matches = []
        for match in data:
            opponents = match.get("opponents", [])
            team1 = opponents[0]["opponent"]["name"] if len(opponents) > 0 else "TBD"
            team2 = opponents[1]["opponent"]["name"] if len(opponents) > 1 else "TBD"
            match_time = match.get("begin_at", "Unknown")
            match_id = match.get("id", "0")

            matches.append({
                "team1": team1,
                "team2": team2,
                "time": match_time,
                "match_id": str(match_id)
            })

        return matches

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching matches: {e}")
        return []
