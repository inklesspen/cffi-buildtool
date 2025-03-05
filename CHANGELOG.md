# Changelog

## 1.1.1 (2025-03-04)

-   Add [PyPI trusted publisher](https://docs.pypi.org/trusted-publishers/) configuration.
-   Switch from tox to nox.
-   Mark the build as not requiring a C compiler (though of course projects _using_ it likely will). (#1)

## 1.1.0 (2024-09-10)

-   Depend on cffi 1.17.1 to take advantage of the new file-like object support in emit_c_code.

## 1.0.0 (2024-08-19)

-   First release on PyPI.
