# -*- coding: utf-8 -*-

import pytest

from flask import testing
from moustache_fusion import webservice


@pytest.fixture
def client() -> testing.FlaskClient:
    webservice.app.config['TESTING'] = True

    with webservice.app.test_client() as client:
        yield client
