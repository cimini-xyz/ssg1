def find_tag_start_end(text, tag, scan_start=0):
    start_pos = text.find(f"<{tag}", scan_start)
    if start_pos == -1:
        return (-1, -1)
    end_pos = text.find(">", start_pos)
    return (start_pos, end_pos)

def insert_content(text, content, position, insert_direction, insert_side):
    if -1 in position:
        raise Exception("Tag not found")
    return insert_direction(text, content, position, insert_side)

def insert_after(text, content, position, insert_side):
    if insert_side == "inside":
        return text[:position[1] + 0] + content + text[position[1] + 0:]
    return text[:position[1] + 1] + content + text[position[1] + 1:]

def insert_before(text, content, position, insert_side):
    if insert_side == "inside":
        return text[:position[0] + 1] + content + text[position[0] + 1:]
    return text[:position[0] + 0] + content + text[position[0] + 0:]

text = "<div>Hello</div>"
tag = "div"
position = find_tag_start_end(text, tag)
#print(insert_content(text, "asdf", position, insert_after, "outside"))
#print(insert_content(text, "fdsa", position, insert_before, "outside"))
tag = "/div"

position = find_tag_start_end(text, tag)
#print(insert_content(text, "asdf", position, insert_after, "inside"))
#print(insert_content(text, "fdsa", position, insert_before, "inside"))

AFTER = 1
BEFORE = 0
OUTSIDE = 1
INSIDE = 0

def insert(text, content, position, direction, side):
    index_pos = position[direction]
    bracket_offset = 1 ^ (direction ^ side)
    before_text = text[:index_pos + bracket_offset]
    after_text = text[index_pos + bracket_offset:]
    padded_content = pad(content, direction, side)
    return before_text + padded_content + after_text

def pad(content, direction, side):
    space_before = direction ^ side
    pad_l = " " if space_before else "" 
    pad_r = "" if space_before else " "
    return pad_l + content + pad_r

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
