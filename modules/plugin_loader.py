"""
Aadi — Dynamic Plugin Loader Architecture
Author: Aaditya Kumar Pandey
"""

import os
import importlib
import pkgutil
from rich.console import Console

console = Console()

def load_dynamic_plugins(package_name="modules"):
    """modules/ फोल्डर के सभी सब-मॉड्यूल्स को डायनेमिकली लोड करता है।"""
    plugins = []
    try:
        package = importlib.import_module(package_name)
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            full_module_name = f"{package_name}.{module_name}"
            mod = importlib.import_module(full_module_name)
            plugins.append(mod)
    except Exception as e:
        console.print(f"[yellow]⚠ Plugin loader notice: {e}[/]")
    return plugins