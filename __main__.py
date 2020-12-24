from parsers.likes import LikesParser
from parsers.comments import CommentsParser
from parsers.stories import StoriesParser
from parsers.connections import ConnectionsParser
from parsers.inbox import InboxParser

print('Welcome to Your Instagram Year in Review!!!')
print('Enter the year (default 2020)')
print('-> ', end='')
try:
    year = str(int(input()))
except:
    year = '2020'
last_year = str(int(year) - 1)

print('Enter your IG username:')
print('-> ', end='')
try:
    username = input()
except:
    username = ''

Parsers = [
    ConnectionsParser,
    CommentsParser,
    LikesParser,
    StoriesParser,
    InboxParser
]

for Parser in Parsers:
    parser = Parser(username=username)
    parser.process(year=year)
    parser.print()
    print('\n')
