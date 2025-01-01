import re
from datetime import datetime
import random
from html.parser import HTMLParser
from pathlib import Path
from shutil import move, copy2
from collections import namedtuple

Article = namedtuple('Article', ['file', 'title', 'published', 'category'])


RESERVED_NAMES = ["PRN", "CON", "NUL", "AUX"]
RESERVED_NAMES += list(f"COM{i}" for i in range(1,10)) + list(f"LPT{i}" for i in range (1,10))
GENERATED_FILENAMES = set()

def main():
    html_dir = Path("html")
    articles_dir = html_dir / "article/"
    html_files = articles_dir.glob("*.html")
    articles = []

    for html_file in html_files:
        parser = ArticleParser(html_file)
        parser.parse()
        process_filename(parser)
        articles.append(parser.to_named_tuple())
    
    index_path = html_dir / "index.html"
    index_path.write_text(generate_page(generate_article_index_page(sorted(articles, key=lambda article: article.published, reverse=True))))

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

def generate_article_index_page(articles):
    return "<ul class=\"articles\">" + "\n".join(
        f"<li><a href=\"{article.file.name}\">{article.title}</a>{article.published.strftime(' – %b %-d')}"  for article in articles
    ) + "\n</ul>\n"

class ArticleParser(HTMLParser):
    article_title = None
    published_time = None
    category_type = None
    open_tag = None
    html_file = None

    def __init__(self, html_file):
        super().__init__()
        self.html_file = html_file

    def parse(self):
        self.feed(self.html_file.read_text())

    def handle_starttag(self, tag, attrs):
        self.open_tag = tag
        attrs_dict = dict(attrs)
        if tag == "time" and not self.published_time and "datetime" in attrs_dict:
            try:
                self.published_time = datetime.strptime(attrs_dict['datetime'], "%m/%d/%Y %H:%M:%S")
            except ValueError:
                pass
        if tag == "category" and not self.category_type and "type" in attrs_dict:
            self.category_type = attrs_dict['type']

    def handle_endtag(self, tag):
        self.open_tag = None
    
    def handle_data(self, data):
        if self.open_tag == "h1" and self.article_title is None:
            self.article_title = data

    def to_named_tuple(self):
        return Article(
            self.html_file,
            self.article_title,
            self.published_time,
            self.category_type
        )


def has_alphanumeric(article_title):
    return bool(re.search(r'[a-zA-Z0-9]', article_title))

def remove_non_alphanumeric(text):
    return re.sub(r'[^a-zA-Z0-9 ]','', text)

def replace_whitespace(text, char = '-'):
    return re.sub(r'\s+', char, text)

def truncate_filename(filename):
    if (string_len := len(filename)) > 240:
        split = filename.split("-")
        split_index = len(split) - 1

        print(filename,"\n",string_len,split_index, len(split[0]))

        if split_index == 0 or len(split[0]) > 240:
            filename = filename[:240]
        else: 
            c_count = 0
            while split_index and string_len - c_count > 240:
                print(split_index)
                print(split[split_index])
                print(len(split[split_index]))
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
            
def format_filename(article_title):
    filename = ""
    if article_title and has_alphanumeric(article_title):
        filename = remove_non_alphanumeric(article_title)
        filename = replace_whitespace(filename, '-')
        filename = filename.lower()
        filename = truncate_filename(filename)
        filename = remove_reserved_filename(filename)
    if not filename:
        filename = generate_unique_filename()
    return filename + ".html"

def process_filename(parser):
    html_file = parser.html_file
    valid_filename_string = format_filename(parser.article_title)
    if not valid_filename_string == html_file.name:
        html_file.rename(html_file.parent / valid_filename_string)
        
main()