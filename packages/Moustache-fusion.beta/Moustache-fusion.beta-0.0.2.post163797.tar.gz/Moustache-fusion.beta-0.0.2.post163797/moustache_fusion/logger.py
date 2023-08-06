# -*- coding: utf-8 -*-

import json
import logging.config
import re


class RelpathFilter(logging.Filter):
    """
    This filter adds a relpath contextual information to logging records.

    The relative path is computed with respect to the regular expressions given
    to the constructor (replaced with a blank string).
    """

    def __init__(self, regexps=None):
        """
        """
        if regexps is None:
            regexps = []
        self.regexps = regexps

    def filter(self, record):
        """
        """
        record.relpath = record.pathname
        for regexp in self.regexps:
            record.relpath = re.sub(regexp, "", record.relpath)

        return True


class RelsourceFilter(RelpathFilter):
    """
    This filter adds a relsource (relpath:lineno) contextual information to
    logging records.

    The relative path is computed with respect to the regular expressions given
    to the constructor (replaced with a blank string).
    """

    def __init__(self, regexps=None):
        """
        """
        super().__init__(regexps)

    def filter(self, record):
        """
        """
        result = super().filter(record)
        record.relsource = record.relpath + ":" + str(record.lineno)

        return result


class logger(object):
    """
    """

    @staticmethod
    def configure(filename):
        """
        """
        with open(filename) as f:
            config = json.load(f)
            logging.config.dictConfig(config)

        logger = logging.getLogger("moustache_fusion")
        logger.debug("Using logging config file \"%s\"" % filename)

    @staticmethod
    def __getattr__(name):
        """
        """
        return getattr(logging.getLogger("moustache"), name)
