import requests
from bs4 import BeautifulSoup

def get_upcoming_matches():
    url = 'https://www.hltv.org/matches'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    matches = []
    for match in soup.select('.upcomingMatches .match'):
        try:
            team1 = match.select_one('.matchTeam.team1 .matchTeamName').text.strip()
            team2 = match.select_one('.matchTeam.team2 .matchTeamName').text.strip()
            time_element = match.select_one('.matchTime')
            time = time_element['data-unix'] if time_element else 'Unknown'
            link = match.select_one('a.a-reset')
            href = link['href'] if link else ''
            match_id = href.split('/')[2] if href else '0'

            matches.append({
                'team1': team1,
                'team2': team2,
                'time': time,
                'match_id': match_id
            })
        except Exception as e:
            continue

    return matches
