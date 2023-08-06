# -*- coding: utf-8 -*-
"""
This file holds tests for all cases where the request is the reason of failure of the API call (HTTP code 400).
"""

import sys

from tests.helpers.api import api_v1_pdf_swap_helper, normalize_json_reponse_message

sys.path.append('/app/moustache_fusion')


def test_without_json(client):
    data = {
        'main': 'nominal_case/main.pdf',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    expected = {'message': 'JSON file with replacements for field "params" was not provided'}
    assert normalize_json_reponse_message(response) == expected


def test_without_main(client):
    data = {
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    assert normalize_json_reponse_message(response) == {
        'message': '"principal" key is not in request files '
                   + "(ImmutableMultiDict([('params', <FileStorage: 'data.json' ('application/json')>), "
                   + "('annexe', <FileStorage: 'pdf_1.pdf' ('application/pdf')>), "
                   + "('annexe', <FileStorage: 'pdf_2.pdf' ('application/pdf')>)]))",
    }


def test_without_annexe(client):
    data = {
        'main': 'nominal_case/main.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': []
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    assert normalize_json_reponse_message(response) == {
        'message': 'File name "pdf_1.pdf" present in "params" JSON data but not in "annexe" files'
    }


def test_with_non_unique_pattern(client):
    data = {
        'main': 'nominal_case/main.pdf',
        'data': 'nominal_case/failure_with_non_unique_patterns.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    assert normalize_json_reponse_message(response) == {
        'message': 'Non unique pattern "PDF_1" found for file "pdf_2.pdf" (already found for file "pdf_1.pdf")'
    }


def test_with_missing_pattern(client):
    data = {
        'main': 'nominal_case/main-without-PDF_2.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    assert normalize_json_reponse_message(response) == {
        'message': 'Pattern "PDF_2" not found in main document /tmp/tmp_dir/file.pdf'
    }


def test_with_unexpected_font_size(client):
    data = {
        'main': 'nominal_case/main.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ],
        'font_size': '-1'
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    assert normalize_json_reponse_message(response) == {
        'message': 'Expected positive non-zero integer value for field "font_size" but got "-1"'
    }


def test_with_invalid_pos_x_value(client):
    data = {
        'main': 'nominal_case/main.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ],
        'pos_x': '-1'
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    assert normalize_json_reponse_message(response) == {
        'message': 'Expected positive integer value for field "pos_x" but got "-1"'
    }


def test_with_invalid_pos_y_value(client):
    data = {
        'main': 'nominal_case/main.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ],
        'pos_y': '-1'
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    assert normalize_json_reponse_message(response) == {
        'message': 'Expected positive integer value for field "pos_y" but got "-1"'
    }


def test_with_same_inner_file_name(client):
    data = {
        'main': 'nominal_case/main.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            {'nominal_case/pdf_2.pdf': 'pdf_2.pdf'},
            {'nominal_case/pdf_2.pdf': 'pdf_2.pdf'},
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    assert normalize_json_reponse_message(response) == {
        'message': '"annexe"[3] file name "pdf_2.pdf" was already sent in request files '
                   + "(ImmutableMultiDict([('principal', <FileStorage: 'main.pdf' ('application/pdf')>), "
                   + "('params', <FileStorage: 'data.json' ('application/json')>), "
                   + "('annexe', <FileStorage: 'pdf_1.pdf' ('application/pdf')>), "
                   + "('annexe', <FileStorage: 'pdf_2.pdf' ('application/pdf')>), "
                   + "('annexe', <FileStorage: 'pdf_2.pdf' ('application/pdf')>)]))"
    }


def test_with_wrong_main_mime_type(client):
    data = {
        'main': __file__,
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    assert normalize_json_reponse_message(response) == {
        'message': '"principal" PDF document "main.pdf" MIME type is not "application/pdf" '
                   + '(found "text/x-python" MIME type for "/tmp/tmp_dir/file.pdf")'
    }


def test_with_wrong_json_mime_type(client):
    data = {
        'main': 'nominal_case/main.pdf',
        'data': __file__,
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    expected = {'message': 'Invalid JSON provided for field "params"'}
    assert normalize_json_reponse_message(response) == expected


def test_with_wrong_inner_mime_type(client):
    data = {
        'main': 'nominal_case/main.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            __file__,
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    assert normalize_json_reponse_message(response) == {
        'message': '"annexe" PDF document "pdf_1.pdf" MIME type is not "application/pdf" '
                   + '(found "text/x-python" MIME type for "/tmp/tmp_dir/file.pdf")'
    }


def test_with_corrupted_main(client):
    data = {
        'main': 'nominal_case/main-corrupted.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    assert normalize_json_reponse_message(response) == {
        'message': '"principal" PDF document "main.pdf" seems to be corrupted '
                   + '(using command /usr/bin/pdftotext /tmp/tmp_dir/file.pdf /dev/null)',
    }


def test_with_corrupted_inner(client):
    data = {
        'main': 'nominal_case/main.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            {'nominal_case/pdf_1-corrupted.pdf': 'pdf_1.pdf'},
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    # @fixme: 400
    assert response.status_code == 500
    assert normalize_json_reponse_message(response) == {
        'message': 'Error while opening inner PDF "pdf_1.pdf" (invalid literal for int() with base 10: b\'n\')'
    }


def test_with_encrypted_main(client, tmpdir):
    # @todo: same for inner PDF
    data = {
        'main': 'nominal_case/main-document_open_password.pdf',
        'data': 'nominal_case/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'nominal_case/pdf_1.pdf',
            'nominal_case/pdf_2.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 400
    expected = {'message': 'Cannot open encrypted "principal" PDF document "main.pdf"'}
    assert normalize_json_reponse_message(response) == expected
