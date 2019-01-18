import types
import marshal
import pickle


def load_code(pickled_code):
    funcname, marshaled_code = pickle.loads(pickled_code)
    code = marshal.loads(marshaled_code)
    func = types.FunctionType(code, globals(), funcname)
    return func


def dump_code(func):
    byte_func = marshal.dumps(func.__code__)
    funcname = func.__name__
    pickled_code = pickle.dumps((funcname, byte_func))
    return pickled_code
