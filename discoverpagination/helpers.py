from math import ceil
from typing import List, Dict, Tuple, TypeVar
from difflib import SequenceMatcher
from random import shuffle

KT = TypeVar('KT')
VT = TypeVar('VT')

PAGE_NUMBER_NAME = r'page_number_of_a_really_long_length'
PAGE_NUMBER_TEMPLATE_STR = r'${' + PAGE_NUMBER_NAME + r'}'


def section_continuous_numbers(arr: List[int]) -> List[List[int]]:
    number_lists = []
    if not arr:
        return []
    sorted_unique = sort_unique(arr)

    current_number = sorted_unique[0] - 1
    current_index = 0
    number_lists.append([])
    for number in sorted_unique:
        if number == current_number + 1:
            number_lists[current_index].append(number)
            current_number = number
        else:
            current_index = current_index + 1
            number_lists.append([])
            number_lists[current_index].append(number)
            current_number = number

    return number_lists


def shuffle_split_dictionary_in_half(d: Dict[KT, VT]) -> Tuple[Dict[KT, VT], Dict[KT, VT]]:
    shuffled_keys = list(d.keys())
    half_length = ceil(len(shuffled_keys) / 2)
    shuffle(shuffled_keys)

    first_half = {k: v for k, v in d.items() if shuffled_keys.index(k) <= half_length - 1}
    second_half = {k: v for k, v in d.items() if shuffled_keys.index(k) > half_length - 1}

    return first_half, second_half


def normalize_page_numbers_to_template(page_number_dict: Dict[int, Tuple[int, str]]) -> Dict[int, Tuple[int, str]]:
    return {k: (v[0], v[1].replace(str(k), PAGE_NUMBER_TEMPLATE_STR)) for k, v in page_number_dict.items()}


def get_window_from_found_pages(section_pages: List[int], found_pages: Dict[int, Tuple[int, str]],
                                document_size: int) -> Tuple[int, int]:
    if not section_pages:
        raise IndexError("section_pages must contain at least 1 value.")

    if not found_pages:
        raise Exception("found_numbers must contain at least 1 value.")

    sorted_unique = sort_unique(section_pages)
    start = sorted_unique[0]
    end = sorted_unique[-1]

    max_found = max([page for page in found_pages.keys()])

    start_line = 0
    if start > 1:
        start_page = max({page: t for page, t in found_pages.items() if page < start}.keys())
        start_line = found_pages[start_page][0]

    end_line = document_size - 1
    if max(section_pages) < max_found:
        end_page = min({page: t for page, t in found_pages.items() if page >= end}.keys())
        end_line = found_pages[end_page][0]

    return start_line, end_line


def longest_match_in_page_marker_pair(page_markers: Dict[int, Tuple[int, str]]) -> str:
    if len(page_markers) != 2:
        raise ValueError("'page_markers' must be a Dict of len 2.")
    normalized_page_numbers = normalize_page_numbers_to_template(page_markers)

    normalized_lines = [v[1] for k, v in normalized_page_numbers.items()]

    return longest_match_from_list(normalized_lines)


def longest_match_from_list(normalized_lines: List[str]) -> str:
    if len(normalized_lines) != 2:
        raise ValueError("'normalized_lines' must be a list of len 2.")

    seq_match = SequenceMatcher(isjunk=None, a=normalized_lines[0], b=normalized_lines[1], autojunk=False)
    match_obj = seq_match.find_longest_match(alo=0, ahi=len(normalized_lines[0]), blo=0, bhi=len(normalized_lines[1]))

    if match_obj.size < 1:
        raise ValueError("No matching strings found, confirm there is a common string template.")

    if match_obj.size < len(PAGE_NUMBER_TEMPLATE_STR):
        raise ValueError("Match length is less than PAGE_NUMBER_TEMPLATE_STR, something is wrong.")

    return normalized_lines[0][match_obj.a:match_obj.a + match_obj.size]


def sort_unique(arr: List[int]) -> List[int]:
    return sorted(list(set(arr)))


def get_lines_range_from_page_range(start_page: int, end_page: int, found_pages: Dict[int, Tuple[int, str]],
                                    document) -> Tuple[int, int]:
    start_line = 0
    end_line = len(document) - 1

    if start_page > 1 and start_page - 1 in found_pages.keys():
        start_line = found_pages[start_page - 1][0]

    if end_page <= max([x for x, y in found_pages.items()]) and end_page in found_pages.keys():
        end_line = found_pages[end_page][0]

    if start_page - 1 not in found_pages.keys() or end_page not in found_pages.keys():
        return get_window_from_found_pages([start_page, end_page], found_pages, document_size=len(document))

    return start_line, end_line


__all__ = ['section_continuous_numbers', 'get_window_from_found_pages', 'sort_unique', 'get_lines_range_from_page_range', 'PAGE_NUMBER_TEMPLATE_STR', 'normalize_page_numbers_to_template', 'longest_match_in_page_marker_pair', 'longest_match_from_list',
           'shuffle_split_dictionary_in_half', 'PAGE_NUMBER_NAME']
