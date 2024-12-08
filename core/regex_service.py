from dataclasses import asdict
import json
import re
from typing import List
from requests import RequestException, get

from core.models import Result
from core.repositories import ResultRepository



PATTERN = r'https?://[\w.-]+(?:\.[\w.-]+)*(?:[/?#][^\s]*)?'

class RegexService:
    def __init__(self, result_repository: ResultRepository):
        self.result_repository = result_repository

    def _find_urls(self, text: str) -> List[str]:
        return re.findall(PATTERN, text)
    
    def get_urls_in_file(self):
        result_data = self.result_repository.get_all()
        result_str = ", ".join([str(asdict(result)) for result in result_data])
        urls = self._find_urls(result_str)
        return Result(link="jsonFile", urls=urls)

    def get_urls_in_web(self, url: str):
        try:
            response = get(url)
            if response.status_code == 200:
                snils = self._find_urls(response.text)
                self.result_repository.add(Result(link=url, urls=snils))
                return Result(link=url, urls=snils)
            else:
                print(f"Error: Unable to fetch URL {url}, Status Code: {response.status_code}")
                return Result(link=url, urls=[])
        except RequestException as e:
            print(f"Error: {e}")
            return Result(link=url, urls=[])

    def get_urls_in_text(self, text: str = "") -> List[str]:
        urls = self._find_urls(text)
        self.result_repository.add(Result(link='text', urls=urls))
        return urls



