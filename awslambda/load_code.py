import types
import marshal
import pickle
import base64


def load_code(base64str_data):
    b = base64.b64decode(base64str_data.encode())
    funcname, marshaled_code, arg, kwargs = pickle.loads(b)
    code = marshal.loads(marshaled_code)
    func = types.FunctionType(code, globals(), funcname)
    return func, arg, kwargs
