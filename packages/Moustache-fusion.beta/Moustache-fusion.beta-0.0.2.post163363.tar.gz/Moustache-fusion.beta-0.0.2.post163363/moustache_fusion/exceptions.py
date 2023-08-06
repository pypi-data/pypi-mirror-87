# -*- coding: utf-8 -*-

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class CommandException(Exception):
    """
    Exception to raise when a command returns a non-zero code.
    """
    def __init__(self, message: str, *, command: str, returncode: int, stderr: str, stdout: str):
        Exception.__init__(self, message)
        self.message = message
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = stdout

    def to_dict(self):
        rv = {}
        rv['message'] = self.message
        rv['command'] = self.command
        rv['returncode'] = self.returncode
        rv['stdout'] = self.stdout
        rv['stderr'] = self.stderr
        return rv
