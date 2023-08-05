import os
import urllib
import urllib.request

from .error import UserError


def build_opener(default_opener=urllib.request.urlopen):
    proxy_env = os.environ.get("HTTPS_PROXY") or os.environ.get("ALL_PROXY")
    if proxy_env is not None and proxy_env.startswith("socks"):
        protocol, host, port = proxy_env.split(":")
        return socks_opener((protocol, host.lstrip("/"), int(port)))
    return default_opener


def socks_opener(proxy_settings):
    """Returns an opener based on proxy settings: Normal opener if no proxy
    settings are given, PySocks opener if proxy settings are given
    """
    return urllib.request.build_opener(
        socks_handler(*proxy_settings)).open


def socks_handler(protocol, host, port):
    try:
        import socks   # pylint: disable=import-outside-toplevel
        from sockshandler import SocksiPyHandler  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError:
        raise UserError(
            "module PySocks needs to be available when using a proxy") from None
    protocol_mapping = {
        "socks4": socks.SOCKS4,
        "socks5": socks.SOCKS5
    }
    try:
        protocol = protocol_mapping[protocol]
    except KeyError:
        raise UserError("Invalid scheme " + protocol) from None
    return SocksiPyHandler(protocol, host, port)


urlopen = build_opener()


def post(url: str, data: bytes):
    request = urllib.request.Request(
        url, data, method='POST',
        headers={"Content-Type": "application/json; charset=UTF-8"})
    with urlopen(request) as response:
        response_text = response.read()
        return response_text
