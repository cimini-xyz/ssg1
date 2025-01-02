
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
    arg_parser = argparse.ArgumentParser(description='Static Site Generator')
    arg_parser.add_argument(
        '--group', 
        default='flat', 
        choices=['flat', 'year', 'yearmonth', 'category'],
        help='Groups article list on main page by year, year-month, category, or none'
    )
    parsed_args = arg_parser.parse_args()

    html_dir = Path("html")
    articles_dir = html_dir / "article/"
    html_files = articles_dir.glob("*.html")
    
    articles = []

    for html_file in html_files:
        html_parser = ArticleParser(html_file)
        html_parser.parse()
        process_filename(html_parser.html_file, html_parser.metadata['title'])
        articles.append(html_parser.to_named_tuple())
    
    index_path = html_dir / "index.html"
    sorted_articles = sort_articles_by_published_time(articles)

    grouping_strategies = {
        'year' : {
            'group_function' : group_by_year ,
            'timestamp' : " – %b %-d"
        } ,
        'yearmonth' : {
            'group_function' : group_by_year_month ,
            'timestamp' : " – %b %-d"
        } ,
        'category' : {
            'group_function' : group_by_category ,
            'timestamp' : " – %b %-d %Y"
        }
    }
    if parsed_args.group in grouping_strategies:
        strategy = grouping_strategies[parsed_args.group]
        article_index = render_grouped_index(group_articles(sorted_articles, strategy['group_function']), strategy['timestamp'])
    else:
        article_index = render_article_index(sorted_articles)
    index_path.write_text(render_page(article_index))

main()