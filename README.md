# Static Site Generator

A focused HTML static site generator that handles site organization and index generation.

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