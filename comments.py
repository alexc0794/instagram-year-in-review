import os
import json
import re
from dateutil.parser import parse
from datetime import datetime


def comments_by_year(year, number = 5):
    with open(os.path.dirname(__file__) + '/data/comments.json') as file:
        data = json.load(file)

    assert 'media_comments' in data

    comments = data['media_comments']
    comments_this_year = []
    recipient_to_comments = {}
    users_to_tag_count = {}

    for comment in comments:
        [date_string, message, recipient] = comment
        date = parse(date_string)
        if str(date.year) == str(year):
            comments_this_year.append(comment)
            recipient_comments = recipient_to_comments.get(recipient) or []
            recipient_comments.append([date_string, message])
            recipient_to_comments[recipient] = recipient_comments

            users_tagged = re.findall(r"@(\w+)\b", message)
            for user in users_tagged:
                users_to_tag_count[user] = (users_to_tag_count.get(user) or 0) + 1


    recipient_ordered_by_comment_count = list(recipient_to_comments.keys())
    recipient_ordered_by_comment_count.sort(key=lambda recipient: len(recipient_to_comments[recipient]), reverse=True)

    users_ordered_by_tag_count = list(users_to_tag_count.keys())
    users_ordered_by_tag_count.sort(key=lambda user: users_to_tag_count[user], reverse=True)

    print('You commented on posts a total of {0} times'.format(len(comments_this_year)))
    print('You commented the most on these users\' posts'.format(number))
    for recipient in recipient_ordered_by_comment_count[:number]:
        print('  {0} {1} times'.format(recipient, len(recipient_to_comments[recipient])))
    print('You tagged these users the most in comments')
    for user in users_ordered_by_tag_count[:number]:
        print('  {0} {1} times'.format(user, users_to_tag_count[user]))
