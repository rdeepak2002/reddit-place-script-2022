# Pre-requisite

 * __Nox__ can be installed following these instructions: https://nox.thea.codes/en/stable/

# Developing

 1. Add any new source file (extension `.py`) to the list of files to be checked in `noxfile.py`
 2. Run `nox` on the root of the repo

# Rules

`nox` will run the following: 
  * `black` to format the code: https://black.readthedocs.io/en/stable/
  * `flake8` to check for style issues: https://flake8.pycqa.org/en/latest/