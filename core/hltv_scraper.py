import requests

def get_upcoming_matches():
    try:
        response = requests.get("https://hltv-api.vercel.app/api/upcoming.json")
        response.raise_for_status()
        data = response.json()
        matches = []

        for match in data[:5]:  # Limit to 5 for preview
            match_id = match.get("match_id", "0")
            team1 = match.get("team1", "TBD")
            team2 = match.get("team2", "TBD")
            match_time = match.get("time", "Unknown")
            matches.append({
                "team1": team1,
                "team2": team2,
                "time": match_time,
                "match_id": str(match_id)
            })
        return matches
    except requests.RequestException as e:
        print(f"Error fetching upcoming matches: {e}")
        return []

def fetch_recent_results():
    try:
        response = requests.get("https://hltv-api.vercel.app/api/results.json")
        response.raise_for_status()
        data = response.json()
        results = []
        for match in data:
            match_id = match.get("match_id", "0")
            winner = match.get("winner", "Unknown")
            results.append({
                "match_id": str(match_id),
                "winner": winner
            })
        return results
    except requests.RequestException as e:
        print(f"Error fetching match results: {e}")
        return []
