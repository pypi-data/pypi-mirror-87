# -*- coding: utf-8 -*-

import sys

from tests.helpers.api import api_v1_pdf_swap_helper
from tests.helpers.comparison import compare_response_to_reference, expected_same_exported_images

sys.path.append('/app/moustache_fusion')


def test_nominal_case_numbered_false(client, tmpdir):
    data = {
        'main': 'nominal_case/main.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_false.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 141000 <= response.content_length <= 142000

    case_path = 'webservice/api_v1_pdf_swap/nominal_case_numbered_false'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(10)


def test_nominal_case_numbered_true(client, tmpdir):
    data = {
        'main': 'nominal_case/main.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 205000 <= response.content_length <= 206000

    case_path = 'webservice/api_v1_pdf_swap/nominal_case_numbered_true'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(10)


def test_nominal_case_numbered_true_with_main_embedded_odt(client, tmpdir):
    # @todo: same for inner PDF
    data = {
        'main': 'nominal_case/main-with_odt.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 205000 <= response.content_length <= 206000

    case_path = 'webservice/api_v1_pdf_swap/nominal_case_numbered_true'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(10)


def test_nominal_case_numbered_true_with_main_permission_password(client, tmpdir):
    # @todo: same for inner PDF
    data = {
        'main': 'nominal_case/main-other_password.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 205000 <= response.content_length <= 206000

    case_path = 'webservice/api_v1_pdf_swap/nominal_case_numbered_true'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(10)


def test_nominal_case_numbered_true_with_main_pdf_a_1a(client, tmpdir):
    # @todo: same for inner PDF
    data = {
        'main': 'nominal_case/main-pdf_a_1a.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 206000 <= response.content_length <= 207000

    case_path = 'webservice/api_v1_pdf_swap/nominal_case_numbered_true'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(10)


def test_pattern_on_multiple_pages(client, tmpdir):
    """
    @info: covers 2 cases
        - some inner PDF are used multiple times
        - the last page is not from the main content
    """
    data = {
        'main': 'pattern_on_multiple_pages/main.pdf',
        'data': 'pattern_on_multiple_pages/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'pattern_on_multiple_pages/pdf_1.pdf',
            'pattern_on_multiple_pages/pdf_2.pdf',
            'pattern_on_multiple_pages/pdf_3.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 254000 <= response.content_length <= 255000

    case_path = 'webservice/api_v1_pdf_swap/pattern_on_multiple_pages'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(11)
