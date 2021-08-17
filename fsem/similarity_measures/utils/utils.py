def check_if_none(*args):
    for arg in args:
        if arg is None:
            raise ValueError('Missing parameter')


def check_if_type(_type, *args):
    for arg in args:
        if not isinstance(arg, _type):
            raise TypeError('Wrong type of parameter')
