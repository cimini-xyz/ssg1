from ssg1 import ArticleParser, format_filename, has_alphanumeric, GENERATED_FILENAMES
from pathlib import Path
from shutil import move, copy2

def test_article_parser():
    html_document = Path('html/understanding-python-decorators.html')
    html_content = html_document.read_text()
    parser = ArticleParser(html_document)
    parser.parse()
    print(parser.article_title, parser.published_time, parser.category_type)
    print(format_filename(parser.article_title))



if __name__ == "__main__":
    test_article_parser()