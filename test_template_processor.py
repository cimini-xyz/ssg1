from template_processor import *

def test_all_directions(text, tag, insert_text):
    position = find_tag_start_end(text, tag)
    print(insert(text, insert_text, position, AFTER, OUTSIDE))
    print(insert(text, insert_text, position, AFTER, INSIDE))
    print(insert(text, insert_text, position, BEFORE, OUTSIDE))
    print(insert(text, insert_text, position, BEFORE, INSIDE))

def test():
    print(":)")
    text = "<div>Hello</div>"
    tag = "div"
    insert_text = "TEXT"
    test_all_directions(text, tag, insert_text)
    tag = "/div"
    test_all_directions(text, tag, insert_text)

def main():
    test()

main()