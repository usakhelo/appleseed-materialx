
# Build mtlx node defs based on appleseed installation

import os
import json
import sys

import MaterialX as mx

# Add appleseed to PYTHONPATH
sys.path.append(r'E:\GIT\appleseed\appleseed\sandbox\lib\v110\Release\python2.7')
# Add appleseed .dll to PATH
os.environ['PATH'] += os.pathsep + r'E:\GIT\appleseed\appleseed\sandbox\bin\v110\Release'
import appleseed as asr

oso_shaders_dir = r'E:\GIT\appleseed\appleseed\sandbox\shaders\appleseed'
osl_shaders_dir = r'E:\GIT\appleseed\appleseed\src\appleseed.shaders\src\appleseed'
osl_include_dir = r'E:\GIT\appleseed\appleseed\src\appleseed.shaders\include'

def check_multioutput(query):
    
    num_outputs = 0
    num_params = query.get_num_params()
    for i in range(0, num_params):
        pinfo = query.get_param_info(i)
        if pinfo.get('isoutput'):
            num_outputs += 1
        if num_outputs > 1:
            break
    return num_outputs > 1

def add_ports(nodeDef, query):

    num_params = query.get_num_params()
    for i in range(0, num_params):
        pinfo = query.get_param_info(i)

        pname = pinfo.get('name', '')
        ptype = pinfo.get('type', '')
        pvalue = None

        if pinfo.get('validdefault'):
            pvalue = pinfo.get('default')

        if pinfo.get('isclosure') and ptype == 'pointer':
            ptype = 'surfaceshader'
        elif ptype == 'point' or ptype == 'normal' or ptype == 'vector':
            ptype = 'vector3'
        elif ptype == 'color':
            ptype = 'color3'
        elif ptype == 'int':
            ptype = 'integer'
        elif ptype == 'matrix':
            ptype = 'matrix44'
        elif pinfo.get('isarray'):
            if ptype.startswith('float'):
                ptype = 'floatarray'
            elif ptype.startswith('int'):
                ptype = 'integerarray'
            elif ptype.startswith('color'):
                ptype = 'color3rarray'
            elif ptype.startswith('point'):
                ptype = 'vector3rarray'
        
        if ptype != 'string' and pvalue is not None:
            pvalue = ', '.join(str(pvalue).split(' '))

        if pinfo.get('isoutput'):
            def_output = nodeDef.addOutput(name=pname, type=ptype)
            if pvalue is not None:
                def_output.setValue(pvalue, ptype)
        else:
            def_input = nodeDef.addInput(name=pname, type=ptype)
            if pvalue is not None:
                def_input.setValue(pvalue, ptype)


def generate_appleseed_nodedefs():
    doc = mx.createDocument()
    
    # Add library includes

    q = asr.ShaderQuery()

    for root, dir, files in os.walk(oso_shaders_dir):
        for file in files:
            if file.endswith('.oso'):
                filename = os.path.join(root, file)
                q.open(filename)
                name = q.get_shader_name()
                # Create a nodedef taking three color3 and producing another color3
                nodeType = 'multioutput' if check_multioutput(q) else 'surfaceshader'
                nodeDef = doc.addNodeDef('ND_%s' % name, nodeType, name)  # type to be determined from shader type
                add_ports(nodeDef, q)

    outfile = 'appleseed_auto_defs.mtlx'
    mx.writeToXmlFile(doc, outfile)

def generate_appleseed_impls():
    doc = mx.createDocument()

    for root, dir, files in os.walk(osl_shaders_dir):
        for file in files:
            if file.endswith('.osl'):
                filename = os.path.join(root, file)
                name = os.path.basename(os.path.splitext(file)[0])
                # Create a implementation node
                nodeImpl = doc.addImplementation('IM_%s' % name)
                nodeImpl.setFile(filename)
                nodeImpl.setFunction(name)
                nodeImpl.setLanguage('genosl')
                nodeImpl.setNodeDefString('ND_%s' % name)

    outfile = 'appleseed_auto_impls.mtlx'
    mx.writeToXmlFile(doc, outfile)

if __name__ == '__main__':
    # for each file in appleseed osl library
    # generate nodedef
    # add it to command appleseed_defs.mtlx file
    # in each library folder (appleseed, maya, max etc) drop the _impl.mtlx file
    # which will refer osl shaders in that folder
    generate_appleseed_nodedefs()
    generate_appleseed_impls()