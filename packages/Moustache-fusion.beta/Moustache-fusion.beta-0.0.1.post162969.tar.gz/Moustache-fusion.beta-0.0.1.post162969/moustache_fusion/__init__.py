# -*- coding: utf-8 -*-

"""
    Module de fusion documentaire
"""
__version__ = '0.0.1-162969'


def launch():
    from moustache_fusion import webservice
    webservice.default_app().run(debug=True, host='0.0.0.0')
