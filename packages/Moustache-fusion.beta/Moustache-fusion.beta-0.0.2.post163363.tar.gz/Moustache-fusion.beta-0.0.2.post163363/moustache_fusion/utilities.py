# -*- coding: utf-8 -*-

import magic
import subprocess

from moustache_fusion.exceptions import CommandException

# Paths for all utilities that will be needed in the service.
PATHS = {
    'pdfgrep': '/usr/bin/pdfgrep',
    'pdfinfo': '/usr/bin/pdfinfo',
    'pdftk': '/usr/bin/pdftk',
    'pdftotext': '/usr/bin/pdftotext'
}


def uc_only_first(string: str) -> str:
    """
    Uppercase the first letter of the string while leaving the other letters unchanged.
    """
    if len(string) > 0:
        if len(string) == 1:
            string = string.upper()
        elif len(string) > 1:
            string = string[0].upper() + string[1:]
    return string


def validate_pdf(path: str, alias: str):
    """
    Assert the file is a PDF and is not corrupted (using pdftotext) or raise a RuntimeError.
    """
    # 1. Check MIME type
    mime = magic.from_file(path, mime=True)
    if mime != 'application/pdf':
        msgstr = '%s MIME type is not "application/pdf" (found "%s" MIME type for "%s")'
        raise RuntimeError(msgstr % (alias, mime, path))

    xpdf_tools_error_codes = {
        0: 'No error',
        1: 'Error opening a PDF file',
        2: 'Error opening an output file',
        3: 'Error related to PDF permissions',
        99: 'Other error'
    }

    # 2. Check for a possible corrupted PDF
    cmd = '{0} {1} /dev/null'.format(PATHS['pdftotext'], path)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout_content, stderr_content = process.communicate()

    if process.returncode == 0 and stderr_content != '':
        msgstr = '%s seems to be corrupted (using command %s)'
        raise RuntimeError(msgstr % (uc_only_first(alias), cmd))
    elif process.returncode != 0 and process.returncode in xpdf_tools_error_codes:
        msgstr = 'Received error code %d (%s) while validating %s (using command %s)'
        raise RuntimeError(msgstr % (process.returncode, xpdf_tools_error_codes[process.returncode], alias, cmd))
    elif process.returncode != 0:
        msgstr = 'Received error code %d (unknown error) while validating %s (using command %s)'
        raise RuntimeError(msgstr % (process.returncode, xpdf_tools_error_codes[process.returncode], alias, cmd))


def get_pdf_page_count(path: str) -> int:
    """
    Returns the number of pages of a PDF document or raises a CommandException.
    """
    process = subprocess.run([PATHS['pdfinfo'], path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode != 0:
        raise CommandException(
            'Error trying to get page count',
            command='%s %s' % (PATHS['pdfinfo'], path),
            returncode=process.returncode,
            stdout=process.stdout.decode('utf-8'),
            stderr=process.stderr.decode('utf-8')
        )

    lines = process.stdout.decode('utf-8').split()
    try:
        pageinfo = lines.index('Pages:')
    except ValueError:
        raise CommandException(
            'Could not find "Pages:" in output',
            command='%s %s' % (PATHS['pdfinfo'], path),
            returncode=process.returncode,
            stdout=process.stdout.decode('utf-8'),
            stderr=process.stderr.decode('utf-8')
        )

    line = lines[pageinfo + 1]
    if not line.isdigit():
        raise CommandException(
            'Could not find integer page count from output',
            command='%s %s' % (PATHS['pdfinfo'], path),
            returncode=process.returncode,
            stdout=process.stdout.decode('utf-8'),
            stderr=process.stderr.decode('utf-8')
        )

    return int(line)


def get_pdf_pattern_pages(path: str, pattern: str) -> list:
    result = []

    cmd = '{0} --cache --color never --page-number "{1}" {2}'.format(PATHS['pdfgrep'], pattern, path)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout_content, stderr_content = process.communicate()

    if process.returncode == 0:
        stdout_content = stdout_content.split()
        for line in stdout_content:
            value = line.split(':')[0]
            if not value.isdigit():
                msgstr = 'Could not read start page'
                raise RuntimeError(msgstr)
            result.append(int(value))
    elif process.returncode != 1:
        raise CommandException(
            'Error trying to get pages with pattern "%s"' % pattern,
            command='%s %s' % (PATHS['pdfinfo'], path),
            returncode=process.returncode,
            stdout=process.stdout.decode('utf-8'),
            stderr=process.stderr.decode('utf-8')
        )

    return result
