import os
import json
from dateutil.parser import parse
from datetime import datetime

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
filepaths = ['/data/media1.json', '/data/media2.json', '/data/media3.json', '/data/media4.json', '/data/media5.json']

def _get_stories_this_year(filepath, year):
    try:
        with open(filepath) as file:
            data = json.load(file)
        assert 'stories' in data
    except:
        return []

    stories_this_year = []
    stories = data['stories']

    for story in stories:
        assert 'caption' in story
        assert 'taken_at' in story
        caption = story['caption']
        taken_at = story['taken_at']
        date = parse(taken_at)
        if str(date.year) == str(year):
            stories_this_year.append([caption, date])

    return stories_this_year


def stories_by_year(year):
    stories_this_year = []

    directory = os.getcwd() + '/data'
    for subdirectory in os.listdir(directory):
        if subdirectory.startswith('media'):
            filepath = directory + "/" + subdirectory
            filepath_stories_this_year = _get_stories_this_year(filepath, year)
            stories_this_year = stories_this_year + filepath_stories_this_year

    weekday_to_story_frequency = [0, 0, 0, 0, 0, 0, 0] # List of zeroes for each day of week
    for story in stories_this_year:
        [caption, date] = story
        weekday_to_story_frequency[date.weekday()] += 1

    print('You posted a total of {0} stories'.format(len(stories_this_year)))
    for weekday in range(len(weekday_to_story_frequency)):
        frequency = weekday_to_story_frequency[weekday]
        day = WEEKDAYS[weekday]
        try:
            percentage = int(float(frequency) / float(len(stories_this_year)) * 100)
        except:
            percentage = 0
        print('  {0} times on {1}s ({2}%)'.format(frequency, day, percentage))
