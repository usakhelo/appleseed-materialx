# appleseed-materialx
Experiments with [MaterialX](https://github.com/materialx/MaterialX) and [appleseed renderer](https://github.com/appleseedhq/appleseed)

## Roadmap:
- Python script to build appleseed mtlx library
  - [x] Generate `appleseed_defs.mtlx` files
- Convert appleseed shaders to .mtlx from studio and/or DCC plugin
  - [x] Simplest case is done - `as_double_shade.osl`
- Generate and compile appleseed OSL shaders from .mtlx files
  - [X] Simple Python script to generate OSL from .mtlx files
  - [ ] Compile OSL to OSO
  - [ ] Validate shaders
- [ ] Export nodes and material assignments from appleseed studio to .mtlx file
- [ ] Import .mtlx into DCC application and appleseed.studio
- [ ] Alternative to MaterialXViewer with interactive appleseed renderer
