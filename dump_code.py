import types
import marshal
import pickle
from awslambda import load_code


def dump_code(func, arg, kwargs):
    byte_func = marshal.dumps(func.__code__)
    funcname = func.__name__
    pickled_data = pickle.dumps((funcname, byte_func, arg, kwargs))
    hex_pickled_data = ''.join([str("%X" % i).zfill(2) for i in pickled_data])
    hex_encoded_pickled_data = hex_pickled_data.encode()
    return hex_encoded_pickled_data


def test():
    def method(i):
        return i+100
    funcdata = dump_code(func=method)
    print(funcdata)
    print(type(funcdata))
    reborn_func = load_code(funcdata)
    print(reborn_func(10))


if __name__ == '__main__':
    test()
