import inspect

from typing import Callable


def get_filter_body(lambda_: Callable) -> str:
    """
    Returns body of lambda for filter representation
    :param lambda_: Callable
    :return: body if lambda found, else empty string
    """
    if 'lambda' not in str(lambda_):
        return ''
    _, __, text = inspect.getsource(lambda_).partition('lambda')
    text = text.split(':')[1].lstrip().rstrip()
    count = 0
    result = []
    for char in text:
        if char == '(':
            count += 1
        if char == ')':
            count -= 1
        if count < 0:
            break
        result.append(char)
    return ''.join(result)
