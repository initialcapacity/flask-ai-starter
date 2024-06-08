import requests
from bs4 import BeautifulSoup


def extract_text(url: str) -> str:
    response = requests.get(url)

    return ' '.join(BeautifulSoup(response.text, "html.parser").stripped_strings)


