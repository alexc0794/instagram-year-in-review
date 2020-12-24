import os
import json
from dateutil.parser import parse
from datetime import datetime


def connections_by_year(year):
    with open(os.path.dirname(__file__) + '/data/connections.json') as file:
        data = json.load(file)

    assert 'followers' in data
    assert 'following' in data


    followers = data['followers']
    following = data['following']

    def get_connections_this_year(connections, year):
        connections_this_year = {}
        for username in connections:
            date_string = connections[username]
            date = parse(date_string)
            if str(date.year) == str(year):
                connections_this_year[username] = date_string
        return connections_this_year

    followers_this_year = get_connections_this_year(followers, year)
    following_this_year = get_connections_this_year(following, year)

    print('You followed {0} users'.format(len(list(following_this_year.keys()))))
    print('You were followed by {0} users'.format(len(list(followers_this_year.keys()))))
