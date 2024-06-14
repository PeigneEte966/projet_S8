import re
from bs4 import BeautifulSoup
import requests
import json

def fetch_wikipedia_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def clean_section_title(title):
    # Supprimer tout ce qui se trouve entre crochets et ses espaces adjacents
    return re.sub(r'\[[^\]]+\]\s*', '', title)

def clean_context_text(text):
    # Supprimer tout ce qui se trouve entre crochets et ses espaces adjacents
    return re.sub(r'\[[^\]]+\]\s*', '', text)

def parse_wikipedia_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    content_list = []

    current_h2 = None
    current_h3 = None
    h2_paragraphs = []

    for tag in soup.find_all(['h2', 'h3', 'p']):
        if tag.name == 'h2':
            if current_h2 and h2_paragraphs:
                content_list.append({
                    "title": clean_section_title(current_h2),
                    "subtitle": None,
                    "contexte": " ".join(h2_paragraphs)
                })
            current_h2 = tag.get_text(strip=True)
            current_h3 = None
            h2_paragraphs = []
        elif tag.name == 'h3' and current_h2:
            if current_h2 and h2_paragraphs:
                content_list.append({
                    "title": clean_section_title(current_h2),
                    "subtitle": None,
                    "contexte": " ".join(h2_paragraphs)
                })
                h2_paragraphs = []
            current_h3 = tag.get_text(strip=True)
            paragraphs = []
            for sibling in tag.find_next_siblings():
                if sibling.name in ['h2', 'h3']:
                    break
                if sibling.name == 'p':
                    paragraphs.append(clean_context_text(sibling.get_text(strip=True)))
            if paragraphs:
                content_list.append({
                    "title": clean_section_title(current_h2),
                    "subtitle": clean_section_title(current_h3),
                    "contexte": " ".join(paragraphs)
                })
        elif tag.name == 'p' and current_h2 and not current_h3:
            h2_paragraphs.append(clean_context_text(tag.get_text(strip=True)))

    if current_h2 and h2_paragraphs:
        content_list.append({
            "title": clean_section_title(current_h2),
            "subtitle": None,
            "contexte": " ".join(h2_paragraphs)
        })

    return content_list

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# URL de la page Wikipedia à récupérer
url = "https://www.rtbf.be/article/les-chiffres-fous-et-les-anecdotes-improbables-de-l-euro-de-1960-a-1988-10759567"

# Récupérer la page Wikipedia
html = fetch_wikipedia_page(url)

# Analyser la page Wikipedia
data = parse_wikipedia_page(html)

# Enregistrer les données dans un fichier JSON
json_filename = 'chiffresAnecdotes.json'
save_to_json(data, json_filename)

print(f"Les données ont été enregistrées dans {json_filename}.")
