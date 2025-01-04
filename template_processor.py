def find_tag_start_end(text, tag, scan_start=0):
    start_pos = text.find(f"<{tag}", scan_start)
    if start_pos == -1:
        return (-1, -1)
    end_pos = text.find(">", start_pos)
    return (start_pos, end_pos)

AFTER = 1
BEFORE = 0
OUTSIDE = 1
INSIDE = 0

def insert(text, content, position, direction, side):
    index_pos = position[direction]
    bracket_offset = 1 ^ (direction ^ side)
    before_text = text[:index_pos + bracket_offset]
    after_text = text[index_pos + bracket_offset:]
    return before_text + content + after_text

def cut(text, start_tag_position, end_tag_position):
    return text[:start_tag_position[0]] + text[end_tag_position[1] + 1:]

def pad(content, char, direction, side):
    char_before = direction ^ side
    pad_l = char if char_before else "" 
    pad_r = "" if char_before else char
    return pad_l + content + pad_r


def apply_main_index_template(index_fragment, index_template):
    tag = "/header"
    insert_position = find_tag_start_end(index_template, tag)
    index_fragment = pad(index_fragment, "\n", BEFORE, OUTSIDE)
    return insert(index_template, index_fragment, insert_position, AFTER, OUTSIDE)