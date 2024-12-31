import re
from datetime import datetime
import random 

RESERVED_NAMES = ["PRN", "CON", "NUL", "AUX"]
RESERVED_NAMES += list(f"COM{i}" for i in range(1,10)) + list(f"LPT{i}" for i in range (1,10))

def main():
    pass

def remove_non_alphanumeric(text):
    return re.sub(r'[^a-zA-Z0-9 ]','', text)

def replace_whitespace(text, char = '-'):
    return re.sub(r'\s+', char, text)

def truncate_filename(filename):
    if (string_len := len(filename)) > 240:
        split = filename.split("-")
        split_index = len(split) - 1

        if split_index == 0 or len(split[0]) > 240:
            filename = filename[:240]
        else: 
            while split_index and string_len - (c_count := 0) > 240:
                c_count += len(split[split_index])
                c_count += int(split_index > 0)
                split_index = max(0, split_index - 1)
            filename = "-".join(split[0:split_index + 1])
    return filename

def remove_reserved_filename(filename):
    if filename.upper() in RESERVED_NAMES:
        return ""
    return filename

def generate_unique_filename():
    return "article-" + datetime.now().strftime("%H%M%S%f")[:-6] + str(random.randint(1000,9999))

def format_filename(article_title):
    # Convert article title into slugged file name for its html document
    filename = remove_non_alphanumeric(article_title)
    filename = replace_whitespace(filename, '-')
    filename = filename.lower()
    filename = truncate_filename(filename)
    filename = remove_reserved_filename(filename)
    # Need to generate unique ID if string is none at this stage
    if not filename:
        filename = generate_unique_filename()
    return filename + ".html"

def move_file(file_path, filename_string):
    file_path.source.move(file_path.source.parents[0] / filename_string)

def process_filename(file_path, filename_string, article_title):
    valid_filename_string = format_filename(article_title)
    if not valid_filename_string == filename_string:
        move_file(file_path, valid_filename_string)
        
main()