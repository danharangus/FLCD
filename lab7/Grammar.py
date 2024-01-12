

class Grammar:
    def __init__(self):
        self.__nonterminals = []
        self.__terminals = []
        self.__startSymbol = ''
        self.__productions = {}
        self.__numberedProductions = {}

    def getNonterminals(self):
        return self.__nonterminals
    
    def getTerminals(self):
        return self.__terminals
    
    def getStartSymbol(self):
        return self.__startSymbol
    
    def getProductions(self) -> dict:
        return self.__productions

    def getNumberedProductions(self) -> dict:
        return self.__numberedProductions
    
    def getProductionThatContains(self, element):
        res = {}
        for lhs in self.__productions.keys():
            res[lhs] = []
            for list in self.__productions[lhs]:
                if element in list:
                    res[lhs].append(list)
        new_res = {}
        for key in res.keys():
            if res[key] != []:
                new_res[key] = res[key]
        return new_res
    
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
            if lhs not in self.__nonterminals or len(lhs) != 1:
                print("Nonterminal not found or more than one nonterminal is present!")
                return False
            for list in self.__productions[lhs]:
                for element in list:
                    if element not in self.__nonterminals and element not in self.__terminals and element != '&':
                        print(f"Element not found! {element}")
                        return False
        return True

    def number_prodcutions(self):
        i = 1
        for lhs in self.__productions.keys():
            self.__numberedProductions[lhs] = []
            for list in self.__productions[lhs]:
                self.__numberedProductions[lhs].append((i, list))
                i += 1

    def getProductionNumber(self, lhs, rhs):
        for production in self.__numberedProductions[lhs]:
            if production[1] == rhs:
                return production[0]
        return -1 

def main(): 
    grammar = Grammar()
    grammar.readFromFile("lab5-6-7/files/g1.txt")
    grammar.print_nonterminals()
    grammar.print_terminals()
    grammar.print_productions()
    print(grammar.getProductions())
    grammar.print_production('A')
    print(grammar.checkCFG())
    #print(grammar.getProductionThatContains('A'))
    p = grammar.getProductionThatContains('B')
    for key in p.keys():
        prods = p[key]
        for prod in prods:
            print(f"{key} -> {prod}")
    #print(grammar.getProductionThatContains('C'))
    grammar.number_prodcutions()
    

if __name__ == "__main__":
    main()