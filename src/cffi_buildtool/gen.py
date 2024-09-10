import io

from cffi.api import FFI


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
    return ffi


def make_ffi_from_sources(modulename: str, cdef: str, csrc: str):
    ffibuilder = FFI()
    ffibuilder.cdef(cdef)
    ffibuilder.set_source(modulename, csrc)
    return ffibuilder


def generate_c_source(ffi: FFI):
    output = io.StringIO()
    ffi.emit_c_code(output)
    return output.getvalue()
