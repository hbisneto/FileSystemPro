from filesystem import wrapper as wr

class Watcher(object):
    """
    Watcher Class
    """
    def __init__(self, root):
        """
        This is the constructor method that initializes the Watcher object with a root directory to watch
        """
        self.root = root
        self.saved_state = self.get_state(root)

    def get_state(self, path):
        """
        This method returns a dictionary where the keys are the absolute paths of all files in the given path and the values are file metadata obtained from the core.enumerate_files(path) function
        """
        files = wr.enumerate_files(path)
        named_files = dict([(x["abspath"], x,) for x in files])
        return named_files

    def diff(self):
        """
        This method compares the current state of the file system with the saved state and identifies any changes (created, updated, or removed files). It returns a list of dictionaries where each dictionary contains the metadata of a changed file and an additional key "change" indicating the type of change.
        """
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
        """
        This method returns a string representation of the Watcher object.
        """
        return "filesystem.Watcher: %s" % (self.root)