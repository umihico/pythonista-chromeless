import types
import marshal
import pickle


def load_code(ff_byte_code):
    pickled_code = bytes([int(ff_byte_code[i:i+2], 16) for i in range(0, len(ff_byte_code), 2)])
    funcname, marshaled_code = pickle.loads(pickled_code)
    code = marshal.loads(marshaled_code)
    func = types.FunctionType(code, globals(), funcname)
    return func


def dump_code(func):
    byte_func = marshal.dumps(func.__code__)
    funcname = func.__name__
    pickled_code = pickle.dumps((funcname, byte_func))
    ff_code = ''.join([str("%X" % i).zfill(2) for i in pickled_code])
    ff_byte_code = ff_code.encode()
    return ff_byte_code


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
