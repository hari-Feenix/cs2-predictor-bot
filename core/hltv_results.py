import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime

def get_recent_hltv_results():
    url = 'https://www.hltv.org/results'
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)

    if response.status_code != 200:
        print(f"⚠️ Failed to fetch HLTV data: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    matches = soup.select('.result-con')
    results = []

    for match in matches[:10]:  # Limit to 10 recent results
        try:
            team1 = match.select_one('.team1 .team').text.strip()
            team2 = match.select_one('.team2 .team').text.strip()
            score = match.select_one('.result-score').text.strip()
            time_tag = match.select_one('.time')
            timestamp = datetime.utcnow()
            if time_tag and time_tag.has_attr('data-unix'):
                timestamp = datetime.fromtimestamp(int(time_tag['data-unix']) / 1000)

            results.append({
                'team1': team1,
                'team2': team2,
                'score': score,
                'timestamp': timestamp
            })
        except Exception as e:
            print("⚠️ Error parsing match:", e)
            continue

    return results
