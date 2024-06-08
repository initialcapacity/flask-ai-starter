from typing import List

import feedparser
import requests


def extract_links(url: str) -> List[str]:
    response = requests.get(url)

    result = feedparser.parse(response.text)

    return [e.link for e in result.entries]
