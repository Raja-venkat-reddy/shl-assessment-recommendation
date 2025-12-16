import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

# ---------------- CONFIG ----------------
BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/products/product-catalog/"
OUTPUT_PATH = "data/shl_catalog.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest"
}

PAGE_SIZE = 12
REQUEST_DELAY = 1.2
DETAIL_DELAY = 0.8
TIMEOUT = 60
MAX_RETRIES = 3

# 🔑 Multiple catalog categories (key improvement)
CATEGORY_TYPES = [2, 3, 4, 5, 6]  
# 2 = Individual
# others = Ability / Personality / Language / Coding (discovered via Network)


# ---------------- FETCH CATALOG PAGE ----------------
def fetch_page(start, category, retries=MAX_RETRIES):
    params = {
        "start": start,
        "type": category
    }

    for attempt in range(1, retries + 1):
        try:
            r = requests.get(
                CATALOG_URL,
                headers=HEADERS,
                params=params,
                timeout=TIMEOUT
            )
            r.raise_for_status()
            return r.text
        except requests.exceptions.ReadTimeout:
            print(f"⏳ Timeout (cat={category}, start={start}) retry {attempt}/{retries}")
            time.sleep(5)
        except requests.exceptions.RequestException:
            break

    return None


# ---------------- EXTRACT LINKS ----------------
def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/products/" in href and "job" not in href.lower():
            links.add(urljoin(BASE_URL, href))

    return links


# ---------------- SCRAPE DETAIL ----------------
def scrape_detail(url):
    for _ in range(MAX_RETRIES):
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            break
        except requests.exceptions.ReadTimeout:
            time.sleep(5)
    else:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    name_tag = soup.find("h1")
    name = name_tag.get_text(strip=True) if name_tag else ""

    description = soup.get_text(" ", strip=True)
    text = description.lower()

    test_type = []
    if any(k in text for k in ["personality", "behavior", "behaviour"]):
        test_type.append("P")
    if any(k in text for k in ["skill", "knowledge", "ability", "cognitive", "technical"]):
        test_type.append("K")

    if not test_type:
        test_type = ["K"]

    return {
        "name": name,
        "url": url,
        "description": description[:1200],
        "test_type": test_type,
        "duration": None,
        "adaptive_support": "Unknown",
        "remote_support": "Unknown"
    }


# ---------------- MAIN ----------------
def main():
    all_links = set()

    print("🔍 Collecting assessment links across categories...")

    for category in CATEGORY_TYPES:
        print(f"\n📂 Category type={category}")
        start = 0

        while True:
            print(f"   ↳ start={start}")
            html = fetch_page(start, category)
            if html is None:
                break

            links = extract_links(html)
            new_links = links - all_links

            if not new_links:
                break

            all_links.update(new_links)
            start += PAGE_SIZE
            time.sleep(REQUEST_DELAY)

    print(f"\n🔗 Total unique assessment links found: {len(all_links)}")

    assessments = []
    for idx, url in enumerate(all_links, 1):
        print(f"[{idx}/{len(all_links)}] Scraping {url}")
        data = scrape_detail(url)
        if data and data["name"]:
            assessments.append(data)
        time.sleep(DETAIL_DELAY)

    print(f"\n✅ Total assessments scraped: {len(assessments)}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(assessments, f, indent=2, ensure_ascii=False)

    print(f"📁 Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()