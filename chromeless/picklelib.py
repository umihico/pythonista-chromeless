
import pickle
import zlib
import base64


def dumps(obj):
    return base64.b64encode(zlib.compress(pickle.dumps(obj))).decode()


def loads(obj):
    return pickle.loads(zlib.decompress(base64.b64decode(obj.encode())))
