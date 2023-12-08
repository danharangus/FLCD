class Grammar:
    def __init__(self):
        self.__nonterminals = []
        self.__terminals = []
        self.__startSymbol = ''
        self.__productions = {}

    def getNonterminals(self):
        return self.__nonterminals
    
    def getTerminals(self):
        return self.__terminals
    
    def getStartSymbol(self):
        return self.__startSymbol
    
    def getProductions(self):
        return self.__productions
    
    def readFromFile(self, filename):
        with open(filename, 'r') as f:
            self.__nonterminals = f.readline().strip().split(' ')
            self.__terminals = f.readline().strip().split(' ')
            self.__startSymbol = f.readline().strip()
            for line in f.readlines():
                line = line.strip()
                if line == '':
                    continue
                production = line.split('=')
                lhs = production[0].strip()
                rhs = production[1].strip().split('|')
                v = []
                for element in rhs:
                    a = []
                    for char in element:
                        if char != ' ':
                            a.append(char)
                    v.append(a)
                self.__productions[lhs] = v
            print(self.__productions)

    def print_nonterminals(self):
        print("Nonterminals: ", end='')
        for nonterminal in self.__nonterminals:
            print(nonterminal, end=' ')
        print()

    def print_terminals(self):
        print("Terminals: ", end='')
        for terminal in self.__terminals:
            print(terminal, end=' ')
        print()

    def print_productions(self):
        print("Productions: ")
        for lhs in self.__productions.keys():
            print(lhs + " = ", end='')
            for list in self.__productions[lhs]:
                for element in list:
                    print(element, end=' ')
                if list != self.__productions[lhs][-1]:
                    print('| ', end='')
                    continue
                print('', end='')
            print()

    def print_production(self, lhs):
        print(f"Production for {lhs}:")
        print(lhs + " = ", end='')
        for list in self.__productions[lhs]:
            for element in list:
                print(element, end=' ')
            if list != self.__productions[lhs][-1]:
                print('| ', end='')
                continue
            print('', end='')

    def checkCFG(self):
        print("\nChecking if grammar is CFG...")
        for lhs in self.__productions.keys():
            if lhs not in self.__nonterminals:
                print("Nonterminal not found!")
                return False
            for list in self.__productions[lhs]:
                for element in list:
                    if element not in self.__nonterminals and element not in self.__terminals:
                        print("Element not found!")
                        return False
        return True
    

def main(): 
    grammar = Grammar()
    grammar.readFromFile("files/g1.txt")
    grammar.print_nonterminals()
    grammar.print_terminals()
    grammar.print_productions()
    grammar.print_production('A')
    print(grammar.checkCFG())

if __name__ == "__main__":
    main()