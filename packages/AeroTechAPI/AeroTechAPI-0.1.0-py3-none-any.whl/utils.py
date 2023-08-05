from collections.abc import Iterable


def is_container(arg):
    '''Returns True if argument is an iterable but not a string, else False'''
    return isinstance(arg, Iterable) and not isinstance(arg, str)

def str_to_num(string):
    '''
    This function checks wether a string should be converted to int
    or to float.
    Returns either an int, a float or the original string, depending on
    which conversion is possible.
    '''
    try:
        result = float(string.replace(',', '.'))
        if result.is_integer():
            result = int(string.replace(',', '.'))
    except ValueError:
        result = string
    return result

def accept_strings(f):
    '''
    Decorator function that makes functions accept numerical values 
    as strings and converts them to float or int
    '''
    def wrapper(self, *args, **kwargs):
        _temp = []
        for arg in args:
            if isinstance(arg, str):
                if '.' in arg:
                    _temp.append(int(float(arg)))
                else:
                    _temp.append(int(arg))
            elif isinstance(arg, float):
                _temp.append(float)
            elif isinstance(arg, int):
                _temp.append(arg)
            else:
                raise ValueError  
        args = tuple(_temp)
        return f(self, *args, **kwargs)
    return wrapper

    