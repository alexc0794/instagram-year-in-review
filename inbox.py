import os
import json
from datetime import datetime


def inbox_by_year(year, number = 10):
    directory = os.getcwd() + '/data/messages/inbox'
    directory_to_message_data = {}
    for subdirectory in os.listdir(directory):
        message_data = get_message_data('{0}/{1}'.format(directory, subdirectory))
        directory_to_message_data[subdirectory] = message_data

    user_directory_to_message_types = {}

    user_directories = list(directory_to_message_data.keys())
    for user_directory in user_directories:
        message_data = directory_to_message_data[user_directory]
        texts = []
        photos = []
        videos = []

        for message_datum in message_data:
            messages = message_datum['messages']
            for message in messages:
                date = datetime.fromtimestamp(float(message['timestamp_ms']) / 1000.0)
                if str(date.year) == str(year):
                    if 'content' in message:
                        texts.append(message)
                    if 'photos' in message and len(message['photos']) > 0:
                        photos.append(message)
                    if 'videos' in message and len(message['videos']) > 0:
                        videos.append(message)

        if texts or photos or videos:
            # Dont add to mapping if no messages were exchanged in the given year
            user_directory_to_message_types[user_directory] = {
                'texts': texts,
                'photos': photos,
                'videos': videos
            }

    print('You messaged a total of {0} people'.format(len(list(user_directory_to_message_types.keys()))))

    def get_total(key):
        total = 0
        for user_directory in user_directories:
            total += len(user_directory_to_message_types.get(user_directory, {}).get(key, []))
        return total

    for key in ['texts', 'photos', 'videos']:
        total = get_total(key)
        print('You sent a total of {0} {1} this year'.format(total, key))

    print('')

    def get_users_by_message_frequency(key, users):
        users.sort(key=lambda user_directory: len(user_directory_to_message_types.get(user_directory, {}).get(key, [])), reverse=True)
        return users

    for key in ['texts', 'photos', 'videos']:
        print('You exchanged the most {0} with these people'.format(key))
        users = get_users_by_message_frequency(key, user_directories)
        for user in users[:number]:
            print('  {0} {1} {2}'.format('_'.join(user.split('_')[0:-1]), len(user_directory_to_message_types.get(user, {}).get(key, [])), key))
        print('')


    def get_users_by_message_disparity(your_username, users, sort_by_user_sent):
        user_to_percentage_you_sent = {}
        valid_users = []
        for user in users:
            texts = user_directory_to_message_types.get(user, {}).get('texts', [])
            total = len(texts)
            if total < 1:
                continue

            total_you_sent = 0
            for text in texts:
                if text['sender_name'] == your_username:
                    total_you_sent += 1
            try:
                percentage_you_sent = float(total_you_sent) / float(total)
            except:
                percentage_you_sent = 0
            valid_users.append(user)
            user_to_percentage_you_sent[user] = int(percentage_you_sent * 100)

        valid_users.sort(key=lambda user: user_to_percentage_you_sent.get(user, 0), reverse=sort_by_user_sent)
        return valid_users, user_to_percentage_you_sent

    print('There were some people that weren\'t very talktative')
    users_by_message_disparity, user_to_percentage_you_sent = get_users_by_message_disparity('alegs.chow', user_directories, True)
    for user in users_by_message_disparity[:number]:
        print('  you sent {1}% of the messages to {0}'.format('_'.join(user.split('_')[0:-1]), user_to_percentage_you_sent[user]))

    print('')

    print('And there were others you weren\'t very talkative to')
    users_by_message_disparity, user_to_percentage_you_sent = get_users_by_message_disparity('alegs.chow', user_directories, False)
    for user in users_by_message_disparity[:number]:
        print('  you sent {1}% of the messages to {0}'.format('_'.join(user.split('_')[0:-1]), user_to_percentage_you_sent.get(user, 0)))



def get_message_data(directory):
    message_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open('{0}/{1}'.format(directory, filename)) as file:
                data = json.load(file)
                assert 'participants' in data
                assert 'messages' in data
                message_data.append(data)
    return message_data
