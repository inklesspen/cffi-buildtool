# /// script
# dependencies = ["nox"]
# ///
import nox

nox.options.default_venv_backend = "uv"


@nox.session()
def clean(session: nox.Session):
    session.install("coverage")
    session.run("coverage", "erase")


@nox.session()
def check(session: nox.Session):
    session.install("twine")
    tempdir = session.create_tmp()
    session.run("uv", "build", "-o", tempdir)
    session.run("twine", "check", f"{tempdir}/*")


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "pypy3.8", "pypy3.9", "pypy3.10"], requires=["clean"])
def test(session):
    session.env["PYTHONUNBUFFERED"] = "yes"
    session.run_install("uv", "sync", "--frozen", "--group=test", env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location})
    session.run("pytest", "--cov", "--cov-append", "--cov-report=term-missing", "--cov-report=xml", "-vv", "tests")


@nox.session(requires=["test"])
def report(session):
    session.install("coverage")
    session.run("coverage", "report")
    session.run("coverage", "html")


if __name__ == "__main__":
    nox.main()
