# -*- coding: utf-8 -*-

import pytest
import re
import sys

from moustache_fusion.exceptions import CommandException
from moustache_fusion.utilities import get_pdf_page_count, get_pdf_pattern_pages
from tests.helpers import get_fixture_path

sys.path.append('/app/moustache_fusion')


@pytest.mark.parametrize('path, expected', [
    ('nominal_case/main.pdf', 10),
    ('nominal_case/pdf_1.pdf', 3),
    ('nominal_case/pdf_2.pdf', 1)
])
def test_get_pdf_page_count_success(path, expected):
    assert expected == get_pdf_page_count(get_fixture_path(path))


def test_get_pdf_page_count_failure_error_trying_to_get_page_count():
    with pytest.raises(CommandException) as exc_info:
        get_pdf_page_count(get_fixture_path('nominal_case/success_with_annexes_pages_numbered_false.json'))

    assert exc_info.value.message == 'Error trying to get page count'
    assert exc_info.value.returncode == 1
    assert re.match(r'Syntax Warning: May not be a PDF file', exc_info.value.stderr) is not None
    assert exc_info.value.command == '/usr/bin/pdfinfo ' \
           + '/app/tests/fixtures/nominal_case/success_with_annexes_pages_numbered_false.json'

@pytest.mark.parametrize('path, pattern, expected', [
    ('pattern_on_multiple_pages/main.pdf', 'PDF_1', [4, 6]),
    ('pattern_on_multiple_pages/main.pdf', 'PDF_2', [7, 9]),
    ('pattern_on_multiple_pages/main.pdf', 'PDF_3', [11]),
    ('pattern_on_multiple_pages/main.pdf', 'PDF_4', []),
])
def test_get_pdf_get_pdf_pattern_pages_success(path, pattern, expected):
    assert expected == get_pdf_pattern_pages(get_fixture_path(path), pattern)