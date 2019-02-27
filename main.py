import unittest
from lexer import Lexer
from pparser import Parser

filename = 'input.txt'
lines = ['']
file = open(filename, "r")
line = file.read(1)
i = 0
while line:
    if line != '\n':
        lines[i] += line
    elif line == '\n':
        lines.append('')
        i += 1
    line = file.read(1)
file.close()
print(lines)


class Test(unittest.TestCase):
    def test1(self):
        token_list = []
        for i, l in enumerate(lines):
            if l.strip():
                token_list.append(Lexer(l, i + 1).tokenize())

        for i, tokens in enumerate(token_list):
            print("-----------")
            print('Input #' + str(i + 1) + ':')
            if tokens[0].kind != None:
                print("Lexer:" + str(tokens))
                tokens = Parser(tokens).parse()
                print("Parser:" + str(tokens))
            else:
                print("Syntax Error")
                for i, invalid_token in enumerate(tokens):
                    print(str(invalid_token) + ' (line ' + str(invalid_token.loc.line) + ', col ' + str(
                        invalid_token.loc.col) + ')')
                    if i + 1 != len(tokens):
                        print("|")



if __name__ == '__main__':
    unittest.main()
