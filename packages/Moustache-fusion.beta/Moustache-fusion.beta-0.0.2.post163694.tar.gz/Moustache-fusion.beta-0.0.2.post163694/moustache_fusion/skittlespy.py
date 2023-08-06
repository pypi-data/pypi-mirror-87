# -*- coding: utf-8 -*-

import subprocess
from PyPDF2 import PdfFileWriter, PdfFileReader
import copy
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from itertools import count, product
from string import ascii_uppercase
import tempfile

from moustache_fusion.logger import logger
from moustache_fusion.datatransfer import SwapRequest
from moustache_fusion.exceptions import InvalidUsage, CommandException
from moustache_fusion.utilities import get_pdf_page_count, get_pdf_pattern_pages, PATHS


# alphabet de lettre (A,B, ..., AB, AC)
def multiletters(seq):
    for n in count(1):
        for s in product(seq, repeat=n):
            yield ''.join(s)


letter = multiletters(ascii_uppercase)


def set_inner_pdfs_page_count(swap_request: SwapRequest):
    """
    Read page count for every annexe file.
    """
    logger().debug('Reading page count for every inner PDF document...')

    for pdf in swap_request.inner_pdfs:
        try:
            pdf.length = get_pdf_page_count(pdf.path)
        except CommandException as exc:
            exc.message = '%s for annexe "%s"' % (exc.message, pdf.name)
            raise exc

    logger().debug('...reading page count for every inner PDF document done')


# TODO test if not null
def set_annexe_pattern_pages(swap_request: SwapRequest):
    """
    Try to find all pages mentioning the patterns.
    """
    logger().debug('Searching for patterns in main document "%s" ...' % swap_request.main_pdf.path)

    new_annexes = []
    for pdf in swap_request.inner_pdfs:
        #  @todo: make test with multiple replacements, cleanup code / replace with get_pdf_pattern_pages
        logger().debug('...searching for pattern "%s" ...' % pdf.pattern)

        pages = get_pdf_pattern_pages(swap_request.main_pdf.path, pdf.pattern)
        if len(pages) == 0:
            # @todo: custom exception
            msgstr = 'Pattern "%s" not found in main document %s'
            raise RuntimeError(msgstr % (pdf.pattern, swap_request.main_pdf.path))

        for page in pages:
            new_pdf = copy.deepcopy(pdf)
            new_pdf.alias = next(letter)
            new_pdf.start = page
            new_annexes.append(new_pdf)

    logger().debug('...searching for patterns in main document "%s" done' % swap_request.main_pdf.path)
    swap_request.inner_pdfs = new_annexes


# create and execute script to replace annexes
# cmd = "/usr/bin/pdftk A=main.pdf B=annexe.pdf cat A1-10 B A12-end output generated.pdf"
# TODO test if not null
def replace_annexes(swap_request: SwapRequest, temp_directory):
    # generate aliases (/usr/bin/pdftk A=main.pdf B=annexe.pdf)
    # Sort inner PDF documents by position
    swap_request.inner_pdfs.sort(key=lambda pdf: pdf.start)

    swap_request.main_pdf.alias = next(letter)
    cmd = "{0} {1}={2} ".format(PATHS['pdftk'], swap_request.main_pdf.alias, swap_request.main_pdf.path)

    for pdf in swap_request.inner_pdfs:
        pdf.alias = next(letter)
        # cmd += pdf.alias + "=" + annex['path'] + " "
        cmd += "{0}={1} ".format(pdf.alias, pdf.path)

    # (cat A1-10 B A12-end output generated.pdf)
    cmd += "cat "
    general_doc_position = 1
    general_doc_pages = get_pdf_page_count(swap_request.main_pdf.path)

    for pdf in swap_request.inner_pdfs:
        if general_doc_position <= pdf.start - 1:
            cmd += "{0}{1}-{2} {3} ".format(
                swap_request.main_pdf.alias,
                general_doc_position,
                pdf.start - 1,
                pdf.alias
            )
        else:
            cmd += "{0} ".format(pdf.alias)

        general_doc_position = pdf.start + pdf.length

    # Check if there are remaining pages from the main PDF document
    if general_doc_position < general_doc_pages:
        cmd += "{0}{1}-end".format(swap_request.main_pdf.alias, general_doc_position)

    output_file = tempfile.NamedTemporaryFile(dir=temp_directory, delete=False, suffix='.pdf').name
    cmd += " output {0}".format(output_file)

    logger().debug(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout_content, stderr_content = process.communicate()
    if process.returncode != 0:
        raise CommandException(
            'Error while replacing inner PDF documents in main PDF document',
            command=cmd,
            returncode=process.returncode,
            stdout=stdout_content,
            stderr=stderr_content
        )

    return output_file


def add_inner_pdfs_page_numbers(swap_request, temp_directory):
    logger().debug('Adding page numbers to inner PDF files...')

    for inner_pdf in swap_request.inner_pdfs:
        logger().debug(
            '...adding page numbers to inner PDF file "%s" (alias "%s")...' % (inner_pdf.name, inner_pdf.alias))

        try:
            original_file = PdfFileReader(open(inner_pdf.path, 'rb'))
        except Exception as exc:
            msgstr = 'Error while opening inner PDF "%s" (%s)'
            raise RuntimeError(msgstr % (inner_pdf.name, exc))

        output = PdfFileWriter()
        start = inner_pdf.start
        end = start + inner_pdf.length
        increment = 0
        while start < end:
            packet = io.BytesIO()
            # @todo: get real page size / orientation
            le_can = canvas.Canvas(packet, pagesize=A4)
            le_can.setFont(swap_request.options.fontName, swap_request.options.fontSize)
            le_can.drawString(swap_request.options.pos_x, swap_request.options.pos_y, "{0}".format(start))
            le_can.save()

            # move to the beginning of the buffer
            packet.seek(0)
            new_pdf = PdfFileReader(packet)

            logger().debug("%s cur=%d [%d-%d]" % (inner_pdf.path, increment, start, end))
            page = original_file.getPage(increment)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
            increment += 1
            start += 1

        # finally, write "output" to a real file
        result_path = tempfile.NamedTemporaryFile(delete=False, dir=temp_directory, suffix='.pdf').name
        output_stream = open(result_path, 'wb')
        output.write(output_stream)
        output_stream.close()
        logger().debug("%s to %s" % (inner_pdf.path, result_path))
        inner_pdf.path = result_path

    logger().debug('...done adding page numbers to inner PDF files')


def check_patterns(swap_request: SwapRequest) -> None:
    """
    Check that all patterns are unique or raise an exception.
    @todo: merge with checks done in WS (MIME, non-corrupted PDF, ...)
    """
    found = {}
    logger().debug('%s' % swap_request.inner_pdfs)
    for pdf in swap_request.inner_pdfs:
        if pdf.pattern in found:
            msgstr = 'Non unique pattern "%s" found for file "%s" (already found for file "%s")'
            raise InvalidUsage(msgstr % (pdf.pattern, pdf.name, found[pdf.pattern]))
        found[pdf.pattern] = pdf.name


def swap(swap_request: SwapRequest, temp_directory: str) -> str:
    logger().debug('skittles starts')

    # @todo: in WS
    check_patterns(swap_request)

    set_inner_pdfs_page_count(swap_request)
    set_annexe_pattern_pages(swap_request)

    if swap_request.with_annexes_pages_numbered:
        add_inner_pdfs_page_numbers(swap_request, temp_directory)
    else:
        logger().debug('No page number to add')

    output_file = replace_annexes(swap_request, temp_directory)
    logger().debug('file created: %s' % output_file)
    return output_file


def get_available_fonts() -> list:
    """
    Returns a list of all available fonts to use when inserting page numbers.
    """
    from reportlab.pdfbase import pdfmetrics
    result = []
    for font_name in pdfmetrics.standardFonts:
        result.append(font_name)
    return result
