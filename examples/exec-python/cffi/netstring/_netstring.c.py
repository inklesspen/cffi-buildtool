from cffi import FFI

ffibuilder = FFI()

ffibuilder.cdef(
    """\
int netstring_read(char *buffer, size_t buffer_length, char **netstring_start, size_t *netstring_length);

#define NETSTRING_ERROR_TOO_LONG     -1
#define NETSTRING_ERROR_NO_COLON     -2
#define NETSTRING_ERROR_TOO_SHORT    -3
#define NETSTRING_ERROR_NO_COMMA     -4
#define NETSTRING_ERROR_LEADING_ZERO -5
#define NETSTRING_ERROR_NO_LENGTH    -6
"""
)

ffibuilder.set_source(
    "netstring._netstring",
    """\
#include "netstring.h"
""",
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
