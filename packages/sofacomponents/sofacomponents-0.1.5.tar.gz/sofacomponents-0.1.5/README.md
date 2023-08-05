# Easily build complex simulation graphs for SOFA

Install
```bash
pip install sofacomponents
```

## Quick start

```python
from sofacomponents import Node, SofaFactory

# build the factory
fa = SofaFactory(debug=False)

# create the root node
root = Node()
# add attributes
root.attrs(dt=0.05, gravity=[0, -1, 0])
# add sofa components from the factory
root.add(
    fa.VisualStyle(displayFlags="showVisual"),
    fa.DefaultAnimationLoop(),
    fa.RequiredPlugin(pluginName="SofaOpenglVisual SofaPython"),
)
# add child node
childNode = root.child("childNode").add(
    fa.MeshVTKLoader(filename="mesh.vtk"),
    # add components not from the factory
    fa.UnknownComponent(data="foo"),
)

# display the scene
print(root)

# Export the scene
root.write_scene_to("scene.py")

# Export the graph
root.write_graph_to("graph.txt")
```

Output:
```text
root
  └ VisualStyle (displayFlags=showVisual)
  └ DefaultAnimationLoop ()
  └ RequiredPlugin (pluginName=SofaOpenglVisual SofaPython)
  └ childNode
    └ MeshVTKLoader (filename=mesh.vtk)
    └ UnknownComponent (data=foo)
```

Python generated scene:
```python
import Sofa

class SceneElectroMechanical(Sofa.PythonScriptController):
    def __init__(self, node):
        self.createGraph(node)

    def createGraph(self, root):
        # root
        root.dt = 0.05
        root.gravity = [0, -1, 0]
        root.createObject("VisualStyle", displayFlags="showVisual")
        root.createObject("DefaultAnimationLoop",)
        root.createObject("RequiredPlugin", pluginName="SofaOpenglVisual SofaPython")

        # root/childNode
        childNode = root.createChild("childNode")
        childNode.createObject("MeshVTKLoader", filename="mesh.vtk")
        childNode.createObject("UnknownComponent", data="foo")

def createScene(root_node):
    SceneElectroMechanical(root_node)
```



## Extend

Create a factory instanciating the `SofaFactory` class.

The `sofa_component` decorator allows to update the parameters directory with:
1. the general default parameters (See `SofaFactory._defaults`)
2. the `params` you choose for your component
3. the custom `kwargs` given by the user



```python
from sofacomponents import SofaFactory, sofa_component

class MyFactory(SofaFactory):
    def __init__(self, debug=False):
        super().__init__(debug)
   
    @sofa_component
    def MyComponentNoParams(self, **kwargs):
        """ Minimum signature to register the component to the factory """
        return "MyComponentName"

    @sofa_component
    def MyComponent(self, **kwargs):
        params = dict(
            data="foo",
            # ...
        )
        return "MyComponentName", params
```

And then
```python
# build the factory
fa = MyFactory()
```


## Embeded documentation

![pycharm documentation](sofacomponents/lib/FEM_doc.png)