import types
import marshal
import pickle
import base64


def _dump_codes(called_name_as_method, arg, kwargs, stored_funcs, chrome_options=None):
    dumped_funcs = {name: marshal.dumps(
        func.__code__) for name, func in stored_funcs.items()}
    pickled_data = pickle.dumps((called_name_as_method, arg, kwargs, dumped_funcs, chrome_options))
    base64str_data = base64.b64encode(pickled_data).decode()
    return base64str_data


def _unpickle_result(base64str_data):
    try:
        return pickle.loads(base64.b64decode(base64str_data.encode()))
    except Exception as e:
        # '{"message": "Internal server error"}'
        # '{"message": "Endpoint request timed out"}'
        raise Exception(
            f"lambda returned {base64str_data}. please check CloudWatch and capacity of lambda is enough.")


if __name__ == '__main__':
    test()
