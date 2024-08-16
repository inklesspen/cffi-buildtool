from ._netstring import ffi
from ._netstring import lib


class NetstringError(Exception):
    pass


error_codes = {
    lib.NETSTRING_ERROR_TOO_LONG: "Input buffer is too long",
    lib.NETSTRING_ERROR_NO_COLON: "No colon was found after the number",
    lib.NETSTRING_ERROR_TOO_SHORT: "Number of bytes greater than buffer length",
    lib.NETSTRING_ERROR_NO_COMMA: "No comma was found at the end",
    lib.NETSTRING_ERROR_LEADING_ZERO: "Leading zeros are not allowed",
    lib.NETSTRING_ERROR_NO_LENGTH: "Length not given at start of netstring",
}


def parse_netstring(somebytes: bytes) -> bytes:
    """Return a parsed netstring.

    >>> parse_netstring(b"12:hello world!,")
    b"hello world!"
    """
    buf = ffi.from_buffer(somebytes)
    netstring_start = ffi.new("char **")
    netstring_len = ffi.new("size_t *")
    result = lib.netstring_read(buf, len(somebytes), netstring_start, netstring_len)
    if result != 0:
        raise NetstringError(error_codes[result])
    return ffi.string(netstring_start[0], netstring_len[0])
