import sys
import os


class Node:
    def __init__(self, name="root", parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.objects = []
        self._attrs = {}

    def child(self, name):
        self.children.append(Node(name, self))
        return self.children[-1]

    def add(self, *objs):
        for obj in objs:
            self.objects.append(obj)
        return self

    def __repr__(self):
        return self.printSelf()

    def printSelf(self, i=2, display_args=True):
        s = "{}\n".format(self.name)
        carret = u"\u2514"
        if sys.version_info[0] == 2:  # Python 2.7
            carret = carret.encode("utf-8")

        for o in self.objects:
            kwargs = ""
            if display_args:
                kwargs = " ({})".format(
                    ", ".join([k + "=" + str(v) for k, v in o[1].items()])
                )
            s += "{}{} {}{}\n".format(" " * i, carret, o[0], kwargs)

        for d in self.children:
            s += "{}{} {}\n".format(" " * i, carret, d.printSelf(i + 2, display_args))

        return s.rstrip()

    def write_graph_to(self, fname, display_args=False):
        with open(fname, "w") as f:
            f.write(self.printSelf(display_args=display_args))

    def dump_into(self, node):
        """ Direct use in a scene """
        createObject = getattr(node, "createObject")
        createChild = getattr(node, "createChild")

        for k, v in self._attrs.items():
            setattr(node, k, v)

        for obj in self.objects:
            createObject(obj[0], **obj[1])

        for d in self.children:
            child_node = createChild(d.name)
            d.dump_into(child_node)

    def write_scene_to(self, fname):
        temp = os.path.join(os.path.dirname(__file__), "lib", "template_scene.txt")
        with open(temp, "r") as f:
            content = f.read()

        content = content.format(self.to_python())

        with open(fname, "w") as f:
            f.write(content)

    def to_python(self):
        """ Export the scene to file """
        s = []

        for k, v in self._attrs.items():
            s.append("{}.{} = {}".format(self.name, k, v))

        for o in self.objects:
            kwargs = [k + "=" + cc(v) for k, v in o[1].items()]
            s.append(
                "{}.createObject('{}', {})".format(self.name, o[0], ", ".join(kwargs))
            )

        for d in self.children:
            s.append("")
            s.append("# {}/{}".format(self.par(), d.name))
            s.append("{} = {}.createChild('{}')".format(d.name, self.name, d.name))
            s.append(d.to_python())

        return "\n        ".join(s)

    def attrs(self, **kwargs):
        self._attrs.update(kwargs)

    def par(self):
        if self.parent is not None:
            return "/".join([self.parent.par(), self.name])
        else:
            return self.name


def cc(v):
    return "'{}'".format(v) if type(v) is str else str(v)
