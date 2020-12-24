import os
import json
from dateutil.parser import parse
from datetime import datetime
from typing import Dict, Any, List, Optional
from . import Parser


class ConnectionsParser(Parser):
    connections_data: Dict[str, Any]
    followers: List[Any]
    following: List[Any]

    def __init__(self, username: str) -> None:
        super().__init__(username=username)
        self.connections_data = self.load_json('connections.json')
        self.validate()

    def validate(self) -> None:
        assert 'followers' in self.connections_data
        assert 'following' in self.connections_data

    def process(self, year: Optional[int]) -> None:
        def filter_connections(connections: Dict[str, Any], year: Optional[int]) -> List[str]:
            filtered_connections = []
            for username in connections:
                date_string = connections[username]
                date = parse(date_string)
                if year is not None and str(date.year) != str(year):
                    continue
                filtered_connections.append(username)
            return filtered_connections

        self.followers = filter_connections(connections=self.connections_data['followers'], year=year)
        self.following = filter_connections(connections=self.connections_data['following'], year=year)


    def print(self, number=10) -> None:
        print('You followed {0} users'.format(len(self.following)))
        print('You were followed by {0} users'.format(len(self.followers)))
