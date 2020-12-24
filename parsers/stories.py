import os
import json
from dateutil.parser import parse
from datetime import datetime
from typing import Dict, Any, List, Optional
from . import Parser

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class StoriesParser(Parser):
    stories_data: List[Dict[str, Any]]
    stories: List[Any]
    weekday_to_story_frequency: Dict[int, Any]

    def __init__(self, username: str) -> None:
        super().__init__(username=username)
        stories_data = []
        directory = os.getcwd() + '/data'
        for subdirectory in os.listdir(directory):
            if subdirectory.startswith('media'):
                try:
                    with open('{0}/{1}'.format(directory, subdirectory)) as file:
                        stories_data.append(json.load(file))
                except:
                    continue

        self.stories_data = stories_data
        self.validate()

    def validate(self):
        for stories_datum in self.stories_data:
            assert 'stories' in stories_datum

    def process(self, year: Optional[int]):
        stories = []
        for stories_datum in self.stories_data:
            for story in stories_datum['stories']:
                assert 'caption' in story
                assert 'taken_at' in story
                caption = story['caption']
                taken_at = story['taken_at']
                date = parse(taken_at)
                if year is not None and str(date.year) != str(year):
                    continue

                stories.append([caption, date])

        weekday_to_story_frequency = [0, 0, 0, 0, 0, 0, 0] # List of zeroes for each day of week
        for story in stories:
            [caption, date] = story
            weekday_to_story_frequency[date.weekday()] += 1

        self.stories = stories
        self.weekday_to_story_frequency = weekday_to_story_frequency

    def print(self):
        print('You posted a total of {0} stories'.format(len(self.stories)))
        for weekday in range(len(self.weekday_to_story_frequency)):
            frequency = self.weekday_to_story_frequency[weekday]
            day = WEEKDAYS[weekday]
            try:
                percentage = int(float(frequency) / float(len(self.stories)) * 100)
            except:
                percentage = 0
            print('  {0} times on {1}s ({2}%)'.format(frequency, day, percentage))
