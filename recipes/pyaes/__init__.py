from pythonforandroid.recipe import PythonRecipe


class PyaesRecipe(PythonRecipe):
    version = "1.6.1"
    url = "https://pypi.org/packages/source/p/pyaes/pyaes-{version}.tar.gz"
    depends = ["setuptools"]
    site_packages_name = "pyaes"
    call_hostpython_via_targetpython = False


recipe = PyaesRecipe()
