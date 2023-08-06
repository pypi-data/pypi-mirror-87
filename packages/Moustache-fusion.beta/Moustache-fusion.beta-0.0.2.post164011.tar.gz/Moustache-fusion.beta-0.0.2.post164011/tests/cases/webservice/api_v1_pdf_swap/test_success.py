# -*- coding: utf-8 -*-

import sys

from tests.helpers.api import api_v1_pdf_swap_helper
from tests.helpers.comparison import compare_response_to_reference, expected_same_exported_images

sys.path.append('/app/moustache_fusion')


def test_main10p_m3p_i3p_m1p_i1p_m2p_numbered_false(client, tmpdir):
    data = {
        'main': 'main10p_m3p_i3p_m1p_i1p_m2p/main.pdf',
        'data': 'main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_false.json',
        'inner': [
            'inner_3_pages/lorem_ipsum.pdf',
            'inner_1_page/edgar_allan_poe_murders.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 141000 <= response.content_length <= 142000

    case_path = 'webservice/api_v1_pdf_swap/main10p_m3p_i3p_m1p_i1p_m2p_numbered_false'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(10)


def test_main10p_m3p_i3p_m1p_i1p_m2p_numbered_true(client, tmpdir):
    data = {
        'main': 'main10p_m3p_i3p_m1p_i1p_m2p/main.pdf',
        'data': 'main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'inner_3_pages/lorem_ipsum.pdf',
            'inner_1_page/edgar_allan_poe_murders.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 205000 <= response.content_length <= 206000

    case_path = 'webservice/api_v1_pdf_swap/main10p_m3p_i3p_m1p_i1p_m2p_numbered_true'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(10)


def test_main10p_m3p_i3p_m1p_i1p_m2p_numbered_true_with_main_embedded_odt(client, tmpdir):
    # @todo: same for inner PDF
    data = {
        'main': 'main10p_m3p_i3p_m1p_i1p_m2p/main-with_odt.pdf',
        'data': 'main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'inner_3_pages/lorem_ipsum.pdf',
            'inner_1_page/edgar_allan_poe_murders.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 205000 <= response.content_length <= 206000

    case_path = 'webservice/api_v1_pdf_swap/main10p_m3p_i3p_m1p_i1p_m2p_numbered_true'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(10)


def test_main10p_m3p_i3p_m1p_i1p_m2p_numbered_true_with_main_permission_password(client, tmpdir):
    # @todo: same for inner PDF
    data = {
        'main': 'main10p_m3p_i3p_m1p_i1p_m2p/main-other_password.pdf',
        'data': 'main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'inner_3_pages/lorem_ipsum.pdf',
            'inner_1_page/edgar_allan_poe_murders.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 205000 <= response.content_length <= 206000

    case_path = 'webservice/api_v1_pdf_swap/main10p_m3p_i3p_m1p_i1p_m2p_numbered_true'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(10)


def test_main10p_m3p_i3p_m1p_i1p_m2p_numbered_true_with_main_pdf_a_1a(client, tmpdir):
    # @todo: same for inner PDF
    data = {
        'main': 'main10p_m3p_i3p_m1p_i1p_m2p/main-pdf_a_1a.pdf',
        'data': 'main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'inner_3_pages/lorem_ipsum.pdf',
            'inner_1_page/edgar_allan_poe_murders.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 206000 <= response.content_length <= 207000

    case_path = 'webservice/api_v1_pdf_swap/main10p_m3p_i3p_m1p_i1p_m2p_numbered_true'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(10)


def test_main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p(client, tmpdir):
    """
    @info: covers 2 cases
        - some inner PDF are used multiple times
        - the last page is not from the main content
    """
    data = {
        'main': 'main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p/main.pdf',
        'data': 'main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'inner_1_page/dylan_thomas_night.pdf',
            'inner_1_page/edgar_allan_poe_murders.pdf',
            'inner_1_page/dylan_thomas_wood.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 254000 <= response.content_length <= 255000

    case_path = 'webservice/api_v1_pdf_swap/main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(11)


def test_main1p_i1p(client, tmpdir):
    data = {
        'main': 'main1p_i1p/main.pdf',
        'data': 'main1p_i1p/data.json',
        'inner': [
            'inner_1_page/edgar_allan_poe_murders.pdf'
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 46000 <= response.content_length <= 47000

    case_path = 'webservice/api_v1_pdf_swap/main1p_i1p'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(1)
