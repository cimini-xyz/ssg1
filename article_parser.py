from html.parser import HTMLParser
from collections import defaultdict, namedtuple
from datetime import datetime

Article = namedtuple(
    'Article', ['file', 'title', 'published', 'category']
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