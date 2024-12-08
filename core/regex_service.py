from dataclasses import asdict
import json
import re
from typing import List

from requests import RequestException, get
from models import Result
from repositories import ResultRepository

PATTERN = r''

class RegexService:
    def __init__(self, result_repository: ResultRepository):
        self.result_repository = result_repository
        pass

    def _find_snils(self, text: str) -> List[str]:
        return re.findall(PATTERN, text)
    
    def get_snils_in_file(self):
        result_data = self.result_repository.get_all()
        result_str = ", ".join([str(asdict(result)) for result in result_data])
        snils = self._find_snils(result_str)
        return Result(link="jsonFile", snils=snils)

    def get_snils_in_web(self, url: str):
        try:
            response = get(url)
            if response.status_code == 200:
                snils = self._find_snils(response.text)
                self.result_repository.add(Result(link=url, snils=snils))
                return Result(link=url, snils=snils)
            else:
                print(f"Error: Unable to fetch URL {url}, Status Code: {response.status_code}")
                return Result(link=url, snils=[])
        except RequestException as e:
            print(f"Error: {e}")
            return Result(link=url, snils=[])

    def get_snils_in_text(self, text: str = "") -> List[str]:
        snils = self._find_snils(text)
        self.result_repository.add(Result(link='text', snils=snils))
        return snils



