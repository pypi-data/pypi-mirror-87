#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pathlib
import tempfile
import os
import getopt
import sys
import shutil
import logging

from flask import Flask, request, send_file, jsonify, render_template
from io import StringIO
from logging.config import fileConfig
from werkzeug.exceptions import InternalServerError

from moustache_fusion import skittlespy
from moustache_fusion.datatransfer import SwapRequest, InnerPdf
from moustache_fusion.exceptions import CommandException, InvalidUsage
from moustache_fusion.logger import logger
from moustache_fusion.utilities import PATHS, validate_pdf

logger().configure('/app/config/logging_config.json')


class API:
    class V1:
        class PDF:
            class SWAP:
                ANNEXES = 'annexe'
                DEFAULTS = {
                    'font_name': 'Helvetica',
                    'font_size': 10,
                    'pos_x': 200,
                    'pos_y': 20
                }
                FILE = 'principal'

                class FONT:
                    NAME = 'font_name'
                    SIZE = 'font_size'
                    POS_X = 'pos_x'
                    POS_Y = 'pos_y'

                JSON = 'params'
                #  @todo: /api/v1/pdf/swap
                URL = '/api'


#  @todo: report enhancements in moustache
#  @todo: "mandatory" kwarg for both functions (default True)


class FileRetriever():
    """
    This static class provides static utility methods to retrieve files from the flask (werkzeug) HTTP request by key.
    """

    @classmethod
    def _dest_file(cls, filename: str, dest_directory: str, *, temp_name: bool = False):
        if temp_name is False:
            dest_file = os.path.join(dest_directory, filename)
        else:
            suffix = ''.join(pathlib.Path(filename).suffixes)
            dest_file = tempfile.NamedTemporaryFile(dir=dest_directory, delete=False, suffix=suffix).name
        return dest_file

    @classmethod
    def retrieve_single(cls, key: str, dest_directory: str, *, temp_name: bool = False):
        """
        Retrieves a single (mandatory) file from the request by key and stores it in the destination directory,
        returning the complete path to the saved file.
        """
        if key not in request.files:
            raise InvalidUsage("\"%s\" key is not in request files (%s)" % (key, request.files))

        file = request.files[key]
        if file.filename.strip() == '':
            raise InvalidUsage("\"%s\" key has an empty filename in request files (%s)" % (key, request.files))

        dest_file = cls._dest_file(file.filename, dest_directory, temp_name=temp_name)

        logger().debug("Retrieving \"%s\" file \"%s\" to \"%s\"" % (key, file.filename, dest_file))
        file.save(dest_file)
        return dest_file

    @classmethod
    def retrieve_multiple(cls, key: str, dest_directory: str, *, temp_name: bool = False):
        """
        Retrieves a (possibly empty) list of files from the request by key (possibly non-existent) and stores them in
        the destination directory, returning a dict with original filenames as key and complete path to the saved file
        as value.
        """
        filelist = request.files.getlist(key)
        file_mapping = {}
        logger().debug("Retrieving %d %s file(s)..." % (len(filelist), key))

        for index, file in enumerate(filelist):
            if file.filename.strip() == '':
                msgstr = "\"%s\"[%d] key has an empty filename in request files (%s)"
                raise InvalidUsage(msgstr % (key, index + 1, request.files))

            if file.filename in file_mapping:
                msgstr = '"%s"[%d] file name "%s" was already sent in request files (%s)'
                raise InvalidUsage(msgstr % (key, index + 1, file.filename, request.files))

            dest_file = cls._dest_file(file.filename, dest_directory, temp_name=temp_name)
            logger().debug(
                "... retrieving %s %d \"%s\" (%s) to \"%s\"" % (
                    key,
                    index + 1,
                    file.filename,
                    'None' if file.mimetype is None or file.mimetype == '' else "'" + file.mimetype + '"',
                    dest_file
                )
            )
            file.save(dest_file)
            file_mapping[file.filename] = dest_file

        return file_mapping


# Assert that all program paths we will need exist and are executable
for alias, path in PATHS.items():
    if os.path.exists(path) is False:
        print('Path for %s does not exist: %s' % (alias, path), file=sys.stderr)
        exit(1)
    if os.access(path, os.X_OK) is False:
        print('Path for %s is not executable: %s' % (alias, path), file=sys.stderr)
        exit(1)

app = Flask(__name__)
# TODO a virer ?
app.secret_key = 'super secret key'


class Form():
    def __init__(self, defaults: dict = {}):
        self.defaults = defaults

    def _get(self, key: str):
        if key in self.defaults:
            default = self.defaults[key]
        else:
            default = None

        return request.form.get(key, default=default)

    def get_int(self, key: str, *, required: bool = True, negative: bool = True, zero: bool = True):
        value = self._get(key)

        if negative is True and zero is False:
            msgstr = 'Expected non-zero integer value for field "%s" but got "%s"'
        elif negative is False and zero is False:
            msgstr = 'Expected positive non-zero integer value for field "%s" but got "%s"'
        elif negative is False and zero is True:
            msgstr = 'Expected positive integer value for field "%s" but got "%s"'
        else:
            msgstr = 'Expected integer value for field "%s" but got "%s"'

        if required is True and (value is None or str(value).strip() == ''):
            raise InvalidUsage(msgstr % (key, str(value) if value is not None else ''))

        try:
            intval = int(str(value))
            if intval == 0 and zero is False:
                raise InvalidUsage(msgstr % (key, str(intval)))
            if intval < 0 and negative is False:
                raise InvalidUsage(msgstr % (key, str(intval)))
            return intval
        except ValueError:
            msgstr = 'Expected integer value for field "%s" but got "%s"'
            raise InvalidUsage(msgstr % (key, str(value)))

    def get_value_from_list(self, key: str, accepted: list, *, required: bool = True):
        value = self._get(key)

        if required is True and (value is None or str(value).strip() == '') or value not in accepted:
            msgstr = 'Unexpected value "%s" for field "%s"'
            raise InvalidUsage(
                msgstr % (str(value) if value is not None else '', key),
                400,
                {'accepted': accepted}
            )

        return value


def setlogger(conffile):
    if not os.path.isfile(conffile):
        logging.getLogger().error("Can't access %s" % conffile)
        sys.exit(1)

    fileConfig(conffile)
    logger = logging.getLogger()
    logger.debug("Using %s for logging config file" % conffile)
    logger().handlers = logger.handlers


@app.errorhandler(CommandException)
def handle_command_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = 500
    logger().debug('... API: command exception, aborting request (%s)' % (error.message))
    return response


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    logger().debug('... API: invalid usage, aborting request (%s)' % (error.message))
    return response


@app.errorhandler(InternalServerError)
def handle_internal_server_error(error):
    response = jsonify({'message': error.description})
    response.status_code = error.code
    logger().debug('... API: internal server error, aborting request (%s)' % error.description)
    return response


@app.route('/')
def www_v1_index():
    logger().debug('WWW: rendering HTML template')
    fonts = skittlespy.get_available_fonts()
    return render_template('index.html', API=API.V1, fonts=fonts)


# @todo: Check if json is compliant
@app.route(API.V1.PDF.SWAP.URL, methods=['POST'])
def api_v1_pdf_swap():
    logger().debug('API: starting swap...')

    swap_request = None
    temp_directory = None

    try:
        swap_request = SwapRequest()
        temp_directory = tempfile.mkdtemp()

        # @todo: add json/json_stream to FileRetriver
        if API.V1.PDF.SWAP.JSON not in request.files:
            raise InvalidUsage('JSON file with replacements for field "%s" was not provided' % API.V1.PDF.SWAP.JSON)

        try:
            j = request.files[API.V1.PDF.SWAP.JSON]
            json_content = j.stream.read()
            data = json.load(StringIO(json_content.decode('utf-8')))
        except json.JSONDecodeError:
            raise InvalidUsage('Invalid JSON provided for field "%s"' % API.V1.PDF.SWAP.JSON)
        logger().debug("... retrieved JSON data %s" % (data))

        #  @todo: with_annexes_pages_numbered should come from the "form"
        swap_request.main_pdf.path = FileRetriever.retrieve_single(API.V1.PDF.SWAP.FILE, temp_directory, temp_name=True)
        try:
            alias = '"%s" PDF document "%s"' % (API.V1.PDF.SWAP.FILE, request.files[API.V1.PDF.SWAP.FILE].filename)
            validate_pdf(swap_request.main_pdf.path, alias)
        except RuntimeError as exc:
            raise InvalidUsage(str(exc))

        annexes_filelist = FileRetriever.retrieve_multiple(API.V1.PDF.SWAP.ANNEXES, temp_directory, temp_name=True)
        # @todo deal with extra files in annexes_filelist ?
        # @todo pb si nom de fichier non unique ?
        for annexe in data['annexes']:
            if annexe['name'] in annexes_filelist:
                pdf = InnerPdf(name=annexe['name'], path=annexes_filelist[annexe['name']], pattern=annexe['pattern'])
                swap_request.inner_pdfs.append(pdf)

                try:
                    alias = '"%s" PDF document "%s"' % (API.V1.PDF.SWAP.ANNEXES, pdf.name)
                    validate_pdf(pdf.path, alias)
                except RuntimeError as exc:
                    raise InvalidUsage(str(exc))
            else:
                msgstr = 'File name "%s" present in "%s" JSON data but not in "%s" files'
                raise InvalidUsage(msgstr % (annexe['name'], API.V1.PDF.SWAP.JSON, API.V1.PDF.SWAP.ANNEXES))

        try:
            swap_request.with_annexes_pages_numbered = data['options']['with_annexes_pages_numbered']
        except KeyError:
            pass

        # Validation
        form = Form(API.V1.PDF.SWAP.DEFAULTS)
        swap_request.options.fontName = form.get_value_from_list(
            API.V1.PDF.SWAP.FONT.NAME,
            skittlespy.get_available_fonts()
        )
        swap_request.options.fontSize = form.get_int(API.V1.PDF.SWAP.FONT.SIZE, negative=False, zero=False)
        swap_request.options.pos_x = form.get_int(API.V1.PDF.SWAP.FONT.POS_X, negative=False)
        swap_request.options.pos_y = form.get_int(API.V1.PDF.SWAP.FONT.POS_Y, negative=False)

        output_file = skittlespy.swap(swap_request, temp_directory)
        result = send_file(output_file, attachment_filename='result.pdf', as_attachment=True)
    except CommandException:
        raise
    except InvalidUsage:
        raise
    except RuntimeError as exc:
        raise InternalServerError(description=str(exc))
    except Exception as exc:
        logger().exception(exc)
        raise InternalServerError(str(exc), 500, exc)
    finally:
        if temp_directory is not None:
            shutil.rmtree(temp_directory)
        del swap_request

    logger().debug('API: ...swap succeeded')
    return result


def default_app():
    return app


def usage():
    print("usage :")
    print("-p --port=port\tport d'écoute")
    print("-d --debug\t\tactive les traces sur stderr")
    print("-l --logger=loggerfile\t\tfichier de configuration du logger")


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:dl:", ["help", "port=", "debug", "logger="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(1)

    portparam = None
    debugparam = False
    loggerparam = None

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-p", "--port"):
            portparam = int(a)
        elif o in ("-d", "--debug"):
            debugparam = True
        elif o in ("-l", "--logger"):
            loggerparam = a
        else:
            print("unhandled option")
            usage()
            sys.exit(1)

    if loggerparam:
        setlogger(loggerparam)

    app.run(debug=debugparam, host='0.0.0.0', port=portparam, threaded=True)
