import requests

headers = {"User-Agent": "Mozilla/5.0"}

# Try FIFA's other endpoints
urls = [
    "https://www.fifa.com/en/match-centre/competition/17",
    "https://digitalhub.fifa.com/api/match/2026",
    "https://fdh-api.fifa.com/v1/competitions/17/matches",
]

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"{url[:60]}... -> {r.status_code}")
    except Exception as e:
        print(f"{url[:60]}... -> {e}")