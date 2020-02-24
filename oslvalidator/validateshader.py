import MaterialX.PyMaterialXRender
import MaterialX.PyMaterialXRenderOsl as renderosl

def validate_shader():
    validator = renderosl.OslRenderer.create()
    validator.setOslIncludePath('C:/plugins/appleseed/appleseed-materialx/libraries/appleseed/appleseed/')
    validator.setOslCompilerExecutable('C:/plugins/appleseed/OpenShadingLanguage/package/bin/oslc.exe')
    validator.setOslTestShadeExecutable('C:/plugins/appleseed/OpenShadingLanguage/package/bin/testshade.exe')
    validator.setOslTestRenderExecutable('C:/plugins/appleseed/OpenShadingLanguage/package/bin/testrender.exe')
    validator.initialize()
    
    validator.compileOSL('C:/plugins/appleseed/appleseed-materialx/double_shade.osl')
    validator.setOslOutputFilePath('../oslvalidator/')
    validator.setOslShaderName('as_double_shade')  #The value is used to replace the %shader% token in the input XML scene file.
    validator.setOslShaderOutput('out_color', 'surfaceshader')
    validator.useTestRender(False)
    # validator.validateCreation(ShaderPtr shader)
    validator.validateRender()

    # when .useTestRender(True):
    #validator.setOslTestRenderSceneTemplateFile(scene_path)

if __name__ == '__main__':
    validate_shader()
