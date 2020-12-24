import json
import os
from abc import ABC, abstractmethod
from typing import Optional

class Parser(ABC):
    username: str
    def __init__(self, username: str) -> None:
        self.username = username


    @abstractmethod
    def validate(self) -> None:
        pass

    @abstractmethod
    def process(self, year: Optional[int]) -> None:
        pass

    @abstractmethod
    def print(self) -> None:
        pass

    def load_json(self, filename: str):
        try:
            filepath = '{0}/data/{1}'.format(os.getcwd(), filename)
            with open(filepath) as file:
                data = json.load(file)
                return data
        except:
            print('There was a problem loading {0}'.format(filename))
