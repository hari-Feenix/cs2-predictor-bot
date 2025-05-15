import requests

def get_upcoming_matches():
    try:
        response = requests.get("https://hltv-api.vercel.app/api/matches")
        if response.status_code != 200:
            print("API responded with:", response.status_code)
            return []

        data = response.json()
        matches = []

        for m in data[:5]:
            matches.append({
                "team1": m.get("team1", "TBD"),
                "team2": m.get("team2", "TBD"),
                "time": m.get("time", "Unknown"),
                "match_id": str(m.get("id", "0"))
            })

        return matches

    except Exception as e:
        print("Error fetching matches:", e)
        return []
