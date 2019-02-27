from lexer import Location, TokenKind
import sys


class Parser:
    def __init__(self, token_list):
        self.loc = Location(0, 0)
        self.token_list = token_list
        self.parse_tree = []
        self.errors = []

    def parse(self):
        self.find_error()
        self.propositions()
        if len(self.errors) == 0:
            print(self.parse_tree)
            return str(self.parse_tree)
        else:
            print(self.errors)
            return 'Error(s) -> ' + str(self.errors)



    def propositions(self):
        self.parse_tree.append(sys._getframe().f_code.co_name)
        self.proposition()
        self.more_propositions()

    def more_propositions(self):
        self.parse_tree.append(sys._getframe().f_code.co_name)
        if self.isEmpty():
            self.parse_tree.append('epsilon')
        elif self.top() == TokenKind.COMMA:
            self.pop()  # comma
            self.propositions()

    def proposition(self):
        self.parse_tree.append(sys._getframe().f_code.co_name)
        if not self.if_compound():
            self.atomic()
        else:
            self.compound()

    def atomic(self):
        self.parse_tree.append(sys._getframe().f_code.co_name)
        self.pop()  # ID

    def compound(self):
        self.parse_tree.append(sys._getframe().f_code.co_name)
        if self.top() == TokenKind.ID:
            self.atomic()
            self.connective()
            self.proposition()

        elif self.top() == TokenKind.LPAR:
            self.pop()
            self.proposition()
            self.pop()
        elif self.top() == TokenKind.NOT:
            self.pop()
            self.proposition()

    def connective(self):
        self.parse_tree.append(sys._getframe().f_code.co_name)
        self.pop()

    # add more methods if needed

    def find_error(self):
        par = []
        for i, token in enumerate(self.token_list):
            if token.kind == TokenKind.ID and i - 1 >= 0 and self.token_list[i - 1].kind == TokenKind.ID:
                self.error('invalid ID', token)
            elif token.kind == TokenKind.LPAR:
                par.append(TokenKind.LPAR)
            elif token.kind == TokenKind.RPAR:
                if len(par) == 0:
                    self.error('invalid set of parentheses', None)
                    break
                else:
                    par.pop()
            elif token.kind == TokenKind.NOT:
                if (i + 1 == len(self.token_list) or
                        i + 1 < len(self.token_list)
                        and self.token_list[i + 1].kind != TokenKind.LPAR and self.token_list[
                            i + 1].kind != TokenKind.ID):
                    self.error('invalid NOT symbol', token)

        if len(par) != 0:
            self.error('invalid set of parentheses', None)

    def if_connective(self, kind):
        if kind == TokenKind.AND or kind == TokenKind.OR or kind == TokenKind.IMPLIES or kind == TokenKind.IFF:
            return True
        else:
            return False

    def if_compound(self):
        if (len(self.token_list) > 1 and self.if_connective(self.token_list[1].kind) or self.top() == TokenKind.LPAR or
                self.top() == TokenKind.NOT):
            return True
        else:
            return False

    def isEmpty(self):
        if len(self.token_list) == 0:
            return True
        else:
            return False

    def pop(self):
        if not self.isEmpty():
            self.parse_tree.append(str(self.token_list.pop(0)))
        else:
            self.errors.append('Missing value')

    def top(self):
        if not self.isEmpty():
            return self.token_list[0].kind
        else:
            return None

    def error(self, s, token):
        if token != None and s == None:
            self.errors.append('(line ' + str(token.loc.line) + ', col ' + str(token.loc.col) + ')')
        elif s != None and token == None:
            self.errors.append(s)
        elif token != None and s != None:
            self.errors.append(s + ' (line ' + str(token.loc.line) + ', col ' + str(token.loc.col) + ')')
