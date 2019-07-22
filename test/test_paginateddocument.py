from discoverpagination.paginateddocument import discover_pages, is_intraline_document, page_number_template
from string import Template
from unittest import TestCase


class TestDiscoverPages(TestCase):

    def test_discover_pages_find_intraline_number(self):
        # arrange
        document = ["""engendered, probably, by the decomposition of rank vegetable substances\n""",
                    """in a hot and humid soil.[7] The season of the bilious fever,--_vómito_,\n""",
                    """as it is called,--which scourges these coasts, continues from the spring\n""",
                    """to the autumnal equinox, when it is checked by the cold winds that\n"""]


        # action
        result = discover_pages(document, page_number_template, 7, force_short_discovery=True)

        # assert
        self.assertTrue(7 in result)
        pass

    def test_discover_pages_find_intraline_number_as_pattern(self):
        # arrange
        document = ["""engendered, probably, by the decomposition of rank vegetable substances\n""",
                    """in a hot and humid soil.[7] The season of the bilious fever,--_vómito_,\n""",
                    """as it is called,--which scourges these coasts, continues from the spring\n""",
                    """to the autumnal equinox, when it is checked by the cold winds that\n""",
                    """engendered, probably, by the decomposition of rank vegetable substances\n""",
                    """in a hot and humid soil. The season of the bilious fever,--_vómito_,\n""",
                    """as it is called,--which [8]scourges these coasts, continues from the spring\n""",
                    """to the autumnal equinox, when it is checked by the cold winds that\n"""
                    ]

        # action
        result = discover_pages(document, page_number_template, 7, force_short_discovery=True)

        # assert
        self.assertTrue(7 in result)


class TestIsIntralineDocument(TestCase):

    def test_is_intraline_document_true(self):
        # arrange
        page_numbers_forward = {7: (1, 'in a hot and humid soil.[7] The season of the bilious fever,--_vómito_,'),
                                8: (6, 'as it is called,--which [8]scourges these coasts, continues from the spring')}
        page_number_reverse = {8: (6, 'as it is called,--which [8]scourges these coasts, continues from the spring'),
                               7: (1, 'in a hot and humid soil.[7] The season of the bilious fever,--_vómito_,')}

        # action
        result = is_intraline_document(page_numbers_forward, page_number_reverse)

        # assert
        self.assertTrue(result)
