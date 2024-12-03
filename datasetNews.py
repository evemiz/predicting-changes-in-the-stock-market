# Script to extract the features from the artical from a json file
import json
import google.generativeai as genai
import csv
import re
import os
import time
import google.api_core.exceptions


genai.configure(api_key="AIzaSyCuS3RTubm6BQLGjPdOSYwtFBrU8EZWuFw")

emotions = [
    "Fear", "Optimism", "Anger", "Joy", "Trust",
    "Despair", "Economic Security", "Uncertainty", "Fear for the future"
]


def create_prompt(title, content, date):
    return f"Given the title: {title}, the content: {content}, and the publication date: {date}, please analyze the emotions evoked by this article. Provide a list of emotions that the article evokes. Only list emotions from the following list if they are mentioned: Fear, Optimism, Anger, Joy, Trust, Despair, Economic Security, Uncertainty, Fear for the future. Respond with a list of emotions that are present in the article. Example: ['Fear', 'Despair', 'Uncertainty']"


def load_articles(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        articles = []
        for keyword, keyword_articles in data.items():
            articles.extend(keyword_articles)
        return articles


def analyze_emotions(title, content, date):
    prompt = create_prompt(title, content, date)
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(prompt)
        return response.text
    except google.api_core.exceptions.ResourceExhausted as e:
        print(f"Resource exhausted error: {e}. Retrying in 60 seconds.")
        time.sleep(60)
        return analyze_emotions(title, content, date)
    except Exception as e:
        print(f"Unexpected error on article {title}: {e}.")
        return None


def process_emotions(response_text):
    found_emotions = []
    match = re.search(r"\[([^\]]+)\]", response_text)
    if match:
        found_emotions = match.group(1).replace("'", "").split(', ')
    return found_emotions


def save_to_csv(data, filename='emotions_dataset.csv'):
    file_exists = os.path.exists(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['title', 'date'] + emotions)
        for row in data:
            writer.writerow(row)


def main():
    articles_file = 'articles-2022-2024/articles-2022-10.json'
    print(articles_file)
    articles = load_articles(articles_file)
    results = []

    for article in articles:
        title = article.get("title")
        content = article.get("content")
        date = article.get("date")
        response_text = analyze_emotions(title, content, date)
        found_emotions = process_emotions(response_text)
        row = [title, date] + [1 if emotion in found_emotions else 0 for emotion in emotions]
        results.append(row)

    save_to_csv(results)


if __name__ == '__main__':
    main()
