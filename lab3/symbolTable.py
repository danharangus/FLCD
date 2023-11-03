from hashTable import HashTable

class SymbolTable:
    def __init__(self, size):
        self.table = HashTable(size)
        self.crt = 1

    def insert(self, name):
        pos = self.get(name)
        if pos is not None:
            return pos
        self.table.put(name, self.crt)
        self.crt += 1
        return self.crt - 1

    def get(self, name):
        return self.table.get(name)

    def __str__(self):
        return self.table.__str__()
    

