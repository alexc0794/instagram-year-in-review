from likes import likes_by_year
from comments import comments_by_year
from stories import stories_by_year
from connections import connections_by_year
from inbox import inbox_by_year

print('Welcome to Your Instagram Year in Review!!!')
print('Enter a year (otherwise will default to 2020)')

try:
    year = str(int(input()))
except:
    year = '2020'
last_year = str(int(year) - 1)

print('In {0}'.format(year))
connections_by_year(year)
print('\n')


print('In {0}'.format(year))
likes_by_year(year)
print('\n')


print('In {0}'.format(year))
comments_by_year(year)
print('\n')


print('In {0}'.format(year))
stories_by_year(year)
print('\n')


print('In {0}'.format(year))
inbox_by_year(year)
print('')
