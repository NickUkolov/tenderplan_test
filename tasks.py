import xmltodict
from bs4 import BeautifulSoup
from celery import Task

from common import requests_get


class FetchLinks(Task):
    name = "fetch_links"

    def run(self, page_url: str) -> list:
        response = requests_get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")

        orders_blocks = soup.find_all(
            "div", class_="w-space-nowrap ml-auto registry-entry__header-top__icon"
        )
        links = [
            link.find("a", {"href": True}, target="_blank").get("href")
            for link in orders_blocks
        ]

        return links


class ParseXML(Task):
    name = "parse_xml"

    def run(self, link: str) -> tuple:
        xml_link = link.replace("view.html", "viewXml.html")
        xml_response = requests_get("https://zakupki.gov.ru" + xml_link)

        xml_data = xmltodict.parse(xml_response.content)
        xml_dict = next(iter(xml_data.values()))
        publish_date = xml_dict.get("commonInfo", {}).get("publishDTInEIS")
        return link, publish_date
