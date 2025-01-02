import re
from datetime import datetime
import random
from html.parser import HTMLParser
from pathlib import Path
from shutil import move, copy2
from collections import namedtuple, defaultdict
import argparse

Article = namedtuple('Article', ['file', 'title', 'published', 'category'])


RESERVED_NAMES = ["PRN", "CON", "NUL", "AUX"]
RESERVED_NAMES += list(f"COM{i}" for i in range(1,10)) + list(f"LPT{i}" for i in range (1,10))
GENERATED_FILENAMES = set()

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
        process_filename(html_parser)
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
 
    index_path.write_text(generate_page(article_index))

def generate_page(content):
    return f"""
<!DOCTYPE html>
<html>
<head><title>Articles</title></head>
<body>
{content}
</body>
</html>
"""

def generate_index_list_item(article, timestamp_format=" – %b %-d %Y"):
    published_strftime = ""
    if article.published:
        published_strftime = article.published.strftime(timestamp_format)
    return (
        f'<li><a href="{article.file.name}">'
        f'{article.title}</a>'
        f'{published_strftime}'
    )

def sort_articles_by_published_time(articles):
    return sorted(
        articles, 
        key=lambda article: 
        (article.published is None, article.published), 
        reverse=True)

def group_articles(articles, group_function):
    groups = defaultdict(list)
    for article in articles:
        key = group_function(article)
        groups[key].append(article)
    return groups

def group_by_year(article):
    if isinstance(article.published, datetime):
        return article.published.strftime("%Y %b")

def group_by_year_month(article):
    if isinstance(article.published, datetime):
        return article.published.strftime("%Y %b")

def group_by_category(article):
    return article.category
    
def render_article_index(articles):
    lines = ["<ul class=\"articles\">"]
    for article in articles:
        lines.append(generate_index_list_item(article))
    lines.append("</ul>")
    return "\n".join(lines)

def render_grouped_index(groups, timestamp):
    lines = ["<ul class=\"articles\">"]

    for group in groups.keys():
        lines.append(f"<h3>{group}</h3>")

        for article in groups[group]:
            lines.append(generate_index_list_item(article, timestamp))

    lines.append("</ul>")

    return "\n".join(lines)

class ArticleParser(HTMLParser):
    

    def __init__(self, html_file):
        super().__init__()
        self.metadata = defaultdict(None)
        self.metadata['title'] = None
        self.metadata['category'] = None
        self.metadata['published'] = None
        
        self.open_tag = None
        self.html_file = html_file

    def parse(self):
        self.feed(self.html_file.read_text())

    def done(self):
        return 
    
    def handle_starttag(self, tag, attrs):
        self.open_tag = tag
        if not self.done() and tag == "meta":
            attrs_dict = dict(attrs)
            for key in self.metadata.keys():
                if not self.metadata[key] and key == attrs_dict["name"]:
                    self.metadata[key] = attrs_dict["content"]

    def handle_endtag(self, tag):
        self.open_tag = None
    
    def handle_data(self, data):
        pass
        #if self.open_tag == "h1" and self.article_title is None:
        #    self.article_title = data

    def to_named_tuple(self):
        if self.metadata["published"]:
            try:
                self.metadata["published"] = datetime.strptime(self.metadata["published"], "%m/%d/%Y %H:%M:%S")
            except ValueError:
                pass
        else:
            self.metadata["published"] = datetime.fromtimestamp(0)
        return Article( self.html_file, **self.metadata )


def has_alphanumeric(text):
    return bool(re.search(r'[a-zA-Z0-9]', text))

def remove_non_alphanumeric(text):
    return re.sub(r'[^a-zA-Z0-9 ]','', text)

def replace_whitespace(text, char = '-'):
    return re.sub(r'\s+', char, text)

def truncate_filename(filename):
    if (string_len := len(filename)) > 240:
        split = filename.split("-")
        split_index = len(split) - 1

        if split_index == 0 or len(split[0]) > 240:
            filename = filename[:240]
        else: 
            c_count = 0
            while split_index and string_len - c_count > 240:
                c_count += len(split[split_index])
                c_count += int(split_index > 0)
                split_index = max(0, split_index - 1)
            filename = "-".join(split[0:split_index + 1])
    return filename

def remove_reserved_filename(filename):
    if filename.upper() in RESERVED_NAMES:
        return ""
    return filename

def generate_article_id():
    return f"article-{datetime.now().strftime('%H%M%S%f')[:-6]}{str(random.randint(1000,9999))}"

def generate_unique_filename():
    retry_count, retry_limit = 0, 1000 
    filename = generate_article_id()
    while filename in GENERATED_FILENAMES and retry_count < retry_limit:
        filename = generate_article_id()
        retry_count += 1
    if retry_count >= retry_limit:
        raise RuntimeError(f"Failed to generate unique filename after {retry_limit} attempts")
    GENERATED_FILENAMES.add(filename)
    return filename

def slugify_string(string):
    slug = remove_non_alphanumeric(string)
    slug = replace_whitespace(slug, '-')
    slug = slug.lower()
    return slug

def sanitize_filename(filename):
    filename = truncate_filename(filename)
    filename = remove_reserved_filename(filename)
    return filename

def format_filename(article_title):
    filename = ""
    # remove article_title check?
    if article_title and has_alphanumeric(article_title):
        filename = slugify_string(article_title)
        filename = sanitize_filename(filename)
    if not filename:
        filename = generate_unique_filename()
    return filename + ".html"

def process_filename(parser):
    html_file = parser.html_file
    valid_filename_string = format_filename(parser.metadata["title"])
    if not valid_filename_string == html_file.name and valid_filename_string:
        html_file.rename(html_file.parent / valid_filename_string)
        
main()