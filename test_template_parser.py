from template_parser import TemplateParser
from pathlib import Path

def main():
    html_dir = Path("html")
    articles_dir = html_dir / "article/"
    html_files = articles_dir.glob("*.html")
    template_parser = TemplateParser()

    for html_file in html_files:
        template_parser.feed(html_file.read_text())


main()