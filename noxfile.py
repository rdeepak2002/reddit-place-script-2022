import nox

locations = "main.py", "noxfile.py", "mappings.py"


@nox.session
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session
def lint(session):
    args = session.posargs or locations
    session.install("flake8")
    session.run("flake8", *args)
