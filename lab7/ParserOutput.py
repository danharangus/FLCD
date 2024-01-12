from dataclasses import dataclass

@dataclass
class ParserNode:
    symbol: str
    parent: int
    sibling: int
    last_child: int

    def __str__(self):
        return f"({self.symbol}, {self.parent}, {self.sibling}, {self.last_child})"
    

class ParserOutput:
    
    def __init__(self) :
        self._nodes = []

    def len(self):
        return len(self._nodes)
    
    def add_node(self, symbol, parent = None):
        symbol = symbol if symbol is not None else "None"
        
        node_index = self.len() 
        
        parent_index = 0

        if parent is not None:
            parent_index = parent
            last_sibling = self._nodes[parent_index].last_child
            if last_sibling is not None:
                self._nodes[last_sibling].sibling = node_index
            
            self._nodes[parent_index].last_child = node_index
        
        node = ParserNode(symbol, parent_index, None, None)
        self._nodes.append(node)
    
    def get_symbol(self, index):
        return self._nodes[index].symbol if index is not None and 0 <= index < self.len() else None
    
    def display(self):
        print("Parse Tree:")
        for index, node in enumerate(self._nodes):
            parent = self.get_symbol(node.parent)
            sibling = self.get_symbol(node.sibling)

            print("Node {}: Symbol = {}, Parent = {}, Sibling = {}".format(index, node.symbol, parent, sibling))


parser_output = ParserOutput()
parser_output.add_node("S")
parser_output.add_node("a", parent=0)
parser_output.add_node("S", parent=0)
parser_output.add_node("b", parent=0)
parser_output.add_node("S", parent=0)
parser_output.add_node("c", parent=2)
parser_output.add_node("c", parent=4)
parser_output.display()
        


 