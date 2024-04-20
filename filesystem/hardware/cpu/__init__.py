import psutil

def cpu_percent():
    # Obter a porcentagem de uso da CPU
    return psutil.cpu_percent()

def cpu_times():
    # Obter os tempos da CPU
    return psutil.cpu_times()

def cpu_count():
    # Obter o número de núcleos lógicos da CPU
    return psutil.cpu_count()