from hashTable import HashTable

class SymbolTable:
    def __init__(self, size):
        self.table = HashTable(size)
        self.crt = 1

    def insert(self, name):
        self.table.put(name, self.crt)
        self.crt += 1

    def get(self, name):
        return self.table.get(name)

    def display(self):
        return self.table.__str__()
    

