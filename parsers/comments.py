import os
import json
import re
from dateutil.parser import parse
from datetime import datetime
from typing import Dict, Any, List, Optional
from . import Parser

class CommentsParser(Parser):
    comments_data: Dict[str, Any]
    comments: List[Any]
    user_recipient_to_comments: Dict[str, List[Any]]
    users_to_tag_count: Dict[str, int]

    def __init__(self, username: str) -> None:
        super().__init__(username=username)
        self.comments_data = self.load_json('comments.json')
        self.validate()

    def validate(self):
        assert 'media_comments' in self.comments_data

    def process(self, year: Optional[int]) -> None:
        comments = []
        user_recipient_to_comments = {}
        users_to_tag_count = {}

        for comment in self.comments_data['media_comments']:
            [date_string, message, user_recipient] = comment
            date = parse(date_string)
            if year is not None and str(date.year) != str(year):
                continue

            comments.append(comment)
            user_recipient_to_comments[user_recipient] = user_recipient_to_comments.get(user_recipient, []) + [[date_string, message]]

            users_tagged = re.findall(r"@(\w+)\b", message)
            for user in users_tagged:
                users_to_tag_count[user] = users_to_tag_count.get(user, 0) + 1

        self.comments = comments
        self.user_recipient_to_comments = user_recipient_to_comments
        self.users_to_tag_count = users_to_tag_count

    def print(self, number=10):
        print('You commented on posts a total of {0} times'.format(len(self.comments)))

        user_recipients_ordered_by_comment_count = list(self.user_recipient_to_comments.keys())
        user_recipients_ordered_by_comment_count.sort(key=lambda user_recipient: len(self.user_recipient_to_comments[user_recipient]), reverse=True)

        print('You commented the most on these users\' posts')
        for user_recipient in user_recipients_ordered_by_comment_count[:number]:
            print('  {0} {1} times'.format(user_recipient, len(self.user_recipient_to_comments[user_recipient])))

        users_ordered_by_tag_count = list(self.users_to_tag_count.keys())
        users_ordered_by_tag_count.sort(key=lambda user: self.users_to_tag_count[user], reverse=True)

        print('You tagged these users the most in comments')
        for user in users_ordered_by_tag_count[:number]:
            print('  {0} {1} times'.format(user, self.users_to_tag_count[user]))
