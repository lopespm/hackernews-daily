import logging
import asyncio
from pyppeteer import launch
from PIL import Image
from os import path
import signal, psutil, os


def save_optimized(story, size, prefix, generated_folder):
	image = Image.open(f'{generated_folder}/{story.id}.png')
	image.thumbnail(size, Image.ANTIALIAS)
	image.save(f'{generated_folder}/{prefix}_{story.id}.png')
	image.save(f'{generated_folder}/{prefix}_{story.id}.webp')

async def save_screenshots(days, generated_folder):
	browser = await launch(headless=True)
	page = await browser.newPage()
	all_stories = (story for day in days for story in day.stories)
	for idx, story in enumerate(all_stories):
		logging.info(f'{story.id}: Gathering screenshot for story')
		try:
			full_image_path = get_full_image_path(story, generated_folder)
			if (path.exists(full_image_path)):
				logging.info(f'Skipping {story.id}, {full_image_path} already exists')
				continue

			if (story.link.endswith('.pdf')):
				logging.info(f'Skipping {story.id}, {story.link} is a pdf')
				continue

			if (page.isClosed()):
				page = await browser.newPage()

			await asyncio.wait_for(visit_page_and_take_screenshot(page, story, generated_folder), timeout=30)

		except Exception as error:
			logging.error(f'An exception occurred while gathering the screens for story {story.id}. Skipping story and restarting browser.')
			logging.error(error)
			try:
				await asyncio.wait_for(browser.close(), timeout=10)
				kill_child_processes(os.getpid())
			except Exception as error:
				logging.error(f'An exception occurred while trying to kill the browser')
				logging.error(error)
			browser = await launch(headless=True)
			page = await browser.newPage()

	await browser.close()

async def visit_page_and_take_screenshot(page, story, generated_folder):
	full_image_path = get_full_image_path(story, generated_folder)
	logging.info(f'{story.id}: Visiting page {story.link}')
	await page.goto(story.link)
	logging.info(f'{story.id}: Attempt to accept cookies')
	await attempt_to_accept_cookies(page)
	logging.info(f'{story.id}: Take screenshot')
	await page.screenshot({'path': full_image_path})
	logging.info(f'{story.id}: Saving optimized screenshots')
	save_optimized(story, [316, 316], 'default', generated_folder)
	logging.info(f'{story.id}: Finished screenshot')

def get_full_image_path(story, generated_folder):
	return f'{generated_folder}/{story.id}.png'

async def attempt_to_accept_cookies(page):
	await page.evaluate("""() => {
		function xcc_contains(selector, text) {
		var elements = document.querySelectorAll(selector);
		return Array.prototype.filter.call(elements, function(element){
			return RegExp(text, "i").test(element.textContent.trim());
		});
		}
    	var _xcc;
    	_xcc = xcc_contains('[id*=cookie] a, [class*=cookie] a, [id*=cookie] button, [class*=cookie] button', '^(Accept|Accept All|Alle akzeptieren|Akzeptieren|Verstanden|Zustimmen|Okay|OK)$');
    	if (_xcc != null && _xcc.length != 0) { _xcc[0].click(); }
		}""");

def kill_child_processes(parent_pid, sig=signal.SIGTERM):
	try:
		parent = psutil.Process(parent_pid)
	except psutil.NoSuchProcess:
		logging.info(f'No process exists for pid {parent_pid}')
		return
		children = parent.children(recursive=True)
	for process in children:
		logging.info(f'Killing process {process}')
		process.send_signal(sig)
