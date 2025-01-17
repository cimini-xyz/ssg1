from collections import defaultdict
from datetime import datetime
from pathlib import Path
from article_parser import Article

BASE_HEADING = "<h2><a href='index.html'>Posts</a> <a href='category/index.html'> Categories</a></h2>\n"
CATEGORY_HEADING = "<h2><a href='../index.html'>Posts</a> <a href='index.html'> Categories</a></h2>\n"
def render_article_index(articles):
    lines = ["<ul class=\"articles\">"]
    for article in articles:
        lines.append(generate_index_list_item(article))
    lines.append("</ul>")
    return "\n".join(lines)


def render_index(groups, timestamp, heading=BASE_HEADING):
    lines = [
        heading,
        "<ul class=\"articles\">"
        ]
    for group in groups.keys():
        if group != "":
            lines.append(f"<h4>{group}</h4>")
        for article in groups[group]:
            lines.append(generate_index_list_item(article, timestamp))
    lines.append("</ul>")
    return "\n".join(lines)


def render_page(content):
    return f"""
<!DOCTYPE html>
<html>
<head><title>Articles</title></head>
<body>
{content}
</body>
</html>
"""

#not generalized enough, should take article fields as parameters
def generate_index_list_item(article, timestamp_format=" – %b %-d %Y"):
    published_strftime = ""
    if article.published:
        published_strftime = article.published.strftime(timestamp_format)
    return (
        f'<li><a href="{article.filename_reference}">'
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
        return article.published.strftime("%Y")


def group_by_year_month(article):
    if isinstance(article.published, datetime):
        return article.published.strftime("%Y %b")


def group_by_category(article):
    return article.category

def group_by_none(article):
    return ""

GROUPING_STRATEGIES = {
        'flat' : {
            'group_function': group_by_none,
            'timestamp' : " – %b %-d %Y"
        },
        'year': {
            'group_function': group_by_year,
            'timestamp': " – %b %-d"
        },
        'yearmonth': {
            'group_function': group_by_year_month,
            'timestamp': " – %b %-d"
        },
        'category': {
            'group_function': group_by_category,
            'timestamp': " – %b %-d %Y"
        }
    }

def process_group_choice(articles, grouping_choice):
    strategy = GROUPING_STRATEGIES['flat']
    if grouping_choice in GROUPING_STRATEGIES:
        strategy = GROUPING_STRATEGIES[grouping_choice]
    grouped_articles = group_articles(articles, strategy['group_function'])
    return render_index(grouped_articles, strategy['timestamp'])

def update_category_file_reference(filename):
    return f"../{filename}"

def generate_category_indices(articles):
    strategy = GROUPING_STRATEGIES['category']
    new_articles = [
        Article(
            article.file,
            update_category_file_reference(article.filename_reference),
            article.title,
            article.published,
            article.category
            )
        for article in articles
        ]

    grouped_articles = group_articles(new_articles, strategy['group_function'])
    output = []
    for category in grouped_articles.keys():
        group = {category : grouped_articles[category]}
        output_path = Path(f"html/category/{category}.html") 
        print(output_path)
        output.append(
            {'category': category, 'output': output_path, 'render' : render_index(group, strategy['timestamp'], CATEGORY_HEADING)}
        )
    return output   

def generate_articles_per_category_index():
    pass

def generate_categories_index(categories):
    lines = [
        CATEGORY_HEADING,
        "<ul class=\"categories\">"
        ]
    
    for category in categories:
        lines.append((
            f'<li><a href="{category}.html">'
            f'{category}</a>'
        ))

    lines.append("</ul>")
    return "\n".join(lines)

