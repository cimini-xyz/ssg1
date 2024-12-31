def format_filename_string(filename_string, article_title):
    pass

def update_filename_on_system(file_path, filename_string):
    pass

def process_filename(file_path, filename_string, article_title):
    valid_filename_string = format_filename_string(filename, article_title)
    if not valid_filename_string == filename_string:
        update_filename_on_system(file_path, valid_filename_string)
        
