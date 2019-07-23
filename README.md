[![Build Status](https://travis-ci.org/wharton/DiscoverPagination.svg?branch=master)](https://travis-ci.org/wharton/S3WebCache)
[![PyPI version](https://badge.fury.io/py/DiscoverPagination.svg)](https://badge.fury.io/py/DiscoverPagination)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# DiscoverPagination

A python package for discovering numbered page delineation in documents.

## Repository

[https://github.com/wharton/DiscoverPagination](https://github.com/wharton/DiscoverPagination)

## Background
In the Research and Analytics Department we are asked for several different types of text processing assignments.
These usually take the form of "please extract the X section from Y document type 10k times" Some of these
have a Table of Contents, but it is difficult to use the ToC because we do not know which pages are which.

This package is designed to discover where pages are marked, and then reference those page numbers to get 
sections of text. Much of the work we do involves SEC filings, which are in a type of XML format. This is 
optimized for that type of document, but should do well in other cases.


## Requirements
 - Python 3.6
 - fuzzywuzzy: Fuzzy matching
 - python-Levenshtein: Speeds up fuzzy matching library


## Quickstart

### Install

    $ pip install DiscoverPagination

### Usage
    $ python
    >> from discoverpagination import *
    >> with open('./example_texts/0001193125-08-010038.txt') as inputfile:
    ...       doc = PaginatedDocument(inputfile, clean_xml=True)
    >> pages = doc[20:22]
    >> print(pages)
    [' <P><FONT>19 </FONT></P>\n', '\n', '\n', '<p>\n', '<HR>\n', '\n', ' <P><FONT>The ...


## Methods
The way the pages are discovered takes several steps and relies on a few assumptions.

### Assumptions
 1. Pages are marked
 2. Page markings are in sequential order
 3. Page markings use numeric characters
 4. Pages are numbered at the end of page
 5. Page numbers do not occur mixed with text. (There is an attempt to handle this case.)

### Steps
 1. Document is read from file
 2. (OPTIONAL) XML documents are cleaned of tag attributes.
 3. Document is scanned for page markers line by line, starting with "1". (Configurable) 
 4. As each number is found, the line index and text is stored in a Dict keyed to page number.
 5. The page is incremented after each number is found until no more document lines remain.
 6. The document is rescanned in reverse order to find page markers.
 7. Page markers that are the same or nearby to each other are kept.
 8. A common "best_match" format is determined by ranking each type of line.
 9. The missing page numbers are scanned for with this "best_match" in the areas they should be. E.g. A
    missing page 5 is searched for between pages 4 and 6 with the best pattern.
 10. If there are still missing pages it uses fuzzy matching to guess based on placement and pattern.
 11. The document is returned and can be referenced by slicing. doc[10:12] gets lines for pages 10 to 12.
    

## Tests

    python setup.py test
    

## Reference

[fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)\
[python-Levenshtein](https://github.com/ztane/python-Levenshtein/)\
[SEC EDGAR](https://www.sec.gov/edgar/aboutedgar.htm)


## Contributors

[Douglas H. King](https://github.com/douglascodes)


## License

[MIT](./LICENSE.TXT)