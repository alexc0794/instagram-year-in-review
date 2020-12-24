import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum
from . import Parser

class MessageType(Enum):
    AUDIO = 'audio_files'
    TEXT = 'content'
    PHOTO = 'photos'
    VIDEO = 'videos'
    SHARE = 'share'


class InboxParser(Parser):
    directory_to_message_data: Dict[str, Any]
    user_directory_to_message_types: Dict[str, Any]

    @property
    def users(self) -> List[Any]:
        return list(self.user_directory_to_message_types.keys())

    def __init__(self, username: str) -> None:
        super().__init__(username=username)
        directory_to_message_data = {}
        inbox_path = '{0}/data/messages/inbox'.format(os.getcwd())
        for username_directory in os.listdir(inbox_path):
            directory = '{0}/{1}'.format(inbox_path, username_directory)
            message_data = []
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    with open('{0}/{1}'.format(directory, filename)) as file:
                        data = json.load(file)
                        assert 'participants' in data
                        assert 'messages' in data
                        message_data.append(data)
            directory_to_message_data[username_directory] = message_data

        self.directory_to_message_data = directory_to_message_data
        self.validate()

    def validate(self) -> None:
        pass

    def process(self, year: Optional[int]) -> None:
        user_directory_to_message_types = {}
        for user_directory in list(self.directory_to_message_data.keys()):
            message_data = self.directory_to_message_data[user_directory]

            type_to_messages = {}
            for message_type in MessageType:
                type_to_messages[message_type.value] = []

            for message_datum in message_data:
                messages = message_datum['messages']
                for message in messages:
                    date = datetime.fromtimestamp(float(message['timestamp_ms']) / 1000.0)
                    if year is not None and str(date.year) != str(year):
                        continue

                    for message_type in MessageType:
                        if message_type.value in message:
                            type_to_messages[message_type.value] = type_to_messages.get(message_type.value, []) + [message]

            if len(list(type_to_messages.keys())) > 0:
                # Dont add to mapping if no messages were exchanged in the given year
                user_directory_to_message_types[user_directory] = type_to_messages

        self.user_directory_to_message_types = user_directory_to_message_types

    def get_total_by_message_type(self, message_type: MessageType) -> int:
        total = 0
        for user_directory in list(self.directory_to_message_data.keys()):
            total += len(self.user_directory_to_message_types.get(user_directory, {}).get(message_type.value, []))
        return total

    def get_users_by_message_frequency(self, message_type: MessageType):
        users = self.users
        users.sort(
            key=lambda user_directory: len(self.user_directory_to_message_types.get(user_directory, {}).get(message_type.value, [])),
            reverse=True
        )
        return users

    def get_all_messages_from_user(self, user: str) -> List[Any]:
        messages = []
        messages_by_type = self.user_directory_to_message_types.get(user, {})
        for message_type in list(messages_by_type.keys()):
            messages += messages_by_type[message_type]
        return messages

    def get_users_by_message_disparity(self, sort_by_user_sent: bool):
        user_to_percentage_you_sent = {}
        users = []
        for user in self.users:
            messages = self.get_all_messages_from_user(user=user)
            total = len(messages)
            if total < 1:
                continue

            total_you_sent = 0
            for message in messages:
                if message['sender_name'] == self.username:
                    total_you_sent += 1
            try:
                percentage_you_sent = float(total_you_sent) / float(total)
            except:
                percentage_you_sent = 0
            users.append(user)
            user_to_percentage_you_sent[user] = int(percentage_you_sent * 100)

        users.sort(key=lambda user: user_to_percentage_you_sent.get(user, 0), reverse=sort_by_user_sent)
        return users, user_to_percentage_you_sent

    def print(self, number: int=5) -> None:
        print('You messaged a total of {0} people'.format(len(self.users)))

        for message_type in MessageType:
            total = self.get_total_by_message_type(message_type)
            print('You sent a total of {0} {1} this year'.format(total, message_type.value))

        print('')

        for message_type in MessageType:
            print('You exchanged the most {0} with these people'.format(message_type.value))
            users = self.get_users_by_message_frequency(message_type)
            for user in users[:number]:
                print('  {0} {1} {2}'.format('_'.join(user.split('_')[0:-1]), len(self.user_directory_to_message_types.get(user, {}).get(message_type.value, [])), message_type.value))
            print('')

        if (not self.username):
            return

        print('There were some people that weren\'t very talktative')
        users_by_message_disparity, user_to_percentage_you_sent = self.get_users_by_message_disparity(True)
        for user in users_by_message_disparity[:number]:
            print('  you sent {1}% of the messages to {0}'.format('_'.join(user.split('_')[0:-1]), user_to_percentage_you_sent[user]))

        print('')

        print('And there were others you weren\'t very talkative to')
        users_by_message_disparity, user_to_percentage_you_sent = self.get_users_by_message_disparity(False)
        for user in users_by_message_disparity[:number]:
            print('  you sent {1}% of the messages to {0}'.format('_'.join(user.split('_')[0:-1]), user_to_percentage_you_sent.get(user, 0)))
