from enum import Enum, auto
import time

class State(Enum):
    OK = auto()
    RUNTIME_ERROR = auto()
    ABORT = auto()
    

class OpCode(Enum):
    PUSH     = auto()
    POP      = auto()
    DUP      = auto()
    CONST    = auto()
    HALT     = auto()

    NOW      = auto()
    PRINT    = auto()

    LOOP     = auto()
    BACK     = auto()
    JUMP     = auto()
    JUMP_IF_FALSE = auto()
    JUMP_IF_TRUE  = auto()   

    ADD      = auto()
    SUB      = auto()
    MUL      = auto()
    DIV      = auto()
    NEG      = auto()
    MOD       = auto()

    TRUE     = auto()
    FALSE    = auto()
    
    EQUAL    = auto()
    NOT_EQUAL = auto()
    GREATER  = auto()
    GREATER_EQUAL = auto()
    LESS     = auto()
    LESS_EQUAL = auto()

    OPADD    = auto()
    OPSUB    = auto()
    OPMUL    = auto()
    OPDIV    = auto()
    OPINC      = auto()
    OPDEC      = auto()
    
    AND      = auto()
    OR       = auto()
    NOT      = auto()
    NEGATE   = auto()
    NIL      = auto()
    RETURN   = auto()

    GLOBAL_SET = auto()
    GLOBAL_GET = auto()
    GLOBAL_ASSIGN = auto()

    LOCAL_SET = auto()
    LOCAL_GET = auto()

class Local:
    def __init__(self, name, index, depth, isArgument):
        self.name = name
        self.index = index
        self.depth = depth
        self.isArgument = False
        self.value = None
        

class Compiler:
    def __init__(self,name, interpreter):
        self.bytes = []
        self.lines = []
        self.constants = []
        self.stack = []
        self.index = 0
        self.name=name
        self.locals=[]
        self.scopeDepth = 0
        self.ip = 0
        self.interpreter = interpreter

    def declareVariable(self, name, isArgument):
        for i in range(len(self.locals) - 1, -1, -1):
            if self.locals[i].name == name and self.locals[i].depth == self.scopeDepth:
                print(f"Variable '{name}' already declared in this scope")
                return False
        self.locals.append(Local(name, len(self.locals), self.scopeDepth, isArgument))
        return True
    
    def resolveLocal(self, name):
        for i in range(len(self.locals) - 1, -1, -1):
            if self.locals[i].name == name and self.locals[i].depth == self.scopeDepth:
                return self.locals[i].index
        return -1

    def push(self, value):
        self.stack.append(value)
    
    def pop(self):
        return self.stack.pop()
    
    def popn(self, n):
        return [self.stack.pop() for _ in range(n)]
    
    def peek(self, index=0):
        return self.stack[len(self.stack) - 1 - index]
    
    def addConstant(self, value):
        if value in self.constants:
            return self.constants.index(value)
        self.constants.append(value)
        return self.constants.index(value)
    
    def write(self, byte, line):
        self.bytes.append(byte)
        self.lines.append(line)

    def write_bytes(self, b0, b1, line):
        self.write(b0, line)
        self.write(b1, line)

    def beginScope(self):
        self.scopeDepth += 1

    def endScope(self):
        self.scopeDepth -= 1

    def disassemble(self):
        self.disassembleCode()

    def disassembleCode(self):
        print(f"================== {self.name} ==================")
        total = int(len(self.bytes))
        offset = 0
        while offset < total:
            offset = self.disassembleInstruction(offset)
        print(" ")
            


    def disassembleInstruction(self, offset):
        print("0x{:04d} ".format(offset),end='')
        if (offset>0 and self.lines[offset] == self.lines[offset-1]):
            print("   | ",end='')
        else:
            print("{:4d} ".format(self.lines[offset]),end='')

        instruction = self.bytes[offset]

        if (instruction==OpCode.TRUE):
            return self.simpleInstruction("TRUE", offset)
        elif (instruction==OpCode.FALSE):
            return self.simpleInstruction("FALSE", offset)
        elif (instruction==OpCode.NIL):
            return self.simpleInstruction("NIL", offset)
        elif (instruction==OpCode.NOW):
            return self.simpleInstruction("NOW", offset)
        elif (instruction==OpCode.ADD):
            return self.simpleInstruction("ADD", offset)
        elif (instruction==OpCode.SUB):
            return self.simpleInstruction("SUB", offset)
        elif (instruction==OpCode.MUL):
            return self.simpleInstruction("MUL", offset)
        elif (instruction==OpCode.DIV):
            return self.simpleInstruction("DIV", offset)
        elif (instruction==OpCode.NEG):
            return self.simpleInstruction("NEG", offset)
        elif (instruction==OpCode.MOD):
            return self.simpleInstruction("MOD", offset)
        elif (instruction==OpCode.EQUAL):
            return self.simpleInstruction("EQUAL", offset)
        elif (instruction==OpCode.NOT_EQUAL):
            return self.simpleInstruction("NOT_EQUAL", offset)
        elif (instruction==OpCode.GREATER):
            return self.simpleInstruction("GREATER", offset)
        elif (instruction==OpCode.GREATER_EQUAL):
            return self.simpleInstruction("GREATER_EQUAL", offset)
        elif (instruction==OpCode.LESS):
            return self.simpleInstruction("LESS", offset)
        elif (instruction==OpCode.LESS_EQUAL):
            return self.simpleInstruction("LESS_EQUAL", offset)
        elif (instruction==OpCode.OPADD):
            return self.simpleInstruction("OP_ADD", offset)
        elif (instruction==OpCode.OPSUB):
            return self.simpleInstruction("OP_SUB", offset)
        elif (instruction==OpCode.OPMUL):
            return self.simpleInstruction("OP_MUL", offset)
        elif (instruction==OpCode.OPDIV):
            return self.simpleInstruction("OP_DIV", offset)
        elif (instruction==OpCode.OPINC):
            return self.simpleInstruction("OP_INC", offset)
        elif (instruction==OpCode.OPDEC):
            return self.simpleInstruction("OP_DEC", offset)
        elif (instruction==OpCode.AND):
            return self.simpleInstruction("AND", offset)
        elif (instruction==OpCode.OR):
            return self.simpleInstruction("OR", offset)
        elif (instruction==OpCode.NOT):
            return self.simpleInstruction("NOT", offset)
        elif (instruction==OpCode.PUSH):
            return self.byteInstruction("PUSH", offset)
        elif (instruction==OpCode.POP):
            return self.simpleInstruction("POP", offset)
        elif (instruction==OpCode.DUP):
            return self.simpleInstruction("DUP", offset)
        elif (instruction==OpCode.HALT):
            return self.simpleInstruction("HALT", offset)
        elif (instruction==OpCode.PRINT):
            return self.simpleInstruction("PRINT", offset)
        elif (instruction==OpCode.RETURN):
            return self.simpleInstruction("RETURN", offset)
        elif (instruction==OpCode.JUMP):
            return self.jumpInstruction("JUMP", 1, offset)
        elif (instruction==OpCode.JUMP_IF_FALSE):
            return self.jumpInstruction("JUMP_IF_FALSE", 1, offset)
        elif (instruction==OpCode.JUMP_IF_TRUE):
            return self.jumpInstruction("JUMP_IF_TRUE", 1, offset)
        elif (instruction==OpCode.LOOP):
            return self.jumpInstruction("LOOP", -1, offset)
        elif (instruction==OpCode.BACK):
            return self.jumpInstruction("BACK", -1, offset)
        elif (instruction==OpCode.LOCAL_GET):
            return self.constantInstruction("LOCAL_GET", offset)
        elif (instruction==OpCode.LOCAL_SET):
            return self.constantInstruction("LOCAL_SET", offset)
        elif (instruction==OpCode.CONST):
            return self.constantInstruction("CONST", offset)
        elif (instruction==OpCode.GLOBAL_GET):
            return self.constantInstruction("GLOBAL_GET", offset)
        elif (instruction==OpCode.GLOBAL_SET):
            return self.constantInstruction("GLOBAL_SET", offset)
        elif (instruction==OpCode.GLOBAL_ASSIGN):
            return self.constantInstruction("GLOBAL_ASSIGN", offset)
            
        else :
            print("UNKNOWN")
            return len(self.bytes)
        



    def simpleInstruction(self, name, offset):
        print(f"{name}")
        return offset + 1
 
    def byteInstruction(self, name, offset):
        slot = self.bytes[offset + 1]
        print("{:<16s} {:>4d}".format(name, slot))
        return offset + 2
 
    def constantInstruction(self, name, offset):
       slot = self.bytes[offset + 1]
       print("{:<16s} {:>4d} '".format(name, slot),end='')
       value = self.constants[slot]
       print(f"{value}'")
       return offset + 2
    def jumpInstruction(self, name, sign, offset):
        jump = self.bytes[offset + 1] << 8
        jump |= self.bytes[offset + 2]
        print("{:<16s} {:>4d} -> {}".format(name, offset, offset + 3 + sign * jump))
        return offset + 3


    def READ_BYTE(self):
        byte = self.bytes[self.ip]
        self.ip += 1
        return byte
    def READ_CONSTANT(self):
        return self.constants[self.READ_BYTE()]
    def READ_SHORT(self):
        self.ip += 2
        return self.bytes[self.ip - 2] << 8 | self.bytes[self.ip - 1]

    def run(self):
        while True:
            intruction = self.READ_BYTE()
            #lineIndex = ( self.ip - self.bytes ) // 2
            #line = self.lines[lineIndex]

            if intruction == OpCode.HALT:
                print("HALT")
                return State.ABORT
            elif intruction == OpCode.POP:
                self.pop()
            elif intruction == OpCode.TRUE:
                self.push(True)
            elif intruction == OpCode.FALSE:
                self.push(False)
            elif intruction == OpCode.NIL:
                self.push(None)
            elif intruction == OpCode.DUP:
                value = self.peek(0)
                self.push(value)
            elif intruction == OpCode.CONST:
                const = self.READ_CONSTANT()
                self.push(const)
            
            #OPERATORS **************************************************************************************************************
            elif intruction == OpCode.OPINC:
                value = self.pop()
                self.push(value + 1)
            elif intruction == OpCode.OPDEC:
                value = self.pop()
                self.push(value - 1)
            #OPEATIONS
            elif intruction == OpCode.ADD:
                right = self.pop()
                left = self.pop()
                self.push(left + right)
            elif intruction == OpCode.SUB:
                right = self.pop()
                left = self.pop()
                self.push(left - right)
            elif intruction == OpCode.MUL:
                right = self.pop()
                left = self.pop()
                self.push(left * right)
            elif intruction == OpCode.DIV:
                right = self.pop()
                left = self.pop()
                self.push(left / right)
            elif intruction == OpCode.MOD:
                right = self.pop()
                left = self.pop()
                self.push(left % right)
            #BUILT IN
            elif intruction == OpCode.PRINT:
                value = self.pop()
                print(value)
            elif intruction == OpCode.NOW:
                self.push(time.time())
            #VARIABLES LOCAL
            elif intruction == OpCode.LOCAL_GET:
                slot = self.READ_BYTE()
                self.locals[slot].value = self.peek(0)
            elif intruction == OpCode.LOCAL_SET:
                slot = self.READ_BYTE()
                self.push(self.locals[slot].value)
            #VARIABLES GLOBAL
            elif intruction == OpCode.GLOBAL_GET:
                name = self.READ_CONSTANT()
                value = self.interpreter.globals.get(name)
                if not value:
                    print(f"Variable {name} not defined")
                    return State.RUNTIME_ERROR
                self.push(value)
            
            elif intruction == OpCode.GLOBAL_SET:
                name  = self.READ_CONSTANT()
                value = self.peek()
                if  self.interpreter.globals.define(name,value)==False:
                    print(f"Variable {name} already defined")
                    return State.RUNTIME_ERROR
                self.pop
                
            elif intruction == OpCode.GLOBAL_ASSIGN:
                name = self.READ_CONSTANT()
                value = self.peek()
                if not self.interpreter.globals.assign(name,value):
                    print(f"Undefined variable {name} ")
                    return State.RUNTIME_ERROR
            #CALL
            elif intruction == OpCode.RETURN:
                self.pop()
                return State.OK
            else:
                print(f"UNKNOWN INSTRUCTION {intruction}")
                return State.RUNTIME_ERROR

            
            

        return State.OK