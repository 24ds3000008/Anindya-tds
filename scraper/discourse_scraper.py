import requests
import time
import json
import os

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
OUTPUT_FILE = "data/discourse_posts.json"

def get_latest_topics(page=1):
    url = f"{BASE_URL}/latest.json?page={page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("topic_list", {}).get("topics", [])
    return []

def get_topic_posts(topic_id):
    url = f"{BASE_URL}/t/{topic_id}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def scrape_forum(pages=10):
    all_data = []
    for page in range(1, pages + 1):
        print(f"Fetching page {page}...")
        topics = get_latest_topics(page)
        for topic in topics:
            topic_id = topic["id"]
            print(f" - Fetching topic {topic_id}...")
            topic_data = get_topic_posts(topic_id)
            if topic_data:
                all_data.append(topic_data)
            time.sleep(0.5)  # Respectful delay
    return all_data

if __name__ == "__main__":
    posts = scrape_forum(pages=2)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Scraped {len(posts)} topics saved to {OUTPUT_FILE}")