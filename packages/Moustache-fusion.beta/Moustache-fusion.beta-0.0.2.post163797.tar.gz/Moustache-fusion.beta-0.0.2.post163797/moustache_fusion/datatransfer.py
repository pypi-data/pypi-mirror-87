# -*- coding: utf-8 -*-
"""
Data Transfer Objects
"""


class AbstractPdf():
    alias = None
    length = None
    name = None
    path = None


class MainPdf(AbstractPdf):
    pass


class InnerPdf(AbstractPdf):
    pattern = None
    start = None

    def __init__(self, *, name: str = None, path: str = None, pattern: str = None):
        self.name = name
        self.path = path
        self.pattern = pattern


class NumberingOptions():
    fontName = 'Helvetica'
    fontSize = 10
    x = 200
    y = 20
    # @todo: format -> #page#, #total#, normal text, ... ?


class SwapRequest():
    main_pdf = None
    inner_pdfs = []
    with_annexes_pages_numbered = False
    options = None

    def __init__(self):
        self.main_pdf = MainPdf()
        self.inner_pdfs = []
        self.options = NumberingOptions()
        self.with_annexes_pages_numbered = False
