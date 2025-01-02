import re
from datetime import datetime
import random



RESERVED_NAMES = ["PRN", "CON", "NUL", "AUX"]
RESERVED_NAMES += list(f"COM{i}" for i in range(1, 10)) + \
    list(f"LPT{i}" for i in range(1, 10))
GENERATED_FILENAMES = set()


def process_filename(file, parsed_title):
    valid_filename_string = format_filename(parsed_title)
    if not valid_filename_string == file.name and valid_filename_string:
        file.rename(file.parent / valid_filename_string)


def format_filename(article_title):
    filename = ""
    # remove article_title check?
    if article_title and has_alphanumeric(article_title):
        filename = slugify_string(article_title)
        filename = sanitize_filename(filename)
    if not filename:
        filename = generate_unique_filename()
    return filename + ".html"


def has_alphanumeric(text):
    return bool(re.search(r'[a-zA-Z0-9]', text))


def remove_non_alphanumeric(text):
    return re.sub(r'[^a-zA-Z0-9 ]', '', text)


def replace_whitespace(text, char='-'):
    return re.sub(r'\s+', char, text)


def slugify_string(string):
    slug = remove_non_alphanumeric(string)
    slug = replace_whitespace(slug, '-')
    slug = slug.lower()
    return slug


def sanitize_filename(filename):
    filename = truncate_filename(filename)
    filename = remove_reserved_filename(filename)
    return filename


def truncate_filename(filename):
    if (string_len := len(filename)) > 240:
        split = filename.split("-")
        split_index = len(split) - 1
        if split_index == 0 or len(split[0]) > 240:
            filename = filename[:240]
        else:
            c_count = 0
            while split_index and string_len - c_count > 240:
                c_count += len(split[split_index])
                c_count += int(split_index > 0)
                split_index = max(0, split_index - 1)
            filename = "-".join(split[0:split_index + 1])
    return filename


def remove_reserved_filename(filename):
    if filename.upper() in RESERVED_NAMES:
        return ""
    return filename


def generate_article_id():
    return f"article-{datetime.now().strftime('%H%M%S%f')[:-6]}{str(random.randint(1000,9999))}"


def generate_unique_filename():
    retry_count, retry_limit = 0, 1000
    filename = generate_article_id()
    while filename in GENERATED_FILENAMES and retry_count < retry_limit:
        filename = generate_article_id()
        retry_count += 1
    if retry_count >= retry_limit:
        raise RuntimeError(
            f"Failed to generate unique filename after {retry_limit} attempts")
    GENERATED_FILENAMES.add(filename)
    return filename
