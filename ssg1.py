def format_filename_string(filename_string, article_title):
    slugged_article_title = re.sub(r'[^a-zA-Z0-9 ]','', article_title)
    filename_string = re.sub(r'\s+','-', slugged_article_title)
    return filename_string.lower() + ".html"

def update_filename_on_system(file_path, filename_string):
    file_path.source.move(file_path.source.parents[0] / filename_string)

def process_filename(file_path, filename_string, article_title):
    valid_filename_string = format_filename_string(filename_string, article_title)
    if not valid_filename_string == filename_string:
        update_filename_on_system(file_path, valid_filename_string)
        
