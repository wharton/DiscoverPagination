from fuzzywuzzy import process
from typing import List
import re
from string import Template
PAGE_NUMBER_PATTERN = r"\b\d+\b"
PAGE_NUMBER_RE = re.compile(PAGE_NUMBER_PATTERN, re.IGNORECASE)


def fuzzy_find_by_template(document_slice: List[str], template: Template, page_number: int, offset: int = 0):
    search_sample = template.substitute({'page_number': page_number})
    possible_lines = [l for l in document_slice if str(page_number) in l and PAGE_NUMBER_RE.search(l)]
    if not possible_lines:
        raise Exception
    ratings = process.extract(search_sample,  possible_lines)
    best_match = max(ratings, key=lambda x: x[1])[0]
    lineno = document_slice.index(best_match)

    if best_match[-1:] == "\n":
        return lineno + offset, best_match[:-1]
    elif best_match[-2:] == "\r\n":
        return lineno + offset, best_match[:-2]
    else:
        return lineno + offset, best_match


__all__ = ['fuzzy_find_by_template']
