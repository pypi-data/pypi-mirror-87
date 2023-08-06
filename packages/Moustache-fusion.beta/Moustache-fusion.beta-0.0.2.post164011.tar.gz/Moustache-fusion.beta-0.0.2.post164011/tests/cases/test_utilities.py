# -*- coding: utf-8 -*-

import pytest
import re
import sys

from moustache_fusion.exceptions import CommandException, EncryptedPdfException
from moustache_fusion.utilities import get_pdf_page_count, get_pdf_pattern_pages, uc_only_first, validate_pdf
from tests.helpers import get_fixture_path

sys.path.append('/app/moustache_fusion')


@pytest.mark.parametrize('path, expected', [
    ('main10p_m3p_i3p_m1p_i1p_m2p/main.pdf', 10),
    ('inner_3_pages/lorem_ipsum.pdf', 3),
    ('inner_1_page/edgar_allan_poe_murders.pdf', 1)
])
def test_get_pdf_page_count_success(path, expected):
    assert expected == get_pdf_page_count(get_fixture_path(path))


def test_get_pdf_page_count_failure_error_trying_to_get_page_count():
    with pytest.raises(CommandException) as exc_info:
        path = get_fixture_path('main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_false.json')
        get_pdf_page_count(path)

    assert exc_info.value.message == 'Error trying to get page count'
    assert exc_info.value.returncode == 1
    assert re.match(r'Syntax Warning: May not be a PDF file', exc_info.value.stderr) is not None
    assert exc_info.value.command == '/usr/bin/pdfinfo ' \
           + '/app/tests/fixtures/main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_false.json'


@pytest.mark.parametrize('path, pattern, expected', [
    ('main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p/main.pdf', 'PDF_1', [4, 6]),
    ('main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p/main.pdf', 'PDF_2', [7, 9]),
    ('main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p/main.pdf', 'PDF_3', [11]),
    ('main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p/main.pdf', 'PDF_4', []),
])
def test_get_pdf_get_pdf_pattern_pages_success(path, pattern, expected):
    assert expected == get_pdf_pattern_pages(get_fixture_path(path), pattern)


@pytest.mark.parametrize('string, expected', [
    ('', ''),
    ('a', 'A'),
    ('FooBar', 'FooBar'),
    ('fooBar', 'FooBar'),
    ('foo bar', 'Foo bar'),
])
def test_uc_only_first(string, expected):
    assert expected == uc_only_first(string)


def test_validate_pdf_success():
    assert validate_pdf(get_fixture_path('main10p_m3p_i3p_m1p_i1p_m2p/main.pdf'), 'alias') is None


def test_validate_pdf_failure_corrupted_pdf():
    with pytest.raises(RuntimeError) as exc_info:
        validate_pdf(get_fixture_path('main10p_m3p_i3p_m1p_i1p_m2p/main-corrupted.pdf'), 'alias')

    assert exc_info.value.args[0] == 'Alias seems to be corrupted ' \
           + '(using command /usr/bin/pdftotext /app/tests/fixtures/main10p_m3p_i3p_m1p_i1p_m2p/main-corrupted.pdf '\
           + '/dev/null)'


def test_validate_pdf_failure_encrypted_pdf():
    with pytest.raises(EncryptedPdfException) as exc_info:
        validate_pdf(get_fixture_path('main10p_m3p_i3p_m1p_i1p_m2p/main-document_open_password.pdf'), 'alias')

    assert exc_info.value.args[0] == 'Cannot open encrypted alias'
