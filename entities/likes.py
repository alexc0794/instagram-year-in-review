import os
import json
from dateutil.parser import parse
from datetime import datetime


def likes_by_year(year, number = 10):
    with open(os.getcwd() + '/data/likes.json') as file:
        data = json.load(file)

    assert 'media_likes' in data

    user_to_likes = {};
    media_likes = data['media_likes']
    likes_this_year = []
    for like in media_likes:
        [date_string, username] = like;
        date = parse(date_string)
        if str(date.year) == str(year):
            likes_this_year.append(like)
            user_likes = user_to_likes.get(username) or []
            user_likes.append(date_string)
            user_to_likes[username] = user_likes

    print('You liked a total of {0} posts'.format(len(likes_this_year)))

    users_ordered_by_like_count = list(user_to_likes.keys())
    users_ordered_by_like_count.sort(key=lambda user: len(user_to_likes[user]), reverse=True)

    print('You liked posts from these users the most'.format(year))
    for username in users_ordered_by_like_count[:number]:
        print('  {0} {1} times'.format(username, len(user_to_likes[username])))
