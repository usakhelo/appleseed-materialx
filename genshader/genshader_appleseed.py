import os
import unittest

import MaterialX as mx
import MaterialX.PyMaterialXGenShader as genshader

import MaterialX.PyMaterialXGenOsl as genosl

_fileDir = os.path.dirname(os.path.abspath(__file__))


def _getSubDirectories(libraryPath):
    return [name for name in os.listdir(libraryPath)
            if os.path.isdir(os.path.join(libraryPath, name))]


def _getMTLXFilesInDirectory(path):
    for file in os.listdir(path):
        if file.endswith(".mtlx"):
            yield file


def _loadLibrary(file, doc):
    libDoc = mx.createDocument()
    mx.readFromXmlFileBase(libDoc, file)
    libDoc.setSourceUri(file)
    doc.importLibrary(libDoc)


def _loadLibraries(doc, libraryPath):
    librarySubPaths = _getSubDirectories(libraryPath)
    librarySubPaths.append(libraryPath)
    for path in librarySubPaths:
        filenames = _getMTLXFilesInDirectory(os.path.join(libraryPath, path))
        for filename in filenames:
            filePath = os.path.join(libraryPath, os.path.join(path, filename))
            _loadLibrary(filePath, doc)


def generateOslShader(mtlx_file):
    doc = mx.createDocument()

    searchPath = os.path.join(_fileDir, "../libraries")
    _loadLibraries(doc, os.path.join(searchPath, "stdlib"))
    _loadLibraries(doc, os.path.join(searchPath, "pbrlib"))
    _loadLibraries(doc, os.path.join(searchPath, "appleseed"))

    mx.readFromXmlFileBase(doc, mtlx_file)

    # Find materials and shaderrefs inside mtlx file
    materials = doc.getMaterials()
    material = next(iter(materials))
    if material is not None:
        shaderRefs = material.getShaderRefs()
        if shaderRefs is not None:
            shaderRef = next(iter(shaderRefs))
            if shaderRef is None:
                return

    shadergen = genosl.OslShaderGenerator.create()
    context = genshader.GenContext(shadergen)

    # Add path to find all source code snippets
    context.registerSourceCodeSearchPath(mx.FilePath(searchPath))
    # Add path to find OSL include files
    # context.registerSourceCodeSearchPath(mx.FilePath(os.path.join(searchPath, "stdlib/osl")))

    print(mx.writeToXmlString(doc))

    # Complete mode
    # context.getOptions().shaderInterfaceType = int(ShaderInterfaceType.SHADER_INTERFACE_COMPLETE)
    context.getOptions().shaderInterfaceType = int(genshader.ShaderInterfaceType.SHADER_INTERFACE_REDUCED)

    shaderRefName = shaderRef.getName()
    shader = shadergen.generate(shaderRefName, shaderRef, context)
    if shader is None:
        return

    if len(shader.getSourceCode(genshader.PIXEL_STAGE)) == 0:
        return

    osl_path = os.path.join(os.path.dirname(mtlx_file), shader.getName() + ".osl")
    with open(osl_path, "w+") as osl_file:
        osl_file.write(shader.getSourceCode(genshader.PIXEL_STAGE))


if __name__ == '__main__':
    mtlx_file = os.path.join(_fileDir, "test_material_appleseed.mtlx")
    generateOslShader(mtlx_file)
