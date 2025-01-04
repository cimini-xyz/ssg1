
from datetime import datetime
import random

from article_parser import ArticleParser
from file_utils import process_filename, get_article_html_files
from article_list_utils import *
from template_processor import *

from pathlib import Path
from shutil import move, copy2
from collections import namedtuple, defaultdict
import argparse


def main():
    cmd_args = parse_arguments()
    html_dir = Path("stage")
    articles = process_files(html_dir)

    sorted_articles = sort_articles_by_published_time(articles)
    index_file_path = Path("html") / "index.html"
    index_template_file = Path('template') / 'base.html'
    main_index = process_group_choice(sorted_articles, cmd_args.group)
    
    main_index_page = apply_main_index_template(main_index, index_template_file.read_text())
    index_file_path.write_text(render_page(main_index_page))

    for category in group_articles(sorted_articles, GROUPING_STRATEGIES["category"]['group_function']):
        print(category)

    for article in sorted_articles:
        article_page = apply_main_index_template(article.file.read_text(), index_template_file.read_text())
        (Path("html") / article.file.name).write_text(article_page)




def process_files(html_dir):
    html_files = get_article_html_files(html_dir)


    articles = []
    for html_file in html_files:

        html_parser = ArticleParser(html_file)
        html_parser.parse()

        html_parser.html_file = process_filename(html_parser.html_file, html_parser.metadata['title'])
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