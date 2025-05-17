import requests
from bs4 import BeautifulSoup

def get_upcoming_matches():
    url = "https://bo3.gg/matches/current"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        matches = []

        for match in soup.select(".match-card"):  # update this selector if it changes
            teams = match.select(".match-card__opponents .opponent__name")
            time_tag = match.select_one(".match-card__time")
            if len(teams) >= 2:
                team1 = teams[0].text.strip()
                team2 = teams[1].text.strip()
                time = time_tag.text.strip() if time_tag else "Unknown"

                matches.append({
                    "team1": team1,
                    "team2": team2,
                    "time": time,
                    "match_id": f"{team1}_vs_{team2}_{time.replace(' ', '_')}"
                })

        return matches

    except Exception as e:
        print(f"[ERROR] Fetching upcoming matches: {e}")
        return []

def get_recent_results():
    url = "https://bo3.gg/results"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        results = []

        for match in soup.select(".match-card"):
            teams = match.select(".match-card__opponents .opponent__name")
            scores = match.select(".match-card__score")
            if len(teams) >= 2 and len(scores) == 1:
                score_text = scores[0].text.strip().split(":")
                if len(score_text) == 2:
                    team1 = teams[0].text.strip()
                    team2 = teams[1].text.strip()
                    score1, score2 = score_text

                    results.append({
                        "team1": team1,
                        "team2": team2,
                        "score1": score1,
                        "score2": score2
                    })

        return results

    except Exception as e:
        print(f"[ERROR] Fetching recent results: {e}")
        return []
