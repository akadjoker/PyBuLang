
from Lexer import Lexer
from Token import TokenType, Token
from Parser import Parser
from Visitor import Visitor
from Ast import  *
from ByteCode import ByteGenerator
from Compiler import Compiler

import threading



class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name, value):
        if name in self.values:
            return False
        self.values[name] = value
        return True

    def get(self, name):
        if name in self.values:
            return self.values[name]
        return None
        


    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return True
        return False
    
    def debug(self):
        print(self.values)







class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.current = Compiler("__main__", self)
        self.generator = ByteGenerator(self)

    def GetCurrent(self):
        return self.current
    
    def NewCompiler(self, name):
        compiler = Compiler(name, self)
        return compiler

    def compile(self, statements):
        self.generator.compile(statements)
        self.current.disassemble()
        self.current.run()
        self.globals.debug()

    def error(self, token, message):
        if token.type == TokenType.EOF:
            print(f"[line {token.line}] Error at end: {message}")
        else:
            print(f"[line {token.line}] Error at '{token.lexeme}': {message}")
        exit(1)


    