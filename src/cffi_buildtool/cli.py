"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mcffi_buildtool` python will execute
    ``__main__.py`` as a script. That means there will not be any
    ``cffi_buildtool.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there"s no ``cffi_buildtool.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import argparse
import typing

from .gen import find_ffi_in_python_script
from .gen import generate_c_source
from .gen import make_ffi_from_sources


def exec_python(*, output: typing.TextIO, pyfile: typing.TextIO, ffi_var: str):
    with pyfile:
        ffi = find_ffi_in_python_script(pyfile.read(), pyfile.name, ffi_var)
    generated = generate_c_source(ffi)
    with output:
        output.write(generated)


def read_sources(*, output: typing.TextIO, module_name: str, cdef_input: typing.TextIO, csrc_input: typing.TextIO):
    with csrc_input, cdef_input:
        csrc = csrc_input.read()
        cdef = cdef_input.read()
    ffi = make_ffi_from_sources(module_name, cdef, csrc)
    generated = generate_c_source(ffi)
    with output:
        output.write(generated)


parser = argparse.ArgumentParser(description="Command description.")
subparsers = parser.add_subparsers(dest="mode")

exec_python_parser = subparsers.add_parser("exec-python", help="Execute a Python script to build a FFI object")
exec_python_parser.add_argument(
    "--ffi-var", default="ffibuilder", help="Name of the FFI object in the Python script; defaults to 'ffibuilder'."
)
exec_python_parser.add_argument("pyfile", type=argparse.FileType("r", encoding="utf-8"), help="Path to the Python script")
exec_python_parser.add_argument("output", type=argparse.FileType("w", encoding="utf-8"), help="Output path for the C source")

read_sources_parser = subparsers.add_parser("read-sources", help="Read CDEF and C source prelude files")
read_sources_parser.add_argument("module_name", help="Full name of the generated module, including packages")
read_sources_parser.add_argument("cdef", type=argparse.FileType("r", encoding="utf-8"), help="File containing C definitions")
read_sources_parser.add_argument("csrc", type=argparse.FileType("r", encoding="utf-8"), help="File containing C source prelude")
read_sources_parser.add_argument("output", type=argparse.FileType("w", encoding="utf-8"), help="Output path for the C source")


def run(args: typing.Optional[typing.Sequence[str]] = None):
    args = parser.parse_args(args=args)
    if args.mode == "exec-python":
        exec_python(output=args.output, pyfile=args.pyfile, ffi_var=args.ffi_var)
    elif args.mode == "read-sources":
        if args.cdef is args.csrc:
            parser.error("--cdef and --csrc are the same file and should not be")
        read_sources(output=args.output, module_name=args.module_name, cdef_input=args.cdef, csrc_input=args.csrc)
    else:  # pragma: no cover
        raise AssertionError("Unknown subcommand; should not ever happen.")
    parser.exit(0)
