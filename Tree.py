class Node:
    def __init__(self,id,parent=None,depth=0):
        self.id=id
        self.parent=parent
        self.children=[]
        self.depth=depth
   
    def __eq__(self,other):
        if self.id == other.id:
            return True
        return False

    def add_child(self,child):
       self.children.append(child)

class Tree:
    def __init__(self):
        self.nodes=[]
        
    def get_index (self,key):
        result=None
        for index,node in enumerate(self.nodes):
            if node.id==key:
                result=index
                break
        if result==None:
            raise IndexError("No node with key \"%s\" found in current tree" % (key))
        return result

    def __getitem__(self,key):
        return self.nodes[self.get_index(key)]

    def add_node(self,id,parent=None):
        if parent != None:
            depth=self[parent].depth+1
        else:
            depth=0
        node = Node(id,parent,depth)
        self.nodes.append(node)
        if parent != None:
            self[parent].add_child(id)

    def get_common_parent(self,node1,node2):
        print("node1 id: %s, node1 parent: %s" %(self[node1].id,self[node1].parent))
        if node1 == node2:
            return node1
        if (self[node1].parent == None and self[node2].parent == None):
            return None
        if self[node1].depth < self[node2].depth:
            deep_node=node2
            shallow_node=node1
        else:
            deep_node=node1
            shallow_node=node2
        deep_node=self[self[deep_node].parent].id
        return self.get_common_parent(deep_node,shallow_node)

    def is_descendent_of(self,node1,node2):
       # returns True if node2 is in the sub-tree with node1 as the root, false otherwise. Node is considered a descendent of itself - 
       # questionable, but works for these particular requirements
       if node1==node2 or self[node2].parent==node1:
           return True
       elif self[node1].depth == self[node2].depth:
           return False
       return is_decendent_of(node1,self[node2].parent)

if __name__ == "__main__":
    tree = Tree()
    tree.add_node("uk")
    tree.add_node("england","uk")
    tree.add_node("scotland","uk")
    tree.add_node("sussex","england")
    tree.add_node("lothian","scotland")
    tree.add_node("edinburgh","lothian")
    tree.add_node("haddington","lothian")
    tree.add_node("yorkshire","england")
    tree.add_node("york","england")
    r=tree.get_common_parent("uk","england")
    print(r)
    r=tree.get_common_parent("edinburgh","haddington")
    print(r)
    r=tree.get_common_parent("edinburgh","sussex")
    print(r)
    r=tree.get_common_parent("york","sussex")
    print(r)
    r=tree.get_common_parent("york","cornwall")
    print(r)
    var = input()

