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
    padded_content = pad(content, "\n", direction, side)
    return before_text + padded_content + after_text

def pad(content, char, direction, side):
    char_before = direction ^ side
    pad_l = char if char_before else "" 
    pad_r = "" if char_before else char
    return pad_l + content + pad_r


