#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
curl -i -X POST http://localhost:5000/api \
    -F "params=@ressources/test-ok/skittles.json" \
    -F "principal=@ressources/test-ok/principal.pdf" \
    -F "annexe=@ressources/test-ok/annexe1.pdf" \
    -F "annexe=@ressources/test-ok/annexe2.pdf" > resultws.pdf
"""
import json
import magic
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
from moustache_fusion.datatransfer import SwapRequest
from moustache_fusion.exceptions import InvalidUsage
from moustache_fusion.logger import logger

logger().configure('/app/config/logging_config.json')


class API:
    class V1:
        class PDF:
            class SWAP:
                ANNEXES = 'annexe'
                FILE = 'principal'
                JSON = 'params'
                #  @todo: /api/v1/pdf/swap
                URL = '/api'


#  @todo: report enhancements in moustache
#  @todo: raise error if key already exists in retrieve_multiple
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


app = Flask(__name__)
# TODO a virer ?
app.secret_key = 'super secret key'


def setlogger(conffile):
    if not os.path.isfile(conffile):
        logging.getLogger().error("Can't access %s" % conffile)
        sys.exit(1)

    fileConfig(conffile)
    logger = logging.getLogger()
    logger.debug("Using %s for logging config file" % conffile)
    logger().handlers = logger.handlers


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
    return render_template('index.html', API=API.V1)


# @todo: Check if json is compliant
@app.route(API.V1.PDF.SWAP.URL, methods=['POST'])
def api_v1_pdf_swap():
    logger().debug('API: starting swap...')

    temp_directory = None

    try:
        swap_request = SwapRequest()
        temp_directory = tempfile.mkdtemp()

        # @todo: test with empty / unreadable JSON
        # @todo: add json/json_stream to FileRetriver
        if API.V1.PDF.SWAP.JSON not in request.files:
            raise InvalidUsage("Le fichier json de paramètres n'est pas présent")

        j = request.files['params']
        json_content = j.stream.read()
        data = json.load(StringIO(json_content.decode('utf-8')))
        logger().debug("... retrieved JSON data %s" % (data))

        #  @todo: with_annexes_pages_numbered should come from the "form"
        swap_request.main_pdf = FileRetriever.retrieve_single(API.V1.PDF.SWAP.FILE, temp_directory, temp_name=True)
        mime = magic.from_file(swap_request.main_pdf, mime=True)
        if mime != 'application/pdf':
            msgstr = 'Main PDF document "%s" MIME type is not "application/pdf" (found "%s" MIME type for "%s")'
            raise InvalidUsage(msgstr % (API.V1.PDF.SWAP.FILE, mime, request.files[API.V1.PDF.SWAP.FILE].filename))

        # @todo: DTO
        data['general'] = {}
        data['general']['path'] = swap_request.main_pdf

        annexes_filelist = FileRetriever.retrieve_multiple(API.V1.PDF.SWAP.ANNEXES, temp_directory, temp_name=True)
        # @todo deal with extra files in annexes_filelist ?
        # @todo pb si nom de fichier non unique ?
        for annexe in data['annexes']:
            if annexe['name'] in annexes_filelist:
                # @todo: annexe['path'], and keep name
                pdf = {'name': annexe['name'], 'path': annexes_filelist[annexe['name']], 'pattern': annexe['pattern']}
                swap_request.pdfs.append(pdf)

                annexe['path'] = annexes_filelist[annexe['name']]

                mime = magic.from_file(pdf['path'], mime=True)
                if mime != 'application/pdf':
                    msgstr = 'Document "%s" MIME type is not "application/pdf" (found "%s" MIME type for "%s")'
                    raise InvalidUsage(msgstr % (API.V1.PDF.SWAP.ANNEXES, mime, pdf['name']))
            else:
                msgstr = 'File name "%s" present in "%s" JSON data but not in "%s" files'
                raise InvalidUsage(msgstr % (annexe['name'], API.V1.PDF.SWAP.JSON, API.V1.PDF.SWAP.ANNEXES))

        output_file = tempfile.NamedTemporaryFile(dir=temp_directory, delete=False, suffix='.pdf').name

        #  @todo: service
        # logger().debug("============ swap_request=%s output_file=%s" % (swap_request, output_file))
        # logger().debug("============ data=%s output_file=%s" % (data, output_file))

        skittlespy.skittles(data, output_file)
        result = send_file(output_file, attachment_filename='result.pdf', as_attachment=True)
    except InvalidUsage:
        raise
    except RuntimeError as exc:
        raise InternalServerError(description=str(exc))
    except Exception as exc:
        logger().exception(exc)
        raise InternalServerError()
    finally:
        if temp_directory is not None:
            shutil.rmtree(temp_directory)

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
