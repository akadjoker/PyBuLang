
class Node:
    def __init__(self):
        self.token = None

    def accept(self, visitor):
        pass

class Empty(Node):
    def __init__(self):
        pass

    def accept(self, visitor):
        visitor.visit_empty(self)

class Binary(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        visitor.visit_binary(self)

class Unary(Node):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        visitor.visit_unary(self)
    
class PreProcess(Node):
    def __init__(self, variable, operator):
        self.variable = variable
        self.operator = operator
    
    def accept(self, visitor):
        visitor.visit_pre_process(self)

class PostProcesst(Node):
    def __init__(self, variable, operator):
        self.variable = variable
        self.operator = operator
    
    def accept(self, visitor):
        visitor.visit_post_process(self)


class Logical(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        visitor.visit_logical(self)



class Grouping(Node):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        visitor.visit_grouping(self)


class Declaration(Node):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        visitor.visit_declaration(self)

class Variable(Node):
    def __init__(self, name):
        self.name = name


    def accept(self, visitor):
        visitor.visit_variable(self)


class Assign(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        visitor.visit_assign(self)


class Nil(Node):
    def __init__(self, token):
        self.token = token
    def accept(self, visitor):
        visitor.visit_nil(self)

class Boolean(Node):
    def __init__(self, value, token):
        self.value = value
        self.token = token

    def accept(self, visitor):
        visitor.visit_boolean(self)

class Number(Node):
    def __init__(self, value,token):
        self.value = value
        self.token = token

    def accept(self, visitor):
        visitor.visit_number(self)

class String(Node):
    def __init__(self, value, token):
        self.value = value
        self.token = token

    def accept(self, visitor):
        visitor.visit_string(self)


class Now(Node):
    def __init__(self, token):
        self.token = token
    def accept(self, visitor):
        visitor.visit_now(self)

#
# Statements
#   
class Statement(Node):
    pass

class ExprStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        visitor.visit_expression_statement(self)


class Program(Node):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        visitor.visit_program(self)

class BlockStatement(Statement):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        visitor.visit_block_statement(self)


class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        visitor.visit_print_statement(self)