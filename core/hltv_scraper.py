import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_upcoming_matches():
    url = "https://www.hltv.org/matches"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        matches = []

        match_blocks = soup.select("div.upcomingMatch")

        for block in match_blocks[:5]:  # Get top 5 matches
            team_names = block.select(".matchTeamName")
            time_tag = block.select_one(".matchTime")

            if len(team_names) == 2 and time_tag and time_tag.has_attr("data-unix"):
                team1 = team_names[0].text.strip()
                team2 = team_names[1].text.strip()
                timestamp = int(time_tag["data-unix"]) / 1000
                match_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%SZ')
                match_id = f"{team1}_vs_{team2}_{int(timestamp)}"

                matches.append({
                    "team1": team1,
                    "team2": team2,
                    "time": match_time,
                    "match_id": match_id
                })

        return matches

    except Exception as e:
        print(f"Error fetching HLTV matches: {e}")
        return []
