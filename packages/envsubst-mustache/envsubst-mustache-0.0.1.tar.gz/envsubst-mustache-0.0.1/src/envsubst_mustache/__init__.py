from sys import stdin, stdout
from os import environ
from os import _Environ
from json import loads as json_parse
from json import JSONDecodeError
from chevron import render as render_mustache


def environ_parse(env: _Environ = environ) -> dict:
    """
    parse environment variables as JSON (if we can) and return a dictionary of the environment variables
    """

    _return = {}

    for var in env:
        try:
            _return[var] = json_parse(env[var])
        except JSONDecodeError:
            _return[var] = str(env[var])

    return _return

def main():
    stdout.write(render_mustache(''.join(stdin), environ_parse()))
