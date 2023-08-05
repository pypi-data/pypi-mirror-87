import base64
import hashlib


def b64encode(obj):
    if isinstance(obj, str):
        obj = obj.encode("utf-8")
    base64code = base64.b64encode(obj).decode("utf-8")
    return base64code


def b64decode(code):
    if isinstance(code, str):
        code = code.encode("utf-8")
    content = base64.b64decode(code).decode("utf-8")
    return content


def get_md5_hash(instance):
    if isinstance(instance, str):
        md5_hash = hashlib.md5(instance.encode(encoding='utf8')).hexdigest()
    elif isinstance(instance, bytes):
        md5_hash = hashlib.md5(instance).hexdigest()
    else:
        md5_hash = hashlib.md5(instance.read()).hexdigest()
    return md5_hash
