import importlib
import sys

from molotov.util import request
from aiohttp import ClientResponseError


def raise_response_error(resp, status, message):
    err = ClientResponseError(resp.request_info, tuple())
    err.message = message
    err.status = status
    raise err


def get_server_info(url, method, headers):
    info = {}
    res = request(url, "HEAD", headers=headers)
    server = res["headers"].get("server", "Unknown")
    info["software"] = server
    if headers:
        info["headers"] = dict(headers)
    return info


def print_server_info(info, stream=sys.stdout):
    stream.write("-------- Server info --------\n\n")
    stream.write(f"Server Software: {info['software']}\n")
    for k, v in info.get("headers", {}).items():
        stream.write(f"{k}: {v}\n")
    stream.write("\n")
    stream.flush()


def resolve(name):
    func = None

    if "." in name:
        splitted = name.split(".")
        mod_name = ".".join(splitted[:-1])
        func_name = splitted[-1]
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
    else:
        for ns in globals(), __builtins__:
            if name in ns:
                func = ns[name]
                break

    if func is None:
        raise ImportError(f"Cannot find '{name}'")
    return func
