"""Nox configuration for running tests."""
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
