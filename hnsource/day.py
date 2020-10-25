from collections import namedtuple

Day = namedtuple('Day', ('date_display', 'stories'))
DayWithStoryIds = namedtuple('DayWithStoryIds', ('date', 'story_ids'))
