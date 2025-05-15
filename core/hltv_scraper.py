import requests
from bs4 import BeautifulSoup

def get_upcoming_matches():
    url = 'https://www.hltv.org/matches'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    matches = []

    for match in soup.select('.match-day .upcomingMatch'):
        try:
            team1 = match.select_one('.matchTeam.team1 .matchTeamName').text.strip()
            team2 = match.select_one('.matchTeam.team2 .matchTeamName').text.strip()
            time = match.select_one('.matchTime').text.strip()
            href = match.find('a', href=True)['href']
            match_id = href.split('/')[-2]
            matches.append({
                'team1': team1,
                'team2': team2,
                'time': time,
                'match_id': match_id
            })
        except Exception:
            continue

    return matches
