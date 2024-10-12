

class Visitor:
    def visit_binary(self, expr):
        pass

    def visit_unary(self, expr):
        pass

    def visit_number(self, expr):
        pass

    def visit_string(self, expr):
        pass

    def visit_boolean(self, expr):
        pass

    def visit_nil(self, expr):
        pass

    def visit_pre_increment(self, expr):
        pass

    def visit_post_decrement(self, expr):
        pass


    def visit_variable(self, expr):
        pass

    def visit_assign(self, expr):
        pass

    def visit_declaration(self, expr):
        pass

    def visit_grouping(self, expr):
        pass

    def visit_expression_statement(self, stmt):
        pass

    def visit_program(self, program):
        pass

    def visit_block_statement(self, stmt):
        pass

    def visit_print_statement(self, stmt):
        pass

