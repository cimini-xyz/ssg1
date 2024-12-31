import re

RESERVED_NAMES = ["PRN", "CON", "NUL", "AUX"]
RESERVED_NAMES += list(f"COM{i}" for i in range(1,10)) + list(f"LPT{i}" for i in range (1,10))

def main():
    pass

def remove_non_alphanumeric_char(string):
    return re.sub(r'[^a-zA-Z0-9 ]','', string)

def replace_whitespace_char_with(char, string):
    return re.sub(r'\s+',char, string)

def truncate_filename_string(filename_string):
    if string_len := len(filename_string) > 240:
        split = filename_string.split("-")
        split_index = len(split) - 1

        if split_index == 0 or len(split[0]) > 240:
            filename_string = filename_string[:240]
        else: 
            while split_index and string_len - c_count > 240:
                c_count += len(split[split_index])
                c_count += int(split_index > 0)
                split_index = max(0, split_index - 1)
            filename_string = "-".join(split[0:split_index + 1])
    return filename_string

def remove_reserved_name(filename_string):
    if filename_string.upper() in RESERVED_NAMES:
        return ""
    return filename_string

def format_filename_string(article_title):
    # Convert article title into slugged file name for its html document
    filename_string = remove_non_alphanumeric_char(article_title)
    filename_string = replace_whitespace_char_with('-', filename_string)
    filename_string = filename_string.lower()
    filename_string = truncate_filename_string(filename_string)
    filename_string = remove_reserved_name(filename_string)
    # Need to generate unique ID if string is none at this stage
    if not filename_string:
        filename_string = 
    return filename_string + ".html"

def update_filename_on_system(file_path, filename_string):
    file_path.source.move(file_path.source.parents[0] / filename_string)

def process_filename(file_path, filename_string, article_title):
    valid_filename_string = format_filename_string(article_title)
    if not valid_filename_string == filename_string:
        update_filename_on_system(file_path, valid_filename_string)
        
main()