import MaterialX.PyMaterialXRender
import MaterialX.PyMaterialXRenderOsl as renderosl


def validate_shader():
    validator = renderosl.OslRenderer.create()
    validator.setOslIncludePath('C:/plugins/appleseed/appleseed-materialx/libraries/stdlib/osl')
    validator.setOslCompilerExecutable('C:/plugins/appleseed/windows-deps/stage/vc140/osl-release/bin/oslc.exe')
    # validator.setOslTestShadeExecutable('C:/plugins/appleseed/OpenShadingLanguage/package/bin/testshade.exe')
    # validator.setOslTestRenderExecutable('C:/plugins/appleseed/OpenShadingLanguage/package/bin/testrender.exe')
    validator.initialize()

    validator.setOslOutputFilePath('C:/plugins/appleseed/appleseed-materialx/genshader/')
    validator.setOslShaderName('as_double_shade')  # The value is used to replace the %shader% token in the input XML scene file.
    validator.setOslShaderOutput('out', 'color')
    validator.compileOSL('C:/plugins/appleseed/appleseed-materialx/genshader/as_double_shade.osl')
    validator.useTestRender(False)
    # validator.validateCreation(ShaderPtr shader)
    validator.render()

    # when .useTestRender(True):
    # validator.setOslTestRenderSceneTemplateFile(scene_path)


if __name__ == '__main__':
    validate_shader()
