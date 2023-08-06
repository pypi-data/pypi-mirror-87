# -*- coding: utf-8 -*-

import subprocess
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from itertools import count, product
from string import ascii_uppercase
import tempfile

from moustache_fusion.logger import logger
from moustache_fusion.exceptions import InvalidUsage, CommandException
from moustache_fusion.utilities import get_pdf_page_count, get_pdf_pattern_pages, PATHS


# alphabet de lettre (A,B, ..., AB, AC)
def multiletters(seq):
    for n in count(1):
        for s in product(seq, repeat=n):
            yield ''.join(s)


letter = multiletters(ascii_uppercase)


def set_annexes_length(annexes):
    """
    Read page count for every annexe file.
    """
    logger().debug('Reading page count for every annexe file...')

    for annexe in annexes:
        try:
            annexe['length'] = get_pdf_page_count(annexe['path'])
        except CommandException as exc:
            exc.message = '%s for annexe "%s"' % (exc.message, annexe['name'])
            raise exc

    logger().debug('...reading page count for every annexe file done')

# TODO test if not null
def set_annexe_pattern_pages(annexes, document_path):
    """
    Try to find all pages mentioning the patterns.
    Cache is used because a pattern can be used multiple times (pdfgrep 2.0+).
    """
    logger().debug('Searching for patterns in main document "%s" ...' % document_path)

    new_annexes = []
    for annex in annexes:
        # @todo: make test with multiple replacements, cleanup code / replace with get_pdf_pattern_pages
        #logger().debug({annex['pattern']: get_pdf_pattern_pages(document_path, annex['pattern'])})
        # --------------------------------------------------------------------------------------------------------------
        logger().debug('...searching for pattern "%s" ...' % annex['pattern'])

        cmd = '{0} --cache --color never --page-number "{1}" {2}'.format(PATHS['pdfgrep'], annex['pattern'],
                                                                         document_path)
        logger().debug("exec %s" % cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
        stdout_content, stderr_content = process.communicate()
        if process.returncode == 1:
            msgstr = 'Pattern "%s" not found in main document %s'
            raise RuntimeError(msgstr % (annex['pattern'], document_path))
        elif process.returncode != 0:
            if not stderr_content:
                msgstr = 'Error code %d returned while searching for pattern "%s" in main document %s'
                stderr_content = msgstr % (process.returncode, annex['pattern'], cmd)
            raise RuntimeError(stderr_content)

        stdout_content = stdout_content.split()
        for line in stdout_content:
            v = line.split(":")[0]
            if not v.isdigit():
                msgstr = 'Could not read start page for annexe "%s" using command %s (output was: %s)'
                raise RuntimeError(msgstr % (annex['name'], cmd, line))
            annex['alias'] = next(letter)
            annex['startPage'] = int(v)
            new_annexes.append(dict(annex))
            logger().debug("%s alias=%s start page=%d" % (annex['name'], annex['alias'], annex['startPage']))

    logger().debug('...searching for patterns in main document "%s" done' % document_path)
    logger().debug(new_annexes)
    return new_annexes


# create and execute script to replace annexes
# cmd = "/usr/bin/pdftk A=main.pdf B=annexe.pdf cat A1-10 B A12-end output generated.pdf"
# TODO test if not null
def replace_annexes(docs, outputfile):
    # generate aliases (/usr/bin/pdftk A=main.pdf B=annexe.pdf)
    # sort Annexes by position
    docs['annexes'].sort(key=lambda ann: ann['startPage'])

    docs['general']['alias'] = next(letter)
    cmd = "{0} {1}={2} ".format(PATHS['pdftk'], docs['general']['alias'], docs['general']['path'])
    logger().debug(docs)
    for annex in docs['annexes']:
        annex['alias'] = next(letter)
        # cmd += annex['alias'] + "=" + annex['path'] + " "
        cmd += "{0}={1} ".format(annex['alias'], annex['path'])

    # (cat A1-10 B A12-end output generated.pdf)
    cmd += "cat "
    general_doc_position = 1

    for annex in docs['annexes']:
        if general_doc_position <= annex['startPage'] - 1:
            cmd += "{0}{1}-{2} {3} ".format(
                docs['general']['alias'],
                general_doc_position,
                annex['startPage'] - 1,
                annex['alias']
            )
        else:
            cmd += "{0} ".format(annex['alias'])

        general_doc_position = annex['startPage'] + annex['length']

    cmd += "{0}{1}-end output {2}".format(docs['general']['alias'], general_doc_position, outputfile)

    logger().debug(cmd)
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout_content, stderr_content = res.communicate()
    if res.returncode != 0:
        msgstr = 'Error while replacing annexes using command %s (error code %d, output was: %s)'
        raise RuntimeError(msgstr % (cmd, res.returncode, stderr_content))


def add_page_numbering_to_annexes(docs):
    for annexe in docs['annexes']:
        start = annexe['startPage']
        try:
            existing_pdf = PdfFileReader(open(annexe['path'], "rb"))
        except Exception as exc:
            msgstr = 'Error while opening annexe "%s" (%s)'
            raise RuntimeError(msgstr % (annexe['name'], exc))
        output = PdfFileWriter()
        end = start + annexe['length']
        increment = 0
        while start < end:
            packet = io.BytesIO()
            # @todo: parameters
            le_can = canvas.Canvas(packet, pagesize=A4)
            le_can.setFont('Helvetica', 10)
            le_can.drawString(200, 20, "{0}".format(start))
            le_can.save()

            # move to the beginning of the buffer
            packet.seek(0)
            new_pdf = PdfFileReader(packet)

            logger().debug("%s cur=%d [%d-%d]" % (annexe['path'], increment, start, end))
            page = existing_pdf.getPage(increment)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
            increment += 1
            start += 1

        # finally, write "output" to a real file
        new_annexe_name = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False).name
        output_stream = open(new_annexe_name, 'wb')
        output.write(output_stream)
        output_stream.close()
        logger().debug("%s to %s" % (annexe['path'], new_annexe_name))
        annexe['path'] = new_annexe_name


def check_patterns(data: dict) -> None:
    """
    Check that all patterns are unique or raise an exception.
    """
    found = {}
    for pdf in data['annexes']:
        if pdf['pattern'] in found:
            msgstr = 'Non unique pattern "%s" found for file "%s" (already found for file "%s")'
            raise InvalidUsage(msgstr % (pdf['pattern'], pdf['name'], found[pdf['pattern']]))
        found[pdf['pattern']] = pdf['name']


# @todo: temp_dir parameter, return file path
def skittles(data: dict, outputfile: str) -> None:
    logger().debug("skittles starts")

    check_patterns(data)

    set_annexes_length(data['annexes'])
    # logger().debug('************** %s' % data)
    data['annexes'] = set_annexe_pattern_pages(data['annexes'], data['general']['path'])
    # logger().debug('************** %s' % data)

    try:
        with_page_numbering = data["options"]["with_annexes_pages_numbered"]
    except KeyError:
        with_page_numbering = False

    if with_page_numbering:
        add_page_numbering_to_annexes(data)
    else:
        logger().debug("skip add_page_numbering_to_annexes")
    replace_annexes(data, outputfile)

    logger().debug("file created: %s" % outputfile)
