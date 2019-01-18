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


"""
test is in ../dump_code.py
"""
