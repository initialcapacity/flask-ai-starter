from typing import List

from starter.documents.documents_gateway import DocumentsGateway
from starter.documents.documents_service import DocumentsService
from starter.rss.link_extractor import extract_links
from starter.rss.text_extractor import extract_text


class DocumentCollector:
    def __init__(self, gateway: DocumentsGateway, service: DocumentsService):
        self.gateway = gateway
        self.service = service

    def collect(self, feed_urls: List[str]):
        sources = [
            link
            for feed_url in feed_urls
            for link in extract_links(feed_url) if not self.gateway.exists(link)
        ]

        for source in sources:
            content = extract_text(source)
            self.service.create(source, content)
