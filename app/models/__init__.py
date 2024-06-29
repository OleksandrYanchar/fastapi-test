import importlib
import os
import pkgutil


def import_all_models():
    package_dir = os.path.dirname(__file__)
    for module_loader, name, ispkg in pkgutil.walk_packages([package_dir]):
        importlib.import_module(f"{__name__}.{name}")


import_all_models()
