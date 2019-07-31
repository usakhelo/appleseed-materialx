
# Build mtlx node defs based on appleseed installation

import os
import json
import sys

# Add appleseed to PYTHONPATH
sys.path.append('C:\\plugins\\appleseed\\appleseed\\sandbox\\lib\\vc140\\Release\\python')
# Add appleseed .dll to PATH
os.environ['PATH'] += os.pathsep + 'C:\\plugins\\appleseed\\appleseed\\sandbox\\bin\\vc140\\Release'

oso_shaders_dir = "C:\\plugins\\appleseed\\appleseed\\sandbox\\shaders\\appleseed"

shaderparams = {}

import appleseed as asr
q = asr.ShaderQuery()

for root, dir, files in os.walk(oso_shaders_dir):
    for file in files:
        if file.endswith(".oso"):
            filename = os.path.join(root, file)
            q.open(filename)
            name = q.get_shader_name()

            num_params = q.get_num_params()

            print name
            for i in range(0, num_params):
                pinfo = q.get_param_info(i)

                pname = pinfo['name'] if 'name' in pinfo else ''
                ptype = pinfo['type'] if 'type' in pinfo else ''
                pvalue = pinfo['value'] if 'value' in pinfo else ''
                plabel = pinfo['label'] if 'label' in pinfo else ''
                ppage = pinfo['page'] if 'page' in pinfo else ''
                print '\t', pname, ptype, pvalue, plabel, ppage