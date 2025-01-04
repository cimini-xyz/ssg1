
from datetime import datetime
import random

from article_parser import ArticleParser
from file_utils import process_filename
from article_list_utils import *

from pathlib import Path
from shutil import move, copy2
from collections import namedtuple, defaultdict
import argparse


def main():
    cmd_args = parse_arguments()
    html_dir = Path("html")
    articles = process_files(html_dir)

    sorted_articles = sort_articles_by_published_time(articles)

    index_file_path = html_dir / "index.html"
    main_index = process_group_choice(sorted_articles, cmd_args.group)

    index_file_path.write_text(render_page(main_index))




def process_files(html_dir):
    articles_dir = html_dir / "article/"

    html_files = articles_dir.glob("*.html")

    articles = []
    for html_file in html_files:

        html_parser = ArticleParser(html_file)
        html_parser.parse()

        process_filename(html_parser.html_file, html_parser.metadata['title'])
        articles.append(html_parser.to_named_tuple())

    return articles

def render_main_index(articles, grouping_choice):
    pass
    


def parse_arguments():
    arg_parser = argparse.ArgumentParser(description='Static Site Generator')
    arg_parser.add_argument(
        '--group',
        default='flat',
        choices=['flat', 'year', 'yearmonth', 'category'],
        help='Groups article list on main page by year, year-month, category, or none'
    )
    return arg_parser.parse_args()



main()