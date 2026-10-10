from pythonforandroid.recipe import RustCompiledComponentsRecipe


class PydanticCoreRecipe(RustCompiledComponentsRecipe):
    version = "2.41.4"
    url = "https://github.com/pydantic/pydantic-core/archive/refs/tags/v{version}.tar.gz"
    site_packages_name = "pydantic_core"

    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)
        env["ANDROID_API_LEVEL"] = str(self.ctx.ndk_api)
        return env


recipe = PydanticCoreRecipe()
