"""Nox configuration for running tests and linting."""

import nox


@nox.session(python=False)
def tests(session):
    """Run all tests and generate an HTML report."""
    session.run(
        "pytest",
        "src/tech_assesment_001",
        "--html=report.html",
        "--self-contained-html",
        "-v",
    )


@nox.session(python=False)
def black(session):
    """Run black formatter."""
    session.run("black", "src", "noxfile.py")


@nox.session(python=False)
def isort(session):
    """Run isort formatter."""
    session.run("isort", "src", "noxfile.py")


@nox.session(python=False)
def pylint(session):
    """Run pylint."""
    session.run("pylint", "src", "noxfile.py")


@nox.session(python=False)
def lint(session):
    """Run all linters and formatters."""
    session.run("nox", "-s", "black", "isort", "pylint")
