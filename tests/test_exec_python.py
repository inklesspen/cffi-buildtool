import pytest

import cffi_buildtool.gen

SIMPLE = """\
from cffi import FFI

ffibuilder = FFI()

ffibuilder.cdef("int netstring_read(char *buffer, size_t buffer_length, char **netstring_start, size_t *netstring_length);")

ffibuilder.set_source("netstring._netstring", '#include "netstring.h"')

something_else = 42
"""

CALLABLE = """\
from cffi import FFI

def make_ffi():
    ffibuilder = FFI()
    ffibuilder.cdef("int netstring_read(char *buffer, size_t buffer_length, char **netstring_start, size_t *netstring_length);")
    ffibuilder.set_source("netstring._netstring", '#include "netstring.h"')
    return ffibuilder

def something_else():
    return 42
"""


def test_exec_python():
    module_name, csrc, ffi = cffi_buildtool.gen.find_ffi_in_python_script(SIMPLE, "_netstring.c.py", "ffibuilder")
    assert module_name == "netstring._netstring"
    assert csrc.strip() == '#include "netstring.h"'
    cdef = "\n".join(ffi._cdefsources)
    assert "int netstring_read" in cdef


def test_exec_python_callable():
    module_name, csrc, ffi = cffi_buildtool.gen.find_ffi_in_python_script(CALLABLE, "_netstring.c.py", "make_ffi")
    assert module_name == "netstring._netstring"
    assert csrc.strip() == '#include "netstring.h"'
    cdef = "\n".join(ffi._cdefsources)
    assert "int netstring_read" in cdef


def test_exec_python_not_found():
    with pytest.raises(NameError, match="Expected to find the FFI object with the name 'notfound', but it was not found."):
        cffi_buildtool.gen.find_ffi_in_python_script(SIMPLE, "_netstring.c.py", "notfound")


def test_exec_python_bad_type():
    with pytest.raises(TypeError, match=".+not an instance of cffi.api.FFI"):
        cffi_buildtool.gen.find_ffi_in_python_script(SIMPLE, "_netstring.c.py", "something_else")


def test_exec_python_callable_bad_type():
    with pytest.raises(TypeError, match=".+not an instance of cffi.api.FFI"):
        cffi_buildtool.gen.find_ffi_in_python_script(CALLABLE, "_netstring.c.py", "something_else")
