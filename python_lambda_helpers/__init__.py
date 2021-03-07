"""Top-level package for Python Lambda Helpers."""

__author__ = """Carlos Vences"""
__email__ = 'sales@semantic.mx'
__version__ = '1.0.0'


def execution_error(msg: str = '') -> dict:
    if not msg:
        msg = 'Bad Request'

    return {
        'headers': {'Content-type': 'text/html'},
        'statusCode': 400,
        'body': msg,
    }
