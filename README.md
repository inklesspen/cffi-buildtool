# Overview

CFFI Buildtool lets you build [CFFI](https://cffi.readthedocs.io/en/stable/)-based Python extension modules without setuptools.

-   Free software: MIT license

## Installation

    pip install cffi-buildtool

You can also install the in-development version with:

    pip install https://github.com/inklesspen/cffi-buildtool/archive/main.zip

## Documentation

In the PEP 517/518 world, there are many choices for [build backends](https://packaging.python.org/en/latest/glossary/#term-Build-Backend). Of course, a lot of the choices only support pure-Python packages, but even for packages with C extensions, you can choose from [meson-python](https://meson-python.readthedocs.io/en/latest/), [scikit-build-core](https://scikit-build-core.readthedocs.io/en/latest/), and probably a few others. Unfortunately, the CFFI docs only explain how to integrate with setuptools and a setup.py configuration. Worse, the normal ways of generating C source for your extension require distutils to be available, which was removed from the Python standard library in Python 3.12.

This tool exists to fill this gap. Examples are provided for projects using meson-python, but it should be useful for any PEP 517 build backend which allows you to run a helper tool during the build. It runs in two modes: "exec-python" and "read-sources".

### exec-python mode

In the CFFI docs, under ["Main mode of usage"](https://cffi.readthedocs.io/en/stable/overview.html#main-mode-of-usage), you'll find an example build script that looks like this (but with more comments):

```python
from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef("""
    float pi_approx(int n);
""")

ffibuilder.set_source("_pi_cffi",
"""
    #include "pi.h"
""",
    libraries=['piapprox'])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
```

This Python script, if executed, will generate a C source file named `_pi_cffi.c` and compile it. However, the CFFI docs go on to recommend using the setuptools `cffi_modules` option instead of directly executing the script. When you do this, setuptools and CFFI execute the build script, capture the ffibuilder object, and use it to add the C extension module to the build targets.

CFFI Buildtool's exec-python mode works similarly. It ignores the library names, though; linking against the appropriate libraries is a job for your build backend. (For example, with meson-python you would add the necessary library dependencies to the `py.extension_module()` invocation.)

```console
$ gen-cffi-src exec-python piapprox_build.py _pi_cffi.c
```

Or, if you named the FFI object something other than `ffibuilder`:

```console
$ gen-cffi-src exec-python --ffi-var=ffidef piapprox_build.py _pi_cffi.c
```

This mode is probably most useful for smaller modules. The larger and more complicated a module gets, the more annoying it is to have a Python build script that only exists to provide C source to a build tool. That's why the other mode exists.

### read-sources mode

In this mode, the C definitions ("cdef") and C source prelude ("csrc") are provided as separate files, instead of being bundled into a Python script. If you are wrapping a large library, or if you have defined some functions in C [for performance reasons](https://cffi.readthedocs.io/en/stable/overview.html#purely-for-performance-api-level-out-of-line), you should consider using this mode. It means your C source will be in a file ending in `.c`, so your editor and presubmits can work with it without friction.

```
/* piapprox.cdef.txt */
float pi_approx(int n);
```

```c
/* piapprox.csrc.c */
#include "pi.h"
```

When you run the tool in this mode, you need to provide the desired module name on the command line.

```console
$ gen-cffi-src read-sources _pi_cffi piapprox.cdef.txt piapprox.csrc.c _pi_cffi.c
```
