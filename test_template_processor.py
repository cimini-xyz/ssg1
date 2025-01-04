from template_processor import *
from file_utils import *
from pathlib import Path
def test_all_directions(text, tag, insert_text):
    position = find_tag_start_end(text, tag)
    padded_insert_text = pad(insert_text, " ", AFTER, OUTSIDE)
    print(insert(text, padded_insert_text, position, AFTER, OUTSIDE))
    padded_insert_text  = pad(insert_text, " ", AFTER, INSIDE)
    print(insert(text, padded_insert_text, position, AFTER, INSIDE))
    padded_insert_text = pad(insert_text, " ", BEFORE, OUTSIDE)
    print(insert(text, padded_insert_text, position, BEFORE, OUTSIDE))
    padded_insert_text  = pad(insert_text, " ", BEFORE, INSIDE)
    print(insert(text, padded_insert_text, position, BEFORE, INSIDE))

def test():
    print(":)")
    text = "<div>Hello</div>"
    tag = "div"
    insert_text = "TEXT"
    test_all_directions(text, tag, insert_text)
    tag = "/div"
    test_all_directions(text, tag, insert_text)

def cut_meta_tag_all_articles():
    html_dir = Path("html")
    html_files = get_article_html_files(html_dir)
    for html_file in html_files:
        content = html_file.read_text()
        print(content)
        scan_start = 0
        position = (0, 0)
        while -1 not in position:
            position = find_tag_start_end(content, "meta")
            content = cut(content, position, position)
        print(content)
                         
            
            


def main():
    test()
    cut_meta_tag_all_articles()

main()