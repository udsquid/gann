"""
This module provides methods to help complete the command in command
interpreters like 'cmd'.

Callee need to transform its usage first:

form:
    Usage:
        index product <symbol>
        index range (start | end) <date> [<time>]
        index range reset
        index status
        index (search | searchf) <operator> <value>
            [((and | or) <operator> <value>)]

to:
    return [['index', 'product', '<symbol>'],
            ['index', 'range', ['start', 'end'], '<date>', '[<time>]'],
            ['index', 'range', 'reset'],
            ['index', 'status'],
            ['index', ['search', 'searchf'], '<operator>', '<value>',
                ['and', 'or'], '<operator>', '<value>'],
            ]

"""

import re

def match_command(form, text, line, level=1):
    _input = line.split()
    if len(form) < len(_input):
        return None
    if len(_input) == 1:
        return form[level]

    if level+1 >= len(_input):
        if text:
            return complete_token(form[level], text)
        else:
            if not match_token(form[level], _input[level]):
                return None
            if level+1 >= len(form):
                return None
            return form[level+1]
    else:
        if not match_token(form[level], _input[level]):
            return None
        return match_command(form, text, line, level+1)

def match_token(form_token, input_token):
    if type(form_token) == list:
        return input_token in form_token
    elif re.search('\<.+\>', form_token):
        return True
    else:
        return input_token == form_token

def complete_token(form_token, input_token):
    if type(form_token) == list:
        completion = []
        for token in form_token:
            if token.startswith(input_token):
                completion.append(token)
        return completion
    elif re.search('\<.+\>', form_token):
        return input_token
    else:
        if not form_token.startswith(input_token):
            return None
        return form_token
