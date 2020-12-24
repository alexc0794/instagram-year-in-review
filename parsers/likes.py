import os
import json
from dateutil.parser import parse
from datetime import datetime
from typing import Dict, Any, List, Optional
from . import Parser


class LikesParser(Parser):
    likes_data: Dict[str, Any]
    likes: List[Any]
    user_to_likes: Dict[str, Any]

    def __init__(self, username: str) -> None:
        super().__init__(username=username)
        self.likes_data = self.load_json('likes.json')
        self.validate()

    def validate(self) -> None:
        assert 'media_likes' in self.likes_data

    def process(self, year: Optional[int]) -> None:
        likes = []
        user_to_likes = {}

        for like in self.likes_data['media_likes']:
            [date_string, username] = like;
            date = parse(date_string)
            if year is not None and str(date.year) != str(year):
                continue
            likes.append(like)
            user_to_likes[username] = user_to_likes.get(username, []) + [date_string]

        self.likes = likes;
        self.user_to_likes = user_to_likes

    def print(self, number=10) -> None:
        print('You liked a total of {0} posts'.format(len(self.likes)))

        users_ordered_by_like_count = list(self.user_to_likes.keys())
        users_ordered_by_like_count.sort(key=lambda user: len(self.user_to_likes[user]), reverse=True)

        print('You liked posts from these users the most')
        for username in users_ordered_by_like_count[:number]:
            print('  {0} {1} times'.format(username, len(self.user_to_likes[username])))
