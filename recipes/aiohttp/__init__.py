from pythonforandroid.recipe import PyProjectRecipe


class AiohttpRecipe(PyProjectRecipe):
    version = "3.14.4"
    url = "https://pypi.org/packages/source/a/aiohttp/aiohttp-{version}.tar.gz"
    depends = ["setuptools"]

    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)
        env["AIOHTTP_NO_EXTENSIONS"] = "1"
        return env


recipe = AiohttpRecipe()
