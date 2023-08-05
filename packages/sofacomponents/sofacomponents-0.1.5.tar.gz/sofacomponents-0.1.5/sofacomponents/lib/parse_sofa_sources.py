import glob
import os
import re


indent = "    "  # base indent
SINDENT = indent  # margin left


def parse_sources(src_path):
    ls = glob.glob(os.path.join(src_path, "**", "CMakeLists.txt"), recursive=True)

    classes = dict()
    for f in ls:
        classes.update(getFilesFromCMakeLists(f))

    classes = remove_bad_files(classes)
    # print(classes)

    cleaned = {}
    for i, (k, v) in enumerate(classes.items()):
        cleaned[os.path.basename(k)] = {}
        for e in v:
            cleaned[os.path.basename(k)].update(find_initData(f"{k}.{e}"))
    # print(cleaned)

    content = "from sofacomponents.lib.base_component import sofa_component\n\n"
    content += "class BaseSofaComponents:\n"

    for cls, args in cleaned.items():
        content += build_func(cls, args)
    # print(content)

    fname = os.path.join(os.path.dirname(__file__), "generated_classes.py")
    with open(fname, "w") as f:
        f.write(content)


def remove_bad_files(classes):
    cp = dict(classes)

    def delete_if(k, v):
        bname = os.path.basename(k)
        a = len(v) == 1 or "_test" in bname or bname[:4] == "init"
        b = not os.path.isfile(f"{k}.{v[0]}")
        return a or b

    for k, v in classes.items():
        if delete_if(k, v):
            del cp[k]

    return cp


def find_initData(fname):
    try:
        with open(fname, "r") as f:
            lines = f.readlines()
    except:
        return {}
    good = {}
    for line in lines:
        if "initData" in line:
            try:
                idt, msg = extract_from_initData(line)
                if check_args(idt, msg):
                    good[idt] = msg
            except:
                pass
    return good


def check_args(k, v):
    if k == "":
        return False
    if " " in k:
        return False
    if k in ["global", "in", "from", "yield"]:
        return False
    return True


def extract_from_initData(line):
    line = line.replace('\\"', "")
    line = line.split('"')
    idt, msg = line[-4], line[-2]
    return idt, msg


def getFilesFromCMakeLists(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    d = os.path.dirname(fname)
    res = dict()
    for line in lines:
        p = re.match("(.+?)\\.(\\w+)$", line.strip())
        if p:
            if not "#" in p[1]:
                k = os.path.join(d, p[1])
                l = res.get(k, list())
                l.append(p[2])
                res[k] = l

    return res


def build_func(name, d):
    s = template__(name, _doc_string(name, d), _kwargs(d), _params(d))
    return s


def template__(func_name, doc_string, kwargs, kwargs_dict):
    s = f"{SINDENT}@sofa_component\n"
    args = ["self", "**kwargs"]
    if len(kwargs) > 0:
        args.insert(1, kwargs)

    s += f"{SINDENT}def {func_name}({', '.join(args)}):\n"
    s += f"{SINDENT}{doc_string}\n"
    s += f"{SINDENT}{kwargs_dict}\n"
    s += f'{SINDENT}{indent}return "{func_name}", params\n\n'
    return s


def _params(args):
    s = indent + f'params = dict({", ".join(map(lambda x: f"{x}={x}", args))})'
    if len(args) > 0:
        s += f"\n{SINDENT}{indent}params = {{k: v for k, v in params.items() if v is not None}}"
    return s


def _kwargs(args):
    return ", ".join(map(lambda x: f"{x}=None", args))


def _doc_string(func_desc, args):
    s = indent + f'"""\n'
    s += f"{SINDENT}{indent}{func_desc}\n"
    if len(args) > 0:
        # s += f"\n{indent}Parameters:\n"
        s += "\n"
        for k, v in args.items():
            s += f"{SINDENT}{indent}:param {k}: {v}\n"
    s += f'{SINDENT}{indent}"""'
    return s


if __name__ == "__main__":
    parse_sources("/media/gaetan/UbuntuHDD/sofa/src/v20.06")
