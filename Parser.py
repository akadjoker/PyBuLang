import time
from Token import TokenType, Token
from enum import Enum, auto
from Visitor import Visitor
from Ast import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.current_loop = None
        self.isPanicMode = False

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF
    
    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
    
    def consume(self, type, message):   
        if self.check(type):
            return self.advance()
        self.error(self.peek(),message)

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            self.advance()
    
    def error(self, token, message):
        if token.type == TokenType.EOF:
            print(f" Error   ({message}) at line {token.line}")
        else:
            print(f" Error  token: '{token.lexeme}' {message} at line {token.line}")
        exit(1)
    
    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return Program(statements)


    def expression(self):
        return self.assignment()
    
    def assignment(self):
            expr = self.expr_or()
            if self.match(TokenType.EQUAL):# =
                equals = self.previous()
                value = self.assignment()
                if isinstance(expr, Variable):
                    name = expr.name
                    return Assign(name, value)
                self.error(equals, "Invalid assignment target")
            elif self.match(TokenType.EQUAL_PLUS) or self.match(TokenType.EQUAL_MINUS) or self.match(TokenType.EQUAL_MULT) or self.match(TokenType.EQUAL_DIV):
               
                operator = self.previous()
               
                value = self.assignment()

                if isinstance(expr, Variable):
                    name = expr.name
                    adition =  Binary(expr, operator, value)
                    return Assign(name,adition)
                self.error(operator, "Invalid assignment target")


            return expr    

    def expr_or(self):
        expr = self.expr_and()
        if self.match(TokenType.OR):
            operator = self.previous()
            right = self.expr_and()
            return Logical(expr, operator, right)
        return expr
    
    def expr_and(self):
        expr = self.equality()
        if self.match(TokenType.AND):
            operator = self.previous()
            right = self.expr_and()
            return Logical(expr, operator, right)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):# == !=
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):# > >= < <=
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr
    

    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):# + -
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    
    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR, TokenType.PERCENT):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    
    def unary(self):
        if self.match(TokenType.MINUS, TokenType.BANG):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        
        # Pré-incremento (++i)
        if self.match(TokenType.PLUS_PLUS):
            operator = self.previous()
            expr = self.unary()  # A expressão a ser incrementada
            if isinstance(expr, Variable):
                return PreProcess(expr, operator)
            self.error(operator, "Invalid increment target")

        # Pré-decremento (--i)
        if self.match(TokenType.MINUS_MINUS):
            operator = self.previous()
            expr = self.unary()  # A expressão a ser decrementada
            if isinstance(expr, Variable):
                return PreProcess(expr, operator)
            self.error(operator, "Invalid decrement target")
        
        # Pós-incremento (i++)
        expr = self.primary()
        if self.match(TokenType.PLUS_PLUS):
            operator = self.previous()
            if isinstance(expr, Variable):
                return PostProcesst(expr, operator)
            self.error(operator, "Invalid increment target")
        
        # Pós-decremento (i--)
        if self.match(TokenType.MINUS_MINUS):
            operator = self.previous()
            if isinstance(expr, Variable):
                return PostProcesst(expr, operator)
            self.error(operator, "Invalid decrement target")
        return expr

    def primary(self):
        if self.match(TokenType.FALSE):
            return Boolean(False, self.previous())
        
        if self.match(TokenType.TRUE):
            return Boolean(True, self.previous())
        
        if self.match(TokenType.NIL):
            return Nil(self.previous())
        
        if self.match(TokenType.NUMBER):
            return  Number(self.previous().literal, self.previous())
        
        if self.match(TokenType.STRING):
            return  String(self.previous().literal, self.previous())

        if self.match(TokenType.NOW):
            return Now(self.previous())

        
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        
        
        if self.match(TokenType.LPAREN):
            return  self.grouping()
        

        self.error(self.peek(), "Expect expression")
        return None
    

    def grouping(self):
        expr = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after expression")
        return Grouping(expr)

    def block(self):
        statements = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RBRACE, "Expect '}' after block")
        return BlockStatement(statements)


    def declaration(self):
        if self.match(TokenType.VAR):
            return self.var_declaration()
        return self.statement()

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration")
        return Declaration(name, initializer)


    def statement(self):
        
        if self.match(TokenType.PRINT):
            return self.print_statement()
        
        if self.match(TokenType.LBRACE):
            return self.block()
        
        return self.expr_statement()

    def expr_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression")
        return ExprStatement(expr)


    def print_statement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'print'")
        expr = self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after value")
        self.consume(TokenType.SEMICOLON, "Expect ';' after value")
        node = PrintStatement(expr)
        node.token = self.previous()
        return node


