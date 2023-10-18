from . import core
class Watcher(object):
    def __init__(self, root):
        self.root = root
        self.saved_state = self.get_state(root)
    
    def get_state(self, path):
        files = core.walk(path)
        named_files = dict([(x["abspath"], x,) for x in files])
        return named_files
    
    def diff(self):
        current_state = self.get_state(self.root)
        
        changed = []
        for k, v1 in current_state.items():
            if k not in self.saved_state:
                continue
            v2 = self.saved_state[k]
            if v1["modified"] != v2["modified"]:
                changed.append(k)
        
        current_set = set(current_state.keys())
        stored_set = set(self.saved_state)
        
        created =  current_set.difference(stored_set)
        removed =  stored_set.difference(current_set)
        
        results = []
        for x in changed:
            i = current_state[x]
            i["change"] = "updated"
            results.append(i)
        
        for x in created:
            i = current_state[x]
            i["change"] = "created"
            results.append(i)

        for x in removed:
            i = self.saved_state[x]
            i["change"] = "removed"
            results.append(i)
        
        # set new state
        self.saved_state = current_state
        
        return results
    
    def __str__(self):
        return "filesystem.Watcher: %s" % (self.root)

