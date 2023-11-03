from pif import Pif
from symbolTable import SymbolTable
import re

class Scanner:
    
    def __init__(self, programPath, tokensPath):
        self.pif = Pif()
        self.constants = SymbolTable(10)
        self.identifiers = SymbolTable(10)
        self.tokens = self.read_accepted_tokens(tokensPath)
        self.program = self.read_program(programPath)
        self.string_processing = False
        self.char_processing = False
        self.string_buffer = ""
        self.char_buffer = ""
        self.separators = ['+', '-', '*', '/', '%', '(', ')', '{', '}', '[', ']', '==', '<', '>', '<=', '>=', '=', '||', '&&', '!=', "'", '"', ',', ';', '!', '.']

    def read_program(self, file_path):
        lines = []
        with open(file_path, "r") as f:
            for line in f.readlines():
                lines.append(line)
        return lines
        
    def read_accepted_tokens(self, tokensPath):
        tokens = []
        with open(tokensPath, "r") as f:
            for line in f.readlines():
                tokens.append(line.strip())  
        return tokens

    def is_identifier(self, token):
        return re.match(r"^[a-zA-Z]([a-zA-Z]|[0-9])*$", token)

    def is_int_constant(self, token):
        return re.match(r"^(0|[-]?[1-9][0-9]*)$", token)

    def is_string_constant(self, token):
        return re.match(r"^[a-zA-Z0-9_ ?\-:*^+=.!]*$", token)

    def is_char_constant(self, token):
        return re.match(r"^[a-zA-Z0-9_ ?\-:*^+=.!]$", token)

    def tokenize_line(self, line):
        for token in self.tokens:
            line = line.replace(token, " " + token + " ")
        return line.strip().split(" ")

    def scan(self):
        crt_line = 1
        for line in self.program:
            crt_tokens = self.tokenize_line(line)
            for token in crt_tokens:
                self.process_token(token, crt_line)
            crt_line = crt_line + 1
        return self.pif, self.constants, self.identifiers

    def process_token(self, token, line):
        if token == "\"":
            if self.string_processing:
                if self.is_string_constant(self.string_buffer):
                    pos = self.constants.insert(self.string_buffer)
                    self.pif.add('constant', pos)
                    self.string_buffer = ""
                    self.string_processing = False
                else:
                    print(self.string_buffer)
                    raise Exception(f'Invalid string at line {line}')
            else:
                self.string_processing = True
        elif token == "\'":
            if self.char_processing:
                if self.is_char_constant(self.char_buffer):
                    pos = self.constants.insert(self.char_buffer)
                    self.pif.add('constant', pos)
                    self.char_buffer = ""
                    self.char_processing = False
                else:
                    raise Exception(f'Invalid string at line {line}')
            else:
                self.char_processing = True
        elif self.string_processing:
            self.string_buffer += token
        elif self.char_processing:
            self.char_buffer += token
        elif self.is_int_constant(token):
            pos = self.constants.insert(token)
            print(self.constants)
            self.pif.add('constant', pos)
        elif token in self.tokens:
            self.pif.add(token, -1)
        elif self.is_identifier(token):
            pos = self.identifiers.insert(token)
            self.pif.add('id', pos)



token_file_name = "token.in"
program_file_name = "p1.txt"
custom_scanner = Scanner(program_file_name, token_file_name)

pif_result, constants_result, identifiers_result = custom_scanner.scan()
print("PIF:")
print(pif_result)

print("Custom Identifiers:")
print(identifiers_result)

print(" Constants:")
print(constants_result)
