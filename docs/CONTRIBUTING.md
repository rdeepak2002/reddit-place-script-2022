# Pre-requisite

 * __Nox__ can be installed following these instructions: https://nox.thea.codes/en/stable/

# Developing

 1. Add any new source file (extension `.py`) to the list of files to be checked in `noxfile.py`
 2. Run [`black`](https://black.readthedocs.io/en/stable/) on the repo with `nox -rs black` to format the code
 3. Run `nox` on the root of the repo

# Rules

`nox` will run the following: 
  * `flake8` to check for formatting issues: https://flake8.pycqa.org/en/latest/
  * `flake8-black` to check for style issues:
