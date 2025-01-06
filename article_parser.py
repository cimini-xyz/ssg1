from html.parser import HTMLParser
from collections import defaultdict, namedtuple
from datetime import datetime

Article = namedtuple(
    'Article', ['file', 'filename_reference', 'title', 'published', 'category']
)


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
        if not self.done() and tag == "article":
            attrs_dict = dict(attrs)
            for key in self.metadata.keys():
                if not self.metadata[key] and key in attrs_dict.keys():
                    self.metadata[key] = attrs_dict[key]

    def handle_endtag(self, tag):
        self.open_tag = None

    def handle_data(self, data):
        pass
        # if self.open_tag == "h1" and self.article_title is None:
        #    self.article_title = data

    def format_metadata(self):
        published_missing = not self.metadata["published"]
        published_is_not_datetime = not published_missing and not isinstance(self.metadata["published"], datetime)
        if published_is_not_datetime:
            try:
                self.metadata["published"] = datetime.strptime(
                        self.metadata["published"],
                        "%Y-%m-%d"
                    )
            except ValueError as e:
                pass
        elif published_missing:
            self.metadata["published"] = datetime.fromtimestamp(0)


    def to_named_tuple(self):
        self.format_metadata()
        print("Here is the file name when converting into output")
        print(self.html_file)
        return Article(self.html_file, self.html_file.name, **self.metadata)
