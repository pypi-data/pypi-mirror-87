import importlib
import sys
try:
    from importlib_metadata import ModuleNotFoundError
except:
    pass

def is_module_available(module_name):
    if sys.version_info < (3, 0):
        # python 2
        try:
            __import__(module_name)
        except ImportError:
            torch_loader = None
        else:
            torch_loader = True
        #torch_loader = importlib.find_loader(module_name)
    elif sys.version_info <= (3, 3):
        # python 3.0 to 3.3
        import pkgutil
        torch_loader = pkgutil.find_loader(module_name)
    elif sys.version_info >= (3, 4):
        # python 3.4 and above
        from importlib import util
        torch_loader = util.find_spec(module_name)

    return torch_loader is not None

def import_module(module_name,package,dependencies):
    try:
        module = importlib.import_module(".." + module_name, package=package)
        return module
    except ModuleNotFoundError as mnfe:
        from pkgutil import iter_modules
        modules = set(x[1] for x in iter_modules())

        for requirement in dependencies:
            if not requirement in modules:
                print("Please install " + requirement + " (pip install " + requirement + ")")

        return None
