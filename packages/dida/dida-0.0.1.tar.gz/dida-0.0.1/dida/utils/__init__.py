from importlib import import_module
from pkgutil import iter_modules


def walk_module(name):
    modules = []
    module = import_module(name)
    modules.append(module)
    for info in iter_modules(module.__path__):
        sub_name = name + '.' + info.name
        if info.ispkg:
            modules.extend(walk_module(sub_name))
        else:
            modules.append(import_module(sub_name))
    return modules
