import logging
import external
import hnapi
import pickle
import itertools
from day import Day, DayWithStoryIds
from datetime import datetime
from collections import deque

DAYS_HISTORY_FILE_NAME = "days_history.dat"
MAX_DAYS_HISTORY_SIZE = 50
MAX_DAYS_BUILT = 10
STORIES_PER_DAY = 10

def reset_from_external_hn_daily():
    days = external.parse()
    days_history = deque([])
    for day in days:
        days_history.append(day)
    pickle.dump( days_history, open( DAYS_HISTORY_FILE_NAME, "wb" ) )

def update_history():
    days_history = pickle.load( open( DAYS_HISTORY_FILE_NAME, "rb" ) )
    today_date = datetime.today().date()

    latest_history_day = days_history[0].date
    if (latest_history_day == today_date):
        logging.info(f'Skipping update. Was already processed today - latest history day: {latest_history_day} | today: {today_date}')
        return

    current_best_story_ids = iter(hnapi.best_story_ids())
    history_previous_story_ids_set = set(story_id for day in days_history for story_id in day.story_ids)
    todays_story_ids = []
    while len(todays_story_ids) < STORIES_PER_DAY:
        story_id = next(current_best_story_ids)
        if story_id not in history_previous_story_ids_set:
            todays_story_ids.append(story_id)

    days_history.appendleft(DayWithStoryIds(today_date, todays_story_ids))
    while len(days_history) > MAX_DAYS_HISTORY_SIZE:
        days_history.pop()

    pickle.dump( days_history, open( DAYS_HISTORY_FILE_NAME, "wb" ) )


def get_all_days_top_stories():
    days_history = pickle.load( open( DAYS_HISTORY_FILE_NAME, "rb" ) )
    days = []
    for day in itertools.islice(days_history, 0, MAX_DAYS_BUILT):
        date_display = day.date.strftime("%d %B %Y")
        stories = [hnapi.get_story(story_id) for story_id in day.story_ids]
        days.append(Day(date_display, stories))
    return days
