import io

from cffi.api import FFI
from cffi.recompiler import Recompiler


def _execfile(pysrc, filename, globs: dict):
    compiled = compile(source=pysrc, filename=filename, mode="exec")
    exec(compiled, globs, globs)  # noqa: S102


def find_ffi_in_python_script(pysrc: str, filename: str, ffivar: str):
    globs = {"__name__": "gen-cffi-src"}
    _execfile(pysrc, filename, globs)
    if ffivar not in globs:
        raise NameError(f"Expected to find the FFI object with the name {ffivar!r}, but it was not found.")
    ffi = globs[ffivar]
    if not isinstance(ffi, FFI) and callable(ffi):
        # Maybe it's a callable that returns a FFI
        ffi = ffi()
    if not isinstance(ffi, FFI):
        raise TypeError(f"Found an object with the name {ffivar!r} but it was not an instance of cffi.api.FFI")
    # TODO: improve this; https://github.com/python-cffi/cffi/issues/47
    module_name, source, source_extension, kwds = ffi._assigned_source
    return module_name, source, ffi


def make_ffi_from_sources(modulename: str, cdef: str, csrc: str):
    ffibuilder = FFI()
    ffibuilder.cdef(cdef)
    ffibuilder.set_source(modulename, csrc)
    return ffibuilder


def generate_c_source(module_name: str, csrc: str, ffi: FFI):
    # TODO: improve this; https://github.com/python-cffi/cffi/issues/47
    recompiler = Recompiler(ffi, module_name)
    recompiler.collect_type_table()
    recompiler.collect_step_tables()
    output = io.StringIO()
    recompiler.write_c_source_to_f(output, csrc)
    return output.getvalue()
