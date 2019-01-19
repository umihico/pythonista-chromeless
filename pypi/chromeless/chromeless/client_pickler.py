import types
import marshal
import pickle
import base64


def dump_code(func, arg, kwargs):
    byte_func = marshal.dumps(func.__code__)
    funcname = func.__name__
    pickled_data = pickle.dumps((funcname, byte_func, arg, kwargs))
    base64str_data = base64.b64encode(pickled_data).decode()
    return base64str_data


def test():
    def _load_code(base64str_data):
        b = base64.b64decode(base64str_data.encode())
        funcname, marshaled_code, arg, kwargs = pickle.loads(b)
        code = marshal.loads(marshaled_code)
        func = types.FunctionType(code, globals(), funcname)
        return func, arg, kwargs

    def method(i):
        return i*10
    funcdata = dump_code(method, (10,), {})
    reborn_func, arg, kwargs = _load_code(funcdata)
    print(reborn_func(*arg, **kwargs))


def unpickle_result(base64str_data):
    try:
        return pickle.loads(base64.b64decode(base64str_data.encode()))
    except Exception as e:
        print(base64str_data)
        raise


if __name__ == '__main__':
    test()
