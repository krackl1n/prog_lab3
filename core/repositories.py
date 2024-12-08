from abc import ABC, abstractmethod
from dataclasses import asdict
import json
from typing import List

from models import Result


class ResultRepository(ABC):
    @abstractmethod
    def add(self, result: Result) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Result]:
        pass

class JsonResultRepository(ResultRepository):
    def __init__(self, file_path: str = "urls.json"):
        self.file_path = file_path

    def _load_result_from_file(self) -> List[Result]:
        try:
            with open(self.file_path, "r") as f:
                data = f.read().strip() 
                if not data: 
                    return []
                return [Result(**result) for result in json.loads(data)]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")
            return []

    def _save_result_to_file(self, results: List[Result]) -> None:
        with open(self.file_path, "w") as f:
            json.dump([asdict(result) for result in results], f, indent=4)

    def add(self, result: Result):
        try:
            results = self._load_result_from_file()  
            results.append(result)  
            self._save_result_to_file(results) 
        except Exception as e:
            print(f"Ошибка при добавлении результата: {e}")

    def get_all(self) -> List[Result]:
        return self._load_result_from_file()