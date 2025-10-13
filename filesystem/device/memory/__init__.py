"""
Memory
#### Dependência opcional: psutil (instale com `pip install psutil` para usar este módulo).

"""

import psutil

def virtual_memory():
    return psutil.virtual_memory()

def swap_memory():
    return psutil.swap_memory()