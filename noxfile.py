import nox

locations = "main.py", "noxfile.py", "src/mappings.py", "src/proxy.py", "src/utils.py"


# This is not run automatically
@nox.session
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-black")
    session.run("flake8", *args)


nox.options.sessions = ["lint"]
