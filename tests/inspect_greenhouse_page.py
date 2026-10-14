
import requests
from bs4 import BeautifulSoup

url = "https://job-boards.greenhouse.io/datacamp/jobs/8074115"

response = requests.get(url, timeout=20)
print("HTTP status:", response.status_code)
print("Final URL:", response.url)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

selectors = [
    "section.adp-body",
    "#content",
    ".job-post-content",
    ".job__description",
    '[data-testid="job-description"]',
    "main",
]

print("\nSELECTOR RESULTS")
print("=" * 60)

for selector in selectors:
    element = soup.select_one(selector)

    if element is None:
        print(f"{selector}: NOT FOUND")
        continue

    text = element.get_text(separator="\n", strip=True)

    print(f"\n{selector}: {len(text)} characters")
    print("Preview:", text[:350])

print("\nPAGE TITLE")
print(soup.title.get_text(strip=True) if soup.title else "None")
