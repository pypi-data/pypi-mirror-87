# -*- coding: utf-8 -*-

import re
import sys

from flask import json
from tests.helpers import get_fixture_path
from tests.helpers.comparison import compare_exported_images, export_pdf_to_images

sys.path.append('/app/moustache_fusion')


def get_nominal_case_path(path: str) -> str:
    return get_fixture_path('nominal_case/' + path)


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

    json_reponse = json.loads(response.get_data(as_text=True))
    assert json_reponse == {'message': 'Le fichier json de paramètres n\'est pas présent'}


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

    json_reponse = json.loads(response.get_data(as_text=True))
    assert json_reponse == {
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

    json_reponse = json.loads(response.get_data(as_text=True))
    assert json_reponse == {
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

    json_reponse = json.loads(response.get_data(as_text=True))
    assert json_reponse == {
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

    json_reponse = json.loads(response.get_data(as_text=True))
    assert json_reponse == {
        'message': 'Main PDF document "principal" MIME type is not "application/pdf" '
                   + '(found "text/x-python" MIME type for "main.pdf")'
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

    json_reponse = json.loads(response.get_data(as_text=True))
    assert json_reponse == {
        'message': 'Document "annexe" MIME type is not "application/pdf" '
                   + '(found "text/x-python" MIME type for "pdf_1.pdf")'
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
    assert response.status_code == 500

    json_reponse = json.loads(response.get_data(as_text=True))
    if 'message' in json_reponse and isinstance(json_reponse['message'], str):
        json_reponse['message'] = re.sub(r'/tmp/[^/]+/[^/]+\.pdf', '/tmp/tmp_dir/file.pdf', json_reponse['message'])
    assert json_reponse == {
        'message': 'Error code 1 returned by command for annexe "pdf_1.pdf": '
                   + '/usr/bin/pdfgrep -n --cache "PDF_1" /tmp/tmp_dir/file.pdf'
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

    json_reponse = json.loads(response.get_data(as_text=True))
    assert json_reponse == {
        'message': 'Error while opening annexe "pdf_1.pdf" (invalid literal for int() with base 10: b\'n\')'
    }
