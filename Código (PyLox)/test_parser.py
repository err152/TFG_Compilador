import unittest
from parser import Parser
from Token import Token,TokenType

class TestLexer(unittest.TestCase):
    
    def test_singleChars(self):
        pars = Parser([Token(0,TokenType.NUMBER,"1"), Token(0,TokenType.PLUS,"+"), Token(0,TokenType.NUMBER,"2"), Token(0,TokenType.EOF,"")])
        print(f"-- tokens in parser : {pars.tokens}")
        expr = pars.parse()
        print(f"-- expr : {expr}")
        #assert b == '[[0,"NUMBER",1], [0,"PLUS",+], [0,"NUMBER",2]]'

                     
if __name__ == '__main__':
    unittest.main()
