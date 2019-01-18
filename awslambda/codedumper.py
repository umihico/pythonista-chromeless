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
    hex_pickled_data = pickle_to_hex_string(pickled_data)
    hex_encoded_pickled_data = hex_pickled_data.encode()
    return hex_encoded_pickled_data


def pickle_to_hex_string(pickled):
    return ''.join([str("%X" % i).zfill(2) for i in pickled])


def hex_string_to_pickle(hex_list):
    return bytes([int(hex_list[i:i+2], 16) for i in range(0, len(hex_list), 2)])


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
