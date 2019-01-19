import types
import marshal
import pickle


def load_code(hex_pickled_data):
    pickled_data = bytes([int(hex_pickled_data[i:i+2], 16)
                          for i in range(0, len(hex_pickled_data), 2)])
    funcname, marshaled_code, arg, kwargs = pickle.loads(pickled_data)
    code = marshal.loads(marshaled_code)
    func = types.FunctionType(code, globals(), funcname)
    return func, arg, kwargs


def dump_code(func, arg, kwargs):
    byte_func = marshal.dumps(func.__code__)
    funcname = func.__name__
    pickled_data = pickle.dumps((funcname, byte_func, arg, kwargs))
    hex_pickled_data = ''.join([str("%X" % i).zfill(2) for i in pickled_data])
    hex_encoded_pickled_data = hex_pickled_data.encode()
    return hex_encoded_pickled_data


def test():
    def method(i):
        return i*10
    funcdata = dump_code(method, (10,), {})
    reborn_func, arg, kwargs = load_code(funcdata)
    print(reborn_func(*arg, **kwargs))


if __name__ == '__main__':
    test()
