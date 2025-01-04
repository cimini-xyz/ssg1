from collections import defaultdict
from datetime import datetime





def render_article_index(articles):
    lines = ["<ul class=\"articles\">"]
    for article in articles:
        lines.append(generate_index_list_item(article))
    lines.append("</ul>")
    return "\n".join(lines)


def render_index(groups, timestamp):
    lines = [
        "<h2>Posts</h2>\n"
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