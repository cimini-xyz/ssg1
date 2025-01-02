from collections import defaultdict
from datetime import datetime


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
        return article.published.strftime("%Y %b")


def group_by_year_month(article):
    if isinstance(article.published, datetime):
        return article.published.strftime("%Y %b")


def group_by_category(article):
    return article.category
