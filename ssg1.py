import re

def remove_non_alphanumeric_char(string):
    return re.sub(r'[^a-zA-Z0-9 ]','', string)

def replace_whitespace_char_with(char, string):
    return re.sub(r'\s+',char, string)

def format_filename_string(article_title):
    filename_string = remove_non_alphanumeric_char(article_title)
    filename_string = replace_whitespace_char_with('-', filename_string)
    filename_string = filename_string.lower() + ".html"
    return filename_string

def update_filename_on_system(file_path, filename_string):
    file_path.source.move(file_path.source.parents[0] / filename_string)

def process_filename(file_path, filename_string, article_title):
    valid_filename_string = format_filename_string(article_title)
    if not valid_filename_string == filename_string:
        update_filename_on_system(file_path, valid_filename_string)
        
