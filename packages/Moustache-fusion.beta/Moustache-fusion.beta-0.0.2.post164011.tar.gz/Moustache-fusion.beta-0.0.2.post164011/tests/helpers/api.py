# -*- coding: utf-8 -*-

import os
import re

from flask import json, wrappers
from tests.helpers import get_fixture_path


def normalize_json_reponse_message(response) -> dict:
    json_reponse = json.loads(response.get_data(as_text=True))

    if 'message' in json_reponse and isinstance(json_reponse['message'], str):
        json_reponse['message'] = re.sub(r'/tmp/[^/]+/[^/]+\.pdf', '/tmp/tmp_dir/file.pdf', json_reponse['message'])

    return json_reponse


def api_v1_pdf_swap_helper(client, data: dict) -> wrappers.Response:
    def abs_path(path: str) -> str:
        if os.path.isabs(path):
            return path
        else:
            return get_fixture_path(path)

    post_data = {}

    if 'main' in data:
        post_data['principal'] = (open(abs_path(data['main']), 'rb'), 'main.pdf')

    if 'data' in data:
        post_data['params'] = (open(abs_path(data['data']), 'rb'), 'data.json')

    if 'inner' in data:
        post_data['annexe'] = []
        for index, path in enumerate(data['inner'], start=1):
            if isinstance(path, str):
                post_data['annexe'].append((open(abs_path(path), 'rb'), os.path.basename(path)))
            elif isinstance(path, dict) and len(path) == 1:
                realpath = list(path.keys())[0]
                filename = list(path.values())[0]
                post_data['annexe'].append((open(abs_path(realpath), 'rb'), filename))
            else:
                raise RuntimeError('@fixme')

    for key, value in data.items():
        if key not in ['data', 'inner', 'main']:
            post_data[key] = value

    return client.post('/api', data=post_data, follow_redirects=True)
