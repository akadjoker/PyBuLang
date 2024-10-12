
from Lexer import Lexer
from Token import TokenType, Token
from Parser import Parser
from Interpreter import Interpreter

f = open("main.bu","rt")
source_code = f.read()
f.close()


lexer = Lexer(source_code)
tokens = lexer.tokenize()


for token in tokens:
     print(token)



parser = Parser(tokens)
node = parser.parse() 


interpreter = Interpreter()
interpreter.compile(node)



