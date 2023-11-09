import requests
from bs4 import BeautifulSoup
from collections import Counter
import csv
from urllib.parse import urlparse

# Etape 1
def count_words_occurrences(text):
    words = text.split()
    word_count = Counter(words)
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_word_count

# Etape 2
def remove_stopwords(word_occurrences, stopwords):
    filtered_occurrences = [(word, count) for word, count in word_occurrences if word.lower() not in stopwords]
    return filtered_occurrences

# Etape 3
def get_stopwords_from_file(file_path):
    with open(file_path, 'r') as file:
        stopwords = [line.strip() for line in file]
    return stopwords

# Etape 5
def remove_html_tags(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text()

# Etape 6
def get_attribute_values(html_text, tag_name, attribute_name):
    soup = BeautifulSoup(html_text, 'html.parser')
    values = [tag.get(attribute_name) for tag in soup.find_all(tag_name)]
    return values

# Etape 8
def extract_domain_name(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

# Etape 9
def filter_urls_by_domain(domain, urls):
    domain_urls = [url for url in urls if extract_domain_name(url) == domain]
    non_domain_urls = [url for url in urls if extract_domain_name(url) != domain]
    return domain_urls, non_domain_urls

# Etape 10
def get_html_text_from_url(url):
    response = requests.get(url)
    return response.text

# Etape 11
def seo_audit(url):
    html_text = get_html_text_from_url(url)
    text_without_html = remove_html_tags(html_text)

    # Etape 1
    word_occurrences = count_words_occurrences(text_without_html)

    # Etape 3
    stopwords = get_stopwords_from_file('parasite.csv')

    # Etape 2
    filtered_occurrences = remove_stopwords(word_occurrences, stopwords)

    # Etape 6
    alt_values = get_attribute_values(html_text, 'img', 'alt')

    # Etape 8
    domain = extract_domain_name(url)

    # Etape 9
    links = get_attribute_values(html_text, 'a', 'href')
    domain_links, non_domain_links = filter_urls_by_domain(domain, links)

    print(f"Mots clefs: {filtered_occurrences[:3]}")
    print(f"Nombre de liens entrants: {len(domain_links)}")
    print(f"Nombre de liens sortants: {len(non_domain_links)}")
    print(f"Présence de balises alt: {bool(alt_values)}")
    
# Testez le programme avec l'URL choisi
url_to_audit = input("Veuillez entrer l'URL à analyser : ")
seo_audit(url_to_audit)
