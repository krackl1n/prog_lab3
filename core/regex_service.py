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
        pass

    def get_snils_in_web(self, url: str):
        pass

    def get_snils_in_text(self, text: str = "") -> List[str]:
        snils = self._find_snils(text)
        self.result_repository.add(Result(link='text', snils=snils))
        return snils



