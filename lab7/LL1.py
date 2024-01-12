from Grammar import Grammar
import copy
from prettytable import PrettyTable
from ParserOutput import ParserOutput

class LL1:
    def __init__(self, grammar):
        self.grammar = grammar
        self.__first = {}
        self.__follow = {}
        self.__table = {}
    
    def concatenation_of_length_one(self, list1, list2):
        if '&' in list1:
            return list1 + list2
        return list1 

    def compute_first(self):
        for terminal in self.grammar.getTerminals():
            self.__first[terminal] = [terminal] # initialize first of terminals with the terminal itself
        
        for lhs in self.grammar.getProductions().keys():
            if lhs not in self.__first.keys():
                self.__first[lhs] = [] # initialize first of nonterminals with empty list
            for elem in self.grammar.getProductions()[lhs]:
                if elem in self.grammar.getTerminals():
                    self.__first[lhs].append(elem) # if rhs is terminal, add it to first of lhs
                elif elem[0] in self.grammar.getTerminals():
                    self.__first[lhs].append(elem[0]) # if rhs starts with terminal, add it to first of lhs

        done = False
        while not done:
            previous = copy.deepcopy(self.__first)
            for lhs in self.grammar.getProductions().keys():
                for production  in self.grammar.getProductions()[lhs]:
                    res = []
                    for elem in production:
                        if len(res) == 0:
                            res += previous[elem]
                        else:
                            res = self.concatenation_of_length_one(res, previous[elem])     
                    self.__first[lhs] += res
                self.__first[lhs] = list(set(self.__first[lhs]))
            if previous == self.__first:
                done = True

    def compute_first_of_production(self, production):
        res = self.__first[production[0]]
        for i in range(1, len(production)):
            res = self.concatenation_of_length_one(res, self.__first[production[i]])
        return list(set(res))

    def print_first(self):
        for key in self.__first.keys():
            print(f"First({key}) = {self.__first[key]}")   
    

    def generate_follow(self):
        for nonterminal in self.grammar.getNonterminals():
            if nonterminal != self.grammar.getStartSymbol():
                self.__follow[nonterminal] = []
        self.__follow[self.grammar.getStartSymbol()] = ['&']
        
        done = False
        while not done:
            previous = copy.deepcopy(self.__follow)
            for nonterminal in self.grammar.getNonterminals():
                productionsForTerminal = self.grammar.getProductionThatContains(nonterminal)
                if productionsForTerminal == {}: # if nonterminal is not in any production
                    continue
                for lhs in productionsForTerminal.keys():
                    productions = productionsForTerminal[lhs]
                    for production in productions:
                        c = production[:]
                        c.pop()
                        if nonterminal == production[-1] and nonterminal not in c :
                            self.__follow[nonterminal] += previous[lhs]
                        else:
                            index = production.index(nonterminal)
                            res = []
                            for i in range(index + 1, len(production)):
                                if len(res) == 0:
                                    res += self.__first[production[i]]
                                else:
                                    res = self.concatenation_of_length_one(res, self.__first[production[i]])
                            if '&' in res:
                                res.remove('&')
                                self.__follow[nonterminal] += res
                                self.__follow[nonterminal] += previous[lhs]
                            else:
                                self.__follow[nonterminal] += res
                    self.__follow[nonterminal] = list(set(self.__follow[nonterminal]))           
            if previous == self.__follow:
                done = True
                
    
    def print_follow(self):
        for key in self.grammar.getNonterminals():
            print(f"Follow({key}) = {self.__follow[key]}")


    def parsing_table(self):
        self.__table = {
            symbol: { t: 'err' for t in self.grammar.getTerminals() + ['$'] } for symbol in self.grammar.getNonterminals() + self.grammar.getTerminals() + ['$']
        }
        self.__table['$']['$'] = 'acc'
        for terminal in self.grammar.getTerminals():
            self.__table[terminal][terminal] = 'pop'
            self.__table['&'][terminal] = 'pop'
        for nonterminal in self.grammar.getNonterminals():
            print(f"Nonterminal: {nonterminal}")
            for production in self.grammar.getProductions()[nonterminal]:
                first = self.compute_first_of_production(production)
                print(f"First({production}) = {first}")
                for terminal in first:
                    if terminal != '&':
                        if self.__table[nonterminal][terminal] == 'err':
                            self.__table[nonterminal][terminal] = [(production, 
                                                                self.grammar.getProductionNumber(nonterminal, production))]
                        else:
                            self.__table[nonterminal][terminal] += [(production, 
                                                                self.grammar.getProductionNumber(nonterminal, production))]
                if '&' in first:
                    for terminal in self.__follow[nonterminal]:
                        if self.__table[nonterminal][terminal] == 'err':
                            self.__table[nonterminal][terminal] = [(production, 
                                                                self.grammar.getProductionNumber(nonterminal, production))]
                        else:
                            self.__table[nonterminal][terminal] += [(production, 
                                                                self.grammar.getProductionNumber(nonterminal, production))]

    def print_table(self):
        if self.check_if_LL1():
            self.flatten()
        x  = PrettyTable()
        x.field_names = [''] + self.grammar.getTerminals() 
        for row in self.__table:
            x.add_row([row]+ [self.__table[row][col] for col in self.grammar.getTerminals() ])
        x.max_width = 1000
        file_path = "out.txt"
        with open(file_path, "w") as file:
            file.write(str(x))

    def check_if_LL1(self):
        for nonterminal in self.grammar.getNonterminals():
            for terminal in self.grammar.getTerminals():
                if self.__table[nonterminal][terminal] != 'err' :
                    if len(self.__table[nonterminal][terminal]) > 1:
                        print(f"Conflict at {nonterminal} {terminal}")
                        return False
        print("Grammar is LL1")
        return True

    def flatten(self):
         for nonterminal in self.grammar.getNonterminals():
            for terminal in self.grammar.getTerminals():
                if self.__table[nonterminal][terminal] != 'err' :
                    self.__table[nonterminal][terminal] = self.__table[nonterminal][terminal][0]

    def parse_sequence(self, sequence):
        output = ParserOutput()
        parent = []
        input_stack = []
        working_stack = [self.grammar.getStartSymbol(),'$']
        result_stack = []
        sequence_of_productions = [working_stack[:]]
        for char in sequence:
            input_stack.append(char)
        input_stack.append('$')
        go  = True
        s = ''
        while go:
            if len(input_stack) == 1 and len(working_stack) != 1:
                input_stack.insert(0,'&')
            
            if len(working_stack) == 1 and len(input_stack) != 1:
                input_stack.remove('&')

            cell = self.__table[working_stack[0]][input_stack[0]]
            if isinstance(cell, tuple):
                result_stack.append(cell[1])
                non_terminal = working_stack.pop(0)
                new_parent = output.len()

                parent_index  = parent[-1] if len(parent) > 0 else None
                output.add_node(non_terminal, parent_index)
                parent.append(new_parent)

                for char in reversed(cell[0]):
                    working_stack.insert(0, char)
                sequence_of_productions.append(working_stack[:])
                       
            elif cell == 'pop':
                terminal = working_stack.pop(0)
                sequence_of_productions.append(working_stack[:])
                if terminal != '&':
                    input_stack.pop(0)

                parent_index  = parent[-1]
                output.add_node(terminal, parent_index)

            elif cell == 'acc':
                go = False
                s += 'acc'
            else:
                go = False
                s += 'err'
                print(f"Error at {input_stack} {working_stack}")
        if s == 'acc':
            print(f"Sequence is accepted, result stack: {result_stack}")
        else:
            print(f"Sequence is not accepted, result stack: {result_stack}")   
        print(f"Sequence of productions: {sequence_of_productions}") 
        return output
            
        
def main():
    grammar = Grammar()
    grammar.readFromFile("g1.txt")
    grammar.print_nonterminals()
    grammar.print_terminals()
    grammar.print_productions()
    grammar.print_production('S')
    grammar.checkCFG()
    grammar.number_prodcutions()
    ll1 = LL1(grammar)
    ll1.compute_first()
    ll1.print_first()
    ll1.generate_follow()
    ll1.print_follow()
    ll1.parsing_table()
    ll1.print_table()
    output = ll1.parse_sequence('(a*a+a)*a')
    output.display()
main()