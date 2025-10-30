"""
Memory
#### Dependência opcional: psutil (instale com `pip install psutil` para usar este módulo).

"""

import psutil as __psutil__

# VIRTUAL MEMORY
def virtual_memory():
    return __psutil__.virtual_memory()

def total_virtual_memory():
    return __psutil__.virtual_memory().total

def available_virtual_memory():
    return __psutil__.virtual_memory().available

def percent_virtual_memory():
    return __psutil__.virtual_memory().percent

def used_virtual_memory():
    return __psutil__.virtual_memory().used

def free_virtual_memory():
    return __psutil__.virtual_memory().free

def active_virtual_memory():
    return __psutil__.virtual_memory().active

def inactive_virtual_memory():
    return __psutil__.virtual_memory().inactive

def buffers_virtual_memory():
    return __psutil__.virtual_memory().buffers

def cached_virtual_memory():
    return __psutil__.virtual_memory().cached

def shared_virtual_memory():
    return __psutil__.virtual_memory().shared

def slab_virtual_memory():
    return __psutil__.virtual_memory().slab

# SWAP MEMORY
def swap_memory():
    return __psutil__.swap_memory()

def total_swap_memory():
    return __psutil__.swap_memory().total

def used_swap_memory():
    return __psutil__.swap_memory().used

def free_swap_memory():
    return __psutil__.swap_memory().free

def percent_swap_memory():
    return __psutil__.swap_memory().percent

def sin_swap_memory():
    return __psutil__.swap_memory().sin

def sout_swap_memory():
    return __psutil__.swap_memory().sout