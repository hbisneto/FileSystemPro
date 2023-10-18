import glob as glob_lib
import os
import shutil

def get_facts(pathname):
    def fun_or_default(pathname, fun, default=-1):
        try:
            return fun(pathname)
        except:
            return default

    head, tail = os.path.split(pathname)
    result = {}
    
    result["modified"] = fun_or_default(pathname, os.path.getmtime)
    result["created"] = fun_or_default(pathname, os.path.getctime)
    result["access"] = fun_or_default(pathname, os.path.getatime)
    result["name"] = tail
    result["name"] = tail
    result["size"] = fun_or_default(pathname, os.path.getsize)
    result["abspath"] = os.path.abspath(pathname)
    result["dirname"] = os.path.dirname(pathname)
    result["is_dir"] = os.path.isdir(pathname)
    result["is_file"] = os.path.isfile(pathname)
    result["is_link"] = os.path.islink(pathname)
    result["exists"] = os.path.exists(pathname)
    result["ext"] = tail.split(".")[-1] if result["is_file"] else ""
    return result

def glob(path):

    path = os.path.expanduser(path)
    print(path)
    result = []
    for x in glob_lib.glob(path):
        result.append(get_facts(x))
    return result

def walk(path):
    results = []
    path = os.path.expanduser(path)
    for root, dirs, files in os.walk(path):
        results.append(get_facts(root))
        results.extend([get_facts(os.path.join(root,x)) for x in files])
    return results

def makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        pass

def delete(path):
    if not os.path.exists(path):
        return
    
    if os.path.isdir(path):
        shutil.rmtree(path)
        return
    
    os.remove(path)

    
def store(path, value):
    with open(path, "w") as f:
        f.write(value)

