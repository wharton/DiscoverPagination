import itertools
import re
from abc import abstractmethod
from collections import Sequence
from string import Template
from typing import TextIO, List, overload, Dict, Tuple
from .helpers import *
from .fuzzyfind import *
from statistics import mean
import operator
import tempfile
import os
import hashlib
from io import StringIO
from collections import Counter
from math import ceil

page_number_template = Template(
    r"(?<!(rule|form|year|ears|tion) )(?<!\d.)(?<![-/,$$:;])(?<!&#)(?<=\D)" + PAGE_NUMBER_TEMPLATE_STR + r"(?=\D)(?![\-:,%/\d])(?!\.(\d|\S))")
tag_attribute_PATTERN = r'(v?align|src|alt|colspan|rowspan|style|cellpadding|id|width|height|(bg)?color|cellspacing|border|face|name|size)=(\'|").*?(\3)'
tag_attribute_RE = re.compile(tag_attribute_PATTERN, flags=re.DOTALL | re.IGNORECASE)

tag_noshade_PATTERN = r'\s(noshade|nowrap)\s?(?=>)?'
tag_noshade_RE = re.compile(tag_noshade_PATTERN, flags=re.DOTALL | re.IGNORECASE)

tag_condense_PATTERN = r'(<\w+)\s*?(>)'
tag_condense_RE = re.compile(tag_condense_PATTERN, flags=re.DOTALL | re.IGNORECASE)

word_PATTEN = r'(?<![\/=])\b[a-zA-Z]{3,}\b(?![\/=])'
word_RE = re.compile(word_PATTEN, re.IGNORECASE)


def clean_document_attributes(dirty_text: List[str]):
    document = list(itertools.dropwhile(lambda x: not re.match('<DOCUMENT>', x, flags=re.IGNORECASE),
                                        dirty_text))
    if len(document) < 1:
        raise Exception("No '<DOCUMENT>' section found.")
    input_end = ''.join(itertools.takewhile(lambda x: not re.match('</DOCUMENT>', x, flags=re.IGNORECASE),
                                            document)) + '</DOCUMENT>'
    input_no_attributes = re.sub(tag_attribute_RE, ' ', input_end)
    input_noshade = re.sub(tag_noshade_RE, ' ', input_no_attributes)
    return StringIO(re.sub(tag_condense_RE, r'\g<1>\g<2>', input_noshade)).readlines()


def discover_new_page_template(page_markers_forward, page_markers_reverse):
    all_page_numbers = sort_unique([k for k in page_markers_forward.keys()])

    # TODO: Do something real with this aside from throw an exception
    if len(page_markers_forward) < 20 or len(page_markers_reverse) < 20:
        raise Exception("This shouldn't be an exception, but here we are.")

    fifteen_percent_forward = ceil((len(page_markers_forward) * .15))
    fifteen_percent_reverse = ceil((len(page_markers_reverse) * .15))

    forward_min = min(all_page_numbers)
    reverse_max = max(all_page_numbers)

    normalized_forward = normalize_page_numbers_to_template(page_markers_forward)
    normalized_reverse = normalize_page_numbers_to_template(page_markers_reverse)

    worsted_forward = {k: v for k, v in normalized_forward.items() if k >= forward_min + fifteen_percent_forward}
    worsted_reverse = {k: v for k, v in normalized_reverse.items() if k <= reverse_max - fifteen_percent_reverse}

    best_match_forward = recurse_through_page_markers(worsted_forward)
    best_match_reverse = recurse_through_page_markers(worsted_reverse)
    pass


def recurse_through_page_markers(page_markers: Dict[int, Tuple[int, str]]) -> str:
    if len(page_markers) == 1:
        return list(page_markers.values())[0][1]
    if len(page_markers) >= 2:
        first_dict, second_dict = shuffle_split_dictionary_in_half(page_markers)
        return longest_match_from_list([recurse_through_page_markers(first_dict), recurse_through_page_markers(second_dict)])


def iterative_page_number_search(template, document_slice, known_pages, start_page):
    last_page = start_page - 1
    last_index = 0
    found_page = True
    while found_page:
        page_number = last_page + 1
        page_find_regex = template.substitute({f"{PAGE_NUMBER_NAME}": page_number})

        for line_number, line in enumerate(document_slice[last_index:], last_index):
            found_page = re.search(page_find_regex, line)
            if found_page:
                if line[-1:] == "\n":
                    known_pages[page_number] = (line_number, line[:-1])
                elif line[-2:] == "\r\n":
                    known_pages[page_number] = (line_number, line[:-2])
                else:
                    known_pages[page_number] = (line_number, line)

                last_index = line_number
                last_page = page_number
                break

    return known_pages


def reversed_sliced_page_number_search(template, forward_document_slice, known_pages, start_page, end_page, last_index):
    last_page = end_page
    found_page = True
    forward_range = range(last_index, last_index + len(forward_document_slice))
    document_slice = zip(forward_range, forward_document_slice)

    reversed_document_slice = reversed(list(document_slice))
    while found_page and start_page <= last_page:

        page_number = last_page
        page_find_regex = template.substitute({f"{PAGE_NUMBER_NAME}": page_number})
        for line_number, line in reversed_document_slice:
            found_page = re.search(page_find_regex, line, re.IGNORECASE)
            if found_page:
                if line[-1:] == "\n":
                    known_pages[page_number] = (line_number, line[:-1])
                elif line[-2:] == "\r\n":
                    known_pages[page_number] = (line_number, line[:-2])
                else:
                    known_pages[page_number] = (line_number, line)
                last_page = page_number - 1
                break

    return known_pages


def retry_missing_pages(search_template, document_slice, missing_page_numbers, known_pages, offset):
    sorted_page_numbers = sort_unique(missing_page_numbers)
    return reversed_sliced_page_number_search(search_template, document_slice, known_pages, sorted_page_numbers[0], sorted_page_numbers[-1], offset)


def match_or_close(page_number, line_marker,  page_markers_forward):
    return (page_number in page_markers_forward and page_markers_forward[page_number][0] == line_marker[0]) or abs(page_markers_forward[page_number][0] - line_marker[0]) < 10


def is_intraline_document(page_markers_forward, page_markers_reverse):
    forward_word_scores = mean([len(word_RE.findall(val[1])) for page, val in page_markers_forward.items()])
    reverse_word_scores = mean([len(word_RE.findall(val[1])) for page, val in page_markers_reverse.items()])

    return forward_word_scores > 4 or reverse_word_scores > 4


def find_forward_and_reverse_page_numbers(page_markers_forward, start_page, template, unmarked_document):
    # Going numerically forward get all page markers
    page_markers_forward = iterative_page_number_search(template, unmarked_document, page_markers_forward, start_page)
    all_page_numbers = sort_unique([k for k in page_markers_forward.keys()])
    # Going backward get all page markers
    page_markers_reverse = reversed_sliced_page_number_search(template, unmarked_document, {}, all_page_numbers[0],
                                                              all_page_numbers[-1], 0)
    return all_page_numbers, page_markers_forward, page_markers_reverse


def discover_pages(unmarked_document, template, start_page):
    page_markers_forward = {}

    all_page_numbers, page_markers_forward, page_markers_reverse = find_forward_and_reverse_page_numbers(
        page_markers_forward, start_page, template, unmarked_document)

    if not is_intraline_document(page_markers_forward, page_markers_reverse):
        # Select forward and backward page markers that match line no
        combined_page_markers = {k: v for k, v in page_markers_reverse.items() if match_or_close(k, v, page_markers_forward)}
    else:
        best_match = discover_new_page_template(page_markers_forward, page_markers_reverse)
        if best_match == PAGE_NUMBER_TEMPLATE_STR:
            combined_page_markers = {k: v for k, v in page_markers_reverse.items() if
                                     match_or_close(k, v, page_markers_forward)}
            
    # Create counts of each type of page marker
    likely_page_markers = Counter()

    for i in combined_page_markers.keys():
        discovered_template = combined_page_markers[i][1].replace(str(i), PAGE_NUMBER_TEMPLATE_STR)
        likely_page_markers[discovered_template] = likely_page_markers[discovered_template] + 1
    best_match = max(likely_page_markers.items(), key=operator.itemgetter(1))[0]
    unfound_pages = sorted([k for k in all_page_numbers if k not in combined_page_markers or combined_page_markers[k][1].replace(str(k), PAGE_NUMBER_TEMPLATE_STR) != best_match])
    found_pages = {k: v for k, v in combined_page_markers.items() if k not in unfound_pages}

    # page_distances = [found_pages[page + 1][0] - found_pages[page][0] for page in all_page_numbers if
    #                   page in found_pages and page + 1 in found_pages]

    # average_lines_per_page = mean(page_distances)

    # Create list of lists for continuous pages
    continuous_sections = section_continuous_numbers(unfound_pages)
    for section in continuous_sections:
        window_start, window_end = get_window_from_found_pages(section, found_pages, len(unmarked_document))

        # Using our best match template, try to find pages in expected window
        found_pages = retry_missing_pages(Template(best_match), unmarked_document[window_start:window_end], section,
                                          found_pages, offset=0)

    # Update list of unfound pages
    unfound_pages = [k for k in unfound_pages if k not in found_pages.keys()]

    continuous_sections = section_continuous_numbers(unfound_pages)
    for section in continuous_sections:
        window_start, window_end = get_window_from_found_pages(section, found_pages, len(unmarked_document))
        document_slice = unmarked_document[window_start:window_end]

        # Use fuzzy matching for any remaining pages that are not found
        for n in section:
            try:
                found_line = fuzzy_find_by_template(document_slice, Template(best_match), n, offset=window_start)
                found_pages[n] = found_line
            except Exception as err:
                continue

    return found_pages


class PaginatedDocument(Sequence):

    @overload
    @abstractmethod
    def __getitem__(self, s: slice) -> List[str]:
        start, stop = get_window_from_found_pages([s.start, s.stop], self.page_endings, len(self.cleaned))
        return self.cleaned[start:stop]

    def __getitem__(self, i: int) -> List[str]:
        start, stop = get_window_from_found_pages([i], self.page_endings, len(self.cleaned))
        return self.cleaned[start:stop]

    def __len__(self):
        return len(self.page_endings)

    def __init__(self, document: TextIO, start_page: int = 1, clean_xml=False, write_tempfile=False):
        self.original = document.readlines()
        self.cleaned = self.original
        if clean_xml:
            self.cleaned = clean_document_attributes(self.original)

        if write_tempfile:
            tempdir = tempfile.gettempdir()
            self.temp_filename = tempdir + os.sep + str(hashlib.sha256(''.join(self.original).encode()).hexdigest())
            with open(self.temp_filename, 'w') as temp:
                temp.writelines(self.cleaned)
        self.page_endings = discover_pages(self.cleaned, page_number_template, start_page)
        self.page_template = self.get_page_template()

    def get_page_template(self):
        likely_page_markers = Counter()
        for i in self.page_endings.keys():
            discovered_template = self.page_endings[i][1].replace(str(i), PAGE_NUMBER_TEMPLATE_STR)
            likely_page_markers[discovered_template] = likely_page_markers[discovered_template] + 1
            return max(likely_page_markers.items(), key=operator.itemgetter(1))[0]


__all__ = ['PaginatedDocument']



