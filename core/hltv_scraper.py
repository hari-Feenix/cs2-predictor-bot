import requests

MATCHES_URL = "https://hltv-api.vercel.app/api/matches.json"
RESULTS_URL = "https://hltv-api.vercel.app/api/results.json"

def get_upcoming_matches(limit=5):
    try:
        response = requests.get(MATCHES_URL)
        response.raise_for_status()
        data = response.json()

        matches = []
        for match in data[:limit]:
            teams = match.get("teams", [])
            team1 = teams[0]["name"] if len(teams) > 0 else "TBD"
            team2 = teams[1]["name"] if len(teams) > 1 else "TBD"
            match_time = match.get("time", "Unknown")
            match_id = str(match.get("id", "0"))

            matches.append({
                "team1": team1,
                "team2": team2,
                "time": match_time,
                "match_id": match_id
            })

        return matches

    except Exception as e:
        print(f"Error fetching matches: {e}")
        return []

def fetch_recent_results(limit=10):
    try:
        response = requests.get(RESULTS_URL)
        response.raise_for_status()
        data = response.json()

        results = {}
        for match in data[:limit]:
            teams = match.get("teams", [])
            if len(teams) < 2:
                continue
            match_id = str(match.get("id", "0"))
            team1 = teams[0]["name"]
            team2 = teams[1]["name"]
            winner = match.get("winner", {}).get("name", None)

            results[match_id] = {
                "team1": team1,
                "team2": team2,
                "winner": winner
            }

        return results

    except Exception as e:
        print(f"Error fetching results: {e}")
        return {}
