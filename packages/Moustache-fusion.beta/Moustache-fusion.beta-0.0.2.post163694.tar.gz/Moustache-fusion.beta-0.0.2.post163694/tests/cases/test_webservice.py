# -*- coding: utf-8 -*-
"""
@todo
    - add tests for
        - main document completely overwritten by inner PDFs (1 page, many pages)
        - nothing to replace
    - make 2 distinct tests for test_api_v1_success_pattern_on_multiple_pages_with_annexes_pages_numbered_true
        - a main PDF file ending with an inner PDF
        - a main PDF where some inner PDF are used multiple times
"""

import re
import sys

from flask import json
from tests.helpers import get_fixture_path
from tests.helpers.comparison import compare_exported_images, export_pdf_to_images

sys.path.append('/app/moustache_fusion')


def get_nominal_case_path(path: str) -> str:
    return get_fixture_path('nominal_case/' + path)


def get_pattern_on_multiple_pages_path(path: str) -> str:
    return get_fixture_path('pattern_on_multiple_pages/' + path)


def expected_compare_exported_images_same(pages: int) -> dict:
    expected = {'common': {}, 'extra': [], 'missing': []}
    for i in range(pages):
        expected['common']['{:05d}.jpg'.format(i + 1)] = 0
    return expected


def compare_response_to_reference(tmpdir, response, case_path: str) -> dict:
    """
    Compare PDF content in reposen with previously exported images.
    """
    pdf = tmpdir.join('result.pdf')
    pdf.write(response.get_data(), 'wb')

    reference_dir = '/app/tests/references/' + case_path

    candidate_dir = '/app/tests/out/' + case_path + '/candidate'
    diffs_dir = '/app/tests/out/' + case_path + '/diffs'

    export_pdf_to_images(str(pdf), candidate_dir)
    return compare_exported_images(reference_dir, candidate_dir, diffs_dir)


def normalize_json_reponse_message(response) -> dict:
    json_reponse = json.loads(response.get_data(as_text=True))

    if 'message' in json_reponse and isinstance(json_reponse['message'], str):
        json_reponse['message'] = re.sub(r'/tmp/[^/]+/[^/]+\.pdf', '/tmp/tmp_dir/file.pdf', json_reponse['message'])

    return json_reponse


def test_www_v1_index(client):
    """
    Test that the index page is reachable.
    """
    response = client.get('/')
    assert b'Moustache-swap' in response.get_data()


def test_api_v1_success_nominal_case_with_annexes_pages_numbered_false(client, tmpdir):
    data = {
        'principal': (open(get_nominal_case_path('main.pdf'), 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_false.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 141000 <= response.content_length <= 142000

    case_path = 'test_webservice/test_api_v1_success_nominal_case_with_annexes_pages_numbered_false'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_compare_exported_images_same(10)


def test_api_v1_success_nominal_case_with_annexes_pages_numbered_true(client, tmpdir):
    data = {
        'principal': (open(get_nominal_case_path('main.pdf'), 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_true.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 205000 <= response.content_length <= 206000

    case_path = 'test_webservice/test_api_v1_success_nominal_case_with_annexes_pages_numbered_true'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_compare_exported_images_same(10)


def test_api_v1_success_pattern_on_multiple_pages_with_annexes_pages_numbered_true(client, tmpdir):
    """
    @info: covers 2 cases
        - some inner PDF are used multiple times
        - the last page is not from the main content
    """
    data = {
        'principal': (open(get_pattern_on_multiple_pages_path('main.pdf'), 'rb'), 'main.pdf'),
        'params': (
            open(get_pattern_on_multiple_pages_path('success_with_annexes_pages_numbered_true.json'), 'rb'),
            'data.json'
        ),
        'annexe': [
            (open(get_pattern_on_multiple_pages_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_pattern_on_multiple_pages_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
            (open(get_pattern_on_multiple_pages_path('pdf_3.pdf'), 'rb'), 'pdf_3.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 254000 <= response.content_length <= 255000

    case_path = 'test_webservice/test_api_v1_success_pattern_on_multiple_pages_with_annexes_pages_numbered_true'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_compare_exported_images_same(11)


def test_api_v1_failure_nominal_case_without_params(client):
    data = {
        'principal': (open(get_nominal_case_path('main.pdf'), 'rb'), 'main.pdf'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 400

    expected = {'message': 'JSON file with replacements for field "params" was not provided'}
    assert normalize_json_reponse_message(response) == expected


def test_api_v1_failure_nominal_case_with_wrong_mime_type_for_params(client):
    data = {
        'principal': (open(get_nominal_case_path('main.pdf'), 'rb'), 'main.pdf'),
        'params': (open(__file__, 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 400

    expected = {'message': 'Invalid JSON provided for field "params"'}
    assert normalize_json_reponse_message(response) == expected


def test_api_v1_failure_nominal_case_without_principal(client):
    data = {
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_true.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 400

    assert normalize_json_reponse_message(response) == {
        'message': '"principal" key is not in request files '
                   + "(ImmutableMultiDict([('params', <FileStorage: 'data.json' ('application/json')>), "
                   + "('annexe', <FileStorage: 'pdf_1.pdf' ('application/pdf')>), "
                   + "('annexe', <FileStorage: 'pdf_2.pdf' ('application/pdf')>)]))",
    }


def test_api_v1_failure_nominal_case_without_annexe(client):
    data = {
        'principal': (open(get_nominal_case_path('main.pdf'), 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_true.json'), 'rb'), 'data.json'),
        'annexe': []
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 400

    assert normalize_json_reponse_message(response) == {
        'message': 'File name "pdf_1.pdf" present in "params" JSON data but not in "annexe" files'
    }


def test_api_v1_failure_nominal_case_with_non_unique_content_pdf_pattern(client):
    data = {
        'principal': (open(get_nominal_case_path('main.pdf'), 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('failure_with_non_unique_patterns.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 400

    assert normalize_json_reponse_message(response) == {
        'message': 'Non unique pattern "PDF_1" found for file "pdf_2.pdf" (already found for file "pdf_1.pdf")'
    }


def test_api_v1_failure_nominal_case_with_wrong_principal_mime_type(client):
    data = {
        'principal': (open(__file__, 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_false.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 400

    assert normalize_json_reponse_message(response) == {
        'message': '"principal" PDF document "main.pdf" MIME type is not "application/pdf" '
                   + '(found "text/x-python" MIME type for "/tmp/tmp_dir/file.pdf")'
    }


def test_api_v1_failure_nominal_case_with_wrong_content_pdf_mime_type(client):
    data = {
        'principal': (open(get_nominal_case_path('main.pdf'), 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_false.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(__file__, 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 400

    assert normalize_json_reponse_message(response) == {
        'message': '"annexe" PDF document "pdf_1.pdf" MIME type is not "application/pdf" '
                   + '(found "text/x-python" MIME type for "/tmp/tmp_dir/file.pdf")'
    }


def test_api_v1_failure_nominal_case_with_corrupted_principal(client, tmpdir):
    data = {
        'principal': (open(get_nominal_case_path('main-corrupted.pdf'), 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_true.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 400

    assert normalize_json_reponse_message(response) == {
        'message': '"principal" PDF document "main.pdf" seems to be corrupted '
                   + '(using command /usr/bin/pdftotext /tmp/tmp_dir/file.pdf /dev/null)',
    }


def test_api_v1_failure_nominal_case_with_corrupted_content_pdf(client, tmpdir):
    data = {
        'principal': (open(get_nominal_case_path('main.pdf'), 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_true.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1-corrupted.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 500

    expected = {
        'message': 'Error while opening inner PDF "pdf_1.pdf" (invalid literal for int() with base 10: b\'n\')'
    }
    assert normalize_json_reponse_message(response) == expected


def test_api_v1_failure_nominal_case_with_missing_pattern(client, tmpdir):
    data = {
        'principal': (open(get_nominal_case_path('main-without-PDF_2.pdf'), 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_true.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 500

    assert normalize_json_reponse_message(response) == {
        'message': 'Pattern "PDF_2" not found in main document /tmp/tmp_dir/file.pdf'
    }


def test_api_v1_failure_nominal_case_with_unexpected_font_size(client, tmpdir):
    data = {
        'principal': (open(get_nominal_case_path('main.pdf'), 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_true.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ],
        'font_size': '-1'
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 400

    assert normalize_json_reponse_message(response) == {
        'message': 'Expected positive non-zero integer value for field "font_size" but got "-1"'
    }


def test_api_v1_failure_nominal_case_with_invalid_pos_x_value(client, tmpdir):
    data = {
        'principal': (open(get_nominal_case_path('main.pdf'), 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_true.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ],
        'pos_x': '-1'
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 400

    assert normalize_json_reponse_message(response) == {
        'message': 'Expected positive integer value for field "pos_x" but got "-1"'
    }


def test_api_v1_failure_nominal_case_with_invalid_pos_y_value(client, tmpdir):
    data = {
        'principal': (open(get_nominal_case_path('main.pdf'), 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_true.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ],
        'pos_y': '-1'
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 400

    assert normalize_json_reponse_message(response) == {
        'message': 'Expected positive integer value for field "pos_y" but got "-1"'
    }


def test_api_v1_failure_nominal_case_with_multiple_times_annexe_file_name(client, tmpdir):
    data = {
        'principal': (open(get_nominal_case_path('main.pdf'), 'rb'), 'main.pdf'),
        'params': (open(get_nominal_case_path('success_with_annexes_pages_numbered_true.json'), 'rb'), 'data.json'),
        'annexe': [
            (open(get_nominal_case_path('pdf_1.pdf'), 'rb'), 'pdf_1.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
            (open(get_nominal_case_path('pdf_2.pdf'), 'rb'), 'pdf_2.pdf'),
        ]
    }
    response = client.post('/api', data=data, follow_redirects=True)
    assert response.status_code == 400

    assert normalize_json_reponse_message(response) == {
        'message': '"annexe"[3] file name "pdf_2.pdf" was already sent in request files '
                   + "(ImmutableMultiDict([('principal', <FileStorage: 'main.pdf' ('application/pdf')>), "
                   + "('params', <FileStorage: 'data.json' ('application/json')>), "
                   + "('annexe', <FileStorage: 'pdf_1.pdf' ('application/pdf')>), "
                   + "('annexe', <FileStorage: 'pdf_2.pdf' ('application/pdf')>), "
                   + "('annexe', <FileStorage: 'pdf_2.pdf' ('application/pdf')>)]))"
    }
