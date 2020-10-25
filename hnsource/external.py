import logging
import time
import feedparser
import hnapi
from day import DayWithStoryIds
from story import Story
from bs4 import BeautifulSoup
from furl import furl
from datetime import datetime

def hn_id_from_link(hn_story_link):
	return furl(hn_story_link).args['id']

def get_story_id(rss_item):
	story = rss_item.find('span', {'class': 'storylink'})
	story_link = story.find('a').get('href')
	hn_story_link = rss_item.find('span', {'class': 'postlink'}).find('a').get('href')
	return hn_id_from_link(hn_story_link)

def parse():
	logging.info(f'Parsing external HN Daily source')
	d = feedparser.parse('http://www.daemonology.net/hn-daily/index.rss')
	days = []
	for day_entry in d['entries']: #[:1]:
		date = datetime.fromtimestamp(time.mktime(day_entry['published_parsed'])).date()
		logging.info(f'Parsing external day {date}')

		html = day_entry['summary_detail']['value']
		soup = BeautifulSoup(html, 'html.parser')
		rss_items = soup.select('ul > li')
		story_ids = [get_story_id(rss_item) for rss_item in rss_items]
		days.append(DayWithStoryIds(date, story_ids))
	return days
