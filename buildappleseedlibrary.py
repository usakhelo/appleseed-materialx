
# Build mtlx node defs based on appleseed installation

import os
import json
import sys

import MaterialX as mx

# Add appleseed to PYTHONPATH
sys.path.append('C:\\plugins\\appleseed\\appleseed\\sandbox\\lib\\vc140\\Release\\python')
# Add appleseed .dll to PATH
os.environ['PATH'] += os.pathsep + 'C:\\plugins\\appleseed\\appleseed\\sandbox\\bin\\vc140\\Release'
import appleseed as asr



oso_shaders_dir = "C:\\plugins\\appleseed\\appleseed\\sandbox\\shaders\\appleseed"


def add_inputs(nodeDef, query):

    num_params = query.get_num_params()
    for i in range(0, num_params):
        pinfo = query.get_param_info(i)

        pname = pinfo.get('name', '')
        ptype = pinfo.get('type', '')
        pvalue = pinfo.get('value', '')
        # plabel = pinfo.get('label', '')
        # ppage = pinfo.get('page', '')

        print pname, ptype, pvalue
        def_input = nodeDef.addInput(name=pname, type=ptype)
        def_input.setValue(pvalue)


def generate_appleseed_nodedefs():
    # for each file in appleseed osl library
    # generate nodedef
    # add it to command appleseed_defs.mtlx file
    # in each library folder (appleseed, maya, max etc) drop the _impl.mtlx file
    # which will refer osl shaders in that folder

    doc = mx.createDocument()
    
    # Add library includes

    q = asr.ShaderQuery()

    for root, dir, files in os.walk(oso_shaders_dir):
        for file in files:
            if file.endswith(".oso"):
                filename = os.path.join(root, file)
                q.open(filename)
                name = q.get_shader_name()
                # Create a nodedef taking three color3 and producing another color3
                nodeDef = doc.addNodeDef("ND_%s" % name, "surfaceshader", name)  # type to be determined from shader type
                add_inputs(nodeDef, q)

    outfile = "appleseed_auto_defs.mtlx"
    mx.writeToXmlFile(doc, outfile)

if __name__ == '__main__':
    generate_appleseed_nodedefs()