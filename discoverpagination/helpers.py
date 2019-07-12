from typing import List, Dict, Tuple


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


__all__ = ['section_continuous_numbers', 'get_window_from_found_pages', 'sort_unique',
           'get_lines_range_from_page_range']
