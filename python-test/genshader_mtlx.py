import os
import unittest

import MaterialX as mx
from MaterialX.PyMaterialXGenShader import *

from MaterialX.PyMaterialXGenOsl import OslShaderGenerator, OSL_UNIFORMS, OSL_OUTPUTS
_fileDir = os.path.dirname(os.path.abspath(__file__))

def _getSubDirectories(libraryPath):
    return [name for name in os.listdir(libraryPath)
            if os.path.isdir(os.path.join(libraryPath, name))]

def _getMTLXFilesInDirectory(path):
    for file in os.listdir(path):
        if file.endswith(".mtlx"):
            yield file

_readFromXmlFile = mx.readFromXmlFileBase

def _loadLibrary(file, doc):
    libDoc = mx.createDocument()
    _readFromXmlFile(libDoc, file)
    libDoc.setSourceUri(file)
    doc.importLibrary(libDoc)

def _loadLibraries(doc, searchPath, libraryPath):
    librarySubPaths = _getSubDirectories(libraryPath)
    librarySubPaths.append(libraryPath)
    for path in librarySubPaths:
        filenames = _getMTLXFilesInDirectory(os.path.join(libraryPath, path))
        for filename in filenames:
            filePath = os.path.join(libraryPath, os.path.join(path, filename))
            _loadLibrary(filePath, doc)

# Unit tests for GenShader (Python).
class TestGenShader(unittest.TestCase):

    def test_ShaderInterface(self):
        doc = mx.createDocument()

        searchPath = os.path.join(_fileDir, "../libraries")
        libraryPath = os.path.join(searchPath, "stdlib")
        _loadLibraries(doc, searchPath, libraryPath)

        exampleName = u"shader_interface"

        exampleShaderFile = os.path.join(_fileDir, "test_shader.mtlx")
        _readFromXmlFile(doc, exampleShaderFile)

        outputs = doc.getOutputs()
        output = next(iter(outputs))

        shadergen = OslShaderGenerator.create()
        context = GenContext(shadergen)
        # Add path to find all source code snippets
        context.registerSourceCodeSearchPath(mx.FilePath(searchPath))
        # Add path to find OSL include files
        context.registerSourceCodeSearchPath(mx.FilePath(os.path.join(searchPath, "stdlib/osl")))

        print(mx.writeToXmlString(doc))
        # Test complete mode
        context.getOptions().shaderInterfaceType = int(ShaderInterfaceType.SHADER_INTERFACE_COMPLETE)
        shader = shadergen.generate(exampleName, output, context)
        self.assertTrue(shader)
        self.assertTrue(len(shader.getSourceCode(PIXEL_STAGE)) > 0)

        ps = shader.getStage(PIXEL_STAGE)
        uniforms = ps.getUniformBlock(OSL_UNIFORMS)
        self.assertTrue(uniforms.size() == 2)

        outputs = ps.getOutputBlock(OSL_OUTPUTS)
        self.assertTrue(outputs.size() == 1)
        self.assertTrue(outputs[0].getName() == output.getName())

        file = open(shader.getName() + "_complete.osl", "w+")
        file.write(shader.getSourceCode(PIXEL_STAGE))
        file.close()
        #os.remove(shader.getName() + "_complete.osl");

if __name__ == '__main__':
    unittest.main()
