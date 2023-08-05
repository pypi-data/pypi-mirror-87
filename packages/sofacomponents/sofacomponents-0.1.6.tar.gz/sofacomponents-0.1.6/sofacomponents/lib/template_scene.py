import Sofa


class SceneElectroMechanical(Sofa.PythonScriptController):
    def __init__(self, node):
        self.createGraph(node)

    def createGraph(self, root):
        # root
        {}


def createScene(root_node):
    SceneElectroMechanical(root_node)
