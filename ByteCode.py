from enum import Enum, auto
from Visitor import Visitor
from Ast import  *
from Compiler import *
from Token import TokenType


class Task:
    def __init__(self):
        self.bytes = []
        self.lines = []


    def write(self, byte, line):
        self.bytes.append(byte)
        self.lines.append(line)

    def emitByte(self, byte, line):
        self.write(byte, line)

    def emitBytes(self, b0, b1, line):
        self.emitByte(b0, line)
        self.emitByte(b1, line)


class ByteGenerator (Visitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.compiler = self.interpreter.GetCurrent()
        self.taks = []

    def processTasks(self):
        while len(self.taks) > 0:
            task = self.taks.pop(0)
            for i in range(len(task.bytes)):
                self.compiler.bytes.append(task.bytes[i])
                self.compiler.lines.append(task.lines[i] )    

    def counter(self):
        return len(self.compiler.bytes)

    def line(self, index):
        if index >= len(self.compiler.lines):
            return self.compiler.lines[-1]
        return self.compiler.lines[index]
    
    def lastLine(self):
        return self.compiler.lines[-1]
    
    def compile(self, program):
        program.accept(self)



    def emitByte(self, byte, line):
        self.compiler.write(byte, line)

    def emitBytes(self, b0, b1, line):
        self.emitByte(b0, line)
        self.emitByte(b1, line)

    def emit_constant(self, value, line):
        self.emitBytes(OpCode.CONST, self.compiler.addConstant(value), line)

    
    def visit_binary(self, expr):

        op   = expr.operator.type
        line = expr.operator.line
        expr.left.accept(self)
        expr.right.accept(self)

        print("BINARY",op, line)

        if op == TokenType.PLUS:
            self.emitByte(OpCode.ADD, line)
        elif op == TokenType.EQUAL_PLUS:
            self.emitByte(OpCode.ADD, line)
        elif op == TokenType.MINUS:
            self.emitByte(OpCode.SUB, line)
        elif op == TokenType.STAR:
            self.emitByte(OpCode.MUL, line)
        elif op == TokenType.SLASH:
            self.emitByte(OpCode.DIV, line)
        elif op == TokenType.PERCENT:
            self.emitByte(OpCode.MOD, line)
        elif op == TokenType.GREATER:
            self.emitByte(OpCode.GREATER, line)
        elif op == TokenType.GREATER_EQUAL:
            self.emitByte(OpCode.GREATER_EQUAL, line)
        elif op == TokenType.LESS:
            self.emitByte(OpCode.LESS, line)
        elif op == TokenType.LESS_EQUAL:
            self.emitByte(OpCode.LESS_EQUAL, line)
        elif op == TokenType.BANG_EQUAL:
            self.emitByte(OpCode.NOT_EQUAL, line)

    def visit_unary(self, expr):
        op = expr.operator.type
        line = expr.operator.line
        expr.right.accept(self)

        if op == TokenType.MINUS:
            self.emitByte(OpCode.NEGATE, line)
        elif op == TokenType.BANG:
            self.emitByte(OpCode.NOT, line)

    def visit_number(self, expr):
        self.emit_constant(expr.value, expr.token.line)
        

    def visit_string(self, expr):
        self.emit_constant(expr.value, expr.token.line)

    def visit_boolean(self, expr):
        self.emit_constant(expr.value, expr.token.line)

    def visit_nil(self, expr):
        self.emit(OpCode.NIL, expr.token.line)


    def visit_pre_process(self, expr):
        print("PRE PROCESS")
        expr.variable.accept(self)  
        if expr.operator.type == TokenType.PLUS_PLUS:
            self.emitByte(OpCode.OPINC, expr.operator.line)
            
        elif expr.operator.type == TokenType.MINUS_MINUS:
            self.emitByte(OpCode.OPDEC, expr.operator.line)
        if isinstance(expr.variable, Variable):
            resolve = self.compiler.resolveLocal(expr.variable.name.lexeme)
            if resolve == -1:
                index = self.compiler.addConstant(expr.variable.name.lexeme)
                self.emitBytes(OpCode.GLOBAL_ASSIGN, index, expr.operator.line)  # Atualiza o valor incrementado/decrementado
            else:
                self.emitBytes(OpCode.LOCAL_SET, resolve, expr.operator.line)  # Atualiza o valor incrementado/decrementado
    def visit_post_process(self, expr):
        print("POST PROCESS")

        
        task = Task()
        self.taks.append(task)
        
        expr.variable.accept(self)  
        if expr.operator.type == TokenType.PLUS_PLUS:
            task.emitByte(OpCode.OPINC, expr.operator.line)

        elif expr.operator.type == TokenType.MINUS_MINUS:
            task.emitByte(OpCode.OPDEC, expr.operator.line)
        if isinstance(expr.variable, Variable):
            resolve = self.compiler.resolveLocal(expr.variable.name.lexeme)
            if resolve == -1:
                index = self.compiler.addConstant(expr.variable.name.lexeme)
                task.emitBytes(OpCode.GLOBAL_ASSIGN, index, expr.operator.line)  # Atualiza o valor incrementado/decrementado
            else:
                task.emitBytes(OpCode.LOCAL_SET, resolve, expr.operator.line)  # Atualiza o valor incrementado/decrementado


        
    

    def visit_expression_statement(self, stmt):
        stmt.expression.accept(self)

    
    def visit_grouping(self, expr):
        expr.expression.accept(self)

    def visit_variable(self, expr):
        #print("READ VARIABLE",expr.name)
        resolve = self.compiler.resolveLocal(expr.name.lexeme)
        if resolve == -1:
            index = self.compiler.addConstant(expr.name.lexeme)
            self.emitBytes(OpCode.GLOBAL_GET, index, expr.name.line)
        else:
            self.emitBytes(OpCode.LOCAL_GET, resolve, expr.name.line)

    def visit_assign(self, expr):
        #print("ASSIGN",expr.name)

        expr.value.accept(self)
        resolve = self.compiler.resolveLocal(expr.name.lexeme)
        if resolve == -1:
            index = self.compiler.addConstant(expr.name.lexeme)
            self.emitBytes(OpCode.GLOBAL_ASSIGN, index, expr.name.line)
        else:
            self.emitBytes(OpCode.LOCAL_SET, resolve, expr.name.line)

    def visit_declaration(self, expr):
        #print("DECLARATION",expr.name.lexeme)
        expr.initializer.accept(self)

        if self.compiler.scopeDepth == 0:
            index = self.compiler.addConstant(expr.name.lexeme)
            self.emitBytes(OpCode.GLOBAL_SET, index, expr.name.line)
        else:
            if not self.compiler.declareVariable(expr.name.lexeme, False):
                self.error(expr.name, "Variable already declared in this scope.")
            

    def visit_program(self, program):
        for statement in program.statements:
            statement.accept(self)
        self.emitByte(OpCode.NIL,self.lastLine()+1)
        self.emitByte(OpCode.RETURN,self.lastLine()+1)

    def visit_block_statement(self, stmt):
        self.compiler.beginScope()
        for declaration in stmt.declarations:
            declaration.accept(self)
        self.compiler.endScope()
        self.processTasks()

    def visit_print_statement(self, stmt):
        stmt.expression.accept(self)
        self.emitByte(OpCode.PRINT, stmt.token.line)
        self.processTasks()
