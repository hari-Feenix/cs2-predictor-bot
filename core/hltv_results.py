import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_recent_hltv_results():
    url = 'https://www.hltv.org/results'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []

    for match in soup.select('.result-con'):
        teams = match.select('.team')
        score = match.select_one('.result-score')
        time_tag = match.select_one('.time')
        link_tag = match.select_one('a.a-reset')

        if len(teams) < 2 or not score or not link_tag:
            continue

        team1 = teams[0].get_text(strip=True)
        team2 = teams[1].get_text(strip=True)
        score_text = score.get_text(strip=True)
        match_link = 'https://www.hltv.org' + link_tag['href']

        try:
            timestamp = datetime.fromtimestamp(int(time_tag['data-unix']) / 1000)
        except Exception:
            timestamp = datetime.utcnow()

        results.append({
            'team1': team1,
            'team2': team2,
            'score': score_text,
            'match_link': match_link,
            'timestamp': timestamp,
        })

    return results
