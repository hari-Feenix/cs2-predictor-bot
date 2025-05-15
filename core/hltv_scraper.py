import requests
from bs4 import BeautifulSoup

def get_upcoming_matches():
    url = 'https://www.hltv.org/matches'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    matches = []
    print("[DEBUG] Scraping HLTV matches...")

    for match in soup.select('.match-day .match'):
        try:
            print("[DEBUG] Match raw HTML:", match.prettify())  # NEW LINE
            team1 = match.select_one('.team1 .team').text.strip()
            team2 = match.select_one('.team2 .team').text.strip()
            time = match.select_one('.matchTime').text.strip()
            match_id = match['href'].split('/')[-2]
            matches.append({
                'team1': team1,
                'team2': team2,
                'time': time,
                'match_id': match_id
            })
        except Exception as e:
            print("[ERROR]", e)
            continue

    print("[DEBUG] Total matches scraped:", len(matches))
    return matches
