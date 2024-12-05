# script to fetch articles from 2022 to 2024 with guardian API

import requests
import json
from datetime import datetime, timedelta

api_key = ''

keywords = [
    "Economic crisis", "Stock market", "Inflation", "Recession", "US economy",
    "Elections", "Climate change", "Nuclear threat", "Unemployment", "Peace",
    "Economic recovery", "Innovation", "Market expansion",
    "Technological progress", "Investment opportunities", "Trade agreements",
    "Taxes", "Venture capital", "Entrepreneurship", "Employment growth",
    "Interest rate", "Artificial intelligence", "Foreign policy",
    "Financial security", "Large-scale fundraising", "Entrepreneurial growth",
    "Startup funding success", "War", "Ceasefire", "Terrorism", "Pandemic"
]


def fetch_articles(keyword, from_date=None, to_date=None):
    url = f'https://content.guardianapis.com/search?q={keyword}&api-key={api_key}&show-fields=bodyText,headline&order-by=relevance&page-size=5'
    if from_date:
        url += f'&from-date={from_date}'
    if to_date:
        url += f'&to-date={to_date}'
    url += '&gl=us'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['response']['results']
    else:
        print(f"Failed to fetch articles for {keyword}. Status code: {response.status_code}")
        return []


def generate_date_ranges(start_date, end_date):
    date_ranges = []
    current_date = start_date

    while current_date <= end_date:
        next_month = current_date.replace(day=28) + timedelta(days=4)  # קח את היום ה-28 של החודש הנוכחי
        last_day_of_month = next_month - timedelta(days=next_month.day)  # מצא את היום האחרון של החודש
        first_day_of_month = current_date.replace(day=1)  # היום הראשון של החודש
        date_ranges.append((first_day_of_month.strftime('%Y-%m-%d'), last_day_of_month.strftime('%Y-%m-%d')))
        current_date = last_day_of_month + timedelta(days=1)

    return date_ranges


start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 11, 30)

date_ranges = generate_date_ranges(start_date, end_date)

for from_date, to_date in date_ranges:
    month_year = datetime.strptime(from_date, '%Y-%m-%d').strftime('%Y-%m')
    all_articles = {}

    print(f"Fetching articles for: {month_year}")

    for keyword in keywords:
        print(f"  Fetching articles for: {keyword}")
        articles = fetch_articles(keyword, from_date, to_date)
        if articles:
            all_articles[keyword] = []
            for article in articles:
                article_info = {
                    'title': article['webTitle'],
                    'date': article['webPublicationDate'],
                    'content': article.get('fields', {}).get('bodyText', '')
                }
                all_articles[keyword].append(article_info)

    file_name = f'articles-{month_year}.json'
    with open(file_name, 'w') as f:
        json.dump(all_articles, f, indent=4)

    print(f"Saved articles for {month_year} to {file_name}")

print("השלמת החיפוש ושמירה לקבצים")
