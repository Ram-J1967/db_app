class TreeNode:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_lvl(self):
        lvl = 0
        p = self.parent
        while p:
            lvl += 1
            p = p.parent
        return lvl
    
    def show(self):
        lvl = self.get_lvl()
        spaces = " - " * lvl
        print(spaces + str(self.data))
        if self.children:
            for child in self.children:
                child.show()
    