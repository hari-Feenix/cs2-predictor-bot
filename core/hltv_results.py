import requests
from bs4 import BeautifulSoup

def fetch_completed_results():
    url = 'https://www.hltv.org/results'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = {}
    for match_link in soup.select('.result-con .a-reset'):
        try:
            href = match_link['href']
            match_id = href.split('/')[-2]
            teams = match_link.select('.team')
            team_names = [t.text.strip() for t in teams]
            winner_element = match_link.select_one('.team-won')

            if winner_element:
                winner = winner_element.text.strip()
                results[match_id] = winner
        except Exception:
            continue

    return results
