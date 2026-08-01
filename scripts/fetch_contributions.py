import requests
from bs4 import BeautifulSoup
import json
import os

USERNAME = "CodeSyedX"
URL = f"https://github.com/users/{USERNAME}/contributions"

def fetch_contributions():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    resp = requests.get(URL, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch contributions HTML: {resp.status_code}")

    soup = BeautifulSoup(resp.text, 'html.parser')
    cells = soup.find_all('td', class_='ContributionCalendar-day')

    days = []
    total_count = 0

    for cell in cells:
        date = cell.get('data-date')
        if not date:
            continue
        
        count = 0
        level = int(cell.get('data-level', 0))
        
        id_attr = cell.get('id')
        if id_attr:
            tool_tip = soup.find('tool-tip', {'for': id_attr})
            if tool_tip:
                txt = tool_tip.text.strip()
                if "No contributions" not in txt:
                    try:
                        count = int(txt.split()[0].replace(',', ''))
                    except ValueError:
                        count = 1

        total_count += count
        days.append({
            "date": date,
            "count": count,
            "level": level
        })

    os.makedirs("data", exist_ok=True)
    payload = {
        "total": total_count,
        "days": days
    }
    
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Fetched {len(days)} days of contributions for {USERNAME}. Total: {total_count}")

if __name__ == "__main__":
    fetch_contributions()