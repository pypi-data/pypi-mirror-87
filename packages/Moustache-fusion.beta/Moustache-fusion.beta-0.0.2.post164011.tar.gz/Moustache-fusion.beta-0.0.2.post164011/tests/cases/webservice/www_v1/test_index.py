# -*- coding: utf-8 -*-

import sys

sys.path.append('/app/moustache_fusion')


def test_success(client):
    """
    Test that the index page is reachable.
    """
    response = client.get('/')
    assert b'Moustache-swap' in response.get_data()
