import types
import marshal
import pickle
import base64
import zlib


def load_methods(base64str_data):
    b = base64.b64decode(base64str_data.encode())
    called_name_as_method, arg, kwargs, dumped_funcs, chrome_options = pickle.loads(
        zlib.decompress(b))
    funcs = {}
    for name, dumped in dumped_funcs.items():
        func = types.FunctionType(marshal.loads(dumped), globals(), name)
        funcs[name] = func
    return called_name_as_method, arg, kwargs, funcs, chrome_options


def pickle_result(result):
    return base64.b64encode(pickle.dumps(result)).decode()
