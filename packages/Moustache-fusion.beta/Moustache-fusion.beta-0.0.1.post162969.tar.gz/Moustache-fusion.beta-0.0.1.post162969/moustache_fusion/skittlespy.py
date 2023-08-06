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
from moustache_fusion.exceptions import InvalidUsage

PDFTK_PATH = '/usr/bin/pdftk'
PDFINFO_PATH = '/usr/bin/pdfinfo'
PDFGREP_PATH = '/usr/bin/pdfgrep'


# alphabet de lettre (A,B, ..., AB, AC)
def multiletters(seq):
    for n in count(1):
        for s in product(seq, repeat=n):
            yield ''.join(s)


letter = multiletters(ascii_uppercase)


def set_annexes_length(annexes):
    for annexe in annexes:
        logger().debug("exec %s %s" % (PDFINFO_PATH, annexe['path']))
        output = subprocess.run([PDFINFO_PATH, annexe['path']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if output.returncode:
            raise Exception(output.stderr.decode('utf-8'))
        output_array = output.stdout.decode('utf-8').split()
        pageinfo = output_array.index("Pages:")
        v = output_array[pageinfo + 1]
        if not v.isdigit():
            raise Exception("Impossible de lire le nombre de pages dans %s:%s" % (annexe['path'], v))
        annexe['length'] = int(v)
        logger().debug("%s pages:%d" % (annexe['path'], annexe['length']))


# find only one + cache file speed +++
# pdfgrep -n --cache "challenge" principal.pdf
# find pattern page
# TODO test if not null
def set_annexe_pattern_pages(annexes, document_path):
    new_annexes = []
    for annex in annexes:
        # ubuntu 16.04 ships with pdfgrep 1.4 which does not support '--cache' parameter
        # cmd = '{0} -n --cache "{1}" {2}'.format(PDFGREP_PATH, annex['pattern'], documentPath)
        cmd = '{0} -n --cache "{1}" {2}'.format(PDFGREP_PATH, annex['pattern'], document_path)
        logger().debug("exec %s" % cmd)
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        outds, errs = res.communicate()
        if res.returncode:
            if not errs:
                errs = "%s retourne %d" % (PDFGREP_PATH, res.returncode)
            raise Exception(errs)

        outds = outds.split()
        for line in outds:
            v = line.split(":")[0]
            if not v.isdigit():
                raise Exception("Impossible de lire la page de départ pour %s" % annex['name'])
            annex['alias'] = next(letter)
            annex['startPage'] = int(v)
            new_annexes.append(dict(annex))
            logger().debug("%s alias=%s start page=%d" % (annex['name'], annex['alias'], annex['startPage']))
    return new_annexes


# create and execute script to replace annexes
# cmd = "/usr/bin/pdftk A=main.pdf B=annexe.pdf cat A1-10 B A12-end output generated.pdf"
# TODO test if not null
def replace_annexes(docs, outputfile):
    # generate aliases (/usr/bin/pdftk A=main.pdf B=annexe.pdf)
    # sort Annexes by position
    docs['annexes'].sort(key=lambda ann: ann['startPage'])

    docs['general']['alias'] = next(letter)
    cmd = "{0} {1}={2} ".format(PDFTK_PATH, docs['general']['alias'], docs['general']['path'])
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
    outds, errs = res.communicate()
    if res.returncode:
        raise Exception(errs)


def add_page_numbering_to_annexes(docs):
    for annexe in docs['annexes']:
        start = annexe['startPage']
        existing_pdf = PdfFileReader(open(annexe['path'], "rb"))
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
    logger().debug('************** %s' % data)
    data['annexes'] = set_annexe_pattern_pages(data['annexes'], data['general']['path'])
    logger().debug('************** %s' % data)

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
