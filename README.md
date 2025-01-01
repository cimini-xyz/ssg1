# Static Site Generator

A focused HTML static site generator that handles site organization and index generation.

## Note on Documentation

This README was generated with the assistance of an AI language model, while the codebase itself was written by me. The documentation has been verified for accuracy and completeness.

## Design Philosophy

This SSG follows the Unix philosophy of "do one thing well". It focuses specifically on organizing and generating HTML site structure, leaving markup conversion (like Markdown to HTML) to specialized tools of your choice.

## Features

- Handles HTML input files
- Generates organized index pages
- Supports multiple grouping strategies (--group option):
  - flat: no grouping
  - year: group by year
  - yearmonth: group by year and month
  - category: group by category

## Usage

1. Convert your markup files to HTML using your preferred tool (pandoc, markdown, etc)
2. Run the SSG to generate your site structure:

## HTML Requirements

Your HTML files must include specific metadata attributes for the parser to work correctly. These should be in the document's head section.

### Required Metadata
- `<meta name="title" content="Your Title">` - Article title
- `<meta name="published" content="YYYY-MM-DD">` - Publication date
- `<meta name="category" content="Your Category">` - Article category

### Example Article HTML
```html
<!DOCTYPE html>
<html>
<head>
    <meta name="title" content="My First Post">
    <meta name="published" content="2023-12-25">
    <meta name="category" content="blog">
</head>
<body>
    <!-- Article content here -->
</body>
</html>