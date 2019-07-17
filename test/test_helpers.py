from unittest import TestCase
from discoverpagination.helpers import *


class TestSplitDictionaryInHalf(TestCase):

    def test_split_dictionary_in_half_len_2(self):
        # arrange
        subject = {1: "one", 2: "two"}

        # action
        first, second = shuffle_split_dictionary_in_half(subject)

        # assert

        self.assertEqual(2, len(subject))
        self.assertEqual(1, len(first))
        self.assertEqual(1, len(second))

        if 1 not in first:
            self.assertTrue(1 in second)

        if 2 not in first:
            self.assertTrue(2 in second)

        if 1 not in second:
            self.assertTrue(1 in first)

        if 2 not in second:
            self.assertTrue(2 in first)

        if 1 in first:
            self.assertTrue(1 not in second)

        if 2 in first:
            self.assertTrue(2 not in second)

        # No overlapping keys
        self.assertFalse([k for k in first.keys() if k in second.keys()])

    def test_split_dictionary_in_half_len_5(self):
        # arrange
        subject = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}

        # action
        first, second = shuffle_split_dictionary_in_half(subject)

        # assert
        self.assertEqual(5, len(subject))
        self.assertEqual(3, len(first))
        self.assertEqual(2, len(second))

        # No overlapping keys
        self.assertFalse([k for k in first.keys() if k in second.keys()])

    def test_split_dictionary_in_half_len_6(self):
        # arrange
        subject = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}

        # action
        first, second = shuffle_split_dictionary_in_half(subject)

        # assert
        self.assertEqual(6, len(subject))
        self.assertEqual(3, len(first))
        self.assertEqual(3, len(second))

        # No overlapping keys
        self.assertFalse([k for k in first.keys() if k in second.keys()])

    def test_split_dictionary_in_half_len_1(self):
        # arrange
        subject = {1: "one"}

        # action
        first, second = shuffle_split_dictionary_in_half(subject)

        # assert
        self.assertEqual(1, len(subject))
        self.assertEqual(1, len(first))
        self.assertEqual(0, len(second))

        # No overlapping keys
        self.assertFalse([k for k in first.keys() if k in second.keys()])

    def test_split_dictionary_in_half_len_0(self):
        # arrange
        subject = {}

        # action
        first, second = shuffle_split_dictionary_in_half(subject)

        # assert
        self.assertEqual(0, len(subject))
        self.assertEqual(0, len(first))
        self.assertEqual(0, len(second))

        # No overlapping keys
        self.assertFalse([k for k in first.keys() if k in second.keys()])


class TestSectionContinuousNumbers(TestCase):

    def test_section_continuous_numbers_make_continuous_sublists(self):
        # arrange
        arr = [1, 1, 1, 1, 1, 2, 3, 5, 5, 5]

        # action
        result = section_continuous_numbers(arr)

        # assert
        self.assertTrue(isinstance(result, list))

        self.assertEqual(2, len(result))

        self.assertEqual(1, result[0][0])
        self.assertEqual(5, result[1][0])

    def test_section_continuous_numbers_make_three_lists_of_one_number(self):
        # arrange
        arr = [1, 3, 5]

        # action
        result = section_continuous_numbers(arr)

        # assert
        self.assertTrue(isinstance(result, list))
        self.assertEqual(3, len(result))
        self.assertEqual(1, result[0][0])
        self.assertEqual(3, result[1][0])
        self.assertEqual(5, result[2][0])

    def test_section_continuous_numbers_make_three_lists_of_three_numbers(self):
        # arrange
        arr = [1, 2, 3, 5, 6, 7, 21, 20, 19]

        # action
        result = section_continuous_numbers(arr)

        # assert
        self.assertTrue(isinstance(result, list))

        self.assertEqual(3, len(result))
        self.assertEqual(3, len(result[0]))
        self.assertEqual(3, len(result[1]))
        self.assertEqual(3, len(result[2]))

        self.assertEqual(1, result[0][0])
        self.assertEqual(3, result[0][2])

        self.assertEqual(5, result[1][0])
        self.assertEqual(7, result[1][2])

        self.assertEqual(19, result[2][0])
        self.assertEqual(21, result[2][2])


class TestGetWindowFromFoundPages(TestCase):
    #
    # def test_get_window_from_found_pages_reversed_start_end_error(self):
    #     # arrange
    #     arr = [16]
    #     found_pages = {6: (984, '    6'), 7: (2904, '    7'), 8: (3036, '    8'), 9: (3212, '    9'),
    #                    10: (3447, '    10'),
    #                    11: (3582, '    11'), 12: (4346, '    12'), 13: (5271, '    13'), 14: (5485, '    14'),
    #                    15: (5526, '    15'),
    #                    20: (8958, '    20'), 21: (9105, '    21'), 22: (9237, '    22'), 23: (9452, '    23'),
    #                    24: (9731, '    24'),
    #                    25: (9969, '    25'), 26: (10403, '    26'), 27: (10531, '    27'), 28: (10662, '    28'),
    #                    29: (10801, '    29'),
    #                    30: (10895, '    30'), 31: (13467, '    31'), 32: (14201, '    32'), 33: (14372, '    33'),
    #                    34: (14448, '    34'),
    #                    35: (17830, '    35'), 36: (18010, '    36'), 37: (18036, '    37'), 38: (22863, '    38'),
    #                    39: (24824, '    39'),
    #                    40: (26515, '    40'), 41: (27785, '    41'), 42: (27958, '    42'), 43: (28166, '    43'),
    #                    44: (29046, '    44'),
    #                    45: (32372, '    45'), 46: (32545, '    46'), 47: (32725, '    47'), 48: (32884, '    48'),
    #                    49: (33034, '    49'),
    #                    50: (33175, '    50'), 51: (33319, '    51'), 52: (33573, '    52'), 53: (33713, '    53'),
    #                    54: (34060, '    54'),
    #                    55: (34202, '    55'), 56: (34336, '    56'), 57: (34391, '    57'), 58: (34463, '    58'),
    #                    59: (34668, '    59'),
    #                    60: (34806, '    60'), 61: (34855, '    61'), 62: (35043, '    62'), 63: (35138, '    63'),
    #                    64: (35268, '    64'),
    #                    19: (1795, '    19'), 18: (1531, '    18'), 17: (1286, '    17')}
    #
    #     # action
    #     start, end = get_window_from_found_pages(arr, found_pages, document_size=110)
    #
    #     # assert
    #     self.assertEqual(0, start)

    def test_get_window_from_found_pages_first_page_equals_zero(self):
        # arrange
        arr = [1]
        found_pages = {2: (20, "ok"), 3: (30, "ok"), 4: (40, "ok"), 5: (50, "ok"), 6: (60, "ok"), 7: (70, "ok"),
                       8: (80, "ok"), 11: (110, "ok")}

        # action
        start, end = get_window_from_found_pages(arr, found_pages, document_size=110)

        # assert
        self.assertEqual(0, start)

    def test_get_window_from_found_pages_end_page_equals_document_size(self):
        # arrange
        arr = [9]
        found_pages = {1: (10, "ok"), 2: (20, "ok"), 3: (30, "ok"), 4: (40, "ok"), 5: (50, "ok"), 6: (60, "ok"),
                       7: (70, "ok"), 8: (80, "ok")}

        # action
        start, end = get_window_from_found_pages(arr, found_pages, document_size=234)

        # assert
        self.assertEqual(233, end)

    def test_get_window_from_found_pages_end_page_beyond_found(self):
        # arrange
        arr = [123]
        found_pages = {1: (10, "ok"), 2: (20, "ok"), 3: (30, "ok"), 4: (40, "ok"), 5: (50, "ok"), 6: (60, "ok"),
                       7: (70, "ok"), 8: (80, "ok")}

        # action
        start, end = get_window_from_found_pages(arr, found_pages, document_size=234)

        # assert
        self.assertEqual(233, end)

    def test_get_window_from_found_pages_start_end_index_single_page(self):
        # arrange
        arr = [9]
        found_pages = {1: (10, "ok"), 2: (20, "ok"), 3: (30, "ok"), 4: (40, "ok"), 5: (50, "ok"), 6: (60, "ok"),
                       7: (70, "ok"), 8: (80, "ok"), 11: (110, "ok")}

        # action
        start, end = get_window_from_found_pages(arr, found_pages, document_size=120)

        # assert

        self.assertEqual(80, start)
        self.assertEqual(110, end)

    def test_get_window_from_found_pages_start_end_index_multi_page(self):
        # arrange
        arr = [4, 5, 6, 7, 8, 9, 10]
        found_pages = {1: (10, "ok"), 2: (20, "ok"), 3: (30, "ok"), 11: (111, "ok"), 12: (120, "ok"), 13: (130, "ok"), 14: (140, "ok")}

        # action
        start, end = get_window_from_found_pages(arr, found_pages, document_size=150)

        # assert

        self.assertEqual(30, start)
        self.assertEqual(111, end)


class TestSortUnique(TestCase):
    def test_sort_unique_empty_array_returns_empty(self):
        # arrange
        arr = []

        # action
        result = sort_unique(arr)

        # assert
        self.assertTrue(isinstance(result, list))
        self.assertEqual(0, len(arr))

    def test_sort_unique_sort_simple(self):
        # arrange
        arr = [1, 2, 3]

        # action
        result = sort_unique(arr)

        # assert
        self.assertTrue(isinstance(result, list))

        self.assertEqual(3, len(result))

        self.assertEqual(1, result[0])
        self.assertEqual(2, result[1])
        self.assertEqual(3, result[2])

    def test_sort_unique_sort_complex(self):
        # arrange
        arr = [3, 1, 2, 10, 3, 6, 8, 8, 9, 10]

        # action
        result = sort_unique(arr)

        # assert
        self.assertTrue(isinstance(result, list))

        self.assertEqual(7, len(result))

        self.assertEqual(1, result[0])
        self.assertEqual(2, result[1])
        self.assertEqual(10, result[6])

    def test_sort_unique_make_unique(self):
        # arrange
        arr = [1, 1, 1, 1, 1, 5, 5, 5, 5, 5]

        # action
        result = sort_unique(arr)

        # assert
        self.assertTrue(isinstance(result, list))

        self.assertEqual(2, len(result))

        self.assertEqual(1, result[0])
        self.assertEqual(5, result[1])


class TestGetLinesRangeFromPageRange(TestCase):
    def test_get_lines_range_from_page_range_two_pages(self):
        # arrange
        found_pages = {1: (10, "ok"), 2: (20, "ok"), 3: (30, "ok")}
        start_page = 2
        end_page = 3
        document = ['Lorem ipsum'] * 31
        # action
        start_line, end_line = get_lines_range_from_page_range(start_page=start_page, end_page=end_page, found_pages=found_pages, document=document)

        # assert
        self.assertEqual(10, start_line)
        self.assertEqual(30, end_line)

    def test_get_lines_range_from_page_range_ten_pages(self):
        # arrange
        found_pages = {1: (10, "ok"), 2: (20, "ok"), 3: (30, "ok"), 4: (40, "ok"), 5: (50, "ok"), 6: (60, "ok"), 7: (70, "ok"), 8: (80, "ok"),
                       9: (90, "ok"), 10: (100, "ok"), 11: (110, "ok"), 12: (120, "ok"), 13: (130, "ok"), 14: (140, "ok"), 15: (150, "ok"), 16: (160, "ok")}

        start_page = 4
        end_page = 14
        document = ['Lorem ipsum'] * 161
        # action
        start_line, end_line = get_lines_range_from_page_range(start_page=start_page, end_page=end_page, found_pages=found_pages, document=document)

        # assert
        self.assertEqual(30, start_line)
        self.assertEqual(140, end_line)

    def test_get_lines_range_from_page_range_where_start_is_missing(self):
        # arrange
        found_pages = {1: (10, "ok"), 2: (20, "ok"), 9: (90, "ok"), 10: (100, "ok"), 11: (110, "ok"), 12: (120, "ok"), 13: (130, "ok"), 14: (140, "ok"), 15: (150, "ok"), 16: (160, "ok")}

        start_page = 4
        end_page = 14
        document = ['Lorem ipsum'] * 161
        # action
        start_line, end_line = get_lines_range_from_page_range(start_page=start_page, end_page=end_page, found_pages=found_pages, document=document)

        # assert
        self.assertEqual(20, start_line)
        self.assertEqual(140, end_line)

    def test_get_lines_range_from_page_range_where_end_is_missing(self):
        # arrange
        found_pages = {1: (10, "ok"), 2: (20, "ok"), 3: (30, "ok"), 4: (40, "ok"), 5: (50, "ok"), 6: (60, "ok"), 7: (70, "ok"), 8: (80, "ok"),
                       16: (160, "ok")}

        start_page = 4
        end_page = 14
        document = ['Lorem ipsum'] * 161
        # action
        start_line, end_line = get_lines_range_from_page_range(start_page=start_page, end_page=end_page,
                                                               found_pages=found_pages, document=document)

        # assert
        self.assertEqual(30, start_line)
        self.assertEqual(160, end_line)


class TestLongestMatchFromList(TestCase):

    def test_longest_match_from_list_simple(self):
        # arrange
        test_list = [PAGE_NUMBER_TEMPLATE_STR, PAGE_NUMBER_TEMPLATE_STR]

        # action
        result = longest_match_from_list(test_list)

        # assert
        expected = PAGE_NUMBER_TEMPLATE_STR
        self.assertEqual(expected, result)

    def test_longest_match_from_list_complex(self):
        # arrange
        test_list = ['They established their capital at Tula ' + PAGE_NUMBER_TEMPLATE_STR + ', north of the Mexican', '' + PAGE_NUMBER_TEMPLATE_STR + " appearance of almost modern constructions."]

        # action
        result = longest_match_from_list(test_list)

        # assert
        expected = PAGE_NUMBER_TEMPLATE_STR
        self.assertEqual(expected, result)

    def test_longest_match_from_list_extremities(self):
        # arrange
        test_list = ['They established their capital at Tula ' + PAGE_NUMBER_TEMPLATE_STR, PAGE_NUMBER_TEMPLATE_STR + " appearance of almost modern constructions."]

        # action
        result = longest_match_from_list(test_list)

        # assert
        expected = PAGE_NUMBER_TEMPLATE_STR
        self.assertEqual(expected, result)

    def test_longest_match_from_list_long(self):
        # arrange
        test_list = ["---ABCDE" + PAGE_NUMBER_TEMPLATE_STR + "FGHI---", "---ABCDE" + PAGE_NUMBER_TEMPLATE_STR + "FGHI---"]

        # action
        result = longest_match_from_list(test_list)

        # assert
        expected = "---ABCDE" + PAGE_NUMBER_TEMPLATE_STR + "FGHI---"
        self.assertEqual(expected, result)

    def test_longest_match_from_list_complex_long(self):
        # arrange
        test_list = ["They established their capital at Tula ---ABCDE" + PAGE_NUMBER_TEMPLATE_STR + "FGHI---, north of the Mexican", "appearance of almost modern---ABCDE" + PAGE_NUMBER_TEMPLATE_STR + "FGHI--- constructions."]

        # action
        result = longest_match_from_list(test_list)

        # assert
        expected = "---ABCDE" + PAGE_NUMBER_TEMPLATE_STR + "FGHI---"
        self.assertEqual(expected, result)


class TestLongestMatchInPageMarkerPair(TestCase):

    def test_longest_match_in_page_marker_pair_simple(self):
        # arrange
        page_markers_forward = {19: (1475, '19'),
                                22: (1484, '22')}

        # action
        result = longest_match_in_page_marker_pair(page_markers_forward)

        # assert
        expected = PAGE_NUMBER_TEMPLATE_STR
        self.assertEqual(expected, result)

    def test_longest_match_in_page_marker_pair_long(self):
        # arrange
        page_markers_forward = {
            19: (1475, 'times.asd19dsa They established their capital at Tula, north of the Mexican'),
            22: (1484, 'appearance of almost modern constructions.fgh22hgf')}

        # action
        result = longest_match_in_page_marker_pair(page_markers_forward)

        # assert
        expected = PAGE_NUMBER_TEMPLATE_STR
        self.assertEqual(expected, result)

    def test_longest_match_in_page_marker_pair_extremities(self):
        # arrange
        page_markers_forward = {
            19: (1475, '19asddsatimes. They established their capital at Tula, north of the Mexican'),
            22: (1484, 'appearance of almost modern constructions.fghhgf22')}

        # action
        result = longest_match_in_page_marker_pair(page_markers_forward)

        # assert
        expected = PAGE_NUMBER_TEMPLATE_STR
        self.assertEqual(expected, result)

    def test_longest_match_in_page_marker_pair_complex(self):
        # arrange
        page_markers_forward = {
            19: (1475, 'times.[19] They established their capital at Tula, north of the Mexican'),
            22: (1484, 'appearance of almost modern constructions.[22]')}

        # action
        result = longest_match_in_page_marker_pair(page_markers_forward)

        # assert
        expected = 's.[' + PAGE_NUMBER_TEMPLATE_STR + ']'
        self.assertEqual(expected, result)

    def test_longest_match_in_page_marker_pair_complex_long(self):
        # arrange
        page_markers_forward = {
            19: (1475, 'times. --ABCD[19]EFGH-- They established their capital at Tula, north of the Mexican'),
            22: (1484, 'appearance of almost modern constructions. --ABCD[22]EFGH--')}

        # action
        result = longest_match_in_page_marker_pair(page_markers_forward)

        # assert
        expected = 's. --ABCD[' + PAGE_NUMBER_TEMPLATE_STR + ']EFGH--'
        self.assertEqual(expected, result)
