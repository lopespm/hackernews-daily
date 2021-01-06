import logging
import asyncio
import hnsource.hnbeststories as hnbeststories
import screenshots
import os
from enum import Enum
from distutils.dir_util import copy_tree
from jinja2 import Environment, FileSystemLoader, select_autoescape

GENERATED_FOLDER = 'generated'

class PageType(Enum):
    LATEST = 1
    ALL = 2

async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        update_history()
        days = hnbeststories.get_all_days_top_stories()
        if not os.path.exists(GENERATED_FOLDER):
            os.makedirs(GENERATED_FOLDER)
        copy_tree("./static", "./" + GENERATED_FOLDER)
        await save_screenshots(days)
        generate_pages(days)
        logging.info("Finished successfuly")
    except Exception as error:
        logging.exception(f'An unexpected error occured: {error}')

def update_history():
    try:
        hnbeststories.update_history()
    except Exception as error:
      logging.error(f'An error occurred while updating days history. Fallback to reconstructing days history from external source')
      logging.error(error)
      hnbeststories.reset_from_external_hn_daily()

async def save_screenshots(days):
    try:
        await screenshots.save_screenshots(days, GENERATED_FOLDER)
    except Exception as error:
        logging.error(f'An error occurred while gathering screenshots')
        logging.error(error)

def generate_pages(days):
    logging.info("Generating pages")
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('page.html')
    template.globals['PageType'] = PageType
    create_page(template, [days[0]], 'index', PageType.LATEST, True)
    create_page(template, [days[0]], 'latest_without_images', PageType.LATEST, with_images=False)
    create_page(template, days, 'all_with_images', PageType.ALL, with_images=True)
    create_page(template, days, 'all_without_images', PageType.ALL, with_images=False)
    copy_tree('templates/css', 'generated/css')

def create_page(template, days, name, type, with_images):
    result_html = template.render(days=days, page_type=type, with_images=with_images)
    with open(f'{GENERATED_FOLDER}/{name}.html', "w") as fh:
        fh.write(result_html)

asyncio.run(main(), debug=True)
