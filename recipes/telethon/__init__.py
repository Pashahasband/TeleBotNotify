from pythonforandroid.recipe import PythonRecipe


class TelethonRecipe(PythonRecipe):
    version = "1.36.0"
    url = "https://pypi.org/packages/source/T/Telethon/Telethon-{version}.tar.gz"
    depends = ["setuptools", "pyaes"]
    site_packages_name = "telethon"
    call_hostpython_via_targetpython = False


recipe = TelethonRecipe()
